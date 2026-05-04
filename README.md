# DeepClean: Automated Data Engineering Pipeline

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)

### Core Technologies
![Pandas](https://img.shields.io/badge/pandas-2.0%2B-150458.svg?style=flat&logo=pandas&logoColor=white)
![NumPy](https://img.shields.io/badge/numpy-1.24%2B-013243.svg?style=flat&logo=numpy&logoColor=white)
![Scikit-Learn](https://img.shields.io/badge/scikit--learn-1.2%2B-F7931E.svg?style=flat&logo=scikit-learn&logoColor=white)
![SciPy](https://img.shields.io/badge/scipy-1.10%2B-8CAAE6.svg?style=flat&logo=scipy&logoColor=white)
![Matplotlib](https://img.shields.io/badge/matplotlib-3.7%2B-11557c.svg?style=flat&logo=plotly&logoColor=white)
![Seaborn](https://img.shields.io/badge/seaborn-0.12%2B-444444.svg?style=flat)
![Streamlit](https://img.shields.io/badge/streamlit-1.24%2B-FF4B4B.svg?style=flat&logo=streamlit&logoColor=white)

DeepClean is a robust Python-based framework designed to automate the critical stages of the Data Engineering cleaning lifecycle. It is available as both a reproducible Python class for programmatic use and a professional Streamlit Web Application for interactive data processing.

## Technical Capabilities

| Module | Description | Statistical Method |
| :--- | :--- | :--- |
| **Night Edition UI** | Dark-themed interactive CSV dashboard. | Streamlit + SVG |
| **Integrity Engine** | Identifies and removes redundant observations. | Exact Row Matching |
| **Temporal Processor** | Deconstructs timestamps into numerical features. | Feature Extraction |
| **Quality Control** | Imputes missing values in numerical columns. | Mean/Median/Mode |
| **Outlier Shield** | Detects and clips extreme statistical anomalies. | Z-Score (3.0 Sigma) |
| **Feature Scaler** | Standardizes numerical ranges for model readiness. | Z-score/Min-Max |

## Repository Architecture

```text
├── src/
│   └── cleaner.py             # Core DeepClean logic
├── docs/
│   └── architecture.md        # Technical design and diagrams
├── app.py                     # Streamlit Night Edition Application
├── data_cleaning_tool.ipynb   # Interactive demonstration
├── requirements.txt           # Dependency manifest
├── LICENSE                    # MIT License
└── README.md                  # Project overview
```

## Installation and Deployment

### Local Environment
1. Clone the repository and navigate to the folder.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Launch the Night Edition app:
   ```bash
   streamlit run app.py
   ```

### Programmatic Usage
```python
from src.cleaner import DeepClean

cleaner = DeepClean(dataframe)
cleaned_df = cleaner.clean()
```

## Technical Documentation
Detailed architectural diagrams and logic flows are available in the [Documentation](docs/architecture.md) directory.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
