import streamlit as st
import pandas as pd
import numpy as np
from src.cleaner import DeepClean
import io

# SVG Assets
SVG_CLEAN = '<svg viewBox="0 0 24 24" width="32" height="32" stroke="#00d4ff" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3v19M5 8l7-5 7 5M5 16l7 5 7-5"/></svg>'
SVG_DATA = '<svg viewBox="0 0 24 24" width="24" height="24" stroke="#00d4ff" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2H2v10h10V2zM22 2h-10v10h10V2zM12 12H2v10h10V12zM22 12h-10v10h10V12z"/></svg>'

st.set_page_config(page_title="DeepClean", page_icon="💠", layout="wide")

# Modern Bento Grid CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    .stApp {
        background-color: #05070a;
        color: #ccd6f6;
    }

    /* Bento Header */
    .bento-header {
        background: rgba(17, 25, 40, 0.75);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 40px;
        text-align: center;
        margin-bottom: 25px;
    }

    /* Bento Grid System */
    .bento-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 20px;
        margin-bottom: 20px;
    }

    .bento-item {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 24px;
        transition: all 0.3s ease;
    }

    .bento-item:hover {
        background: rgba(255, 255, 255, 0.05);
        border-color: #00d4ff;
        transform: scale(1.02);
    }

    .bento-label {
        font-size: 0.7rem;
        color: #8892b0;
        font-weight: 700;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-bottom: 8px;
    }

    .bento-value {
        font-size: 1.8rem;
        color: #00d4ff;
        font-weight: 700;
    }

    /* Sidebar Refinement */
    section[data-testid="stSidebar"] {
        background-color: #0a0c10;
        border-right: 1px solid rgba(255,255,255,0.05);
    }

    /* Neon Button */
    .stButton>button {
        background: transparent;
        color: #00d4ff;
        border: 2px solid #00d4ff;
        padding: 12px 24px;
        border-radius: 12px;
        font-weight: 700;
        width: 100%;
        text-transform: uppercase;
        letter-spacing: 1px;
        transition: all 0.3s;
    }

    .stButton>button:hover {
        background: rgba(0, 212, 255, 0.1);
        box-shadow: 0 0 20px rgba(0, 212, 255, 0.3);
    }

    /* Clean UI for Dataframes */
    .stDataFrame {
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid rgba(255,255,255,0.05);
    }
    </style>
    """, unsafe_allow_html=True)

# App Header
st.markdown(f"""
    <div class="bento-header">
        <div style="margin-bottom:15px;">{SVG_CLEAN}</div>
        <h1 style='margin:0; font-size:2.5rem; letter-spacing:-1px; color:#ffffff;'>DeepClean <span style="color:#00d4ff; font-weight:300;">OS</span></h1>
        <p style='color:#8892b0; margin-top:10px;'>Advanced Data Engineering Intelligence</p>
    </div>
    """, unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### CONFIGURATION")
    scale_type = st.selectbox("Scaling", ["Standard", "MinMax"])
    strategy = st.selectbox("Imputation", ["mean", "median", "mode"])
    z_limit = st.slider("Z-Threshold", 1.0, 5.0, 3.0)
    st.divider()
    st.caption("Environment: Cloud-Optimized")

# Main Logic
file = st.file_uploader("DROP DATASET HERE", type="csv")

if file:
    df_raw = pd.read_csv(file)
    
    col_l, col_r = st.columns([1, 2])
    
    with col_l:
        st.markdown("#### INPUT BUFFER")
        st.code(f"Records: {df_raw.shape[0]}\nFields: {df_raw.shape[1]}")
        if st.button("INITIATE PIPELINE"):
            st.session_state.process = True
            
    with col_r:
        st.markdown("#### RAW PREVIEW")
        st.dataframe(df_raw.head(8), use_container_width=True)

    if st.session_state.get('process', False):
        with st.spinner("Processing..."):
            cleaner = DeepClean(df_raw)
            cleaner.remove_duplicates()
            cleaner.process_dates()
            cleaner.handle_missing_values(strategy=strategy)
            cleaner.handle_outliers(threshold=z_limit)
            cleaner.encode_categorical()
            cleaner.normalize_data(method='standard' if scale_type == "Standard" else 'minmax')
            
            df_final = cleaner.df
            metrics = cleaner.get_summary()

            # Bento Grid Results
            st.divider()
            st.markdown("#### TRANSFORMATION REPORT")
            
            # Rendering metrics in a Bento Grid
            cols = st.columns(4)
            for i, (k, v) in enumerate(metrics.items()):
                with cols[i % 4]:
                    st.markdown(f"""
                        <div class="bento-item">
                            <div class="bento-label">{k.replace('_', ' ')}</div>
                            <div class="bento-value">{v}</div>
                        </div>
                    """, unsafe_allow_html=True)

            st.divider()
            st.markdown("#### OUTPUT STREAM")
            st.dataframe(df_final.head(10), use_container_width=True)
            
            # Export
            res_csv = df_final.to_csv(index=False).encode('utf-8')
            st.download_button("EXPORT CLEANED DATA", res_csv, f"DeepClean_{file.name}", "text/csv")

else:
    st.markdown("""
        <div class="bento-item" style="text-align:center; padding:60px;">
            <div style="color:#8892b0; font-size:1.1rem;">
                Awaiting Data Payload...<br>
                <span style="font-size:0.8rem; opacity:0.6;">Upload a CSV to begin automated cleaning.</span>
            </div>
        </div>
    """, unsafe_allow_html=True)
