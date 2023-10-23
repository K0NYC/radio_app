import streamlit as st
import subprocess

st.set_page_config(
    page_title='Bluetooth',
    page_icon=':signal_strength:',
)

with st.expander('AKG Headphones control', expanded=True):
    if st.button('Info', key='headphones'):
        output = subprocess.run(['bluetoothctl', 'info', '78:5E:A2:24:99:93'], capture_output=True, text=True).stdout
        for line in output.split('\n'):
            line

    if st.button('Connect headphones'):
        output = subprocess.run(['bluetoothctl', 'connect', '78:5E:A2:24:99:93'], capture_output=True, text=True).stdout
        for line in output.split('\n'):
            line

    if st.button('Disonnect headphones'):
        output = subprocess.run(['bluetoothctl', 'disconnect', '78:5E:A2:24:99:93'], capture_output=True, text=True).stdout
        for line in output.split('\n'):
            line

with st.expander("JBL speaker control", expanded=True):
    if st.button('Info', key='speaker'):
        output = subprocess.run(['bluetoothctl', 'info', '5C:FB:7C:BF:E0:97'], capture_output=True, text=True).stdout
        for line in output.split('\n'):
            line

    if st.button('Connect speaker'):
        output = subprocess.run(['bluetoothctl', 'connect', '5C:FB:7C:BF:E0:97'], capture_output=True, text=True).stdout
        for line in output.split('\n'):
            line

    if st.button('Disonnect speaker'):
        output = subprocess.run(['bluetoothctl', 'disconnect', '5C:FB:7C:BF:E0:97'], capture_output=True, text=True).stdout
        for line in output.split('\n'):
            line
