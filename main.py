# Visualisasi Data Menggunakan Bokeh dan deploy aplikasi menggunakan Streamlit Dataset Covid-19 https://www.kaggle.com/datasets/hendratno/covid19-indonesia


import streamlit as st
import pandas as pd
import numpy as np
import datetime
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, HoverTool, NumeralTickFormatter
from bokeh.events import Tap

data_covid = pd.read_csv('test (2).csv')  

data_covid['Date'] = pd.to_datetime(data_covid['Date'])

st.title('Visualisasi Data COVID-19 Indonesia')
st.header('Jumlah Kasus per Hari')

tanggalMulai = data_covid['Date'].min().date()
tanggalAkhir = data_covid['Date'].max().date()

tanggalTerpilih = st.slider('Pilih Tanggal', tanggalMulai, tanggalAkhir, (tanggalMulai, tanggalAkhir))

data_terfilter = data_covid[(data_covid['Date']).dt.date == tanggalTerpilih]

tanggalTerpilih = (tanggalTerpilih[0]), (tanggalTerpilih[1])

dataTerpilih = data_covid[(data_covid['Date'] >= pd.to_datetime(tanggalTerpilih[0])) & (data_covid['Date'] <= pd.to_datetime(tanggalTerpilih[1]))]

kasus = st.selectbox('Pilih Jenis Kasus', list(dataTerpilih[['New Cases', 'New Deaths', 'New Recovered','New Active Cases', 'Total Cases','Total Deaths', 'Total Recovered', 'Total Active Cases']]))


def format_tooltip(column):
    return f'@{column}'

p = figure(title=f'Jumlah {kasus} per Tanggal {tanggalTerpilih[0]} hingga {tanggalTerpilih[1]}', x_axis_type='datetime', 
           x_axis_label='Tanggal', y_axis_label='Jumlah Kasus', plot_width=800, plot_height=400)
source = ColumnDataSource(data=dataTerpilih)
p.line('Date', kasus, source=source, line_width=2)
p.yaxis.formatter = NumeralTickFormatter(format='0,0')

data_grouped = dataTerpilih.groupby('Province')[kasus].sum().reset_index()
prov = data_grouped['Province']
b = figure(title='', x_range=prov, plot_width=800, plot_height=500)
sc = ColumnDataSource(data=data_grouped)
b.vbar(x='Province', top=kasus, source=sc, width=0.9)
b.xaxis.major_label_orientation = "vertical"
b.yaxis.formatter = NumeralTickFormatter(format='0,0')

selected_indices = []

def plot_tap_event(event):
    selected_index = event.index['1d']['indices'][0]
    if selected_index in selected_indices:
        selected_indices.remove(selected_index)
    else:
        selected_indices.append(selected_index)

p.on_event(Tap, plot_tap_event)
b.on_event(Tap, plot_tap_event)

hover1 = HoverTool(tooltips=[('Tanggal','@Date{%F}' ), (kasus,f'@{kasus}')],
                   formatters={'@Date': 'datetime'})
p.add_tools(hover1)

hover2 = HoverTool(tooltips=[(kasus, '@{kasus}'), ])
b.add_tools(hover2)

st.bokeh_chart(p, use_container_width=True)
st.bokeh_chart(b, use_container_width=True)

if selected_indices:
    data_terpilih = dataTerpilih.iloc[selected_indices]
    st.header('Data yang Dipilih')
    st.write(data_terpilih)
