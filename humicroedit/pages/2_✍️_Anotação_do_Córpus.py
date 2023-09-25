import html
import json
from pathlib import Path
from typing import List

import streamlit as st
from htbuilder import H, styles
from htbuilder.units import unit
from st_click_detector import click_detector

div = H.div
span = H.span
a = H.a
px = unit.px
rem = unit.rem
em = unit.em

st.set_page_config(page_title='Anotação do Córpus',
                   page_icon='✍️')


def highlight_text(tokens: List[str],
                   edited_tokens: List[str]):
    out = div()

    for i, token in enumerate(edited_tokens):
        if token == tokens[i]:
            bg = '#21c354'
        elif token != tokens[i]:
            bg = '#c42121'

        token_text = token + ' ' if token else '[REMOVIDO] '

        out(
            span(
                style=styles(
                    background=bg,
                    border_radius=rem(0.33),
                    padding=(rem(0.125), rem(0.5)),
                    overflow='hidden'
                )
            )
            (
                a(href='#', id=i, style=styles(color='white'))(
                    html.escape(token_text)
                )
            )
        )
    return str(out)


if ('authentication_status' not in st.session_state or
        st.session_state['authentication_status'] is None or
        st.session_state['authentication_status'] is False):
    st.warning('Por favor, faça login')
else:
    split_files_path = Path('data/split_annotation')
    filename = split_files_path / st.session_state['username']
    filename = filename.with_suffix('.json')

    if 'data' not in st.session_state:
        with filename.open('r', encoding='utf-8') as file_:
            st.session_state['data'] = json.load(file_)

    data = st.session_state['data']
    if 'current_pun_idx' not in st.session_state:
        st.session_state['current_pun_idx'] = 0

    # Pagination
    with st.container():
        _, col2, _ = st.columns(3)
        with col2:
            input_idx = st.number_input('Ir para texto', min_value=1,
                                        max_value=len(data))
            st.session_state['current_pun_idx'] = input_idx - 1

    current_pun = data[st.session_state['current_pun_idx']]

    # Edition progress
    progress_count = 0
    for pun in data:
        if pun['tokens'] != pun['edited tokens']:
            progress_count += 1
    st.progress(progress_count / len(data),
                text=f'Editadas: {progress_count}/{len(data)}')

    # Show original pun
    st.header(f'Texto original')
    st.write(current_pun['text'])

    # Show text
    st.header('Texto editado')
    content = highlight_text(current_pun['tokens'],
                             current_pun['edited tokens'])
                             
    clicked = click_detector(content)

    # Show editting interface
    if 'edited' not in st.session_state:
        st.session_state['edited'] = False
    if clicked != '':
        def edit_callback():
            new_token = st.session_state['new_token']
            current_pun['edited tokens'][int(clicked)] = new_token
            st.session_state['edited'] = True
        new_token = st.text_input('New token',
                                  current_pun['edited tokens'][int(clicked)],
                                  key='new_token',
                                  on_change=edit_callback)

    if st.session_state['edited']:
        st.toast('Salvando arquivo...')
        with filename.open('w', encoding='utf-8') as file_:
            json.dump(data, file_,
                      ensure_ascii=False,
                      indent=4)
        st.toast(f'Salvo!')
        st.session_state['edited'] = False

    # Show instructions
    with st.expander(':orange[Lembre-se!]', expanded=True):
        st.markdown('''
        - Faça o mínimo de edições possíveis (de preferência uma)
        - O texto novo ainda deve fazer sentido
        - O texto novo deve ser sem graça
        - Foque a edição em palavras de classes abertas (substantivos, adjetivos, verbos e advérbios)
        - Edite outros tipos de tokens para garantir a gramaticalidade do texto
        ''')
