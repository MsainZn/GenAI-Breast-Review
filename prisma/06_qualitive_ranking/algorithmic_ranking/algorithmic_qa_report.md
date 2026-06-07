==================== SELECTION REPORT ====================
File: articles_before_qualitive_assess.csv
Rows total: 224 | Selected: 75
Quality column used: __auto_quality__ | Mode: AUTO_FALLBACK=citations_log1p

-- Quality summary --
Full:     mean=0.0161  median=0.0000  min=0.0000  max=1.0000
Selected: mean=0.0480  median=0.0000  min=0.0000  max=1.0000

== algorithm (top 30 by full %) ==
                               full_%  selected_%  diff_pp
algorithm
Large Language Model (LLM)      45.98       45.33    -0.65
Vision-Language-Model (VLM)     18.75       18.67    -0.08
Backbone (foundational) model   16.07       16.00    -0.07
Diffusions/GANs                 13.39       13.33    -0.06
Drug Discovery                   3.12        2.67    -0.45
RAG                              2.23        2.67     0.44
Explainable AI                   0.45        1.33     0.88

== training_technology (top 30 by full %) ==
                                       full_%  selected_%  diff_pp
training_technology
Supervised Fine-tunnig                  47.77       45.33    -2.44
In-context Learning Or Just Inference   38.39       38.67     0.28
Synthetic Data Generation               10.27       10.67     0.40
Unsupervised Learning                    3.12        4.00     0.88
Federated learning                       0.45        1.33     0.88

== medical_goal (top 30 by full %) ==
                                  full_%  selected_%  diff_pp
medical_goal
Pre-surgery & Treatment Planning   89.29       89.33     0.04
Post-surgery & Follow-up           10.71       10.67    -0.04

== modality_reference (top 30 by full %) ==
                                                                full_%  selected_%  diff_pp
modality_reference
Unknown                                                          30.36       29.33    -1.03
Pathology and Histopathology (Whole-slide / Microscopy Images)   23.66       24.00     0.34
Mammography (Mammogram)                                          16.96       17.33     0.37
Ultrasound                                                       12.95       13.33     0.38
MRI                                                               7.14        6.67    -0.47
CT                                                                4.46        4.00    -0.46
X-ray (Radiograph)                                                3.57        4.00     0.43
Exterior Upper torso Image (RGB)                                  0.89        1.33     0.44

== modality_type (top 30 by full %) ==
               full_%  selected_%  diff_pp
modality_type
Text-only       41.52       44.00     2.48
Imaging-only    32.59       30.67    -1.92
Image-text      25.89       25.33    -0.56

== modality_count (top 30 by full %) ==
                full_%  selected_%  diff_pp
modality_count
Unimodality      71.43       66.67    -4.76
Multimodal       28.57       33.33     4.76

-- Rare theme preservation --
Rare theme threshold: <= 5 occurrences in full set
            theme_col  count_in_full  count_in_selected
             theme_rl              1                  1
        theme_nerf_3d              3                  1
theme_knowledge_graph              4                  1
      theme_federated              5                  2
    theme_ood_anomaly              5                  2

Saved: selected.csv
==========================================================