import os
import sys
import base64
from pathlib import Path
import pandas as pd
import joblib
import altair as alt
import streamlit as st

_app_dir = Path(__file__).resolve().parent
for _p in [_app_dir, _app_dir.parent, _app_dir.parent.parent]:
    if _p.exists() and str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

try:
    from optimizer.crop_optimizer import CropOptimizer
    from optimizer.msp_data import CROP_METADATA, get_crop_price, get_crop_unit, get_crop_category
except Exception:
    CropOptimizer = None
    CROP_METADATA = {}
    get_crop_price = lambda c: 22000.0
    get_crop_unit = lambda c: "Tonne"
    get_crop_category = lambda c: "General"

st.set_page_config(
    page_title="🌾 YIELDICT AI | Crop Yield Prediction & Decision Support",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

def get_resource_path(filename: str) -> Path:
    base_dir = Path(__file__).resolve().parent
    candidates = [
        base_dir / filename,
        base_dir / "ML base_line trainning" / filename,
        base_dir / "ML base_line trainning" / "ML base_line trainning" / filename,
        base_dir.parent / filename,
        base_dir.parent / "ML base_line trainning" / filename,
        base_dir.parent / "ML base_line trainning" / "ML base_line trainning" / filename,
        base_dir.parent / "processed data for training" / filename,
        Path.cwd() / filename,
        Path.cwd() / "ML base_line trainning" / filename,
        Path.cwd() / "ML base_line trainning" / "ML base_line trainning" / filename,
    ]
    for path in candidates:
        if path.is_file():
            return path
    return base_dir / filename


@st.cache_data
def get_base64_bg_css(bg_filename: str) -> str:
    bg_path = get_resource_path(bg_filename)
    if bg_path.is_file():
        try:
            with open(bg_path, "rb") as f:
                encoded = base64.b64encode(f.read()).decode()
            return f"""
            [data-testid="stAppViewContainer"], .stApp {{
                background: linear-gradient(rgba(249, 248, 244, 0.65), rgba(249, 248, 244, 0.65)), url("data:image/png;base64,{encoded}") !important;
                background-size: cover !important;
                background-position: center center !important;
                background-repeat: no-repeat !important;
                background-attachment: fixed !important;
            }}
            [data-testid="stHeader"] {{
                background-color: transparent !important;
            }}
            """
        except Exception:
            return ""
    return ""


bg_css_rule = get_base64_bg_css("background.png")

st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&family=Playfair+Display:wght@600;700&display=swap');

    :root {{
        --paper-bg: transparent;
        --card-paper: rgba(255, 255, 255, 0.92);
        --border-paper: #e3ded1;
        --forest-dark: #1b382b;
        --leaf-green: #2d6a4f;
        --sage-light: #eaf2e8;
        --text-headline: #182820;
        --text-body: #2c3e35;
        --text-muted: #526357;
    }}

    {bg_css_rule}

    .stApp {{
        font-family: 'Plus Jakarta Sans', sans-serif;
        color: var(--text-body);
    }}

    .main .block-container {{
        padding-top: 2rem;
        padding-bottom: 3.5rem;
        max-width: 1180px;
    }}

    .hero-container {{
        background: linear-gradient(135deg, rgba(45, 106, 79, 0.95) 0%, rgba(64, 145, 108, 0.95) 100%);
        backdrop-filter: blur(12px);
        color: #ffffff;
        padding: 2.2rem 2.6rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        border: 1px solid #52b788;
        box-shadow: 0 10px 28px -4px rgba(45, 106, 79, 0.25);
        position: relative;
    }}

    .hero-title {{
        font-family: 'Playfair Display', serif;
        font-size: 2.35rem;
        font-weight: 700;
        color: #ffffff !important;
        margin: 0 0 0.4rem 0;
        letter-spacing: -0.01em;
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }}

    .hero-subtitle {{
        font-size: 1.08rem;
        color: #f0fdf4 !important;
        margin: 0;
        font-weight: 500;
        opacity: 0.95;
    }}

    .card-box {{
        background-color: var(--card-paper);
        backdrop-filter: blur(10px);
        border: 1px solid var(--border-paper);
        border-radius: 16px;
        padding: 1.8rem;
        box-shadow: 0 6px 18px -2px rgba(0, 0, 0, 0.04);
        margin-bottom: 1.5rem;
    }}

    .card-header {{
        font-family: 'Playfair Display', serif;
        font-size: 1.25rem;
        font-weight: 700;
        color: var(--forest-dark);
        margin-bottom: 1.2rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid var(--sage-light);
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }}

    .prediction-box {{
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.96) 0%, rgba(240, 247, 242, 0.96) 100%);
        backdrop-filter: blur(12px);
        border: 2px dashed #40916c;
        border-radius: 16px;
        padding: 2.2rem;
        text-align: center;
        margin-top: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 8px 22px -4px rgba(45, 106, 79, 0.12);
    }}

    .prediction-badge {{
        display: inline-block;
        background-color: #2d6a4f !important;
        color: #ffffff !important;
        font-size: 0.85rem !important;
        font-weight: 700 !important;
        padding: 0.4rem 1.1rem !important;
        border-radius: 20px !important;
        text-transform: uppercase !important;
        letter-spacing: 0.08em !important;
        margin-bottom: 0.85rem !important;
        box-shadow: 0 3px 10px rgba(45, 106, 79, 0.25) !important;
    }}

    .prediction-value {{
        font-family: 'Playfair Display', serif;
        font-size: 3.4rem;
        font-weight: 700;
        color: #143224;
        line-height: 1.1;
        margin: 0.4rem 0;
    }}

    .prediction-disclaimer {{
        font-size: 0.92rem;
        color: #26543c;
        margin-top: 0.85rem;
        font-weight: 500;
    }}

    .metric-pill {{
        background-color: rgba(255, 255, 255, 0.94);
        backdrop-filter: blur(8px);
        border: 1px solid var(--border-paper);
        border-radius: 12px;
        padding: 1.1rem;
        text-align: center;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.03);
    }}
    .metric-pill-val {{
        font-family: 'Playfair Display', serif;
        font-size: 1.5rem;
        font-weight: 700;
        color: var(--forest-dark);
    }}
    .metric-pill-lbl {{
        font-size: 0.82rem;
        color: var(--text-muted);
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.04em;
    }}

    div.stButton > button {{
        background-color: #2b5640 !important;
        color: #ffffff !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
        padding: 0.7rem 2rem !important;
        border-radius: 12px !important;
        border: 1px solid #1e3e2e !important;
        box-shadow: 0 4px 14px rgba(43, 86, 64, 0.25) !important;
        transition: all 0.2s ease-in-out !important;
    }}
    div.stButton > button:hover {{
        background-color: #1b382b !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 6px 18px rgba(27, 56, 43, 0.35) !important;
    }}

    section[data-testid="stSidebar"] {{
        background-color: rgba(242, 239, 233, 0.94) !important;
        backdrop-filter: blur(10px) !important;
        border-right: 1px solid #e0dad0 !important;
    }}
    section[data-testid="stSidebar"] * {{
        color: #1b382b !important;
    }}
    section[data-testid="stSidebar"] h1, 
    section[data-testid="stSidebar"] h2, 
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] h4 {{
        color: #1b382b !important;
        font-weight: 700 !important;
    }}
    section[data-testid="stSidebar"] p, 
    section[data-testid="stSidebar"] li, 
    section[data-testid="stSidebar"] span {{
        color: #2c4235 !important;
    }}
    section[data-testid="stSidebar"] code {{
        background-color: #e2ebd9 !important;
        color: #1b382b !important;
        font-weight: 700 !important;
        border: 1px solid #c4d4b9 !important;
        padding: 0.15rem 0.4rem !important;
        border-radius: 6px !important;
    }}

    h1, h2, h3, h4, h5, h6, .stMarkdown p, .stMarkdown span, .stMarkdown li {{
        color: #182820 !important;
    }}

    label[data-testid="stWidgetLabel"] p,
    label[data-testid="stWidgetLabel"] span,
    div[data-testid="stForm"] label,
    div[data-baseweb="form-control"] label,
    .stSelectbox label p,
    .stNumberInput label p {{
        color: #142c20 !important;
        font-weight: 700 !important;
        font-size: 0.98rem !important;
    }}

    div[data-baseweb="select"] {{
        background-color: #ffffff !important;
        border: 1px solid #c8c0b0 !important;
        border-radius: 10px !important;
    }}
    div[data-baseweb="select"] * {{
        background-color: #ffffff !important;
        color: #142c20 !important;
        font-weight: 600 !important;
    }}
    div[data-baseweb="popover"] * {{
        background-color: #ffffff !important;
        color: #142c20 !important;
    }}
    ul[data-baseweb="menu"] {{
        background-color: #ffffff !important;
    }}
    li[data-baseweb="option"] {{
        background-color: #ffffff !important;
        color: #142c20 !important;
    }}
    li[data-baseweb="option"]:hover {{
        background-color: #eaf2e8 !important;
        color: #1b382b !important;
    }}

    .stNumberInput input {{
        background-color: #ffffff !important;
        color: #142c20 !important;
        border: 1px solid #c8c0b0 !important;
        font-weight: 600 !important;
    }}
    .stNumberInput button {{
        background-color: #eaf2e8 !important;
        color: #1b382b !important;
        border: 1px solid #c8c0b0 !important;
    }}
    .stNumberInput button:hover {{
        background-color: #2b5640 !important;
        color: #ffffff !important;
    }}

    div[data-testid="stSlider"] {{
        margin-top: -14px !important;
        margin-bottom: 0.8rem !important;
        padding-top: 0px !important;
        width: 100% !important;
    }}
    div[data-testid="stSlider"] > div {{
        padding-top: 0px !important;
        padding-bottom: 0px !important;
    }}
    div[data-testid="stSlider"] [data-baseweb="slider"] {{
        width: 100% !important;
    }}
    div[data-testid="stSlider"] div[role="slider"] {{
        background-color: #2ec4b6 !important;
        border: 2.5px solid #ffffff !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.25) !important;
        width: 18px !important;
        height: 18px !important;
    }}
    div[data-testid="stSlider"] [data-testid="stThumbValue"] {{
        display: none !important;
    }}

    div[data-testid="stExpander"] {{
        background-color: rgba(255, 255, 255, 0.95) !important;
        backdrop-filter: blur(12px) !important;
        border: 1px solid #dcd6cd !important;
        border-radius: 14px !important;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.05) !important;
        margin-bottom: 1.2rem !important;
        overflow: hidden !important;
    }}
    div[data-testid="stExpander"] summary,
    div[data-testid="stExpander"] details summary,
    div[data-testid="stExpander"] [data-testid="stExpanderDetailsSummary"] {{
        background-color: #eaf2e8 !important;
        border-bottom: 1px solid #dcd6cd !important;
        padding: 0.85rem 1.25rem !important;
    }}
    div[data-testid="stExpander"] summary *,
    div[data-testid="stExpander"] details summary *,
    div[data-testid="stExpander"] [data-testid="stExpanderDetailsSummary"] * {{
        color: #1b382b !important;
        font-weight: 700 !important;
        font-size: 1.05rem !important;
    }}

    div[data-testid="stAlert"] {{
        border-radius: 12px !important;
        opacity: 1 !important;
        box-shadow: 0 3px 10px rgba(0, 0, 0, 0.04) !important;
        padding: 0.9rem 1.2rem !important;
    }}
    div[data-testid="stAlert"] * {{
        color: #1e293b !important;
        font-weight: 600 !important;
    }}

    div[data-testid="stMetric"] {{
        background-color: #ffffff !important;
        border: 1px solid #dcd6cd !important;
        padding: 1.1rem !important;
        border-radius: 12px !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.04) !important;
    }}
    div[data-testid="stMetricLabel"],
    div[data-testid="stMetricLabel"] *, 
    div[data-testid="stMetricLabel"] p, 
    div[data-testid="stMetricLabel"] span,
    div[data-testid="stMetricLabel"] label,
    [data-testid="stMetricLabel"] {{
        color: #142c20 !important;
        font-weight: 700 !important;
        font-size: 0.88rem !important;
        opacity: 1 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
    }}
    div[data-testid="stMetricValue"],
    div[data-testid="stMetricValue"] *, 
    div[data-testid="stMetricValue"] div {{
        color: #1b382b !important;
        font-family: 'Playfair Display', serif !important;
        font-weight: 800 !important;
        font-size: 1.9rem !important;
        opacity: 1 !important;
    }}

    div[data-testid="stDataFrame"], div[data-testid="stTable"] {{
        background-color: #ffffff !important;
        border: 1px solid #e3ded1 !important;
        border-radius: 10px !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.03) !important;
    }}
    div[data-testid="stDataFrame"] * {{
        color: #182820 !important;
    }}

    .econ-badge {{
        display: inline-block;
        background-color: #eaf2e8;
        color: #1b382b;
        font-weight: 700;
        font-size: 0.82rem;
        padding: 4px 10px;
        border-radius: 20px;
        border: 1px solid #cce3de;
        margin-top: 4px;
    }}
    .profit-pill {{
        background-color: #d8f3dc;
        color: #1b4332;
        font-weight: 800;
        padding: 4px 12px;
        border-radius: 12px;
        border: 1px solid #95d5b2;
        display: inline-block;
    }}
    .risk-pill-low {{
        background-color: #d8f3dc;
        color: #1b4332;
        font-weight: 800;
        padding: 4px 12px;
        border-radius: 12px;
        border: 1px solid #95d5b2;
        display: inline-block;
    }}
    .risk-pill-mod {{
        background-color: #fef3c7;
        color: #92400e;
        font-weight: 800;
        padding: 4px 12px;
        border-radius: 12px;
        border: 1px solid #fde68a;
        display: inline-block;
    }}
    .risk-pill-high {{
        background-color: #fee2e2;
        color: #991b1b;
        font-weight: 800;
        padding: 4px 12px;
        border-radius: 12px;
        border: 1px solid #fecaca;
        display: inline-block;
    }}

    .stTabs [data-baseweb="tab-list"] {{
        gap: 8px;
        background-color: rgba(255, 255, 255, 0.6);
        padding: 6px;
        border-radius: 12px;
        border: 1px solid #e3ded1;
    }}
    .stTabs [data-baseweb="tab"] {{
        border-radius: 8px !important;
        font-weight: 700 !important;
        color: #2d503b !important;
        padding: 8px 18px !important;
    }}
    .stTabs [aria-selected="true"] {{
        background-color: #ffffff !important;
        color: #1b382b !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08) !important;
        border-bottom: 2px solid #2d6a4f !important;
    }}
    </style>
    """,
    unsafe_allow_html=True
)


@st.cache_resource
def load_model():
    for name in ["crop_yield_model.pkl", "random_forest.pkl"]:
        model_path = get_resource_path(name)
        if model_path.is_file():
            model_obj = joblib.load(model_path)
            return model_obj
            
    raise FileNotFoundError("Trained model file ('crop_yield_model.pkl' / 'random_forest.pkl') not found.")


@st.cache_resource
def load_optimizer():
    if CropOptimizer is not None:
        try:
            return CropOptimizer()
        except Exception:
            return None
    return None


@st.cache_data
def load_dataset():
    csv_path = get_resource_path("crop_yield_cleaned.csv")
    if not csv_path.is_file():
        raise FileNotFoundError(f"Cleaned dataset file 'crop_yield_cleaned.csv' not found. Searched path: {csv_path}")
    return pd.read_csv(csv_path)


try:
    model = load_model()
except Exception as e:
    st.error(f"❌ **Failed to load trained model (`crop_yield_model.pkl`)**")
    st.info(f"**Details:** {str(e)}\n\nPlease ensure `crop_yield_model.pkl` is located in the application directory.")
    st.stop()

try:
    df = load_dataset()
except Exception as e:
    st.error(f"❌ **Failed to load cleaned dataset (`crop_yield_cleaned.csv`)**")
    st.info(f"**Details:** {str(e)}\n\nPlease ensure `crop_yield_cleaned.csv` is located in the application directory.")
    st.stop()


crops = sorted(df["crop"].dropna().unique().tolist())
seasons = sorted(df["season"].dropna().unique().tolist())
states = sorted(df["state"].dropna().unique().tolist())

median_area = float(df["area"].median()) if "area" in df.columns else 1000.0
median_rainfall = float(df["annual_rainfall"].median()) if "annual_rainfall" in df.columns else 1400.0
median_fertilizer = float(df["fertilizer"].median()) if "fertilizer" in df.columns else 500000.0
median_pesticide = float(df["pesticide"].median()) if "pesticide" in df.columns else 1500.0


st.markdown(
    """
    <div class="hero-container">
        <div class="hero-title">🌾 YIELDICT AI</div>
        <p class="hero-subtitle">
            AI-powered crop yield estimation using historical agricultural, geographic, and environmental parameters.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)


with st.sidebar:
    st.markdown("### 🌾 YIELDICT AI Dashboard")
    st.write(
        "This application uses a trained **Random Forest Regression** machine learning model to estimate crop yield based on regional, seasonal, and environmental inputs."
    )
    
    st.markdown("---")
    st.markdown("### 📊 Dataset Reference")
    st.markdown(f"- **Total Records:** `{len(df):,}`")
    st.markdown(f"- **Supported Crops:** `{len(crops)}` categories")
    st.markdown(f"- **Supported States:** `{len(states)}` regions")
    st.markdown(f"- **Supported Seasons:** `{len(seasons)}` seasons")

    st.markdown("---")
    st.markdown("### ℹ️ How to Use")
    st.markdown(
        "1. Select the **Crop**, **Season**, and **State**.\n"
        "2. Enter the farm **Area**, **Annual Rainfall**, **Fertilizer**, and **Pesticide** values.\n"
        "3. Click **Predict Yield** to calculate the estimated yield."
    )


st.markdown("### 📝 Enter Agricultural & Environmental Details")

col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown(
        """
        <div class="card-header">
            🌾 Crop & Regional Information
        </div>
        """,
        unsafe_allow_html=True
    )
    
    crop = st.selectbox(
        "Crop Name",
        options=crops,
        index=0 if "Rice" not in crops else crops.index("Rice"),
        help="Select crop type from dataset categories."
    )
    
    season = st.selectbox(
        "Cultivation Season",
        options=seasons,
        index=0 if "Kharif" not in seasons else seasons.index("Kharif"),
        help="Select farming season."
    )
    
    state = st.selectbox(
        "State / Region",
        options=states,
        index=0 if "Assam" not in states else states.index("Assam"),
        help="Select state location."
    )

with col2:
    st.markdown(
        """
        <div class="card-header">
            📊 Agricultural & Environmental Inputs
        </div>
        """,
        unsafe_allow_html=True
    )
    
    area_max = max(500000.0, float(df["area"].max()) if "area" in df.columns else 500000.0)
    rainfall_max = max(5000.0, float(df["annual_rainfall"].max()) if "annual_rainfall" in df.columns else 5000.0)
    fert_max = max(2000000.0, float(df["fertilizer"].max()) if "fertilizer" in df.columns else 2000000.0)
    pest_max = max(50000.0, float(df["pesticide"].max()) if "pesticide" in df.columns else 50000.0)

    init_area = float(round(median_area, 2))
    init_rainfall = float(round(median_rainfall, 2))
    init_fert = float(round(median_fertilizer, 2))
    init_pest = float(round(median_pesticide, 2))

    if "area_sync" not in st.session_state:
        st.session_state.area_sync = init_area
        st.session_state.area_input_box = init_area
        st.session_state.area_slider_ctrl = min(init_area, area_max)

    if "rainfall_sync" not in st.session_state:
        st.session_state.rainfall_sync = init_rainfall
        st.session_state.rain_input_box = init_rainfall
        st.session_state.rain_slider_ctrl = min(init_rainfall, rainfall_max)

    if "fert_sync" not in st.session_state:
        st.session_state.fert_sync = init_fert
        st.session_state.fert_input_box = init_fert
        st.session_state.fert_slider_ctrl = min(init_fert, fert_max)

    if "pest_sync" not in st.session_state:
        st.session_state.pest_sync = init_pest
        st.session_state.pest_input_box = init_pest
        st.session_state.pest_slider_ctrl = min(init_pest, pest_max)

    def sync_area_num():
        val = float(st.session_state.area_input_box)
        st.session_state.area_sync = val
        st.session_state.area_slider_ctrl = min(val, area_max)

    def sync_area_slider():
        val = float(st.session_state.area_slider_ctrl)
        st.session_state.area_sync = val
        st.session_state.area_input_box = val

    def sync_rain_num():
        val = float(st.session_state.rain_input_box)
        st.session_state.rainfall_sync = val
        st.session_state.rain_slider_ctrl = min(val, rainfall_max)

    def sync_rain_slider():
        val = float(st.session_state.rain_slider_ctrl)
        st.session_state.rainfall_sync = val
        st.session_state.rain_input_box = val

    def sync_fert_num():
        val = float(st.session_state.fert_input_box)
        st.session_state.fert_sync = val
        st.session_state.fert_slider_ctrl = min(val, fert_max)

    def sync_fert_slider():
        val = float(st.session_state.fert_slider_ctrl)
        st.session_state.fert_sync = val
        st.session_state.fert_input_box = val

    def sync_pest_num():
        val = float(st.session_state.pest_input_box)
        st.session_state.pest_sync = val
        st.session_state.pest_slider_ctrl = min(val, pest_max)

    def sync_pest_slider():
        val = float(st.session_state.pest_slider_ctrl)
        st.session_state.pest_sync = val
        st.session_state.pest_input_box = val

    # 1. Cultivated Area (Box + Slider)
    st.number_input(
        "Cultivated Area (ha)",
        min_value=0.0,
        step=10.0,
        key="area_input_box",
        on_change=sync_area_num,
        help="Total cultivated area in hectares (ha). Must not be negative."
    )
    st.slider(
        "Area Slider",
        min_value=0.0,
        max_value=area_max,
        step=10.0,
        key="area_slider_ctrl",
        on_change=sync_area_slider,
        label_visibility="collapsed"
    )
    area = float(st.session_state.area_sync)
    
    # 2. Annual Rainfall (Box + Slider)
    st.number_input(
        "Annual Rainfall (mm)",
        min_value=0.0,
        step=50.0,
        key="rain_input_box",
        on_change=sync_rain_num,
        help="Annual rainfall in millimeters (mm). Must not be negative."
    )
    st.slider(
        "Rainfall Slider",
        min_value=0.0,
        max_value=rainfall_max,
        step=10.0,
        key="rain_slider_ctrl",
        on_change=sync_rain_slider,
        label_visibility="collapsed"
    )
    annual_rainfall = float(st.session_state.rainfall_sync)
    
    # 3. Fertilizer Usage (Box + Slider)
    st.number_input(
        "Fertilizer Usage (kg)",
        min_value=0.0,
        step=1000.0,
        key="fert_input_box",
        on_change=sync_fert_num,
        help="Total fertilizer quantity used in kilograms (kg). Must not be negative."
    )
    st.slider(
        "Fertilizer Slider",
        min_value=0.0,
        max_value=fert_max,
        step=500.0,
        key="fert_slider_ctrl",
        on_change=sync_fert_slider,
        label_visibility="collapsed"
    )
    fertilizer = float(st.session_state.fert_sync)
    
    # 4. Pesticide Usage (Box + Slider)
    st.number_input(
        "Pesticide Usage (kg)",
        min_value=0.0,
        step=50.0,
        key="pest_input_box",
        on_change=sync_pest_num,
        help="Total pesticide quantity used in kilograms (kg). Must not be negative."
    )
    st.slider(
        "Pesticide Slider",
        min_value=0.0,
        max_value=pest_max,
        step=10.0,
        key="pest_slider_ctrl",
        on_change=sync_pest_slider,
        label_visibility="collapsed"
    )
    pesticide = float(st.session_state.pest_sync)

st.markdown("<br>", unsafe_allow_html=True)


def validate_inputs(area_val: float, rainfall_val: float, fert_val: float, pest_val: float) -> list[str]:
    errors = []
    if area_val < 0:
        errors.append("Area cannot be negative.")
    if rainfall_val < 0:
        errors.append("Annual Rainfall cannot be negative.")
    if fert_val < 0:
        errors.append("Fertilizer usage cannot be negative.")
    if pest_val < 0:
        errors.append("Pesticide usage cannot be negative.")
    return errors


predict_clicked = st.button("🌱 Predict Yield", width="stretch")

if predict_clicked:
    validation_errors = validate_inputs(area, annual_rainfall, fertilizer, pesticide)
    
    if validation_errors:
        for err in validation_errors:
            st.error(f"⚠️ **Validation Error:** {err}")
    else:
        input_data = pd.DataFrame({
            "crop": [crop],
            "season": [season],
            "state": [state],
            "area": [area],
            "annual_rainfall": [annual_rainfall],
            "fertilizer": [fertilizer],
            "pesticide": [pesticide]
        })
        
        try:
            prediction = float(model.predict(input_data)[0])
            total_prod = prediction * area
            crop_unit = get_crop_unit(crop) if 'get_crop_unit' in globals() else 'Tonne'
            price_val = get_crop_price(crop) if 'get_crop_price' in globals() else 22000.0
            gross_rev = total_prod * price_val
            
            if gross_rev >= 10000000:
                rev_fmt = f"₹{gross_rev / 10000000:.2f} Cr"
            elif gross_rev >= 100000:
                rev_fmt = f"₹{gross_rev / 100000:.2f} Lakhs"
            else:
                rev_fmt = f"₹{gross_rev:,.2f}"

            prod_fmt = f"{total_prod:,.1f} {crop_unit}s" if crop_unit != "Tonne" else f"{total_prod:,.1f} Tonnes"
            msp_info = CROP_METADATA.get(crop, {}) if 'CROP_METADATA' in globals() else {}
            msp_status = "Govt. Declared MSP" if msp_info.get("msp_declared") else "Market Farmgate Rate"
            
            st.markdown(
                f"""
                <div class="prediction-box">
                    <span class="prediction-badge">Primary Yield & Revenue Forecast</span>
                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 1rem; margin-top: 1rem;">
                        <div style="background: rgba(255,255,255,0.75); padding: 1rem; border-radius: 12px; border: 1px solid #dcd6cd;">
                            <div style="font-size: 0.88rem; color: #2d503b; font-weight: 700; text-transform: uppercase;">Estimated Yield</div>
                            <div class="prediction-value" style="font-size: 2rem; margin: 0.2rem 0;">{prediction:,.2f} <span style="font-size: 1.1rem; font-weight: 600;">t/ha</span></div>
                        </div>
                        <div style="background: rgba(255,255,255,0.75); padding: 1rem; border-radius: 12px; border: 1px solid #dcd6cd;">
                            <div style="font-size: 0.88rem; color: #2d503b; font-weight: 700; text-transform: uppercase;">Total Farm Production</div>
                            <div style="font-family: 'Playfair Display', serif; font-size: 2rem; color: #1b382b; font-weight: 800; margin: 0.2rem 0;">{prod_fmt}</div>
                        </div>
                        <div style="background: rgba(255,255,255,0.75); padding: 1rem; border-radius: 12px; border: 1px solid #dcd6cd;">
                            <div style="font-size: 0.88rem; color: #2d503b; font-weight: 700; text-transform: uppercase;">Expected Gross Revenue</div>
                            <div style="font-family: 'Playfair Display', serif; font-size: 2rem; color: #15803d; font-weight: 800; margin: 0.2rem 0;">{rev_fmt}</div>
                            <span class="econ-badge">🏷️ {msp_status}: ₹{price_val:,.0f}/{crop_unit}</span>
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            crop_df = df[df["crop"] == crop]
            if not crop_df.empty:
                hist_mean = crop_df["yield"].mean()
                hist_min = crop_df["yield"].min()
                hist_max = crop_df["yield"].max()
                
                st.info(
                    f"💡 **Dataset Context for '{crop}':** Historical mean yield in dataset is **{hist_mean:.2f} t/ha** "
                    f"(Historical Range: {hist_min:.2f} – {hist_max:.2f} t/ha)."
                )
                
            # --- Optimizer & Decision Support Intelligence Engine ---
            opt_engine = load_optimizer()
            if opt_engine is not None:
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown("### 🌾 Farmer Decision Support & Optimization Intelligence")
                
                advisory = opt_engine.generate_full_advisory(
                    state=state, season=season, area=area,
                    annual_rainfall=annual_rainfall, fertilizer=fertilizer,
                    pesticide=pesticide, primary_crop=crop
                )
                
                tab1, tab2, tab3 = st.tabs([
                    "🏆 Multi-Crop Profitability Leaderboard",
                    "🧪 Fertilizer ROI Sweet-Spot",
                    "🌧️ Climate Stress & Drought Resilience"
                ])
                
                with tab1:
                    recs = advisory.get("top_recommended_crops", [])
                    if recs:
                        top_crop_item = recs[0]
                        
                        top_rev = top_crop_item['expected_gross_revenue_inr']
                        if top_rev >= 10000000:
                            top_rev_fmt = f"₹{top_rev / 10000000:.2f} Cr"
                        elif top_rev >= 100000:
                            top_rev_fmt = f"₹{top_rev / 100000:.2f} Lakhs"
                        else:
                            top_rev_fmt = f"₹{top_rev:,.2f}"
                            
                        st.markdown(
                            f"""
                            <div style="background: rgba(234, 242, 232, 0.9); border: 1px solid #95d5b2; border-radius: 12px; padding: 1rem; margin-bottom: 1.2rem;">
                                <span class="profit-pill">💡 Top Opportunity</span>
                                <div style="font-size: 1.1rem; color: #1b4332; font-weight: 700; margin-top: 6px;">
                                    <b>{top_crop_item['crop']}</b> yields the highest projected gross return of <b>{top_rev_fmt}</b> ({top_crop_item['predicted_yield']:.2f} t/ha) under your farm's conditions.
                                </div>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                        
                        chart_data = pd.DataFrame([
                            {
                                "Crop": r["crop"],
                                "Revenue (₹ Lakhs)": round(r["expected_gross_revenue_inr"] / 100000, 2),
                                "Yield (t/ha)": r["predicted_yield"],
                                "Category": r["category"]
                            }
                            for r in recs
                        ])
                        
                        bar_chart = alt.Chart(chart_data).mark_bar(cornerRadiusTopRight=8, cornerRadiusBottomRight=8).encode(
                            y=alt.Y('Crop:N', sort='-x', title="Crop Name"),
                            x=alt.X('Revenue (₹ Lakhs):Q', title="Projected Revenue (₹ in Lakhs)"),
                            color=alt.Color('Revenue (₹ Lakhs):Q', scale=alt.Scale(range=['#74c69d', '#2d6a4f']), legend=None),
                            tooltip=['Crop', 'Category', 'Yield (t/ha)', 'Revenue (₹ Lakhs)']
                        ).properties(height=280)
                        
                        st.altair_chart(bar_chart, use_container_width=True)
                        
                        display_df = pd.DataFrame([
                            {
                                "Rank": f"#{idx}",
                                "Crop Name": r.get("crop", "Unknown"),
                                "Category": r.get("category", "General"),
                                "Predicted Yield": f"{r.get('predicted_yield', 0.0):.2f} {r.get('yield_unit', 't/ha')}",
                                "Total Production": f"{r.get('total_production', 0.0):,.1f} {r.get('production_unit', 'Tonnes')}",
                                "Price (₹/Unit)": f"₹{r.get('price_per_unit_inr', r.get('price_per_unit', 0)):,.0f}",
                                "Expected Revenue": f"₹{r.get('expected_gross_revenue_inr', 0.0):,.2f}"
                            }
                            for idx, r in enumerate(recs, 1)
                        ])
                        st.dataframe(display_df, width="stretch", hide_index=True)
                
                with tab2:
                    fert_data = advisory.get("fertilizer_optimization", {})
                    if fert_data:
                        fcol1, fcol2, fcol3 = st.columns(3)
                        
                        fcol1.metric("Baseline Dosage", f"{fertilizer / max(1e-5, area):.1f} kg/ha", f"Total: {fertilizer:,.0f} kg")
                        fcol2.metric("Optimal Sweet-Spot", f"{fert_data['optimal_dosage_kg_ha']:.1f} kg/ha", f"{fert_data['optimal_dosage_pct']}% of baseline")
                        
                        uplift_val = fert_data.get('potential_extra_profit_inr', 0.0)
                        fcol3.metric("Profit Uplift Potential", f"+₹{uplift_val:,.2f}" if uplift_val > 0 else "Optimal", "Cost savings vs yield")
                        
                        st.markdown("<br>", unsafe_allow_html=True)
                        st.markdown("#### 📈 Fertilizer Dosage vs. Net Profit Curve")
                        
                        curve_points = fert_data.get("dosage_curve", [])
                        if curve_points:
                            curve_df = pd.DataFrame([
                                {
                                    "Dosage (kg/ha)": pt["fertilizer_rate_kg_ha"],
                                    "Net Profit (₹ Lakhs)": round(pt["net_profit_inr"] / 100000, 2),
                                    "Predicted Yield (t/ha)": pt["predicted_yield"],
                                    "Dosage %": f"{pt['dosage_pct']}%"
                                }
                                for pt in curve_points
                            ])
                            
                            line_chart = alt.Chart(curve_df).mark_line(
                                point=alt.OverlayMarkDef(color='#1b4332', size=70),
                                color='#2d6a4f',
                                strokeWidth=3
                            ).encode(
                                x=alt.X('Dosage (kg/ha):Q', title="Fertilizer Application Rate (kg/ha)"),
                                y=alt.Y('Net Profit (₹ Lakhs):Q', title="Estimated Net Profit (₹ in Lakhs)"),
                                tooltip=['Dosage %', 'Dosage (kg/ha)', 'Predicted Yield (t/ha)', 'Net Profit (₹ Lakhs)']
                            ).properties(height=280)
                            
                            st.altair_chart(line_chart, use_container_width=True)
                            
                        if uplift_val > 0:
                            st.success(f"🌱 **Economic Sweet-Spot Found:** Reducing/adjusting fertilizer to **{fert_data['optimal_dosage_kg_ha']:.1f} kg/ha** can save input costs while preserving peak yield, boosting net farm profit by **₹{uplift_val:,.2f}**.")
                        else:
                            st.info(f"🌱 **Current Dosage is Optimized:** Your baseline dosage of **{fertilizer / max(1e-5, area):.1f} kg/ha** is currently within the maximum profit efficiency window.")
                
                with tab3:
                    climate_data = advisory.get("climate_stress_analysis", {})
                    if climate_data:
                        retention = climate_data.get("yield_retention_in_drought_pct", 100.0)
                        risk_lvl = climate_data.get("climate_risk_level", "Low Drought Risk")
                        
                        ccol1, ccol2 = st.columns(2)
                        ccol1.metric("Drought Resilience Score", f"{retention:.1f}%", "Yield retained under -50% rainfall")
                        
                        with ccol2:
                            st.markdown("**Climate Risk Classification**")
                            if "Low" in risk_lvl:
                                st.markdown(f'<span class="risk-pill-low">🛡️ {risk_lvl}</span>', unsafe_allow_html=True)
                            elif "Moderate" in risk_lvl:
                                st.markdown(f'<span class="risk-pill-mod">⚠️ {risk_lvl}</span>', unsafe_allow_html=True)
                            else:
                                st.markdown(f'<span class="risk-pill-high">🚨 {risk_lvl}</span>', unsafe_allow_html=True)
                        
                        st.markdown("<br>", unsafe_allow_html=True)
                        st.markdown("#### 🌧️ Yield Simulation Across Monsoon Deficit & Excess Scenarios")
                        
                        scenarios = climate_data.get("scenarios", [])
                        if scenarios:
                            scen_df = pd.DataFrame([
                                {
                                    "Scenario": s["scenario"],
                                    "Rainfall (mm)": s["rainfall_mm"],
                                    "Predicted Yield (t/ha)": s["predicted_yield"],
                                    "Total Production (t)": s["total_production"]
                                }
                                for s in scenarios
                            ])
                            
                            scen_chart = alt.Chart(scen_df).mark_bar(cornerRadiusTopLeft=8, cornerRadiusTopRight=8).encode(
                                x=alt.X('Scenario:N', sort=None, title="Monsoon Scenario"),
                                y=alt.Y('Predicted Yield (t/ha):Q', title="Predicted Yield (t/ha)"),
                                color=alt.Color('Predicted Yield (t/ha):Q', scale=alt.Scale(range=['#a7c957', '#386641']), legend=None),
                                tooltip=['Scenario', 'Rainfall (mm)', 'Predicted Yield (t/ha)', 'Total Production (t)']
                            ).properties(height=280)
                            
                            st.altair_chart(scen_chart, use_container_width=True)
                            st.dataframe(scen_df, width="stretch", hide_index=True)
                            
        except Exception as pred_err:
            st.error(f"❌ **Prediction Execution Error:** An error occurred while calculating the yield.")
            st.caption(f"Error details: {str(pred_err)}")


st.markdown("---")
with st.expander("📊 Model Information & Evaluation Metrics", expanded=False):
    st.markdown("#### Selected Model: **Random Forest Regression**")
    st.write(
        "The model is a scikit-learn Pipeline incorporating dynamic One-Hot Encoding for categorical features (`crop`, `season`, `state`) "
        "and Passthrough preprocessing for numerical features, fitted on held-out evaluation datasets."
    )
    
    mcol1, mcol2, mcol3 = st.columns(3)
    
    with mcol1:
        st.markdown(
            """
            <div class="metric-pill">
                <div class="metric-pill-lbl">Mean Absolute Error (MAE)</div>
                <div class="metric-pill-val">9.54</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with mcol2:
        st.markdown(
            """
            <div class="metric-pill">
                <div class="metric-pill-lbl">Root Mean Squared Error (RMSE)</div>
                <div class="metric-pill-val">126.38</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with mcol3:
        st.markdown(
            """
            <div class="metric-pill">
                <div class="metric-pill-lbl">Coefficient of Determination (R²)</div>
                <div class="metric-pill-val">0.9801</div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
    st.markdown("<br>", unsafe_allow_html=True)
    st.info("💡 **Scope & Limitation Note:** Model performance varies across crops because different crops have very different yield scales.")


with st.expander("📈 Dataset & Category Insights", expanded=False):
    dcol1, dcol2, dcol3, dcol4 = st.columns(4)
    dcol1.metric("Supported Crops", f"{len(crops)}")
    dcol2.metric("Supported States", f"{len(states)}")
    dcol3.metric("Supported Seasons", f"{len(seasons)}")
    dcol4.metric("Dataset Records", f"{len(df):,}")
    
    st.markdown("#### Model Feature Pipeline")
    st.dataframe(
        pd.DataFrame({
            "Feature Name": ["crop", "season", "state", "area", "annual_rainfall", "fertilizer", "pesticide"],
            "Type": ["Categorical", "Categorical", "Categorical", "Numerical", "Numerical", "Numerical", "Numerical"],
            "Preprocessing": ["OneHotEncoder", "OneHotEncoder", "OneHotEncoder", "Passthrough", "Passthrough", "Passthrough", "Passthrough"]
        }),
        width="stretch",
        hide_index=True
    )
