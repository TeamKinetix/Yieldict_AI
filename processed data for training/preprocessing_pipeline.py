import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer

df = pd.read_csv("crop_yield_cleaned.csv")

target = "yield"
X = df.drop(columns=[target])
y = df[target]

categorical_features = ["crop", "season", "state"]
numeric_features = [
    "year", "area", "annual_rainfall",
    "fertilizer", "pesticide"
]

preprocessor = ColumnTransformer(
    transformers=[
        ("num", SimpleImputer(strategy="median"), numeric_features),
        ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features),
    ]
)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=42
)

# The preprocessor will be combined with each ML model in the next step.
print("X_train:", X_train.shape)
print("X_test:", X_test.shape)
print("Features:", categorical_features + numeric_features)
