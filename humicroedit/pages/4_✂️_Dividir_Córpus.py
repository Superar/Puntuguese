import json
import random
from pathlib import Path

import numpy as np
import streamlit as st

if ('authentication_status' not in st.session_state or
        st.session_state['authentication_status'] is None or
        st.session_state['authentication_status'] is False):
    st.warning('Por favor, faça login')
elif (st.session_state['authentication_status'] is True and
      st.session_state['username'] not in st.session_state['config']['admins']):
    st.error('Sem permissão')
else:
    st.markdown('# ✂️ Dividir Córpus')

    if st.button('Começar'):
        preprocessed_data_path = Path('data/preprocessed_puns.json')
        split_files_path = Path('data/split_annotation')

        with st.spinner('Dividindo córpus...'):
            st.toast('Carregando dados pré-processados')
            with preprocessed_data_path.open(encoding='utf-8') as file_:
                preprocessed_data = json.load(file_)
            st.toast(f'Carregados {len(preprocessed_data)} trocadilhos')

            st.toast('Recolhendo ids para ignorar')
            ignore_ids = list()
            for filepath in split_files_path.iterdir():
                with filepath.open(encoding='utf-8') as file_:
                    ignore_ids.extend([x['id'] for x in json.load(file_)])
            st.toast(f'Ignorando {len(ignore_ids)} ids')

            st.toast(f'Dividindo córpus')
            for country in st.session_state['config']['countries']:
                sources = st.session_state['config']['sources'][country]
                country_puns = [x for x in preprocessed_data
                                if int(x['id'].split('.')[0]) in sources
                                and x['id'] not in ignore_ids]

                country_users = st.session_state['config']['countries'][country]
                random.shuffle(country_puns)
                split_data = np.array_split(country_puns, len(country_users))
                for i, user in enumerate(country_users):
                    user_filepath = Path(f'data/split_annotation/{user}.json')
                    if user_filepath.exists():
                        with user_filepath.open('r', encoding='utf-8') as file_:
                            user_data = json.load(file_)
                    else:
                        user_data = list()
                    with user_filepath.open('w', encoding='utf-8') as file_:
                        user_data.extend(split_data[i].tolist())
                        json.dump(user_data, file_,
                                  ensure_ascii=False, indent=4)
        st.success('Divisão finalizada!', icon='✅')
