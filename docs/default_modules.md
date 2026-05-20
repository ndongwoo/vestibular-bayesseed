# Default disease modules

The v0.1.0 distribution includes three default worked-example modules:

1. `bppv.json`
2. `meniere_disease.json`
3. `pvp_bvp.json`

These modules are intended for research and educational demonstration. They are not clinically validated diagnostic models.

## 1. BPPV module

File:

```text
default_modules/bppv.json
```

Purpose:

```text
Worked example for a positional/nystagmus-driven vestibular disorder.
```

### Main input nodes

- `positional_trigger`
- `brief_duration_seconds_minutes`
- `dix_hallpike_torsional_upbeating_nystagmus`
- `supine_roll_geotropic_or_apogeotropic_nystagmus`
- `subjective_positional_vertigo_only`
- `atypical_positional_nystagmus`
- `negative_positional_test`
- `central_neurologic_sign_or_mri_lesion`

### Main derived nodes

- `brief_triggered_positional_syndrome`
- `posterior_canal_positional_pattern`
- `horizontal_canal_positional_pattern`
- `subjective_positional_pattern`
- `atypical_positional_red_flag`
- `no_objective_positional_nystagmus`

### Main target node

- `dx_bppv`

### Modeling logic

The module places strong weight on canal-specific nystagmus patterns. Positional trigger and brief duration build a broader positional syndrome, but this is not decisive without positional nystagmus. Subjective BPPV is modeled as positive but weaker. Negative positional testing is only weakly negative because spontaneous resolution or false-negative testing may occur. Central signs and atypical positional red flags compete against BPPV.

## 2. Ménière disease module

File:

```text
default_modules/meniere_disease.json
```

Purpose:

```text
Worked example for an audio-vestibular episodic diagnostic network.
```

### Main input nodes

- `recurrent_spontaneous_episodes`
- `duration_20min_to_12h`
- `fluctuating_hearing_loss`
- `tinnitus`
- `aural_fullness`
- `low_frequency_snhl`
- `mri_endolymphatic_hydrops`
- `vemp_or_ecog_hydrops_compatible`
- `migraine_features`
- `central_neurologic_sign_or_mri_lesion`

### Main derived nodes

- `episodic_vestibular_syndrome`
- `auditory_cluster`
- `objective_low_frequency_cochlear_pattern`
- `endolymphatic_hydrops_evidence`
- `migraine_overlap_pattern`

### Main target node

- `dx_meniere_disease`

### Modeling logic

The module combines episode pattern, fluctuating auditory symptoms, objective low-frequency SNHL, and supportive hydropic evidence. Migraine features are modeled as an overlap or competing pattern, not as a hard exclusion. Hydrops evidence supports MD but should not dominate core clinical criteria.

## 3. PVP/BVP module

File:

```text
default_modules/pvp_bvp.json
```

Purpose:

```text
Worked example for chronic vestibular hypofunction with threshold-based PVP/BVP competition.
```

### Main input nodes

- `age_60_or_older`
- `chronic_dizziness_over_3_months`
- `gait_difficulty_imbalance_or_falls`
- `oscillopsia_or_worse_darkness_uneven_ground`
- `mild_bilateral_vestibular_hypofunction`
- `severe_bilateral_vestibular_hypofunction`
- `central_neurologic_sign_or_mri_lesion`

### Main derived nodes

- `chronic_vestibular_course`
- `gait_balance_symptom_burden`
- `mild_bilateral_vestibular_hypofunction_pattern`
- `severe_bilateral_vestibular_hypofunction_pattern`
- `non_central_chronic_vestibular_pattern`

### Main target nodes

- `dx_presbyvestibulopathy`
- `dx_bilateral_vestibulopathy`

### Modeling logic

PVP is modeled as an age-related chronic vestibular syndrome with mild bilateral vestibular hypofunction. BVP is modeled as the competing severe-threshold diagnosis. Severe bilateral vestibular loss strongly supports BVP and competes against PVP.

## Intercepts

All target-disease intercepts are placeholders. They should be adjusted to the intended clinical pathway before validation.

Examples of pathway-specific settings:

- community dizziness screening;
- first-visit ENT dizziness clinic;
- tertiary vestibular laboratory referral;
- chronic dizziness clinic;
- emergency acute vestibular syndrome pathway.

## Running all default modules

```bash
bayesseed list-modules --modules default_modules/
python examples/run_examples.py
```

## Visualizing a module

```bash
bayesseed mermaid default_modules/bppv.json
bayesseed mermaid default_modules/meniere_disease.json
bayesseed mermaid default_modules/pvp_bvp.json
```
