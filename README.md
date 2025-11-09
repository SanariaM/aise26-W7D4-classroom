# W7D4 — Live Class Repo (Open in VS Code)

This repo includes the **live code** you’ll see me write AND the **breakout TODOs** inside the **same files**.  
Follow these steps exactly in **VS Code**.

---

## Prerequisites (install before class)
- **Python 3.10+** (3.11/3.12 ok) – verify with `python --version` (or `python3 --version`)
- **pip** (comes with Python)
- **VS Code** + the **Python** extension (Microsoft)
- macOS/Linux shell uses `source` to activate venv; Windows PowerShell uses `.\.venv\Scripts\Activate.ps1`

If `python` runs Python 2 on your machine, use `python3` in all commands below.

---

## 1) Open in VS Code
1. Unzip the folder.
2. In VS Code: **File → Open Folder…** and select the project folder.
3. Open the **VS Code Terminal**: **View → Terminal** (we’ll run all commands here).

---

## 2) Create and activate a virtual environment
```bash
# macOS / Linux
python -m venv .venv
source .venv/bin/activate

# Windows PowerShell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

> If VS Code asks you to select an interpreter, choose the one inside `.venv`.

Install dependencies:
```bash
pip install -r requirements.txt
```
This installs: `pandas`, `scikit-learn`, `joblib`.

---

## 3) Run order (what to run, what to expect, and why)

### A) Feature Store (live code + breakout in the same file)
**File:** `feature_store.py`

Run:
```bash
python feature_store.py
python -c "from feature_store import get_features; print(get_features(1))"
```

**Expected:**
- Console prints: `Feature table created`
- New file: `data/user_features.csv`
- The second command prints a single-row dict (user 1) like:
  `{'user_id': 1, 'age': 24, 'avg_purchase': 120.5, 'timestamp': '...'}`

**Why:** We precompute features once so **training and inference are consistent** and faster.

#### Breakout 1 (inside the same file)
Implement two functions in **`feature_store.py`**:
- `add_purchase_frequency_and_save_v2()` → read `data/user_features.csv`, add a derived column `purchase_frequency` (your deterministic rule is fine), write **`data/user_features_v2.csv`**.
- `list_versions()` → return all files in `./data` matching `user_features*.csv` (sorted).

Test after you implement:
```bash
python -c "import feature_store as fs; fs.add_purchase_frequency_and_save_v2(); print(fs.list_versions())"
```
**Expected:**  
- `data/user_features_v2.csv` exists and has the new column.  
- `list_versions()` prints at least `['user_features.csv', 'user_features_v2.csv']`.

---

### B) Model Registry (live code)
**File:** `model_registry.py`

Run:
```bash
python model_registry.py
ls models/
```

**Expected:**
- Console prints: `Model registered: version=YYYYMMDDHHMMSSffffff, MSE=0.000`
- New files in `models/`:
  - `model_<version>.joblib` (the trained model)
  - `metadata_<version>.json` (metrics/metadata, e.g. version, mse, timestamp)

**Why:** This mimics a **model registry**: every model is saved with a unique **version** + **metadata** so we can reproduce results and roll back if needed.

---

### C) Breakout 2 - Experiment Tracking (in the same file)
**File:** `experiment_tracking.py`

Implement:
- `log_run(version: str, mse: float, parameters: dict | None = None)`  
  - Append a row to **`experiment_log.csv`** (create header if file is new).
  - Row format: `version,mse,parameters,timestamp` (convert `parameters` to `str(...)`).
- `get_best_experiment()`  
  - Read the CSV and return the **row (dict)** with the **lowest** `mse`.

Then **uncomment** the two lines at the end of `train_and_register()` in **`model_registry.py`**:
```python
# from experiment_tracking import log_run
# log_run(version=version, mse=float(mse), parameters={"model":"LinearRegression","features":"user_features.csv"})
```
…so each training run logs to `experiment_log.csv` automatically.

Run:
```bash
python model_registry.py
python model_registry.py
python -c "from experiment_tracking import get_best_experiment; print(get_best_experiment())"
```

**Expected:**
- Two “Model registered …” lines with different versions.
- File `experiment_log.csv` appears in the project root with header:
  `version,mse,parameters,timestamp`
- `get_best_experiment()` prints the row (dict) with the **lowest** `mse`.

**Why:** Tracking lets us **compare experiments** and decide what to **promote** in CI/CD.

---

## 4) Troubleshooting

- **`zsh: command not found: #`** — you pasted a **comment** line into the terminal. Only run the commands **without** leading `#`.
- **`No such file or directory: models/`** — run `python model_registry.py` first; it creates the folder.
- **Duplicate versions** — versions include microseconds; if you still clash, wait 1–2 seconds between runs.
- **`ModuleNotFoundError: No module named 'sklearn'`** — activate the venv (`source .venv/bin/activate`) and run `pip install -r requirements.txt`.
- **VS Code uses the wrong Python** — press `Ctrl/Cmd+Shift+P` → “Python: Select Interpreter” → choose the one in `.venv`.
- **Windows activation policy** — if PowerShell blocks activation, run PowerShell as admin and `Set-ExecutionPolicy RemoteSigned` once.

---

## 5) What to submit
- Working implementations for:
  - `add_purchase_frequency_and_save_v2()` + `list_versions()` in `feature_store.py`
  - `log_run(...)` + `get_best_experiment()` in `experiment_tracking.py`
- Short note (2–4 sentences): one limitation + one future improvement.

Good luck! Keep it simple, correct, and reproducible.
