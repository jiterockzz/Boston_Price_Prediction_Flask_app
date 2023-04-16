#Import Libraries
import numpy as np
import pandas as pd
import joblib


from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split



data = pd.read_csv('data/test_xdata.csv', sep=',')
target = pd.read_csv('data/test_y_data.csv', sep=',')



X_train, X_test, y_train, y_test = train_test_split(data,target, test_size=0.2, random_state=51)

# feature scaling not required for random forest but yet trying best
sc = StandardScaler()
sc.fit(X_train)
X_train = sc.transform(X_train)
X_test = sc.transform(X_test)

# 7.831,3.1992,17.8,4.45
###### Load Model

model = joblib.load('model/price_prediction_rfr.joblib')


def Predict(to_predict_list):
    to_predict = np.array(to_predict_list)
    
    to_predict_list = sc.transform([to_predict])
    result = model.predict(to_predict_list)
    return result[0]
    
    
    
   
   
   

  
