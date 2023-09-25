import json
import streamlit as st
from pathlib import Path

st.set_page_config(page_title='Acompanhar Anotação',
                   page_icon='🔎')

if ('authentication_status' not in st.session_state or
        st.session_state['authentication_status'] is None or
        st.session_state['authentication_status'] is False):
    st.warning('Por favor, faça login')
elif (st.session_state['authentication_status'] is True and
      st.session_state['username'] not in st.session_state['config']['admins']):
    st.error('Sem permissão')
else:
    st.markdown('# 🔎 Acompanhar Anotação')

    split_files_path = Path('data/split_annotation')
    countries = st.session_state['config']['countries']
    cols = st.columns(len(countries))

    for i, country in enumerate(countries):
        # Load data from the country
        country_progress = list()
        for annotator in countries[country]:
            filepath = (split_files_path / annotator).with_suffix('.json')
            with filepath.open('r', encoding='utf-8') as file_:
                data = json.load(file_)
            progress_count = 0
            for pun in data:
                if pun['tokens'] != pun['edited tokens']:
                    progress_count += 1
            country_progress.append((annotator, progress_count, len(data)))

        # Write sorted progress
        country_progress = sorted(country_progress,
                                  key=lambda x: x[1]/x[2],
                                  reverse=True)
        with cols[i]:
            st.markdown(f'## {country.capitalize()}')
            for progress in country_progress:
                st.progress(progress[1] / progress[2],
                            text=f'{progress[0]}: {progress[1]}/{progress[2]}')
