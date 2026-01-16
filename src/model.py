import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
import logging

def prepare_time_series(df, crime_type=None, province=None):
    """
    Prepares data for time series analysis.
    Filters by crime/province and groups by year.
    """
    df_filtered = df.copy()
    
    if crime_type:
        df_filtered = df_filtered[df_filtered['codigo_delito_snic_nombre'] == crime_type]
    
    if province:
        df_filtered = df_filtered[df_filtered['provincia_nombre'] == province]
        
    # Group by Year
    ts_data = df_filtered.groupby('anio')['cantidad_hechos'].sum().reset_index()
    return ts_data

def train_and_predict(ts_data, years_ahead=2):
    """
    Trains a Polynomial Regression model (Degree 2) on time series data.
    Returns a dataframe with history + prediction and potential error message.
    """
    if len(ts_data) < 3:
        return None, "Se necesitan al menos 3 años de datos para una proyección avanzada."
        
    # Prepare X (Years) and y (Counts)
    X = ts_data['anio'].values.reshape(-1, 1)
    y = ts_data['cantidad_hechos'].values
    
    # Model: Polynomial Regression Degree 2 (Quadratic)
    # This captures accelerated growth or decline better than a straight line.
    degree = 2
    if len(ts_data) < 5: # If very few points, stick to linear to avoid overfitting
        degree = 1
        
    model = make_pipeline(PolynomialFeatures(degree), LinearRegression())
    model.fit(X, y)
    
    # Future Years
    last_year = int(ts_data['anio'].max())
    future_years = np.array([last_year + i for i in range(1, years_ahead + 1)]).reshape(-1, 1)
    
    # Predict
    future_pred = model.predict(future_years)
    
    # Clip negative predictions (crime count can't be negative)
    future_pred = np.maximum(future_pred, 0)
    
    # Create Result DataFrame
    # 1. History
    hist_df = ts_data.copy()
    hist_df['tipo'] = 'Histórico'
    
    # 2. Prediction
    pred_df = pd.DataFrame({
        'anio': future_years.flatten(),
        'cantidad_hechos': future_pred,
        'tipo': 'Predicción'
    })
    
    result_df = pd.concat([hist_df, pred_df], ignore_index=True)
    
    return result_df, None
