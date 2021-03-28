import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.arima_model import ARIMA

import pandas as pd
import numpy as np

series = pd.read_csv('data.csv', index_col=0)
model_fit = None

def fit():
  global model_fit
  try:
    print(series)
    # (AR=0, 차분=1, MA=1) 파라미터로 ARIMA 모델을 학습합니다.
    model = ARIMA(series, order=(0,1,1))
    # trend : constant를 가지고 있는지, c - constant / nc - no constant
    # disp : 수렴 정보를 나타냄
    model_fit = model.fit(trend='c',full_output=True, disp=False)
    # print(model_fit.summary())

  except Exception as err:
    print(err)

# [[예측값], [stderr], [upper bound(예상 최댓값), lower bound(예상 최솟값)]]
def forecast(steps=1):
  # steps 예상일
  fore = model_fit.forecast(steps=steps)
  # print()
  # print('예측금액: ', fore[0][0])
  # print('stderr: ', fore[1][0])
  # print('예상 최대금액: ', fore[2][0][0])
  # print('예상 최소금액: ', fore[2][0][1])
  return fore[0][0]

def add_data(data):
  global series
  df = pd.DataFrame(
    [data['price']], 
    columns=['market-price'], 
    index=[data['ts']]
  )
  
  series = pd.concat([series, df])

if __name__ == "__main__": 
  fit()
  p = forecast()

  add_data({
    'ts': 1234,
    'price': 123455
  })

  fit()
  p = forecast()

  add_data({
    'ts': 1234,
    'price': 123455
  })
  print(series)