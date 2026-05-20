from __future__ import annotations

from pathlib import Path

from bayesseed.inference import (
    batch_infer,
    infer_case,
    normalize_case_values,
    read_case_file,
)


def _top_disease(result: dict) -> dict:
    return result["disease_results"][0]


def test_normalize_case_values_handles_common_tokens() -> None:
    normalized = normalize_case_values(
        {
            "yes_value": "yes",
            "no_value": "negative",
            "missing_value": "NA",
            "float_value": "0.75",
            "bool_value": True,
        }
    )
    assert normalized == {
        "yes_value": 1,
        "no_value": 0,
        "missing_value": None,
        "float_value": 0.75,
        "bool_value": 1,
    }


def test_infer_bppv_typical_case_ranks_bppv_highest(default_modules_dir: Path) -> None:
    result = infer_case(
        default_modules_dir,
        {
            "positional_trigger": 1,
            "brief_duration_seconds_minutes": 1,
            "dix_hallpike_torsional_upbeating_nystagmus": 1,
            "central_neurologic_sign_or_central_mri_lesion": 0,
        },
    )
    top = _top_disease(result)
    assert top["disease_id"] == "dx_bppv"
    assert top["posterior"] > 0.5
    assert "posterior_canal_positional_pattern" in top["parents_observed"]


def test_infer_md_typical_case_ranks_md_highest(default_modules_dir: Path) -> None:
    result = infer_case(
        default_modules_dir,
        {
            "recurrent_spontaneous_episodes": 1,
            "duration_20min_to_12h": 1,
            "fluctuating_hearing_loss": 1,
            "tinnitus": 1,
            "aural_fullness": 1,
            "low_frequency_snhl": 1,
            "mri_endolymphatic_hydrops": 1,
            "central_neurologic_sign_or_central_mri_lesion": 0,
        },
    )
    top = _top_disease(result)
    assert top["disease_id"] == "dx_meniere_disease"
    assert top["posterior"] > 0.8


def test_infer_pvp_typical_case_ranks_pvp_highest(default_modules_dir: Path) -> None:
    result = infer_case(
        default_modules_dir,
        {
            "age_ge_60": 1,
            "chronic_dizziness_gt_3months": 1,
            "gait_difficulty_imbalance_falls": 1,
            "mild_bilateral_vestibular_hypofunction": 1,
            "severe_bilateral_vestibular_hypofunction": 0,
            "central_neurologic_sign_or_central_mri_lesion": 0,
        },
    )
    top = _top_disease(result)
    assert top["disease_id"] == "dx_presbyvestibulopathy"
    assert top["posterior"] > 0.3


def test_bvp_competing_case_ranks_bvp_above_pvp(default_modules_dir: Path) -> None:
    result = infer_case(
        default_modules_dir,
        {
            "age_ge_60": 1,
            "chronic_dizziness_gt_3months": 1,
            "gait_difficulty_imbalance_falls": 1,
            "severe_bilateral_vestibular_hypofunction": 1,
        },
    )
    disease = {row["disease_id"]: row for row in result["disease_results"]}
    assert (
        disease["dx_bilateral_vestibulopathy"]["posterior"]
        > disease["dx_presbyvestibulopathy"]["posterior"]
    )


def test_read_case_file_and_batch_infer_synthetic_cases(
    default_modules_dir: Path, examples_dir: Path
) -> None:
    cases = read_case_file(examples_dir / "synthetic_cases.csv")
    assert len(cases) == 9
    outputs = batch_infer(default_modules_dir, examples_dir / "synthetic_cases.csv")
    assert len(outputs) == 9
    assert all(output["disease_results"] for output in outputs)
