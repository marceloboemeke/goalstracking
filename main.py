import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
from datetime import datetime
from PIL import Image
import requests

st.title("Goals Tracking")

st.markdown("""
This app allows you to track your personal goals in an intuitive and visual way
""")

data_full = pd.read_csv('https://docs.google.com/spreadsheets/d/1vZbW9ebUqnf-c6JYzt0itvqybiPq31Prd-0Y4Q6F6cU/export?gid=0&format=csv', parse_dates=["Data Inicial","Data Final","Data do Registro","Checkpoint 1", "Checkpoint 2", "Checkpoint 3"], dayfirst=True)

for data in [y for x, y in data_full.groupby('Objetivo')]:
  start_date = data['Data Inicial'].values[0]
  end_date = data['Data Final'].values[0]
  initial_value = data['Valor inicial'].values[0]
  target_value = data['Meta'].values[0]
  measuring_unit = data['Unidade de Medida'].values[0]

  x_axis = pd.to_datetime(data['Data do Registro']).tolist()
  y_axis = data['Valor Atual'].values.tolist()

  fig, ax = plt.subplots()

  im = Image.open(requests.get("https://i.imgur.com/2hL9bGM.png", stream=True).raw)
  ax.imshow(im, extent=[start_date, end_date, 0, target_value], aspect='auto', alpha=0.6)

  fig.figsize = (500,400)
  ax.plot(x_axis, y_axis, marker='o', markersize=3)

  checkpoint_dates = [data['Checkpoint 1'].values[0]] + [data['Checkpoint 2'].values[0]] + [data['Checkpoint 3'].values[0]]

  ax.set_title(data['Objetivo'].values[0])
  ax.set_xlabel('Data')
  ax.set_ylabel(measuring_unit.capitalize())
  ax.set_ybound(initial_value, target_value)
  ax.set_xbound(start_date, end_date)
  ax.set_xticks([ start_date, end_date ], minor = False)
  ax.set_xticks(checkpoint_dates, minor = True)

  ax.set_yticks([
    initial_value
    , target_value * 0.25
    , target_value * 0.5
    , target_value * 0.75
    , target_value
  ])

  #calculate equation for trendline
  # x = mdates.date2num(x_axis)
  # z = np.polyfit(x, y_axis, 1)
  # p = np.poly1d(z)

  # x_axis = [x_axis[-1]] + [end_date]
  # x2 = mdates.date2num(x_axis)

  # # Add trendline
  # ax.plot(x_axis, p(x2), "k--", alpha=0.2)

  plt.grid(visible=True, which='minor')
  plt.grid(visible=True, axis='y', linestyle=':')
  # plt.show()

  st.pyplot(fig)