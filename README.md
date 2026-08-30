# 🌾 YIELDICT AI — Smart Crop Yield Prediction & Farm Decision Support

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](http://localhost:8501)
[![Python Version](https://img.shields.io/badge/Python-3.10%2B-2d6a4f.svg?style=flat&logo=python&logoColor=white)](https://python.org)
[![Scikit-Learn](https://img.shields.io/badge/scikit--learn-1.3%2B-orange.svg?style=flat&logo=scikitlearn&logoColor=white)](https://scikit-learn.org)
[![Git LFS](https://img.shields.io/badge/Git%20LFS-Tracked-blue.svg?style=flat&logo=git-lfs&logoColor=white)](https://git-lfs.github.com)

**YIELDICT AI** is a machine learning agricultural intelligence and decision-support platform designed to forecast crop yields, evaluate farm economics, and provide risk-mitigated crop recommendations for Indian agriculture.

Powered by an ensemble **Random Forest Regression Pipeline** ($R^2 = 0.9805$), the platform transforms raw agro-climatic inputs into monetary insights, optimal fertilizer application curves, and climate drought simulations.

---

## 📸 Key Features

### 1. 🌾 High-Precision Yield & Revenue Forecasting
* **Multi-Parameter Inference:** Evaluates 55 crop types across 30 Indian states and 6 agricultural seasons.
* **Synchronized Controls:** Interactive numeric boxes and sliders for Cultivated Area, Annual Rainfall, Fertilizer Usage, and Pesticide Application.
* **Monetary Valuation:** Calculates total farm output ($Yield \times Area$) and expected gross revenue in INR (₹ Lakhs / ₹ Crores) mapped to Government Minimum Support Price (MSP) benchmarks.

### 2. 🏆 Multi-Crop Profitability Leaderboard
* Evaluates alternative crops viable in the selected state and season.
* Ranks top alternative opportunities and displays an interactive **Altair Revenue Bar Chart** to maximize farm returns.

### 3. 🧪 Fertilizer ROI & Profit Sweet-Spot Optimizer
* Simulates marginal fertilizer cost (₹30/kg) vs. crop yield returns across $25\% - 200\%$ dosage variations.
* Pinpoints the **Economic Sweet-Spot Dosage (kg/ha)** and calculates potential net profit uplift.
* Embeds an interactive **Fertilizer Dosage vs. Net Profit Curve**.

### 4. 🌧️ Climate Stress & Drought Resilience Simulator
* Stress-tests farm yields against 5 monsoon rainfall scenarios ($-50\%$ drought deficit to $+50\%$ excess monsoon).
* Computes a **Drought Resilience Score (%)** and categorizes the farm under automated climate risk tiers (*🛡️ Low Risk / ⚠️ Moderate Risk / 🚨 High Risk*).

### 5. 🎨 Botanical Paper & Nature Glassmorphism UI
* Curated emerald-forest palette (`#2d6a4f`, `#52b788`, `#1b382b`), frosted glass surfaces, and responsive typography (`Playfair Display` + `Plus Jakarta Sans`).

---

## 🛠️ Tech Stack & Dependencies

| Layer | Technology |
| :--- | :--- |
| **Frontend UI** | Streamlit, HTML5, Vanilla CSS3 (Custom Botanical Paper Theme) |
| **Data Visualization** | Altair Interactive Visualizations |
| **Machine Learning** | Scikit-Learn (Pipeline, ColumnTransformer, OneHotEncoder, RandomForestRegressor) |
| **Data Manipulation** | Pandas, NumPy |
| **Serialization** | Joblib, Git LFS |

---

## 🚀 Step-by-Step Setup Guide

### 1. Clone the Repository
```bash
git clone https://github.com/TeamKinetix/Yieldict_AI.git
cd Yieldict_AI
```

### 2. Initialize Git LFS (for Model Weights)
The trained model (`crop_yield_model.pkl`, 175.5 MB) is tracked with Git Large File Storage (LFS):
```bash
git lfs install
git lfs pull
```

### 3. Set Up a Virtual Environment
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## 💻 How to Run

### Method 1: Launch the Main Web Application (Recommended)
```bash
streamlit run "ML base_line trainning/ML base_line trainning/app.py"
```
Or use the launcher wrapper:
```bash
streamlit run "ML base_line trainning/app.py"
```
Once started, open **[http://localhost:8501](http://localhost:8501)** in your browser.

---

### Method 2: Launch the Standalone Optimizer API Server
For microservice setups or programmatic querying:
```bash
python optimizer/server.py
```
Access the advisory endpoint at **`http://localhost:8000`**.

---

### Method 3: Run the CLI Decision Advisory Tool
For fast command-line farm simulations:
```bash
python optimizer/crop_optimizer.py
```

---

## 🧠 Model Training & Pipeline Architecture

The model is trained on 19,689 validated historical agricultural records using a single scikit-learn `Pipeline`:

```
Input Features (7)
│
├── Categorical Features ['crop', 'season', 'state']
│   └── OneHotEncoder(handle_unknown='ignore', sparse_output=False) -> [88 dimensions]
│
├── Numerical Features ['area', 'annual_rainfall', 'fertilizer', 'pesticide']
│   └── Passthrough -> [7 dimensions]
│
└── Regressor
    └── RandomForestRegressor(n_estimators=100, max_depth=None, random_state=42, n_jobs=-1)
```

### Model Performance Metrics
* **Coefficient of Determination ($R^2$):** `0.9805` (98.05% variance explained)
* **Mean Absolute Error (MAE):** `8.79 t/ha`
* **Root Mean Squared Error (RMSE):** `118.42 t/ha`

### How to Retrain the Model:
To reproduce or retrain the pipeline from scratch, open and run all cells in:
```bash
important code/Baseline_Model.ipynb
```
The notebook automatically outputs the updated `crop_yield_model.pkl` pipeline.

---

## 📂 Project Directory Structure

```text
CropYield/
│
├── .gitattributes                  # Git LFS configuration (*.pkl tracking)
├── .gitignore                      # Tailored repository ignore rules
├── .streamlit/                     # Streamlit theme and viewport configuration
│   └── config.toml
│
├── 6 files/                        # PRD, Architecture, and Design specifications
│   ├── PRD.md
│   ├── architecture.md
│   ├── design.md
│   └── phases.md
│
├── important code/                 # Training notebooks & model checkpoints
│   ├── Baseline_Model.ipynb        # Model training & evaluation notebook
│   └── crop_yield_cleaned.csv      # Agricultural dataset (19,689 records)
│
├── ML base_line trainning/         # Web Application core
│   ├── ML base_line trainning/
│   │   ├── app.py                  # Main Streamlit web application
│   │   ├── crop_yield_model.pkl    # Serialized scikit-learn Pipeline (175.5 MB)
│   │   ├── crop_yield_cleaned.csv  # Cleaned dataset
│   │   └── background.png          # UI graphics & branding
│   └── app.py                      # Root launcher script
│
├── optimizer/                      # Advisory & Simulation Engine
│   ├── __init__.py                 # Package initializer
│   ├── crop_optimizer.py           # Multi-crop, fertilizer ROI & climate stress logic
│   ├── msp_data.py                 # Crop pricing, MSP data & categories
│   └── server.py                   # Standalone advisory service (Port 8000)
│
├── processed data for training/    # Cleaned datasets & EDA documentation
│   ├── STEP_3_EDA_REPORT.md
│   └── crop_yield_cleaned.csv
│
├── requirements.txt                # Python package dependencies
└── README.md                       # Master project documentation
```

---

## 👥 Authors & Team
Developed by **Kinetix**. For feedback, inquiries, or contributions, please open a GitHub Issue or Pull Request.
