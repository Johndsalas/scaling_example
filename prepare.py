
import env
import pandas as pd
from sklearn.impute import SimpleImputer
import scipy.stats as stats
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, QuantileTransformer, PowerTransformer,RobustScaler,MinMaxScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score, explained_variance_score
from sklearn.feature_selection import f_regression 
from math import sqrt
from statsmodels.formula.api import ols

def scaler_min_max(df, col_list):
    df_2 = df[col_list]
    df = df.drop(columns = col_list)
    scaler = MinMaxScaler(copy=True, feature_range=(0,1)).fit(df_2)
    df_2 = pd.DataFrame(scaler.transform(df_2), columns=df_2.columns.values).set_index([df_2.index.values])
    df = df.join(df_2)
    return df

def regression_errors(y, yhat, df):
    # SSE - sum of squared errors using MSE * len()
    SSE = mean_squared_error(y, df.yhat) * len(df)
    # MSE - mean of squared errors
    MSE = mean_squared_error(y, df.yhat)
    # RMSE - root mean squared error
    RMSE = sqrt(MSE)
    print("SSE: ", SSE, "MSE: ", MSE, "RMSE: ", RMSE)
    return SSE, MSE, RMSE

def handle_missing_values(df, prop_required_column = .75, prop_required_row = .75):
    threshold = int(round(prop_required_column*len(df.index),0))
    df.dropna(axis=1, thresh=threshold, inplace=True)
    threshold = int(round(prop_required_row*len(df.columns),0))
    df.dropna(axis=0, thresh=threshold, inplace=True)
    return df

def split_my_data(data, train_ratio = .80, seed = 123):
    train, test = train_test_split(data, train_size = train_ratio, random_state = seed)
    return train, test