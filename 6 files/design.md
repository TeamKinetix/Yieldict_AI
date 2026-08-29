# CropYield AI — Product & UI Design

## 1. Design Goal

The application should make machine learning understandable to a non-technical user.

The user should immediately understand:

1. What information to enter.
2. What the model predicts.
3. What the prediction means.
4. Which factors influenced the prediction.

---

# 2. Application Structure

The application should have four main sections.

```text
┌─────────────────────────────────────────┐
│              CropYield AI               │
│     Smart Crop Yield Prediction         │
├─────────────────────────────────────────┤
│                                         │
│  1. Crop Information                    │
│                                         │
│  Crop        [ Rice ▼ ]                 │
│  Region      [ Select Region ▼ ]        │
│                                         │
│  2. Environmental Information           │
│                                         │
│  Rainfall    [ 1200 ] mm                │
│  Temperature [ 27 ] °C                  │
│                                         │
│  3. Farming Information                 │
│                                         │
│  Area        [ 2 ] hectares             │
│  Fertilizer  [ 150 ] kg                │
│                                         │
│          [ Predict Yield ]              │
│                                         │
└─────────────────────────────────────────┘
```

---

# 3. Dashboard

The main dashboard should show:

### Header

```text
CropYield AI
Machine Learning Based Crop Yield Prediction
```

### Short description

```text
Estimate crop yield using historical agricultural
and environmental data.
```

---

# 4. Input Form

Group inputs logically.

## Crop Information

* Crop
* Region/State
* Season if available

## Environmental Information

* Rainfall
* Temperature
* Humidity if available

## Agricultural Information

* Area
* Fertilizer usage
* Pesticide usage
* Soil-related variables if available

---

# 5. Input Validation

Examples:

### Area

Must be greater than zero.

### Rainfall

Should not be negative.

### Temperature

Should be within a reasonable range for the dataset.

### Fertilizer

Should not be negative.

Display friendly messages.

Example:

```text
Please enter a valid cultivated area.
```

---

# 6. Prediction Result

After clicking the prediction button:

```text
┌───────────────────────────────────┐
│        PREDICTED CROP YIELD       │
│                                   │
│             3.8                   │
│          tons/hectare             │
│                                   │
│   Model: Extra Trees Regression   │
└───────────────────────────────────┘
```

The prediction should be the most visually important element.

---

# 7. Confidence / Uncertainty

Do not display a fake confidence percentage.

If uncertainty estimation is implemented later, clearly label it as an estimate.

For the first version, simply show:

```text
Estimated Yield
```

---

# 8. Explainability Section

Display:

```text
Why did the model make this prediction?

Top influencing features:

Rainfall
████████████

Temperature
████████

Fertilizer
██████

Soil Type
████
```

Explain:

> Feature importance indicates how useful features were to the trained model. It does not necessarily mean that a feature directly causes higher yield.

---

# 9. Model Performance Section

Show the model comparison.

Example:

```text
Model              R²       RMSE
-----------------------------------
Linear Regression  0.71     1.21
Random Forest      0.87     0.81
Extra Trees        0.90     0.76
Gradient Boosting  0.89     0.79
```

Use actual experimental results in the final application.

---

# 10. About Section

Include:

```text
About CropYield AI

CropYield AI uses machine learning to estimate
crop yield from agricultural and environmental
information.

The system learns patterns from historical data
and should be used as a decision-support prototype,
not as a guaranteed prediction.
```

---

# 11. Visual Style

Recommended design:

* Clean
* Modern
* Minimal
* Agricultural theme
* Good spacing
* Large prediction result
* Simple charts

Avoid:

* Excessive animations.
* Too many colors.
* Crowded dashboards.
* Technical jargon.

---

# 12. User Journey

```text
LANDING PAGE
     ↓
Read project description
     ↓
ENTER CROP INFORMATION
     ↓
ENTER ENVIRONMENTAL DATA
     ↓
ENTER FARMING DATA
     ↓
CLICK PREDICT
     ↓
VIEW YIELD
     ↓
VIEW IMPORTANT FEATURES
     ↓
VIEW MODEL INFORMATION
```

---

# 13. Responsive Design

The interface should remain usable on:

* Laptop
* Desktop
* Tablet
* Mobile where supported

Input fields should not become excessively wide.

---

# 14. Accessibility

Use:

* Clear labels.
* Readable text.
* Meaningful error messages.
* Good contrast.
* Avoid relying only on color to communicate information.

---

# 15. Hackathon Demo Design

The demo should be fast.

The judge should be able to understand the project within approximately one minute.

Demo sequence:

```text
"This is CropYield AI."

"We enter the crop and environmental conditions."

"Now we click Predict."

"The model estimates the expected yield."

"Here are the features that were most important."

"We also compared several ML models and selected
the best-performing model using MAE, RMSE and R²."
```
