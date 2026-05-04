import streamlit as st
import pandas as pd
import numpy as np
from src.cleaner import DeepClean
import io

# Page Configuration
st.set_page_config(
    page_title="DeepClean | Pro Data Tool",
    page_icon="💎",
    layout="wide"
)

# Advanced CSS Injection
st.markdown("""
    <style>
    /* Main Background and Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .main {
        background-color: #fcfcfd;
    }

    /* Gradient Header */
    .header-container {
        background: linear-gradient(90deg, #1a2a6c, #b21f1f, #fdbb2d);
        padding: 40px;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    }

    /* Metric Cards */
    .metric-container {
        display: flex;
        justify-content: space-between;
        gap: 20px;
        margin: 20px 0;
    }

    .metric-card {
        background-color: white;
        padding: 20px;
        border-radius: 12px;
        border-left: 5px solid #1a2a6c;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        flex: 1;
        transition: transform 0.2s;
    }

    .metric-card:hover {
        transform: translateY(-5px);
    }

    .metric-label {
        font-size: 0.8rem;
        color: #6c757d;
        text-transform: uppercase;
        font-weight: 600;
        letter-spacing: 1px;
    }

    .metric-value {
        font-size: 1.5rem;
        color: #1a2a6c;
        font-weight: 700;
        margin-top: 5px;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #f1f3f5;
        border-right: 1px solid #dee2e6;
    }

    /* Styled Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #1a2a6c 0%, #b21f1f 100%);
        color: white;
        border: none;
        padding: 15px 30px;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(178, 31, 31, 0.2);
    }

    .stButton>button:hover {
        opacity: 0.9;
        transform: scale(1.02);
    }
    </style>
    """, unsafe_allow_html=True)

# Custom Header HTML
st.markdown("""
    <div class="header-container">
        <h1 style='margin:0; font-weight:600;'>DEEPCLEAN</h1>
        <p style='margin:10px 0 0 0; opacity:0.9;'>Professional Grade Data Engineering & Automated Preprocessing</p>
    </div>
    """, unsafe_allow_html=True)

# Sidebar Configuration
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/000000/clean.png", width=80)
    st.title("Control Panel")
    st.divider()
    st.subheader("⚙️ Pipeline Config")
    scaling_method = st.selectbox("Normalization Method", ["StandardScaler", "MinMaxScaler"])
    impute_strategy = st.selectbox("Imputation Strategy", ["mean", "median", "most_frequent"])
    outlier_threshold = st.slider("Z-Score Threshold", 1.0, 5.0, 3.0)
    st.divider()
    st.info("System Version: v2.1.0")

# Main Interface
uploaded_file = st.file_uploader("📂 Upload Dataset (CSV)", type="csv")

if uploaded_file is not None:
    df_raw = pd.read_csv(uploaded_file)
    
    tab1, tab2 = st.tabs(["📊 Data Analysis", "🛠️ Cleaning Engine"])
    
    with tab1:
        st.subheader("Raw Distribution Preview")
        st.dataframe(df_raw.head(10), use_container_width=True)
        
        c1, c2, c3 = st.columns(3)
        c1.write("**Dataset Shape**")
        c1.code(f"{df_raw.shape}")
        c2.write("**Missing Values**")
        c2.code(f"{df_raw.isnull().sum().sum()}")
        c3.write("**Duplicates**")
        c3.code(f"{df_raw.duplicated().sum()}")

    with tab2:
        if st.button("RUN AUTOMATED PIPELINE"):
            with st.spinner("Processing large-scale operations..."):
                cleaner = DeepClean(df_raw)
                
                # Execute Steps
                cleaner.remove_duplicates()
                cleaner.process_dates()
                cleaner.handle_missing_values(strategy=impute_strategy)
                cleaner.handle_outliers(threshold=outlier_threshold)
                cleaner.encode_categorical()
                cleaner.normalize_data(method='standard' if "Standard" in scaling_method else 'minmax')
                
                df_cleaned = cleaner.df
                report = cleaner.get_summary()

                # Results Presentation
                st.success("Success! Data processed through 6-stage engineering pipeline.")
                
                # Custom Metric Cards
                st.markdown("<div class='metric-container'>", unsafe_allow_html=True)
                cols = st.columns(len(report))
                for i, (key, value) in enumerate(report.items()):
                    with cols[i]:
                        st.markdown(f"""
                            <div class="metric-card">
                                <div class="metric-label">{key.replace('_', ' ')}</div>
                                <div class="metric-value">{value}</div>
                            </div>
                        """, unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
                
                st.subheader("Cleaned Dataset Preview")
                st.dataframe(df_cleaned.head(10), use_container_width=True)

                # Export
                csv = df_cleaned.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="DOWNLOAD CLEANED CSV",
                    data=csv,
                    file_name=f"DeepClean_{uploaded_file.name}",
                    mime='text/csv',
                )

else:
    # Onboarding Section
    st.markdown("""
        <div style='background-color:#e9ecef; padding:30px; border-radius:12px; border-left: 6px solid #1a2a6c;'>
            <h3 style='margin-top:0;'>Ready to start?</h3>
            <p>Upload your CSV file using the box above. DeepClean will automatically handle:</p>
            <ul style='columns: 2;'>
                <li><b>Integrity:</b> Duplicate removal</li>
                <li><b>Temporal:</b> Date feature extraction</li>
                <li><b>Quality:</b> Missing value imputation</li>
                <li><b>Robustness:</b> Outlier clipping</li>
                <li><b>ML-Ready:</b> Categorical encoding</li>
                <li><b>Uniformity:</b> Feature scaling</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)
