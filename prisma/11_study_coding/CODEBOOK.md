# Study-level coding and composite maturity index

This folder contains the study-level coding of the 77 included studies (`../09_confirmed_prisma/confirmed_prisma.csv`) and the
outputs of the composite maturity index reported in the manuscript. All values can be regenerated from the repository root with

```bash
python Code/compute_index.py prisma/11_study_coding/study_coding.csv prisma/11_study_coding/public_datasets.csv prisma/11_study_coding
python Code/make_index_figures.py prisma/11_study_coding figs
python Code/sankey_final77.py
```

## Files

| File | Content |
|---|---|
| `study_coding.csv` | One row per included study: BibTeX key, title, primary and optional secondary workflow subdomain, 17 binary evidence indicators, and the reported sample size |
| `method_coding.csv` | One row per included study: data modalities (`;`-separated), training paradigm, and model family used in the Sankey analysis |
| `public_datasets.csv` | The 35 public datasets, benchmarks, and guideline corpora used by the included studies, with modality, use case, citing studies, link, and workflow phase |
| `subdomain_indicators.csv` | Weighted indicator proportions per subdomain (Eq. 1 of the manuscript) and the derived terms |
| `subdomain_scores.csv` | Six dimension scores (1–5) per subdomain (Eq. 2 of the manuscript) |
| `weight_sensitivity.csv` | Spearman correlation between the a priori weights and equal weights within each dimension |

## Workflow subdomains

| Code | Subdomain | Phase |
|---|---|---|
| ID | Initial diagnosis and lesion characterization | Preoperative |
| TPA | Tumor and patient assessment | Preoperative |
| MDT | MDT evaluation, staging, and risk stratification | Preoperative |
| SDM | Patient consultation and shared decision-making | Preoperative |
| SAS | Surgical approach selection | Operative |
| MAR | Margin assessment and intraoperative confirmation | Operative |
| AXL | Axillary lymph node management | Operative |
| REC | Reconstruction planning | Operative |
| POC | Postoperative care and adjuvant therapy planning | Postoperative |
| COM | Communication, symptom capture, and recovery support | Postoperative |
| FUP | Follow-up and long-term monitoring | Postoperative |

A study is assigned to a secondary subdomain only when its contribution clearly spans two decisions; it then contributes half of its weight to each.

## Evidence indicators (binary, one per study)

| Column | Coded as 1 when the study … | Dimension |
|---|---|---|
| `patient_facing` | serves patients directly (patient-facing output or interaction) | Patient-centeredness (0.45) |
| `patient_endpoint` | measures patient-reported or experience endpoints (readability, empathy, comprehension, decisional quality, anxiety) | Patient-centeredness (0.30) |
| `personalized` | produces individualized outputs for a specific patient | Patient-centeredness (0.25) |
| `source_controlled` | constrains generation with retrieved sources, guidelines, or a schema | Grounding and faithfulness (0.35) |
| `extraction` | addresses an extractive or structuring task grounded in a source document | Grounding and faithfulness (0.25) |
| `faithfulness_audited` | audits factual faithfulness with clinical experts | Grounding and faithfulness (0.20) |
| `open_generation` | relies on open-ended generation (enters the score as 1 − x, "bounded generation") | Grounding and faithfulness (0.20) |
| `public_data` | uses task-relevant public data | Data availability (0.65) |
| `specialized` | develops a domain-specialized model or pipeline rather than generic one-shot prompting | Technical maturity (0.30) |
| `benchmarking` | benchmarks against comparators or human baselines | Technical maturity (0.25) |
| `external_validation` | reports external, temporal, or multi-site validation | Technical maturity (0.25); Clinical validation (0.20) |
| `workflow_proximity` | sits directly within a clinical workflow step | Workflow integration (0.55) |
| `integrated_pipeline` | integrates several steps into one pipeline | Workflow integration (0.25) |
| `deployed` | reports a live, pilot, implementation, or trial deployment | Workflow integration (0.20) |
| `real_clinical` | uses real patient data rather than synthetic or benchmark-only data | Clinical validation (0.25) |
| `human_eval` | includes evaluation by clinicians or patients | Clinical validation (0.20) |
| `prospective` | is prospective | Clinical validation (0.15) |
| `sample_size` | reported number of patients, cases, reports, or images (numeric) | Clinical validation (0.20, as min{1, log10(n)/4}) |

Derived terms: evidence volume `ln(1+W_s)/ln(1+max W)` (Technical maturity, 0.20), where `W_s` is the total study weight of the subdomain, and dataset breadth, the number of distinct public resources used in the subdomain divided by the largest such number (Data availability, 0.35).

## Method coding categories

* **Training paradigm**: Inference-only / prompting; Supervised fine-tuning; Self-supervised pretraining; Weakly-supervised learning; Others (semi-/unsupervised; federated).
* **Model family**: Large Language Model (LLM); Vision-Language-Model (VLM); Foundational model; RAG & Agentic Systems; Diffusions/GANs; 3D modeling & XR.
* **Data modality**: Clinical / guideline text; Mammogram; Ultrasound; MRI; CT; X-ray; Histopathology / Pathology; Genomics/Transcriptomics; Exterior breast (RGB).
