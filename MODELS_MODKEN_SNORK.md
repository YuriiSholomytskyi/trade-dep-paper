# Accessing and Running Underlying Models from `modken-snork`

This guide explains how the theoretical and structural models used in this paper ([`paper/trade_recovery_revised.tex`](file:///Users/elenasholomitskaya/Documents/Yura/trade-dep-paper/paper/trade_recovery_revised.tex)) connect to the [`modken-snork`](file:///Users/elenasholomitskaya/Documents/Yura/modken-snork) repository located at the same directory level (`../modken-snork`), and how to access and execute them.

---

## 1. Overview of the Linkage

The primary model integrated with `modken-snork` is the **Layer-2 Dynamic Core-Periphery Model** (`core_periphery_ai`), presented in Section 4.2 and detailed in Appendix H of the paper:

* **Paper Section**: Section 4.2 (*"A dynamic illustration"*) and Appendix H (*"The dynamic core-periphery model"*).
* **Model Purpose**: Solves a semi-structural forward-looking core-periphery gap system comparing an import-intensive core expansion (consumption) against an import-light core expansion (AI/energy investment tilt $\theta$).
* **Paper Output**: Generates [`output/model_layer2_irf.png`](file:///Users/elenasholomitskaya/Documents/Yura/trade-dep-paper/output/model_layer2_irf.png) (3-panel IRF comparison).

In addition, [`scripts/seasonal_adjust.py`](file:///Users/elenasholomitskaya/Documents/Yura/trade-dep-paper/scripts/seasonal_adjust.py) connects to `modken-snork` to utilize its X-13ARIMA-SEATS wrapper (`SeasonalAdjuster`).

---

## 2. Model Location in `modken-snork`

All files for the `core_periphery_ai` model are housed in `../modken-snork`:

| Component | Path relative to workspace root | Description |
|---|---|---|
| **Model Equations** | `../modken-snork/rounds/core_periphery_ai/model/core_periphery_ai.yaml` | System equations (Euler, policy rule, import demand, periphery link) |
| **Parameters** | `../modken-snork/rounds/core_periphery_ai/model/core_periphery_ai_parameters.json` | Calibrated values ($\rho_{ae}, \rho_i, \sigma, \phi_y, \theta, \lambda$, etc.) |
| **Variable Metadata** | `../modken-snork/rounds/core_periphery_ai/model/core_periphery_ai.vardict.json` | Variable dictionary and mappings |
| **Round Registry** | `../modken-snork/rounds/config.json` | Registers `"core_periphery_ai"` in modken |
| **Simulation Script** | `../modken-snork/scratch/cp_ai_irf.py` | Runs Klein solver IRFs and saves `model_layer2_irf.png` |

---

## 3. How to Run the Model via `modken-snork`

### Method A: Running the Existing IRF Script

1. Navigate to the `modken-snork` directory:
   ```bash
   cd ../modken-snork
   ```

2. Run the driver script:
   ```bash
   python scratch/cp_ai_irf.py
   ```

> [!IMPORTANT]
> **Path Configuration Note:**
> In `scratch/cp_ai_irf.py`, the paths were initially set to absolute Windows paths (`C:\Users\ysholomytskyi\...`). If executing on macOS/Linux or outside that environment, ensure the repository root and output directory resolve dynamically:
> ```python
> import os, sys
> REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
> OUT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../trade-dep-paper/output"))
> sys.path.insert(0, REPO)
> ```

---

### Method B: Calling `ModKen` Programmatically in Python

You can interact with, alter parameters of, and solve `core_periphery_ai` directly from Python:

```python
import os
import sys
import numpy as np
import matplotlib.pyplot as plt

# 1. Point to modken-snork root (must precede any pip-installed modken)
SNORK_ROOT = os.path.abspath(os.path.join(os.getcwd(), "..", "modken-snork"))
sys.path.insert(0, SNORK_ROOT)

from modken.modken import ModKen

# 2. Initialize the round
mk = ModKen("core_periphery_ai")

# 3. Read model and solve using the Klein solver (e.g., testing tilt theta = 0.80)
mk.read_model(
    assign={"theta": 0.80},   # theta: AI/energy import-diversion tilt
    use_cache=False,
    solver="Klein"
)

# 4. Run impulse response functions (shocks: SHK_NEWS, SHK_CUS, SHK_P)
shocks = ["SHK_NEWS", "SHK_CUS", "SHK_P"]
mk.run_irf(shocks_list=shocks, n_periods=24)

# 5. Extract results
irfdb = mk.data.irfdb
y_us = np.asarray(irfdb["SHK_NEWS"]["y_US"])
m_us = np.asarray(irfdb["SHK_NEWS"]["m"])
y_p  = np.asarray(irfdb["SHK_NEWS"]["y_P"])

print("Peak US output response:", np.max(y_us))
print("Trough US import response:", np.min(m_us))
print("Periphery output response:", np.min(y_p))
```

### Key Parameter & Shock Reference:
* **`theta`**: The AI/energy investment tilt. When $\theta$ increases (e.g., $0.20 \to 0.80$), US absorption shifts toward domestic capital with low import content ($m = \mu_c c_{US} - \theta\, inv_{US}$).
* **`SHK_NEWS`**: Optimism / AI investment belief shock triggering domestic capex.
* **`SHK_CUS`**: Household consumption demand shock (import-intensive).
* **`SHK_P`**: Periphery idiosyncratic domestic downturn shock.

---

## 4. Self-Contained Standalone Alternative (No ModKen Dependency)

For convenience and portability (e.g. running without having the `modken-snork` environment installed), a standalone analytical implementation of the exact same system is included in this repository:

* **Script**: [`scripts/model_dynamic.py`](file:///Users/elenasholomitskaya/Documents/Yura/trade-dep-paper/scripts/model_dynamic.py)
* **Execution**:
  ```bash
  python scripts/model_dynamic.py
  ```
* **How it works**: Solves the forward-looking Euler equation by backward recursion and produces the identical [`output/model_layer2_irf.png`](file:///Users/elenasholomitskaya/Documents/Yura/trade-dep-paper/output/model_layer2_irf.png).

Similarly, the **Layer-1 Static Risk-Sharing Portfolio Model** is self-contained:
* **Script**: [`scripts/model_layer1.py`](file:///Users/elenasholomitskaya/Documents/Yura/trade-dep-paper/scripts/model_layer1.py)
* **Execution**:
  ```bash
  python scripts/model_layer1.py
  ```
* **Output**: Generates [`output/model_layer1.png`](file:///Users/elenasholomitskaya/Documents/Yura/trade-dep-paper/output/model_layer1.png).

---

## 5. Using the `SeasonalAdjuster` from `modken-snork`

If regenerating seasonal adjustments for the monthly activity panel:
* **Script**: [`scripts/seasonal_adjust.py`](file:///Users/elenasholomitskaya/Documents/Yura/trade-dep-paper/scripts/seasonal_adjust.py)
* **Configuration**: Set the `SNORK_ROOT` environment variable or edit the fallback path in the script:
  ```bash
  export SNORK_ROOT="$(pwd)/../modken-snork"
  python scripts/seasonal_adjust.py
  ```
This loads `modken.data.transforms.SeasonalAdjuster` (wrapping X-13ARIMA-SEATS).

