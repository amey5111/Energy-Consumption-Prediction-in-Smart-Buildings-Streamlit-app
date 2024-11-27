# -*- coding: utf-8 -*-
"""FDS_Experiment_08.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/18rehtzLSqCGZBXh4I7eLKpb02gVJ92PN

Name: Amey Dilip Morye

UID No.: 2024310012

Title: Energy Consumption Prediction in Smart Buildings
"""

# Import required libraries

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler

# Load the dataset using Pandas.
data = pd.read_csv('Energy_consumption.csv')

data.head()

# Fill missing values (if any)
data.fillna(method='ffill', inplace=True)

# Normalize continuous features
scaler = StandardScaler()
data[['Temperature', 'Humidity']] = scaler.fit_transform(data[['Temperature', 'Humidity']])

# Visualize data
sns.pairplot(data, diag_kind='kde')
plt.show()

"""**2.Build a Machine Learning Model**"""

from sklearn.model_selection import train_test_split
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_squared_error

# Split data
X = data[['Temperature', 'Humidity', 'Occupancy']]
y = data['EnergyConsumption']
X_train, X_test, y_train, y_test = train_test_split(X, y,
test_size=0.2, random_state=42)

# Train model
model = Ridge()
model.fit(X_train, y_train)

# Test model
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
print(f'Mean Squared Error: {mse}')

!pip install streamlit

"""**3. Build a Streamlit App**"""

import streamlit as st
import numpy as np

# Streamlit app
st.title("Energy Consumption Prediction")

# Input fields
temperature = st.number_input("Temperature (°C)")
humidity = st.number_input("Humidity (%)")
occupancy = st.radio("Occupancy", (0, 1))
# Prediction button
if st.button("Predict"):
  # Make prediction
  input_features = np.array([[temperature, humidity, occupancy]])
  prediction = model.predict(input_features)[0]
  st.write(f"Predicted Energy Consumption: {prediction:.2f} kWh")

# save model as pickle file
import joblib
joblib.dump(model, 'ridge_model.pkl')