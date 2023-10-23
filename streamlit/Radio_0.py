import time
import subprocess
import streamlit as st
from typing import List, Any


def parse_frequency_list(list_of_freq: List) -> str:
    """
    Take a list of frequencies and return a formatted string
    :param list_of_freq:
    :return: string with formatted frequencies
    """
    formatted_string = ''

    for freq in list_of_freq:
        if ':' in freq:
            return f'-f {freq} '
        formatted_string += f'-f {freq}M '

    return formatted_string


st.set_page_config(
    page_title='SDR',
    page_icon=':signal_strength:',
)

st.title("Radio 0")

tuner, presets = st.tabs(['Config', 'Presets'])

with tuner:
    col1, col2 = st.columns(2)

    with col1:

        with st.status("Radio 0 status", expanded=True):
            check = st.button("Check")
            if check:
                output = subprocess.run(
                    "ps -ef | grep rtl-fm | grep -e '-d 0' | grep -v grep | cut -d ' ' -f 21- | cut -d/ -f 6-",
                    capture_output=True,
                    text=True,
                    shell=True
                ).stdout
                if output:
                    st.info('Radio is running the following parameters:')
                    st.info(output)
                else:
                    st.info('Radio is not running')

        with st.form('frequency_selector'):
            st.write("### Frequency selector")

            frequencies = []
            output = st.text_input(
                label='Enter desired frequencies manually',
                placeholder='See Help for instructions',
                help=
                '''
                    - For single frequency enter 462.5625
                    - For scanning a range, enter 118M:137M:25k. Do not enter any other frequencies with the range.
                    - For scanning multiple frequencies enter frequencies separated by space
                '''
            )
            if output:
                for item in output.split(' '):
                    frequencies.append(item)
                frequencies = parse_frequency_list(frequencies)

            output = st.multiselect(
                "Ham Calling Frequencies",
                ('146.520', '446.000'),
                help=
                '''
                    - 2 meter - 146.520
                    - 70 cm - 446.000
                '''
            )
            if output:
                frequencies = parse_frequency_list(output)

            output = st.multiselect(
                "NOAA Weather Radio",
                ('162.400', '162.425', '162.450', '162.475', '162.500', '162.525', '162.550'),
                help=
                '''
                    - For state specific frequencies and other information check https://www.weather.gov/nwr/station_listing
                '''
            )
            if output:
                frequencies = parse_frequency_list(output)

            output = st.multiselect(
                "FRS/GMRS",
                ('462.5625M:462.7250M:25K', '462.5625', '462.5875', '462.6125', '462.6375', '462.6625', '462.6875',
                 '462.7125', '467.5625', '467.5875', '467.6125', '467.6375', '467.6625', '467.6875', '467.7125',
                 '462.5500', '462.5750', '462.6000', '462.6250', '462.6500', '462.6750', '462.7000', '462.7250'),
                help=
                '''
                    - Scan all channels 462.5625M:462.7250M:25K. Do not select any other frequencies with the range.
                    -	1	 - 	462.5625 
                    -	2	 - 	462.5875 
                    -	3	 - 	462.6125 
                    -	4	 - 	462.6375 
                    -	5	 - 	462.6625 
                    -	6	 - 	462.6875 
                    -	7	 - 	462.7125 
                    -	8	 - 	467.5625 
                    -	9	 - 	467.5875 
                    -	10	 - 	467.6125 
                    -	11	 - 	467.6375 
                    -	12	 - 	467.6625 
                    -	13	 - 	467.6875 
                    -	14	 - 	467.7125 
                    -	15	 - 	462.5500 
                    -	16	 - 	462.5750 
                    -	17	 - 	462.6000 
                    -	18	 - 	462.6250 
                    -	19	 - 	462.6500 
                    -	20	 - 	462.6750 
                    -	21	 - 	462.7000 
                    -	22	 - 	462.7250 
                '''
            )
            if output:
                frequencies = parse_frequency_list(output)

            modulation = st.selectbox(
                'Select modulation',
                ('fm', 'am', 'wbfm', 'raw', 'usb', 'lsb')
            )

            sample_rate = st.selectbox(
                'Select sample rate',
                ('180k', '48k', '30k', '24k', '20k', '16k', '12k', '8k')
            )

            playback_sample_rate = st.selectbox(
                'Select playback sample rate',
                ('180k', '48k', '30k', '24k', '20k', '16k', '12k', '8k')
            )

            tuner_gain = st.selectbox(
                'Select tuner gain.',
                (
                 '0', '0.9', '1.4', '2.7', '3.7', '7.7', '8.7', '12.5', '14.4', '15.7',
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

            st.markdown(
                '### Actions',
                help=
                '''
                    - play to the local sound card
                    - stream to network on port 8080
                    - sound activated recording to a file (must enter a file name below)
                    - play to the local sound card and sound activated recording to a file (must enter a file name below
                '''
            )

            action = st.radio(
                'actions',
                ('play', 'stream', 'sar', 'play-sar'),
                horizontal=True,
                label_visibility='collapsed'
            )

            filename = st.text_input(
                'File name',
                placeholder='File name without extension'
            )

            st.markdown('### Options')

            deinvert = st.checkbox('deinvert')

            preset = st.slider(
                'Select deinvert preset',
                min_value=1,
                max_value=8,
                step=1
            )

            tuner_start_button = st.form_submit_button('Start')

            if tuner_start_button:
                if frequencies:
                    st.info(frequencies)
                else:
                    st.warning("Please enter frequency", icon="⚠️")
                    st.stop()

                if 'sar' in action:
                    if not filename:
                        st.warning("File name required", icon="⚠️")
                        st.stop()
                else:
                    filename = ''

                if 'play-sar' in action:
                    if not filename:
                        st.warning("File name required", icon="⚠️")
                        st.stop()
                else:
                    filename = ''

                if deinvert:
                    deinvert = f'--deinvert {preset}'
                else:
                    deinvert = ''

                rtl_fm_command = \
                    f'nohup \
                    /home/rlevit/.local/bin/rtl-fm {frequencies}  \
                    -M {modulation}  \
                    -s {sample_rate}  \
                    -r {playback_sample_rate} \
                    -d 0  \
                    -g {tuner_gain} \
                    -l {squelch}  \
                    -p {ppm_error}  \
                    --{action} {filename}  \
                    {deinvert} &'

                st.write(':red[Executing:]', rtl_fm_command)

                subprocess.run(
                    '/home/rlevit/.local/bin/rtl-fm-stop 0',
                    capture_output=False,
                    shell=True
                )
                subprocess.run(
                    rtl_fm_command,
                    capture_output=False,
                    shell=True
                )


        with st.form("execution_control"):
            stop = st.form_submit_button(label='Stop')
            if stop:
                result = subprocess.run(
                    '/home/rlevit/.local/bin/rtl-fm-stop 0',
                    capture_output=True,
                    text=True,
                    shell=True
                ).stdout
                st.write(result)

with presets:
    st.header('Presets')

    with st.status("Radio 0 status", expanded=True):
        check = st.button("Check state")
        if check:
            output = subprocess.run(
                "ps -ef | grep rtl-fm | grep -e '-d 0' | grep -v grep | cut -d ' ' -f 21- | cut -d/ -f 6-",
                capture_output=True,
                text=True,
                shell=True
            ).stdout
            if output:
                st.info('Radio is running the following parameters:')
                st.info(output)
            else:
                st.info('Radio is not running')
