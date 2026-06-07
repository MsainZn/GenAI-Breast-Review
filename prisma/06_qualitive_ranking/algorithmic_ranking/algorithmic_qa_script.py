import re
import numpy as np
import pandas as pd

# ============================================================
# DISTRIBUTION-AWARE TOP-75 SELECTION (PRINT REPORT + ONE CSV)
# ============================================================
# Outputs:
#   - Prints a report (quality + distributions + rare themes kept)
#   - Writes ONE file: selected.csv  (75 rows)
# ============================================================

# =========================
# CONFIG (EDIT THIS)
# =========================
CSV_PATH = "articles_before_qualitive_assess.csv"  # your file
N_SELECT = 75

# If you have a qualitative assessment column, set it EXACTLY.
# Otherwise leave None and fallback is used (citations->log1p or all zeros).
QUALITY_COL = None

CORE_COLS = [
    "algorithm",
    "training_technology",
    "medical_goal",
    "modality_reference",
    "modality_type",
    "modality_count",
]

TEXT_COLS = ["title", "abstract", "keywords"]

MIN_PER_LEVEL = 1
RARE_THEME_MAX_COUNT = 5
TOL_FRAC = 0.05

# =========================
# ALLOWED SCHEMA
# =========================
ALLOWED_BY_COL = {
    "algorithm": {
        "Backbone (foundational) model",
        "Diffusions/GANs",
        "Large Language Model (LLM)",
        "Vision-Language-Model (VLM)",
        "RAG",
        "Agentic Frameworks",
        "NeRF, Gaussian, 3D models",
        "Explainable AI",
        "Drug Discovery",
    },
    "training_technology": {
        "In-context Learning Or Just Inference",
        "Supervised Fine-tunnig",
        "Reinforcement Learning",
        "Unsupervised Learning",
        "Synthetic Data Generation",
        "Federated learning",
    },
    "medical_goal": {
        "Pre-surgery & Treatment Planning",
        "Post-surgery & Follow-up",
    },
    "modality_reference": {
        "X-ray (Radiograph)",
        "Mammography (Mammogram)",
        "Ultrasound",
        "MRI",
        "CT",
        "Exterior Upper torso Image (RGB)",
        "Pathology and Histopathology (Whole-slide / Microscopy Images)",
        "Genomics (e.g., genome, exome)",
        "Transcriptomics (e.g., RNA-seq / gene expression)",
        "Wearable / Sensor Time-Series Data (e.g., ECG, PPG, accelerometer)",
    },
    "modality_type": {"Text-only", "Imaging-only", "Image-text"},
    "modality_count": {"Multimodal", "Unimodality"},
}

# =========================
# THEME PATTERNS (broad)
# =========================
THEME_PATTERNS = {
    "rag": r"\brag\b|retrieval[-\s]?augmented|dense retrieval|vector database|bm25",
    "agentic": r"\bagentic\b|multi[-\s]?agent|tool[-\s]?use|function calling|planner|executor|autonomous agent",
    "rl": r"\brl\b|reinforcement learning|ppo\b|dpo\b|preference optimization|reward model",
    "federated": r"\bfederated\b|federated learning|\bfedavg\b|\bfedprox\b",
    "diffusion": r"\bdiffusion\b|ddpm|score[-\s]?based|latent diffusion",
    "gan": r"\bgan\b|cyclegan|stylegan|dcgan",
    "nerf_3d": r"\bnerf\b|gaussian splatting|radiance field|volumetric|\b3d\b",
    "ood_anomaly": r"out[-\s]?of[-\s]?distribution|\bood\b|anomaly detection|novelty detection",
    "adversarial": r"adversarial|poisoning|attack|backdoor|data poisoning",
    "explainable": r"explainable|\bxai\b|shap|lime|saliency|attribution|interpretab",
    "knowledge_graph": r"knowledge graph|\bkg\b|kegg|drugbank|hetionet|graph rag|graph[-\s]?rag",
    "drug_discovery": r"drug discovery|drug repurpos|molecule|ligand|docking|pharmacophore|hit[-\s]?to[-\s]?lead",
    "fairness_bias": r"fairness|bias|equity|subgroup|disparit",
    "privacy_security": r"privacy|secure|hipaa|phi|data leakage|confidential|local hosting",
}

# =========================
# HELPERS
# =========================
def normalize_multi_value_cell(x):
    if pd.isna(x):
        return []
    s = str(x).strip()
    if not s:
        return []
    parts = re.split(r"\s*;\s*|\s*,\s*", s)
    return [p.strip() for p in parts if p.strip()]

def pick_primary_value(values, allowed_set):
    if not values:
        return "Unknown"
    for v in values:
        if v in allowed_set:
            return v
    return values[0] if values[0] else "Unknown"

def validate_or_unknown(v, allowed_set):
    return v if v in allowed_set else "Unknown"

def compute_text(df):
    def row_text(r):
        chunks = []
        for c in TEXT_COLS:
            if c in df.columns:
                chunks.append("" if pd.isna(r[c]) else str(r[c]))
        return " ".join(chunks).lower()
    return df.apply(row_text, axis=1)

def compute_theme_flags(df):
    text = compute_text(df)
    for theme, pat in THEME_PATTERNS.items():
        df[f"theme_{theme}"] = text.str.contains(pat, regex=True).astype(int)

    # sync structured schema into themes
    if "algorithm" in df.columns:
        df.loc[df["algorithm"].eq("RAG"), "theme_rag"] = 1
        df.loc[df["algorithm"].eq("Agentic Frameworks"), "theme_agentic"] = 1
        df.loc[df["algorithm"].eq("Diffusions/GANs"), "theme_gan"] = 1
        df.loc[df["algorithm"].eq("Explainable AI"), "theme_explainable"] = 1
        df.loc[df["algorithm"].eq("Drug Discovery"), "theme_drug_discovery"] = 1
        df.loc[df["algorithm"].eq("NeRF, Gaussian, 3D models"), "theme_nerf_3d"] = 1

    if "training_technology" in df.columns:
        df.loc[df["training_technology"].eq("Reinforcement Learning"), "theme_rl"] = 1
        df.loc[df["training_technology"].eq("Federated learning"), "theme_federated"] = 1

    return df

def build_targets(series, n_select, min_per_level=1):
    counts = series.value_counts(dropna=False)
    props = counts / counts.sum()
    raw = props * n_select

    targets = raw.round().astype(int)
    if min_per_level > 0:
        targets = targets.clip(lower=min_per_level)

    for lvl, cnt in counts.items():
        targets.loc[lvl] = min(int(targets.loc[lvl]), int(cnt))

    diff = int(n_select - targets.sum())
    if diff != 0:
        if diff > 0:
            rema = (raw - np.floor(raw)).sort_values(ascending=False)
            for lvl in rema.index:
                if diff == 0:
                    break
                if targets.loc[lvl] < counts.loc[lvl]:
                    targets.loc[lvl] += 1
                    diff -= 1
        else:
            floor_min = min_per_level if min_per_level > 0 else 0
            for lvl in targets.sort_values(ascending=False).index:
                if diff == 0:
                    break
                if targets.loc[lvl] > floor_min:
                    targets.loc[lvl] -= 1
                    diff += 1
    return targets

def find_quality_col_or_fallback(df, requested_quality_col=None):
    cols = list(df.columns)
    if requested_quality_col is not None and requested_quality_col in cols:
        return requested_quality_col, None

    # detect score-like columns
    candidates = []
    for c in cols:
        cl = c.lower()
        if any(k in cl for k in ["qual", "quality", "assessment", "rating", "score", "qa"]) and \
           not any(bad in cl for bad in ["citation", "citations", "cite"]):
            candidates.append(c)

    if candidates:
        return candidates[0], None

    # fallback: citations if available, else zeros
    fallback_col = "__auto_quality__"
    if "citations" in df.columns:
        df[fallback_col] = pd.to_numeric(df["citations"], errors="coerce").fillna(0)
        df[fallback_col] = np.log1p(df[fallback_col])
        mode = "AUTO_FALLBACK=citations_log1p"
    else:
        df[fallback_col] = 0.0
        mode = "AUTO_FALLBACK=all_zero"

    return fallback_col, mode

def pct_dist(df, col):
    return (df[col].value_counts(normalize=True) * 100).round(2)

def print_dist_block(full_df, sel_df, col, topn=25):
    full = pct_dist(full_df, col)
    sel = pct_dist(sel_df, col)
    comp = pd.concat([full.rename("full_%"), sel.rename("selected_%")], axis=1).fillna(0)
    comp["diff_pp"] = (comp["selected_%"] - comp["full_%"]).round(2)
    comp = comp.sort_values("full_%", ascending=False)

    print(f"\n== {col} (top {topn} by full %) ==")
    print(comp.head(topn).to_string())

# =========================
# LOAD
# =========================
df = pd.read_csv(CSV_PATH)
df.columns = [c.strip() for c in df.columns]

# Quality column or fallback
QUALITY_COL, quality_mode = find_quality_col_or_fallback(df, QUALITY_COL)

df[QUALITY_COL] = pd.to_numeric(df[QUALITY_COL], errors="coerce")
df[QUALITY_COL] = df[QUALITY_COL].fillna(df[QUALITY_COL].min() - 1)

qmin, qmax = df[QUALITY_COL].min(), df[QUALITY_COL].max()
df["_q"] = (df[QUALITY_COL] - qmin) / (qmax - qmin) if qmax > qmin else 0.0

# Normalize/validate the 6 critical columns
for c in CORE_COLS:
    if c not in df.columns:
        df[c] = "Unknown"
    allowed = ALLOWED_BY_COL[c]
    df[c] = df[c].apply(lambda x: pick_primary_value(normalize_multi_value_cell(x), allowed))
    df[c] = df[c].apply(lambda v: validate_or_unknown(v, allowed))

# Theme flags
df = compute_theme_flags(df)
theme_cols = [c for c in df.columns if c.startswith("theme_")]
theme_counts = {c: int(df[c].sum()) for c in theme_cols}
rare_theme_cols = [c for c, k in theme_counts.items() if 0 < k <= RARE_THEME_MAX_COUNT]

STRAT_COLS = CORE_COLS + rare_theme_cols

# Targets + tolerances
targets = {c: build_targets(df[c], N_SELECT, MIN_PER_LEVEL) for c in STRAT_COLS}
tols = {c: {lvl: max(1, int(round(TOL_FRAC * N_SELECT))) for lvl in targets[c].index} for c in STRAT_COLS}

selected_idx = set()
cur = {c: {lvl: 0 for lvl in targets[c].index.tolist()} for c in STRAT_COLS}

def add_idx(i):
    selected_idx.add(i)
    for c in STRAT_COLS:
        lvl = df.at[i, c]
        if lvl not in cur[c]:
            cur[c][lvl] = 0
        cur[c][lvl] += 1

# Stage A: hard coverage (rare-first)
for c in STRAT_COLS:
    lvl_order = targets[c].sort_values(ascending=True).index.tolist()
    for lvl in lvl_order:
        need = min(int(targets[c].loc[lvl]), MIN_PER_LEVEL) if MIN_PER_LEVEL > 0 else 0
        while cur[c].get(lvl, 0) < need and len(selected_idx) < N_SELECT:
            cand = df.index[(df[c] == lvl) & (~df.index.isin(selected_idx))]
            if len(cand) == 0:
                break
            best = df.loc[cand].sort_values("_q", ascending=False).index[0]
            add_idx(best)

def score_row(i):
    row = df.loc[i]
    base = float(row["_q"])

    penalty = 0.0
    for c in STRAT_COLS:
        lvl = row[c]
        upper = int(targets[c].get(lvl, 0) + tols[c].get(lvl, 1))
        if cur[c].get(lvl, 0) >= upper:
            penalty += 1.0

    bonus = 0.0
    for c in STRAT_COLS:
        lvl = row[c]
        tgt = int(targets[c].get(lvl, 0))
        if cur[c].get(lvl, 0) < tgt:
            bonus += (1.0 / max(1, tgt))

    return base + 0.25 * bonus - 0.85 * penalty

# Stage B: balanced greedy fill
pool = df.index[~df.index.isin(selected_idx)]
while len(selected_idx) < N_SELECT and len(pool) > 0:
    best_i = max(pool, key=score_row)
    add_idx(best_i)
    pool = pool[pool != best_i]

selected = df.loc[sorted(selected_idx)].copy()

# =========================
# WRITE ONE FILE
# =========================
selected.to_csv("selected.csv", index=False)

# =========================
# PRINT REPORT
# =========================
print("\n==================== SELECTION REPORT ====================")
print(f"File: {CSV_PATH}")
print(f"Rows total: {len(df)} | Selected: {len(selected)}")
print(f"Quality column used: {QUALITY_COL} | Mode: {quality_mode or 'USER/DETECTED'}")

print("\n-- Quality summary --")
print("Full:     mean={:.4f}  median={:.4f}  min={:.4f}  max={:.4f}".format(
    df["_q"].mean(), df["_q"].median(), df["_q"].min(), df["_q"].max()
))
print("Selected: mean={:.4f}  median={:.4f}  min={:.4f}  max={:.4f}".format(
    selected["_q"].mean(), selected["_q"].median(), selected["_q"].min(), selected["_q"].max()
))

# Core distribution checks
for col in CORE_COLS:
    print_dist_block(df, selected, col, topn=30)

# Rare theme preservation
print("\n-- Rare theme preservation --")
print(f"Rare theme threshold: <= {RARE_THEME_MAX_COUNT} occurrences in full set")
if not rare_theme_cols:
    print("No rare themes detected from text.")
else:
    rows = []
    for c in sorted(rare_theme_cols, key=lambda x: theme_counts[x]):
        rows.append((c, theme_counts[c], int(selected[c].sum())))
    rare_df = pd.DataFrame(rows, columns=["theme_col", "count_in_full", "count_in_selected"])
    print(rare_df.to_string(index=False))

print("\nSaved: selected.csv")
print("==========================================================\n")