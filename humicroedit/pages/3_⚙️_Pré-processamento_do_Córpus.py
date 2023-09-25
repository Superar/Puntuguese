import json
import re
from pathlib import Path

import spacy
import streamlit as st

st.set_page_config(page_title='Pré-processamento do Córpus',
                   page_icon='⚙️')


def merge_data(data):
    for pun in data:
        merged_ner, merged_pos = (pun['ner'].copy(),
                                  pun['pos'].copy())
        merged_tokens, merged_spans = (pun['tokens'].copy(),
                                       pun['token_idx'].copy())

        # Merge NEs
        for i in range(len(pun['tokens'])-1, 0, -1):
            if pun['ner'][i].endswith('I'):
                merged_ner[i-1] = 'MERGED'
                merged_ner.pop(i)
                merged_pos[i-1] = 'NE'
                merged_pos.pop(i)
                merged_tokens[i-1] = merged_tokens[i-1] + \
                    ' ' + merged_tokens[i]
                merged_tokens.pop(i)
                merged_spans.pop(i)

        # Merge pun signs
        for sign in pun['signs']:
            matches = re.finditer(sign['pun sign'], pun['text'], re.I)
            for match in reversed(list(matches)):
                start, end = match.span()
                for i in range(len(merged_tokens)-1, 0, -1):
                    if merged_spans[i] > start and merged_spans[i] < end:
                        merged_ner[i-1] = 'MERGED'
                        merged_ner.pop(i)
                        merged_pos[i-1] = 'PUN'
                        merged_pos.pop(i)
                        merged_tokens[i-1] = merged_tokens[i-1] + \
                            ' ' + merged_tokens[i]
                        merged_tokens.pop(i)
                        merged_spans.pop(i)

        pun['ner'], pun['pos'] = (merged_ner,
                                  merged_pos)
        pun['tokens'], pun['token_idx'] = (merged_tokens,
                                           merged_spans)

    return data


if ('authentication_status' not in st.session_state or
        st.session_state['authentication_status'] is None or
        st.session_state['authentication_status'] is False):
    st.warning('Por favor, faça login')
elif (st.session_state['authentication_status'] is True and
      st.session_state['username'] not in st.session_state['config']['admins']):
    st.error('Sem permissão')
else:
    st.markdown('# ⚙️ Pré-processamento do Córpus')
    if st.button('Começar'):
        datapath = Path('data/puns.json')
        split_files_path = Path('data/split_annotation')

        with st.spinner('Pré-processando'):
            st.toast('Carregando arquivo do córpus')
            with datapath.open(encoding='utf-8') as file_:
                data = json.load(file_)
            st.toast('Córpus carregado')

            st.toast('Recolhendo ids para ignorar')
            ignore_ids = list()
            for filepath in split_files_path.iterdir():
                with filepath.open(encoding='utf-8') as file_:
                    ignore_ids.extend([x['id'] for x in json.load(file_)])
            st.toast(f'Ignorando {len(ignore_ids)} ids')

            st.toast('Rodando pipeline do spacy')
            nlp = spacy.load('pt_core_news_sm')
            texts = [x['text'] for x in data if x['id'] not in ignore_ids]
            texts_ids = [x['id'] for x in data if x['id'] not in ignore_ids]
            texts_signs = [x['signs'] for x in data if x['id'] not in ignore_ids]

            preprocessed_data = list()
            for i, doc in enumerate(nlp.pipe(texts)):
                preprocessed_instance = {'id': texts_ids[i],
                                         'text': texts[i],
                                         'tokens': list(),
                                         'token_idx': list(),
                                         'pos': list(),
                                         'ner': list(),
                                         'signs': texts_signs[i]}
                for token in doc:
                    preprocessed_instance['tokens'].append(token.text)
                    preprocessed_instance['token_idx'].append(token.idx)
                    preprocessed_instance['pos'].append(token.pos_)
                    if token.ent_iob_ == 'O':
                        ner = token.ent_iob_
                    else:
                        ner = f'{token.ent_type_}-{token.ent_iob_}'
                    preprocessed_instance['ner'].append(ner)
                preprocessed_data.append(preprocessed_instance)

            st.toast('Fazendo merge das entidades e signos')
            preprocessed_data = merge_data(preprocessed_data)

            data_to_save = list()
            for x in preprocessed_data:
                data_to_save.append({
                    'id': x['id'],
                    'text': x['text'],
                    'tokens': x['tokens'],
                    'edited tokens': x['tokens']})

            st.toast('Salvando arquivo')
            path_to_save = Path('data/preprocessed_puns.json')
            with path_to_save.open('w', encoding='utf-8') as file_:
                json.dump(data_to_save, file_,
                          ensure_ascii=False, indent=4)
        st.success(f'Aquivo salvo em {path_to_save}', icon='✅')
