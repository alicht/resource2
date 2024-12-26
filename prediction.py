from sklearn.linear_model import LinearRegression
import pandas as pd
import numpy as np

def train_prediction_model(df, target_column):
    """
    Train a prediction model using historical data.
    
    Args:
        df (pd.DataFrame): DataFrame containing historical data with a "Timestamp" column.
        target_column (str): The column to predict (e.g., "Cost", "Total Tokens").
    
    Returns:
        LinearRegression: Trained model.
    """
    # Calculate elapsed time in seconds from the start
    df["Elapsed Time"] = (df["Timestamp"] - df["Timestamp"].min()).dt.total_seconds()
    
    # Extract features (X) and target (y)
    X = df[["Elapsed Time"]].values
    y = df[target_column].values
    
    # Train a linear regression model
    model = LinearRegression()
    model.fit(X, y)
    
    return model

def predict_future_value(model, current_elapsed_time, days_into_future=1):
    """
    Predict the future value using the trained model.
    
    Args:
        model (LinearRegression): Trained model.
        current_elapsed_time (float): Current elapsed time in seconds.
        days_into_future (int): Number of days into the future for the prediction.
    
    Returns:
        float: Predicted value for the given future time.
    """
    future_time = np.array([[current_elapsed_time + (days_into_future * 86400)]])  # Add days in seconds
    return model.predict(future_time)[0]
