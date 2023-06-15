# Romi Rukman-1301194129

# Visualisasi Data Menggunakan Bokeh dan deploy aplikasi menggunakan Streamlit Dataset Covid-19 https://www.kaggle.com/datasets/hendratno/covid19-indonesia


import streamlit as st
import pandas as pd
import numpy as np
import datetime
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.events import Tap

data_covid = pd.read_csv('test.csv')  

data_covid['Date'] = pd.to_datetime(data_covid['Date'])

st.title('Visualisasi Data COVID-19 Indonesia')
st.header('Jumlah Kasus per Hari')

tanggalMulai = datetime.datetime(2020,3,11)
tanggalAkhir = datetime.datetime(2022,9,16)

#min_date = datetime.datetime(2020,3,11)
#max_date = datetime.datetime(2022,9,16)
#slider=st.slider('Pilih', min_date.strftime(%Y-%m-%d), max_date.strftime(%Y-%m-%d), min_date.strftime(%Y-%m-%d))

tanggalTerpilih = st.slider('Pilih Tanggal', tanggalMulai.strftime(%Y-%m-%d), tanggalAkhir.strftime(%Y-%m-%d), tanggalMulai.strftime(%Y-%m-%d))

tanggalTerpilih = (pd.Timestamp.fromtimestamp(tanggalTerpilih[0]), pd.Timestamp.fromtimestamp(tanggalTerpilih[1]))

dataTerpilih = data_covid[(data_covid['Date'] >= tanggalTerpilih[0]) & (data_covid['Date'] <= tanggalTerpilih[1])]

jenis_kasus = st.selectbox('Pilih Jenis Kasus', ['New Cases', 'New Deaths', 'New Recovered','New Active Cases', 'Total Cases', 'Total Deaths', 'Total Recovered', 'Total Active Cases' ])

p = figure(title=f'Jumlah {jenis_kasus} per Hari {tanggalTerpilih}', x_axis_type='datetime', plot_width=800, plot_height=400)
source = ColumnDataSource(data=dataTerpilih)
p.line('Date', jenis_kasus, source=source, line_width=2)

selected_indices = []

def plot_tap_event(event):
    selected_index = event.index['1d']['indices'][0]
    if selected_index in selected_indices:
        selected_indices.remove(selected_index)
    else:
        selected_indices.append(selected_index)

p.on_event(Tap, plot_tap_event)

hover = HoverTool(tooltips=[('Tanggal', '@date{%F}'), (jenis_kasus, f'@{jenis_kasus}')], formatters={'@date': 'datetime'})
p.add_tools(hover)

st.bokeh_chart(p)

if selected_indices:
    data_terpilih = dataTerpilih.iloc[selected_indices]
    st.header('Data yang Dipilih')
    st.write(data_terpilih)