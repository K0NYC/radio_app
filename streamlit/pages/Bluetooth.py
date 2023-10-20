import streamlit as st
import subprocess

st.title('Bluetooth')

if st.button('Connect headphones'):
    output = subprocess.run(['bluetoothctl', 'connect', '78:5E:A2:24:99:93'], capture_output=True, text=True).stdout
    for line in output.split('\n'):
        line

if st.button('Disonnect headphones'):
    output = subprocess.run(['bluetoothctl', 'disconnect', '78:5E:A2:24:99:93'], capture_output=True, text=True).stdout
    for line in output.split('\n'):
        line

if st.button('Info'):
    output = subprocess.run(['bluetoothctl', 'info', '78:5E:A2:24:99:93'], capture_output=True, text=True).stdout
    for line in output.split('\n'):
        line


