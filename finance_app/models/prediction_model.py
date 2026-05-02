import numpy as np
import pandas as pd
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression

class PolynomialPricePredictor:
    def __init__(self, degree: int = 2):
        self.degree = degree
        self.model = LinearRegression()
        self.poly_features = PolynomialFeatures(degree=degree)

    def predict(self, prices: list, days_ahead: int = 5):
        """
        Predict future prices based on a list of historical prices using polynomial regression.
        """
        if len(prices) < self.degree + 1:
            return []
        
        # Prepare data (x: days, y: price)
        X = np.array(range(len(prices))).reshape(-1, 1)
        y = np.array(prices)
        
        X_poly = self.poly_features.fit_transform(X)
        self.model.fit(X_poly, y)
        
        # Predict future days
        future_X = np.array(range(len(prices), len(prices) + days_ahead)).reshape(-1, 1)
        future_X_poly = self.poly_features.transform(future_X)
        predictions = self.model.predict(future_X_poly)
        
        return predictions.tolist()
