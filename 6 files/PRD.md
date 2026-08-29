# Crop Yield Prediction ML System — Product Requirements Document

## 1. Project Overview

### Project Name

**CropYield AI — Machine Learning Based Crop Yield Prediction**

### Project Type

Machine Learning / Predictive Analytics

### Objective

The goal of this project is to build a machine learning system that predicts the expected yield of a crop based on agricultural and environmental factors.

The system will take information such as crop type, location, rainfall, temperature, fertilizer usage, pesticide usage, cultivated area, and other available features and predict the expected crop yield.

The project should also provide basic explainability so that users can understand which factors influenced the prediction.

---

## 2. Problem Statement

Farmers and agricultural decision-makers need to estimate crop production before harvest.

Traditional yield estimation can depend heavily on historical knowledge, manual calculations, and uncertain environmental conditions.

A machine learning model can learn relationships between historical agricultural data and crop yield and provide a data-driven estimate.

### Problem

> Given historical agricultural and environmental information, predict the expected crop yield.

### Machine Learning Type

**Supervised Learning — Regression**

The target variable is continuous.

Example:

```text
Input:
Crop = Rice
Rainfall = 1200 mm
Temperature = 27°C
Area = 2 hectares
Fertilizer = 150 kg

Output:
Predicted Yield = 3.8 tons/hectare
```

---

## 3. Target Users

### Primary Users

* Students and researchers
* Farmers
* Agricultural analysts
* Agricultural planning organizations

### Hackathon User

For the hackathon, the main user will be a person who enters agricultural information into a simple web interface and receives a predicted crop yield.

---

## 4. Project Goals

### Primary Goals

1. Prepare a crop yield dataset.
2. Clean and preprocess the data.
3. Perform exploratory data analysis.
4. Train multiple regression models.
5. Compare model performance.
6. Select the best-performing model.
7. Build a prediction interface.
8. Display prediction results clearly.
9. Provide basic model explainability.
10. Demonstrate the complete ML pipeline.

---

## 5. Machine Learning Models

The project will compare multiple models.

### Baseline Model

**Linear Regression**

Purpose:

* Establish a simple baseline.
* Understand whether basic linear relationships exist.
* Provide a reference point for comparing advanced models.

### Candidate Models

#### Random Forest Regression

Advantages:

* Handles nonlinear relationships.
* Works well with mixed feature relationships.
* Provides feature importance.

#### Extra Trees Regression

Advantages:

* Similar to Random Forest.
* Uses stronger randomization.
* Can perform well on tabular datasets.
* Provides feature importance.

#### Gradient Boosting

Advantages:

* Strong performance on structured/tabular data.
* Can model complex relationships.

#### XGBoost

Optional advanced model if time and implementation quality allow.

---

## 6. Evaluation Metrics

The models will be evaluated using:

### MAE — Mean Absolute Error

Measures average absolute prediction error.

Lower is better.

### RMSE — Root Mean Squared Error

Penalizes larger errors more strongly.

Lower is better.

### R² — R-Squared

Measures how much variation in the target is explained by the model.

Higher is better.

---

## 7. Dataset Requirements

The dataset should contain historical agricultural records.

Potential features include:

```text
Crop
State / Region
Area
Rainfall
Temperature
Humidity
Soil Type
Fertilizer Usage
Pesticide Usage
Year
Season
Production
Yield
```

The exact features depend on the selected dataset.

### Target

The preferred target is:

```text
Yield
```

For example:

```text
Yield = tons/hectare
```

If the dataset contains only production and area, yield can potentially be calculated as:

```text
Yield = Production / Area
```

The calculation must only be performed when the dataset definitions make this valid.

---

## 8. Data Processing

The preprocessing pipeline should include:

1. Load dataset.
2. Inspect columns.
3. Identify target variable.
4. Check missing values.
5. Remove or appropriately handle invalid records.
6. Detect duplicate records.
7. Handle categorical variables.
8. Handle numerical variables.
9. Detect extreme/outlier values where appropriate.
10. Split data into training and validation/test sets.
11. Fit preprocessing only on training data to prevent data leakage.

---

## 9. Data Leakage Prevention

Data leakage must be avoided.

Information that would not be known at prediction time should not be used as an input.

For example, if predicting yield before harvest, actual final production should not be used as a feature.

The preprocessing pipeline should be fitted using training data only.

---

## 10. Model Selection

The model with the strongest validation performance should be selected.

Primary consideration:

* Lower MAE
* Lower RMSE
* Higher R²

However, model selection should also consider:

* Stability
* Interpretability
* Training complexity
* Ease of deployment

---

## 11. Explainability

The application should show why the model produced a prediction.

Possible methods:

### Feature Importance

Show the most influential features.

Example:

```text
Rainfall       ██████████
Temperature    ███████
Fertilizer     █████
Area           ███
Humidity       ██
```

### SHAP

SHAP can optionally be implemented if time allows.

It can show how individual features contributed to a specific prediction.

---

## 12. User Interface

The application should provide a simple prediction form.

Example:

```text
Crop:              [ Rice       ]
Region:            [ West Bengal]
Rainfall:          [ 1200       ]
Temperature:       [ 27         ]
Area:              [ 2          ]
Fertilizer:        [ 150        ]

              [ Predict Yield ]

Predicted Yield:

        3.8 tons/hectare
```

The UI should also display:

* Prediction
* Important factors
* Model performance
* Basic information about the project

---

## 13. Success Criteria

The project is successful if:

* The dataset is processed correctly.
* Multiple regression models are trained.
* Models are evaluated using MAE, RMSE, and R².
* A best model is selected using validation performance.
* A user can enter agricultural information.
* The system returns a crop yield prediction.
* The prediction interface works reliably.
* The project can be demonstrated during the hackathon.
* The methodology can be explained by the team.

---

## 14. Non-Goals

The first version will NOT attempt to:

* Guarantee actual future harvest yield.
* Replace agricultural experts.
* Provide financial advice.
* Provide disease diagnosis.
* Automatically control farming equipment.
* Claim that predictions are universally accurate for every region.

The system is a predictive ML prototype.

---

## 15. Final Deliverable

The final project should contain:

```text
Dataset
↓
Data preprocessing
↓
EDA
↓
Feature engineering
↓
Model training
↓
Model comparison
↓
Best model
↓
Prediction API/application
↓
User interface
↓
Explainability
↓
Final demonstration
```
