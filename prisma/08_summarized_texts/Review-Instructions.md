# README — Article Review CSV Guide

An excel named `candiate_papers.xslx` is used to selected articles in multiple sheets and create **standardized summaries** across all reviewed papers. The goal is to make sure every reviewer captures the same core information in a consistent format, so the final dataset is easy to compare, filter, and analyze.

## General Instructions

- Fill **one row per article**.
- Use the exact column names in the CSV.
- Keep entries **concise but specific**.
- When information is not available in the paper, write `NA`.
- Do **not** invent missing details.
- Use consistent terminology across papers whenever possible.
- For metrics, datasets, and model names, prefer the wording used in the paper.

## CSV Columns and What to Write

| Column name | What to include | Guidance / expected format |
|---|---|---|
| `title` | Full title of the paper | Copy the official paper title exactly as written. |
| `path_to_fulltext` | File path or link to the full paper | Prefer a relative path if the PDF is stored locally in the project folder, for example `papers/author_year_title.pdf`. If the file is online only, provide the URL. |
| `Summary of the paper (highlighting novelty & goals)` | A short summary of the paper | Write 3–6 sentences covering: **(1)** the problem addressed, **(2)** the main goal, **(3)** what is novel or different from prior work, and **(4)** the main takeaway. Avoid copying the abstract word-for-word. |
| `Datasets names (also is public or private)` | All datasets used in the study | List each dataset and label it as `public` or `private`. Example: `BraTS (public); Internal hospital cohort (private)`. If both training and external validation datasets are used, include both. |
| `Baseline model/architecture` | The main model, backbone, comparator, or baseline used | Record the architecture or model family used in the study, such as `U-Net`, `ResNet-50`, `Type of ViT`, `3D CNN`, `Random Forest`, or `GPT 4.5` or etc. If the paper compares multiple baselines, list the all but key ones first. |
| `Training  Approach` | How the model was trained | Include the learning setup and any important strategy, such as `supervised learning`, `semi-supervised learning`, `self-supervised pretraining`, `fine-tuning`, `reinforcement learning`, `prompt engineering / inference-only`, `federated learning`, or `weak supervision`. |
| `Medical Phase (pre/post/treatment)` | The clinical timing of the data or task | Use `pre`, `post`, `both`, or `NA` depending on whether the study focuses on pre-treatment / pre-operative data, post-treatment / post-operative data, both, or does not specify. |
| `Medical Modality` | The medical data source or acquisition modality | Examples: `MRI`, `CT`, `X-ray`, `RGB image`, `Ultrasound`, `Histopathology`, `Genetics`, or `Multi-modal (with stating the ones)`. |
| `Model input modality` | What the model directly receives as input | Examples: `image-only`, `text-only`, `image+text`. These can also include `tabular clinical data`, `time series`, `video`, `multi-modal image + tabular` in case the study include those. This is about the model input, not the broader medical modality only. |
| `Evaluation Metric & value (like the study uses acc=x, IoU=y, & etc)` | The reported evaluation metrics and their values | Report the exact metrics and values used in the paper. Example: `Accuracy=0.91; AUC=0.95; Dice=0.87`. If there are multiple experiments, record the main result or the best clearly identified result and keep the format consistent. |

## Recommended Writing Rules

### 1. Summary field
The summary should focus on:
- the clinical or technical problem,
- the study objective,
- the novelty,
- and the main result or conclusion.

A strong summary usually answers:
- What problem does the paper solve?
- Why is it important?
- What is new compared with previous work?
- What did the authors show?

### 2. Dataset field
For dataset reporting:
- include all datasets used for training, validation, testing, or external validation,
- clearly mark whether each dataset is **public** or **private**,
- mention if the dataset is from a single center, multi-center, or in-house when relevant.

Suggested format:

```text
Dataset A (public); Dataset B (private); External test cohort (private)
```

### 3. Model / baseline field
If the paper proposes a new method, include:
- the proposed model,
- and optionally the strongest baseline(s) used for comparison.

Suggested format:

```text
Proposed: Swin-UNet; Baselines: U-Net, nnU-Net, ResNet-50
```

### 4. Training approach field
Capture the main training strategy, not low-level hyperparameters unless essential.

Examples:
- `Supervised learning with 5-fold cross-validation`
- `Transfer learning from ImageNet`
- `Self-supervised pretraining followed by fine-tuning`
- `Federated learning across 3 hospitals`
- `Weakly supervised classification`

### 5. Medical phase field
Use this field consistently:
- `pre` = before intervention, treatment, or surgery
- `post` = after intervention, treatment, or surgery
- `both` = includes both pre and post phases
- `NA` = not applicable or not clearly specified

### 6. Evaluation metrics field
Please preserve the metric names used by the authors and provide values in a compact format.

Suggested format:

```text
Accuracy=0.89; AUC=0.93; F1=0.84
```

For segmentation or detection studies, examples include:

```text
Dice=0.87; IoU=0.79; Sensitivity=0.91
```

If the paper reports results for multiple datasets, you may write:

```text
Internal: AUC=0.94; External: AUC=0.90
```

## Missing or Ambiguous Information

If the paper does not clearly state a required item:
- use `NA`,
- do not guess,
- and keep the rest of the row complete.

If a paper uses unusual terminology, map it to the closest standard wording while staying faithful to the paper.


## Roles and Recommendations

Based on the intrest and the current sitiation of our team, below division is suggested for compiling the review:

- use `Moe` -> `LLM` and `RAG-Agentic` sheets,
- use `Helena` -> `VLM` and `Diffiusion` sheets,
- use `Felipe` -> `Foundation models` sheet,
- use `Leo` -> `Mixed` sheet.

If a paper uses unusual terminology, map it to the closest standard wording while staying faithful to the paper.


## Final Note

Thank you all for your help and please reach out to me if you need anything else in the meanwhile.
