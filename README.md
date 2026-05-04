# DeepClean OS

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://deep-clean-os.streamlit.app/)

### Live Deployment
**Production URL**: [https://deep-clean-os.streamlit.app/](https://deep-clean-os.streamlit.app/)

---

DeepClean OS is an automated data engineering pipeline designed to transform raw, messy datasets into high-fidelity, ML-ready assets. Utilizing a modular **Bento Grid Architecture**, it provides both a programmatic engine and a sleek, night-mode web interface.

### Technical Stack
![Pandas](https://img.shields.io/badge/pandas-2.0%2B-150458.svg?style=flat&logo=pandas&logoColor=white)
![NumPy](https://img.shields.io/badge/numpy-1.24%2B-013243.svg?style=flat&logo=numpy&logoColor=white)
![Scikit-Learn](https://img.shields.io/badge/scikit--learn-1.2%2B-F7931E.svg?style=flat&logo=scikit-learn&logoColor=white)
![SciPy](https://img.shields.io/badge/scipy-1.10%2B-8CAAE6.svg?style=flat&logo=scipy&logoColor=white)
![Streamlit](https://img.shields.io/badge/streamlit-1.24%2B-FF4B4B.svg?style=flat&logo=streamlit&logoColor=white)

---

## 📐 System Architecture

The pipeline follows a strict **Sequential Dependency Chain** to ensure data integrity at every stage of the transformation process.

```mermaid
graph TD
    Input[/CSV Payload/] --> Dup[Duplicate Scrubber]
    Dup --> Temp[Temporal Transformer]
    Temp --> Imp[Statistical Imputer]
    Imp --> Out[Outlier Clipper]
    Out --> Enc[Categorical Encoder]
    Enc --> Scale[Feature Scaler]
    Scale --> Output[/Cleaned Dataset/]

    style Input fill:#0a0c10,stroke:#8892b0,stroke-width:2px,color:#fff
    style Output fill:#05070a,stroke:#00d4ff,stroke-width:3px,color:#00d4ff
    style Dup fill:rgba(0,212,255,0.05),stroke:#00d4ff
    style Scale fill:rgba(0,212,255,0.05),stroke:#00d4ff
```

---

## 🛠️ Operational Modules

| Module | Technical Logic | Implementation |
| :--- | :--- | :--- |
| **Integrity Engine** | Exact row-hash matching and removal. | `drop_duplicates()` |
| **Temporal Transformer** | Deconstruction of timestamps into Y/M/D/W features. | `pd.to_datetime` |
| **Quality Control** | Statistical mean/median/mode imputation. | `SimpleImputer` |
| **Outlier Shield** | 3-Sigma Z-score clipping and Winsorization. | `scipy.stats` |
| **Model Readiness** | Label encoding and feature standardization. | `StandardScaler` |

---

## 🚀 Getting Started

### Web Interface (Recommended)
Access the live environment at: [deep-clean-os.streamlit.app](https://deep-clean-os.streamlit.app/)

### Local Development
1. Clone the repository.
2. Install dependencies: `pip install -r requirements.txt`.
3. Launch the OS: `streamlit run app.py`.

## 📄 License
Licensed under the MIT License. See [LICENSE](LICENSE) for details.
