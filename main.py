import streamlit as st
import time
from bot import main

st.set_page_config(page_title="SMS", layout="wide")

months = [
    'Selecione um mês',
    1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12
]
years = [
    'Selecione um ano',
    1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000,
    2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011,
    2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022,
    2023, 2024, 2025, 2026
]

st.subheader('Consulta ponto digital SMS')

with st.form(key='Consulta do ponto eletrônico - SMS', clear_on_submit=False):
    cpf = st.text_input(label='CPF', placeholder='Informe o CPF (ex: 100.200.300-40)')

    a, b = st.columns(2)

    month_start = a.selectbox(label='Mês inicial', options=months)
    year_start = b.selectbox('Ano inicial', years)
    month_end = a.selectbox('Mês final', months)
    year_end = b.selectbox('Ano final', years)

    btn_submit = st.form_submit_button('Consultar')

if btn_submit:
    if not cpf:
        st.warning('Informe o CPF com pontos e traço', icon='⚠️')
        st.stop()

    if month_start == 'Selecione um mês':
        st.warning('Selecione o mês de início', icon='⚠️')
        st.stop()

    if year_start == 'Selecione um ano':
        st.warning('Selecione o ano de início', icon='⚠️')
        st.stop()

    if month_end == 'Selecione um mês':
        st.warning('Selecione o mês de término', icon='⚠️')
        st.stop()

    if year_end == 'Selecione um ano':
        st.warning('Selecione o ano de término', icon='⚠️')
        st.stop()

    st.success('Dados enviados. Aguarde o processamento!', icon='✅')

    try:
        main(cpf, month_start, year_start, month_end, year_end)
        st.success('Arquivo gerado com sucesso!', icon='✅')
    except:
        st.error('Ocorreu um erro ao consultar o processamento!', icon='🚨')
