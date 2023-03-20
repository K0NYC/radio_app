import streamlit as st
import subprocess

st.set_page_config(
    page_title='SDR',
    page_icon=':signal_strength:',
)

st.title("Radio 1")

tuner, frequency_reference = st.tabs(['Tuner', 'Frequency Reference'])

with tuner:
    with st.container():
        st.write("### Frequency selector")

        frequency = st.text_input(
            label='Enter desired manual_frequencies. \
            - Ex 462.5625M, \
            - for scanning enter 118M:137M:25k',
            placeholder='Enter desired manual_frequencies'
        )

    with st.form('radio_config'):
        st.write('### Select tuner parameters')

        modulation = st.selectbox(
            'Select modulation',
            ('fm', 'am', 'wbfm', 'raw', 'usb', 'lsb')
        )

        sample_rate = st.selectbox(
            'Select sample rate',
            ('30k', '24k', '20k', '16k', '8k')
        )

        tuner_gain = st.selectbox(
            'Select tuner gain. 0 = auto',
            (
                '0.0', '0.9', '1.4', '2.7', '3.7', '7.7', '8.7', '12.5', '14.4', '15.7',
                '16.6', '19.7', '20.7', '22.9', '25.4', '28.0', '29.7', '32.8', '33.8', '36.4',
                '37.2', '38.6', '40.2', '42.1', '43.4', '43.9', '44.5', '48.0', '49.6'
            )
        )

        squelch = st.slider(
            'Select squelch level. 0 = auto',
            min_value=0,
            max_value=150,
            step=1
        )

        ppm_error = st.slider(
            'Select ppm error correction',
            min_value=0,
            max_value=50,
            step=1
        )

        st.markdown('### Select actions')

        action = st.radio(
            'Select an action: play to the local sound card, \
            stream to network on port 8080, \
            sound activated recording to a file (must enter a file name below)',
            ('play',
             'stream',
             'sar',
             'play-sar'),
            horizontal=True
        )

        filename = st.text_input(
            'File name',
            placeholder='File name without extension'
        )

        st.markdown('### Advanced options')

        deinvert = st.checkbox(
            'deinvert'
        )

        preset = st.slider(
            'Select deinvert preset',
            min_value=1,
            max_value=8,
            step=1
        )

        submitted = st.form_submit_button('Start')

        if submitted:
            if not frequency:
                st.warning("Please enter manual_frequencies", icon="⚠️")
                st.stop()

            if 'sar' in action:
                if not filename:
                    st.warning("File name required", icon="⚠️")
                    st.stop()
            else:
                filename = ''

            if deinvert:
                deinvert = f'--deinvert {preset}'
            else:
                deinvert = ''

            command = f'rtl_fm -f {frequency} ' \
                      f'-M {modulation} ' \
                      f'-s {sample_rate} ' \
                      f'-d 0' \
                      f'-g {tuner_gain} ' \
                      f'-l {squelch} ' \
                      f'-p {ppm_error} ' \
                      f' --{action} {filename}' \
                      f' {deinvert}'
            # p = subprocess.Popen('rtl-fm-stop')
            # p = subprocess.Popen(command)
            st.write(':red[Executing:]', command)

    with st.form("execution_control"):
        stop = st.form_submit_button(label='Stop')
        if stop:
            # p = subprocess.Popen('rtl-fm-stop')
            pass

with frequency_reference:
    st.header('Frequency Reference')

