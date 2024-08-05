# -*- coding: utf-8 -*-
"""Price_Predictor-Template2.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Jd_uJuBVfpCCvEq03fhcq5udfwlGyT9a

Notebook features:
- parse through polygon api stock data JSON files from google drive
- can initialise target features, and
- can initialise multiple sklearn models (currently regression only: LinearRegression, XGBRegressor, ElasticNet)
- ensembles multiple models to do predictions get highest scoring (r2)
- saves predictions (regression coefficients & intercepts) to JSON, and saves trained model as Pickle to google drive.

Template2 attempts to refactor the dictionaries into Dataframes like this:
```
    |   |open |close|...|
-------------------------
AAPL|  0|240.2|241.5|...|
    |  1|238.1|239.2|...|
    |  2|243.1|241.3|...|
NVDA|  0|120.4|121.7|...|
    |  1|128.9|129.1|...|
    |  2|133.1|121.3|...|
```

# 1. Setup

## 1.1 Mount Google Drive
"""

# Mount to this notebook to access JSON saved there.
from google.colab import drive
drive.mount('/content/drive')

"""## 1.2 Imports"""

import os
import json
import numpy as np
import pandas as pd
from pandas import concat
import matplotlib.pyplot as plt

# Data Preprocessing
from datetime import datetime, timedelta
from sklearn.model_selection import train_test_split
# from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import RobustScaler # https://scikit-learn.org/stable/auto_examples/preprocessing/plot_all_scaling.html#robustscaler

# Regression Models
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import ElasticNet
from xgboost import XGBRegressor
from sklearn.neural_network import MLPRegressor
# from sklearn.metrics import r2_score
# from sklearn.metrics import mean_squared_error

# Evaluation
from sklearn.metrics import mean_absolute_error

# Prediction
from sklearn.base import clone

"""## 1.3 Constants"""

# To hold dataframes created from extracted JSON files

#   a: don't think my google drive can be accessed by other users.
#   a: if cannot, download the .json files into your google drive and use your own source path.
SOURCE_DIRECTORY = f'/content/drive/MyDrive/Colab Notebooks/RoboTrader-Data-Random_Combined'
TARGET_JSON = f'combined_part_1.json'

# Output related
NOTEBOOK_NAME = 'Template1'

# add more if required.

"""# 2. Data Preprocessing"""

# The number of 10-min intervals are: 6/hour, 39/day, 195/week(5days), 819/month(21days), 2457/quarter(63days), 9828(84days).
WINDOW_DATAPOINTS_QUANTITY = 819 # Datapoints in total.
FUTURE_DATAPOINTS_QUANTITY = 39  # Datapoints for test.

"""## 2.1 Read JSON from Google Drive, use as Dataframe

todo: read from s3 instead from google drive
"""

# Data Preprocessing Variables - for Stock data extracted from polygon API.
UNWANTED_FEATURES = ['open', 'high', 'low', 'volume', 'otc', 'timestamp', 'transactions']

def json_to_dataframes(source_directory, target):
    all_data = []

    # Iterate over all files in the source directory
    for filename in os.listdir(source_directory):
        # # Check if the file is target .json file
        # if filename != target:
        #     continue

        filepath = os.path.join(source_directory, filename)
        # Check if the file is not empty
        if os.path.getsize(filepath) <= 0:
            print(f"Skipping empty file {filename}")
            continue

        try:
            # Open and read the json file
            with open(filepath, 'r') as file:
                data_dict = json.load(file)
                for stock in data_dict:
                    # Create a DataFrame from the JSON data
                    current_df = pd.DataFrame(data=data_dict[stock]['data'],
                                                    columns=data_dict[stock]['columns'],
                                                    index=data_dict[stock]['index'])
                    # # Do not add to dictionary if df is empty
                    # if (len(current_df.columns) <= 0):
                    #     continue
                    current_df.columns = current_df.columns.str.replace(' ', '')
                    if current_df.shape[0] <= WINDOW_DATAPOINTS_QUANTITY:
                        print(f'Excluded {stock}. Has {current_df.shape[0]} samples when {WINDOW_DATAPOINTS_QUANTITY} is required.')
                        continue
                    current_df['stock'] = stock  # Add stock column for MultiIndex
                    current_df.drop(labels=UNWANTED_FEATURES, axis=1, inplace=True)
                    all_data.append(current_df[-(WINDOW_DATAPOINTS_QUANTITY+FUTURE_DATAPOINTS_QUANTITY):])

        except (json.JSONDecodeError, KeyError) as e:
            print(f"Error processing file {filename}: {e}")

        # Concatenate all DataFrames into a single MultiIndex DataFrame
        if all_data:
            combined_df = pd.concat(all_data)
            combined_df.reset_index(inplace=True)
            combined_df.set_index(['stock', 'index'], inplace=True)
        else:
            combined_df = pd.DataFrame()  # Return an empty DataFrame if no data is collected

    return combined_df

# Load JSON to global MultiIndex Dataframe
df_raw = json_to_dataframes(SOURCE_DIRECTORY, TARGET_JSON)

assert df_raw.shape[0] > 0
print(df_raw.shape)
print(df_raw.describe())
print(df_raw.tail())

"""## 2.2 Feature Engineering"""

df_cleaned = df_raw.copy()
print(df_cleaned.shape)
print(df_cleaned.tail())

"""### 2.2.1 Separate by S&P sectors"""

# TODO.
# stock_sectors = pd.read_csv('https://github.com/datasets/s-and-p-500-companies/raw/main/data/constituents.csv')

"""### 2.2.2 Lag Data as Features"""

FEATURES = ['vwap'] # Volume Weighted Average Price (VWAP) is the average price of a stock weighted by the total trading volume.
LABEL = ['close']

def add_lagged_features(df_main, label, features, future_window):
    """
    Adds lagged features for machine learning models.

    Parameters:
    - df_main (DataFrame): The input MultiIndex DataFrame.
    - lag_cols (list): List of column names to use for creating lag features.
    - future_window (int): The number of lags (periods) to create.

    Returns:
    - DataFrame: The transformed DataFrame with added lag features.
    """
    all_lagged_data = []

    # gets pandas dataframe's Index object e.g., Index(['AAPL', 'NVDA', ...])
    stocks = df_main.index.get_level_values('stock').unique()

    # list of columns used to create lags
    for stock in stocks:
        # Select the data for the current stock
        df = df_main.loc[stock].copy()

        # Create lagged features for the past N periods
        for lag in range(1, future_window):
            df[f'lag_vwap_{lag}'] = df['vwap'].shift(lag)

        # Drop rows with NaN values created by the lagged features
        df.dropna(inplace=True)

        # Reintroduce the stock column for concatenation later
        df['stock'] = stock
        all_lagged_data.append(df)

    # Use only lagging close prices as Feature columns
    for i in range(1, future_window):
        FEATURES.append(f'lag_vwap_{i}')

    # Concatenate all lagged DataFrames into a single MultiIndex DataFrame
    if all_lagged_data:
        combined_lagged_df = pd.concat(all_lagged_data)
        combined_lagged_df.reset_index(inplace=True)
        combined_lagged_df.set_index(['stock', 'index'], inplace=True)
    else:
        combined_lagged_df = pd.DataFrame()  # Return an empty DataFrame if no data is collected

    return combined_lagged_df

"""### 2.2.3 Feature Selection"""

# TODO: With Feature Selection, we will be able to introduce more features in above sections, before choosing the most significant ones.

"""### Execute"""

df_feature_engineered = add_lagged_features(df_cleaned, LABEL, FEATURES, FUTURE_DATAPOINTS_QUANTITY)

print(df_feature_engineered.shape)
print(df_feature_engineered.tail())

"""## 2.3 Train-Test Split and Scale

todo: use RobustScaler
https://scikit-learn.org/stable/auto_examples/preprocessing/plot_all_scaling.html#robustscaler
"""

# Split dataset
def train_test_split_Scale(df, features, label, future_datapoints):
    """
    Splits the DataFrame into train and test sets and scales the features.

    Parameters:
    - df (DataFrame): The input MultiIndex DataFrame with all features and labels.
    - features (list): List of feature columns to use for scaling.
    - label (str): The label column to predict.
    - future_datapoints (int): Number of datapoints to include in the test set from the end of each series.

    Returns:
    - X_train (DataFrame): Scaled training features.
    - X_test (DataFrame): Scaled testing features.
    - y_train (Series): Training labels.
    - y_test (Series): Testing labels.
    """
    train_data = []
    test_data = []

    stocks = df.index.get_level_values('stock').unique()

    for stock in stocks:
        stock_df = df.loc[stock]
        train_df = stock_df[:-future_datapoints].copy()
        test_df = stock_df[-future_datapoints:].copy()

        # Reintroduce the stock column for concatenation later
        train_df['stock'] = stock
        test_df['stock'] = stock

        train_data.append(train_df)
        test_data.append(test_df)

    # Concatenate train and test data into separate MultiIndex DataFrames
    train_data = pd.concat(train_data)
    test_data = pd.concat(test_data)

    # Reset and set index to handle concatenation properly
    train_data.reset_index(inplace=True, drop=False)
    train_data.set_index(['stock', 'index'], inplace=True)
    test_data.reset_index(inplace=True, drop=False)
    test_data.set_index(['stock', 'index'], inplace=True)

    # Split into features and labels
    X_train = train_data[features].astype(float)
    y_train = train_data[label].astype(float)
    X_test = test_data[features].astype(float)
    y_test = test_data[label].astype(float)

    for stock in stocks:
        row_labels = pd.IndexSlice[stock, :]

        # Apply RobustScaler to the features. Fitted scalers are stored for later sections.
        dictionary_X_train_scaler[stock] = RobustScaler().fit(X_train.loc[row_labels])
        dictionary_X_test_scaler[stock] = RobustScaler().fit(X_test.loc[row_labels])
        dictionary_y_train_scaler[stock] = RobustScaler().fit(y_train.loc[row_labels])
        dictionary_y_test_scaler[stock] = RobustScaler().fit(y_test.loc[row_labels])

        X_train.loc[row_labels] = dictionary_X_train_scaler[stock].transform(X_train.loc[row_labels])
        X_test.loc[row_labels] = dictionary_X_test_scaler[stock].transform(X_test.loc[row_labels])
        y_train.loc[row_labels] = dictionary_y_train_scaler[stock].transform(y_train.loc[row_labels])
        y_test.loc[row_labels] = dictionary_y_test_scaler[stock].transform(y_test.loc[row_labels])

    return X_train, X_test, y_train, y_test

# Hold fitted scalers to inverse scaling after predictions later
dictionary_X_train_scaler = {}
dictionary_X_test_scaler = {}
dictionary_y_train_scaler = {}
dictionary_y_test_scaler = {}

# Train-Test Split
# train_test_split_Scale(df_dictionary_feature_engineered, FEATURES, LABEL, FUTURE_DATAPOINTS)
df_X_train, df_X_test, df_y_train, df_y_test = train_test_split_Scale(df_feature_engineered, FEATURES, LABEL, FUTURE_DATAPOINTS_QUANTITY)

# To visualise
print(df_X_train.shape, df_X_train.tail())
print(df_X_test.shape, df_X_test.tail())
print(df_y_train.shape, df_y_train.tail())
print(df_y_test.shape, df_y_test.tail())

"""# 3. Modular Sklearn Models

Using sklearn's Models' .predict method in `Train and Evaluate` and `Predict` sections later.

Thus, the models used here should be available in Sklearn.

## 3.1 Models
"""

# To hold multiple Keras Model objects across notebook so they can be iterated:
models = [] # new models
models_names = []
trained_models = {} # key: stock, value: trained Model object

# XGBRegressor parameters
n_estimators = 1000            # Number of boosted trees to fit. default = 100
max_depth = 5                  # Maximum tree depth for base learners. default = 3
learning_rate = 0.1            # Boosting learning rate (xgb's "eta"). default = 0.1
min_child_weight = 1           # Minimum sum of instance weight(hessian) needed in a child. default = 1
subsample = 1                  # Subsample ratio of the training instance. default = 1
colsample_bytree = 1           # Subsample ratio of columns when constructing each tree. default = 1
colsample_bylevel = 1          # Subsample ratio of columns for each split, in each level. default = 1
gamma = 0                      # Minimum loss reduction required to make a further partition on a leaf node of the tree. default=0

model_seed = 100

# Set and append to models[]
# models = [LinearRegression(), Model2(), Model3(), etc.]
models = [
    LinearRegression(),
    ElasticNet(alpha=0.2, l1_ratio=0.2),
    # MLPRegressor(hidden_layer_sizes=(50, 25), max_iter=1000), # may not use. takes long time to train & performs worse than others.
    XGBRegressor(objective ='reg:squarederror',
                     seed=model_seed,
                     n_estimators=n_estimators,
                     max_depth=max_depth,
                     learning_rate=learning_rate,
                     min_child_weight=min_child_weight,
                     subsample=subsample,
                     colsample_bytree=colsample_bytree,
                     colsample_bylevel=colsample_bylevel,
                     gamma=gamma)
]

for i, model in enumerate(models):
    model_name = str(model).split("(")[0]
    if model_name not in models_names:
        models_names.append(model_name)

"""# 4. Train, Evaluate, Predict"""

# Predictions
predictions_close_price_dictionary = {} # key: stock, value: prediction ('close' price)

"""## 4.1 Functions

### 4.1.1 Plot
"""

def plot_predictions(stock, model_name, y_train, y_test, y_pred, mae, future_y_pred):
    fig, axs = plt.subplots(1, 1, layout='constrained')
    axs.plot(range(len(y_train)-2*FUTURE_DATAPOINTS_QUANTITY), y_train[FUTURE_DATAPOINTS_QUANTITY*2:], color='blue')
    axs.plot(range(len(y_train)-2*FUTURE_DATAPOINTS_QUANTITY,len(y_train)+len(y_test)-2*FUTURE_DATAPOINTS_QUANTITY), y_test, color='green')
    axs.plot(range(len(y_train)-2*FUTURE_DATAPOINTS_QUANTITY,len(y_train)+len(y_pred)-2*FUTURE_DATAPOINTS_QUANTITY), y_pred, color='red')
    plt.plot(range(len(y_train)+len(y_test)-2*FUTURE_DATAPOINTS_QUANTITY,len(y_train)+len(y_test)+len(future_y_pred)-2*FUTURE_DATAPOINTS_QUANTITY), future_y_pred, color='black')
    axs.set_title(f'{stock}: {model_name} - MAE: {mae:.2f}')
    axs.set_xlabel('Period')
    axs.set_ylabel('$USD')

    plt.show()
    return

"""### 4.1.2 Train and Predict"""

# Train, evaluate, and output a fitted model, R2 score, and rmse.
def individual_model_train_predict(stock, model_name, model, X_train, X_test, y_train):
    model_fitted = model.fit(X = X_train[:-FUTURE_DATAPOINTS_QUANTITY],
                             y = y_train[:-FUTURE_DATAPOINTS_QUANTITY])
    y_pred = model_fitted.predict(X_train[-FUTURE_DATAPOINTS_QUANTITY:])
    return model_fitted, y_pred

"""### 4.1.3 Loss Function
todo: to explore using Mean absolute scaled error
"""

def calculate_mae(y_true, y_pred):
    """
    Compute mean absolute error (MAE)
    """
    y_true, y_pred = np.array(y_true), np.array(y_pred)
    return mean_absolute_error(y_true, y_pred)

"""### 4.1.4 Ensemble"""

# # Stacking (one form of ensemble learning)

# # imports
# import time
# from sklearn.metrics import PredictionErrorDisplay
# # from sklearn.model_selection import cross_val_predict, cross_validate

# # from mlxtend.regressor import StackingCVRegressor # d: not too sure what is the difference between this and the sklearn one
# from sklearn.ensemble import StackingRegressor

# # # create stack regressor
# # def create_stackingCV_regressor(models):
# #     return StackingCVRegressor(regressors=models,
# #                                     meta_regressor=xgboost,
# #                                     use_features_in_secondary=True) # ref: https://rasbt.github.io/mlxtend/user_guide/regressor/StackingCVRegressor/#api

# def create_stacking_regressor(models):
#     return StackingRegressor(
#         estimators=models,
#         final_estimator=xgboost) # ref: https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.StackingRegressor.html

# # afterwards we can compare the performance of each individual model vs the STACK
# # which is similar to the portion that you have done below, where you indicated " ### TODO: Shift this to ensemble section ###"

# # a: thanks, will look into it

# # TODO
# def ensemble_models(models):
#     best_score = -9999999
#     best_model_fitted = None
#     y_pred = None

#     for model in models:

#         local_model = clone(model)
#         local_model_name = str(local_model).split("(")[0]
#         model_fitted, y_pred_output, score, rmse = individual_model_train_and_evaluate(stock, local_model_name, local_model,
#                                                     X_train, X_test,
#                                                     y_train, y_test)
#         # print(f'{stock}: {str(model_fitted).split("(")[0]}, score: {score}') # for debugging.
#         if score > best_score:
#             best_score = score
#             best_model_fitted = model_fitted
#             y_pred = y_pred_output

#     return best_model_fitted, best_score, rmse, y_pred

"""### 4.1.5 Prepare future datapoints for  predictions"""

def data_to_supervised_learning(X_test, X_train, n_in, n_out=1, dropnan=True):
    X_train = X_train[n_in:]
    X_future = pd.concat([X_train, X_test], axis=0)
    return X_future.values[-FUTURE_DATAPOINTS_QUANTITY:]

"""## 4.2 Iterate through Functions"""

# Iterate through models[], train and evaluate them.
def all_models_train_and_evaluate(models, df_X_train, df_X_test,
                       df_y_train, df_y_test):

    # Check dictionary lengths before continuing
    if ((df_X_train.shape[0] != df_y_train.shape[0])
        or (df_X_test.shape[0] != df_y_test.shape[0])
    ):
        raise Exception(f"Please make sure all dataframe lengths are equal.")

    stocks = df_X_train.index.get_level_values('stock').unique()

    # Initialise variables
    for stock in stocks:
        row_labels = pd.IndexSlice[stock, :]
        local_X_train = df_X_train.loc[row_labels].values
        local_X_test = df_X_test.loc[row_labels].values
        local_y_train = df_y_train.loc[row_labels].values.ravel()
        local_y_test = df_y_test.loc[row_labels].values.ravel()

        lowest_mae = 9999999
        best_model_fitted = None
        ### TODO: Shift this to ensemble section ###
        for model in models:
            local_model = clone(model)
            local_model_name = str(local_model).split("(")[0]
            model_fitted, y_pred = individual_model_train_predict(stock, local_model_name, local_model,
                                                        local_X_train, local_X_test, local_y_train)
            mae = calculate_mae(y_true=dictionary_y_test_scaler[stock].inverse_transform(local_y_test.reshape(-1, 1)),
                                y_pred=dictionary_y_test_scaler[stock].inverse_transform(y_pred.reshape(-1, 1)))
            # print(f'{stock}: {str(model_fitted).split("(")[0]}, score: {score}') # for debugging.
            if mae < lowest_mae:
                lowest_mae = mae
                best_model_fitted = model_fitted

        # prepare future_x and predict future_y_pred
        future_X = data_to_supervised_learning(df_X_test.loc[row_labels], df_X_train.loc[row_labels], FUTURE_DATAPOINTS_QUANTITY, 1)
        # future_X = data_to_supervised_learning(local_X_test.values, n_in=local_X_train.shape[1]//len(FEATURES), n_out=1, dropnan=True)
        future_y_pred = best_model_fitted.predict(future_X)

        # inverse scaling
        df_dictionary_X_train_scale_inversed[stock] = dictionary_X_train_scaler[stock].inverse_transform(local_X_train)
        df_dictionary_X_test_scale_inversed[stock] = dictionary_X_test_scaler[stock].inverse_transform(local_X_test)
        df_dictionary_y_train_scale_inversed[stock] = dictionary_y_train_scaler[stock].inverse_transform(local_y_train.reshape(-1, 1))
        df_dictionary_y_test_scale_inversed[stock] = dictionary_y_test_scaler[stock].inverse_transform(local_y_test.reshape(-1, 1))
        y_pred = dictionary_y_test_scaler[stock].inverse_transform(y_pred.reshape(-1, 1))
        future_X = dictionary_X_test_scaler[stock].inverse_transform(future_X)
        future_y_pred = dictionary_y_test_scaler[stock].inverse_transform(future_y_pred.reshape(-1, 1))

        best_model_fitted_name = str(best_model_fitted).split("(")[0]
        # if i < 2: # for sample visualisation
        print(f'''\nModel: {best_model_fitted_name}
        Stock: {stock}
        Mean Absolute Error: {mae}''')
        # Coefficient: {best_model_fitted.coef_}
        # Intercept:{best_model_fitted.intercept_}
        plot_predictions(stock, best_model_fitted_name, df_dictionary_y_train_scale_inversed[stock], df_dictionary_y_test_scale_inversed[stock], y_pred, mae, future_y_pred)

        # Store fitted model
        trained_models[stock] = best_model_fitted
        # Store predictions
        predictions_close_price_dictionary[stock] = np.round(future_y_pred.flatten(), 2)

        # # Store intercept
        # predictions_intercept_dictionary[stock] = best_model_fitted.intercept_
        # # Store coefficient
        # if (best_model_fitted_name == "LinearRegression"):
        #     predictions_coef_dictionary[stock] = best_model_fitted.coef_[0]
        # else:
        #     predictions_coef_dictionary[stock] = best_model_fitted.coef_

df_dictionary_X_train_scale_inversed = {}
df_dictionary_X_test_scale_inversed = {}
df_dictionary_y_train_scale_inversed = {}
df_dictionary_y_test_scale_inversed = {}

"""## 4.3 Execute"""

all_models_train_and_evaluate(models, df_X_train, df_X_test,
                       df_y_train, df_y_test)

"""# 5. Prediction Post-processing

## 5.1 Functions

### 5.1.1 Save predictions (.json)
"""

from time import time
class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super().default(obj)

def save_dictionary_as_json(stock, output_dictionary):
    output = output_dictionary[stock]

    f=open(f'/content/drive/MyDrive/Colab Notebooks/RoboTrader-Predictions/{stock}.json',"w")
    f.write(json.dumps(output,cls=NumpyEncoder))
    f.close()

    print(f'Saved {stock}.json predictions')
    return

"""### 5.1.2 Save models (.pkl)"""

import pickle
def save_model_as_local_file(stock, model):
    model_name = str(model).split("(")[0]

    if model_name in models_names:
        if model_name == 'XGBRegressor':
            with open(f'/content/drive/MyDrive/Colab Notebooks/RoboTrader-Models/{stock}.pkl', 'wb') as f:
                pickle.dump(model.save_model, f)  #serialize the object
        else:
            with open(f'/content/drive/MyDrive/Colab Notebooks/RoboTrader-Models/{stock}.pkl', 'wb') as f:
                pickle.dump(model, f)  #serialize the object

    else:
        raise Exception(f"Please implement saving of {stock}'s model: {model_name}.")

    print(f'Saved {stock}.pkl model')
    return

"""### 5.1.3 Upload to S3 Bucket"""

# imports
!pip install boto3
import boto3

def upload_to_s3(stock, model_name):
    # Set up constants for uploading to S3 bucket
    with open(f'/content/drive/MyDrive/Colab Notebooks/env/aws_access_key.txt', 'r') as f:
        aws_access_key_id = f.read()

    with open(f'/content/drive/MyDrive/Colab Notebooks/env/aws_secret_key.txt', 'r') as f:
        aws_secret_access_key = f.read()

    predictions_bucket_name = "fourquant-robotrader-predictions"

    # Set up S3 client
    s3 = boto3.client('s3',
                    aws_access_key_id = aws_access_key_id,
                    aws_secret_access_key = aws_secret_access_key)

    # Upload file to S3 bucket
    with open(f'/content/drive/MyDrive/Colab Notebooks/RoboTrader-Predictions/{stock}.json', "rb") as f:
        s3.upload_fileobj(f, predictions_bucket_name, f'{stock}.json')

    print(f'Uploaded {stock}.json predictions')
    return

"""### 5.1.4 Iterate through all tickers"""

# predictions_coef_dictionary[ticker] = [[-5.90832260e-01  5.43316834e-01  ...]]
def combine_predictions_to_dictionary():

    # timestamp = int(time()) - see whether want to include timestamp on the .json files.
    # add ticker, predicted close prices to dictionary
    for i, ticker in enumerate(trained_models):
        output_dictionary = {}

        model_name = str(trained_models[ticker]).split("(")[0]
        index = list(range(len(predictions_close_price_dictionary[ticker]))), # generates ([0, 1, ... n],)

        # JSON output format
        if model_name == "LinearRegression" or model_name == "XGBRegressor" or model_name == "ElasticNet" or model_name == "MLPRegressor":
            output_dictionary[ticker] = {
                # "model": model_name,
                # "index": index,
                # "coef": predictions_coef_dictionary[ticker],
                # "intercept": predictions_intercept_dictionary[ticker]
                "tickerName": ticker,
                "predictions": predictions_close_price_dictionary[ticker]
            }

        else:
            raise Exception(f"Please ensure loop checks for {model_name} and outputs its JSON.")

        save_dictionary_as_json(ticker, output_dictionary)
        save_model_as_local_file(ticker, trained_models[ticker])
        upload_to_s3(ticker, model_name)

"""## 5.2 Execute"""

combine_predictions_to_dictionary()

"""# Miscellenous to delete"""

'''
28 Jul, a's notes.

ETF1 : A , B , C

Model: Train on ETF1 [
    Features:
        Linear Features: Some kind of technical indicator
        Non-linear Features:
]

Predictions use ETF1_Model predict on A, B, C

Output JSON : pred_A, pred_B, pred_C




Linear - Single Feature -
    Training: X, y
    Prediction: X

Linear - Multi Feature -
    Training: X1, X2, X3, y
    Prediction: X1, X2, X3



model_predictions = {

    "STOCK_1": {             # stock names are keys
        "model": Model
        "columns": [          # list of column header strings
            "close",
            "timestamp",
            ...
        ],
        "index": [            # list of row indexes
            0,
            1,
            ...
        ],
        "data": [             # list of lists of data. One list per row.
            [40, 1721823600],
            [40.2, 1721824200],
            ...
        ]
    }
    "STOCK_2" = {

    }
    ...
}
'''