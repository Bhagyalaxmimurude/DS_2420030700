
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score


# Load Dataset
def load_data():
    df = pd.read_csv("dataset/Bengaluru_House_Data.csv")
    return df


# Clean Dataset
def clean_data(df):
    df = df.drop_duplicates()

    df = df.dropna(
        subset=["location", "size", "total_sqft", "bath", "price"]
    )

    return df


# Convert Area into Numeric Value
def convert_area(value):
    try:
        return float(value)
    except:
        try:
            parts = str(value).split("-")
            return (float(parts[0]) + float(parts[1])) / 2
        except:
            return np.nan


# Prepare Numeric Data
def prepare_data(df):
    data = df.copy()

    data["total_sqft"] = data["total_sqft"].apply(convert_area)
    data["bath"] = pd.to_numeric(data["bath"], errors="coerce")
    data["price"] = pd.to_numeric(data["price"], errors="coerce")

    data = data.dropna(
        subset=["total_sqft", "bath", "price"]
    )

    data = data[
        (data["total_sqft"] > 0) &
        (data["bath"] > 0) &
        (data["price"] > 0)
    ]

    return data


# Train Machine Learning Model
def train_model(df):

    data = prepare_data(df)

    X = data[["total_sqft", "bath"]]
    y = data["price"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = LinearRegression()

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    mae = mean_absolute_error(y_test, predictions)
    r2 = r2_score(y_test, predictions)

    return model, mae, r2
