# DeepClean: Automated Data Engineering Pipeline

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/)
[![Pandas](https://img.shields.io/badge/pandas-2.0%2B-150458.svg?style=flat&logo=pandas&logoColor=white)](https://pandas.pydata.org/)

DeepClean is a robust Python-based framework designed to automate the critical stages of the Data Engineering cleaning lifecycle. It is available as both a reproducible Python class for programmatic use and a **Streamlit Web Application** for interactive data processing.

## Technical Capabilities

| Module | Description | Statistical Method |
| :--- | :--- | :--- |
| **Web Interface** | Interactive CSV uploader and cleaning dashboard. | Streamlit UI |
| **Integrity Engine** | Identifies and removes redundant observations. | Exact Row Matching |
| **Temporal Processor** | Deconstructs timestamps into numerical features. | Feature Extraction |
| **Quality Control** | Imputes missing values in numerical columns. | Mean/Median/Mode |
| **Outlier Shield** | Detects and clips extreme statistical anomalies. | Z-Score (3.0 Sigma) |
| **Feature Scaler** | Standardizes numerical ranges for model readiness. | Z-score/Min-Max |

## Repository Architecture

```text
├── src/
│   └── cleaner.py             # Core DeepClean logic (The Engine)
├── docs/
│   └── architecture.md        # Technical design and diagrams
├── app.py                     # Streamlit Web Application
├── data_cleaning_tool.ipynb   # Interactive demonstration
├── requirements.txt           # Dependency manifest
├── LICENSE                    # MIT License
└── README.md                  # Project overview
```

## Installation and Deployment

### Local Web App
1. Clone the repository and navigate to the folder.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Launch the app:
   ```bash
   streamlit run app.py
   ```

### Programmatic Usage
```python
from src.cleaner import DeepClean

cleaner = DeepClean(dataframe)
cleaned_df = cleaner.clean()
```

## 🚀 Deployment (Streamlit Cloud)
This project is optimized for deployment on Streamlit Cloud. Simply connect your GitHub repository and point the main file to `app.py`.

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
