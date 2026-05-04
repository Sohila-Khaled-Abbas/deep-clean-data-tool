import streamlit as st
import pandas as pd
import numpy as np
from src.cleaner import DeepClean
import io

# SVG Icons as constants
SVG_CLEAN = '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3v19M5 8l7-5 7 5M5 16l7 5 7-5"/></svg>'
SVG_UPLOAD = '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#ffffff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/></svg>'
SVG_CHART = '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg>'

# Page Configuration
st.set_page_config(
    page_title="DeepClean",
    page_icon="💠",
    layout="wide"
)

# Night Mode CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Inter:wght@300;400;600&display=swap');
    
    /* Global Background Override */
    .stApp {
        background-color: #0e1117;
        color: #e6edf3;
    }

    /* Gradient Header (Night Edition) */
    .header-container {
        background: linear-gradient(135deg, #161b22 0%, #21262d 100%);
        padding: 50px;
        border-radius: 15px;
        border: 1px solid #30363d;
        color: #58a6ff;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.5);
    }

    /* Metric Cards (Night Edition) */
    .metric-container {
        display: flex;
        justify-content: space-between;
        gap: 20px;
        margin: 20px 0;
    }

    .metric-card {
        background-color: #161b22;
        padding: 25px;
        border-radius: 12px;
        border: 1px solid #30363d;
        border-top: 4px solid #58a6ff;
        box-shadow: 0 4px 6px rgba(0,0,0,0.2);
        flex: 1;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }

    .metric-card:hover {
        transform: translateY(-8px);
        border-color: #58a6ff;
        box-shadow: 0 12px 20px rgba(0,0,0,0.4);
    }

    .metric-label {
        font-size: 0.75rem;
        color: #8b949e;
        text-transform: uppercase;
        font-weight: 700;
        letter-spacing: 1.5px;
    }

    .metric-value {
        font-size: 1.8rem;
        color: #ffffff;
        font-weight: 700;
        margin-top: 8px;
        font-family: 'JetBrains Mono', monospace;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #010409;
        border-right: 1px solid #30363d;
    }

    /* Dark Mode Buttons */
    .stButton>button {
        background: #238636;
        color: white;
        border: 1px solid rgba(240,246,252,0.1);
        padding: 12px 24px;
        border-radius: 6px;
        font-weight: 600;
        width: 100%;
        transition: background 0.2s;
    }

    .stButton>button:hover {
        background: #2ea043;
        border-color: #8b949e;
    }

    /* Tabs Styling */
    .stTabs [data-baseweb="tab"] {
        color: #8b949e;
    }
    .stTabs [aria-selected="true"] {
        color: #58a6ff !important;
        border-bottom-color: #58a6ff !important;
    }
    
    /* Code blocks and dataframes */
    code {
        color: #ff7b72 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Custom Header
st.markdown("""
    <div class="header-container">
        <h1 style='margin:0; font-weight:700; color:#f0f6fc; letter-spacing:-1px;'>DEEPCLEAN <span style='color:#58a6ff'>PRO</span></h1>
        <p style='margin:10px 0 0 0; color:#8b949e; font-size:1.1rem;'>Night Edition • High-Performance Data Engineering</p>
    </div>
    """, unsafe_allow_html=True)

# Sidebar Configuration
with st.sidebar:
    st.markdown(f"<div style='text-align:center;'>{SVG_CLEAN}</div>", unsafe_allow_html=True)
    st.title("Settings")
    st.divider()
    scaling_method = st.selectbox("Normalization", ["StandardScaler", "MinMaxScaler"])
    impute_strategy = st.selectbox("Imputation", ["mean", "median", "most_frequent"])
    outlier_threshold = st.slider("Z-Threshold", 1.0, 5.0, 3.0)
    st.divider()
    st.caption("Engine: v2.1.0-dark")

# Main Interface
st.markdown(f"### {SVG_UPLOAD} Data Ingestion", unsafe_allow_html=True)
uploaded_file = st.file_uploader("", type="csv", label_visibility="collapsed")

if uploaded_file is not None:
    df_raw = pd.read_csv(uploaded_file)
    
    tab1, tab2 = st.tabs(["Analysis", "Cleaning Pipeline"])
    
    with tab1:
        st.markdown(f"#### {SVG_CHART} Raw Metadata", unsafe_allow_html=True)
        st.dataframe(df_raw.head(10), use_container_width=True)
        
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown('<div class="metric-card"><div class="metric-label">Shape</div><div class="metric-value">'+str(df_raw.shape)+'</div></div>', unsafe_allow_html=True)
        with c2:
            st.markdown('<div class="metric-card"><div class="metric-label">Null Entries</div><div class="metric-value">'+str(df_raw.isnull().sum().sum())+'</div></div>', unsafe_allow_html=True)
        with c3:
            st.markdown('<div class="metric-card"><div class="metric-label">Duplicates</div><div class="metric-value">'+str(df_raw.duplicated().sum())+'</div></div>', unsafe_allow_html=True)

    with tab2:
        if st.button("RUN PIPELINE"):
            with st.spinner("Processing..."):
                cleaner = DeepClean(df_raw)
                cleaner.remove_duplicates()
                cleaner.process_dates()
                cleaner.handle_missing_values(strategy=impute_strategy)
                cleaner.handle_outliers(threshold=outlier_threshold)
                cleaner.encode_categorical()
                cleaner.normalize_data(method='standard' if "Standard" in scaling_method else 'minmax')
                
                df_cleaned = cleaner.df
                report = cleaner.get_summary()

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
                
                st.dataframe(df_cleaned.head(10), use_container_width=True)

                csv = df_cleaned.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="DOWNLOAD CLEANED CSV",
                    data=csv,
                    file_name=f"DeepClean_Night_{uploaded_file.name}",
                    mime='text/csv',
                )

else:
    st.markdown("""
        <div style='background-color:#161b22; padding:30px; border-radius:12px; border: 1px solid #30363d;'>
            <h3 style='margin-top:0; color:#58a6ff;'>Operational Readiness</h3>
            <p style='color:#8b949e;'>Awaiting CSV payload. The system will execute the following modules upon ingestion:</p>
            <code style='color:#79c0ff;'>Duplicates | Temporal | Imputation | Outliers | Encoding | Normalization</code>
        </div>
    """, unsafe_allow_html=True)
