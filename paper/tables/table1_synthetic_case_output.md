# Table 1. Output from synthetic demonstration cases. 

The table summarizes the top-ranked diagnosis, posterior probability, and principal contributing evidence for nine synthetic cases. These examples demonstrate software behavior, derived-node activation, interaction-node activation, and competing diagnostic probabilities; they are not intended to estimate diagnostic accuracy or clinical performance.

| **Case**                | **Expected pattern**              | **Top-ranked diagnosis** | **Posterior** | **Main behavior**                                            |
| ----------------------- | --------------------------------- | ------------------------ | ------------- | ------------------------------------------------------------ |
| S01 PC-BPPV             | Typical posterior-canal BPPV      | BPPV                     | 0.818         | PC positional pattern + brief syndrome + PC concordance      |
| S02 HC-BPPV             | Typical horizontal-canal BPPV     | BPPV                     | 0.802         | HC positional pattern + brief syndrome + HC concordance      |
| S03 subjective BPPV     | Subjective BPPV, lower confidence | BPPV                     | 0.142         | Subjective pattern; no PC/HC concordance boost               |
| S04 central red flag    | Low modeled-diagnosis confidence | MD                       | 0.016         | All modeled diagnoses remain low; BPPV suppressed to 0.005 and BVP to 0.009    |
| S05 definite-like MD    | MD pattern                        | MD                       | 0.900         | Episodic vestibular, auditory, cochlear, and hydrops evidence |
| S06 MD–migraine overlap | MD with migraine overlap          | MD                       | 0.378         | Episodic and auditory evidence with migraine-overlap pattern |
| S07 typical PVP         | PVP                               | PVP                      | 0.450         | Age, chronicity, and mild bilateral hypofunction             |
| S08 BVP competitor      | BVP                               | BVP                      | 0.599         | Severe  bilateral hypofunction + BVP functional syndrome + syndrome-test concordance |
| S09 mixed MD/PVP        | Mixed MD/PVP evidence             | MD                       | 0.450         | Near-tie with PVP; competing MD and PVP evidence             |
