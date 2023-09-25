from pathlib import Path

import streamlit as st
import streamlit_authenticator as stauth
import yaml

# AUTHENTICATION
with Path('humicroedit/config.yaml').open() as file_:
    config = yaml.load(file_, Loader=yaml.loader.SafeLoader)
    st.session_state['config'] = config

authenticator = stauth.Authenticate(config['credentials'],
                                    config['cookie']['name'],
                                    config['cookie']['key'],
                                    config['cookie']['expiry_days'],
                                    config['preauthorized'])
name, authentication_status, username = authenticator.login('Fazer login',
                                                            'main')

if authentication_status:
    authenticator.logout('Terminar sessão', 'main')
    st.title('Nomicroedit')
    st.markdown(f'''
    Bem-vindo(a) *{name}*!

    Obrigado por ter aceitado em participar da criação deste córpus para o reconhecimento de Humor em Português. 🫰 O objetivo desse trabalho será em criar as instâncias negativas para o córpus, ou seja, os exemplos de textos que não são humor.

    A sua tarefa é bastante simples. No menu lateral (à esquerda), há uma página "Anotação do Córpus", em que você será apresentado um trocadilho por vez, a ideia é realizar uma edição mínima que faça o texto perder a sua graça. **Os tokens que podem ser editados estão marcados em verde.** Como a edição deve ser mínima, o ideal é que seja realizada **apenas uma edição**, mas caso não seja possível, mais edições são permitidas.

    Além disso, o site é responsível, então se quiser fazer pelo telefone também pode. :smile:
    ''')

    with st.expander(':orange[Exemplos de edição]', expanded=True):
        st.write('Original: Qual é a sobremesa mais popular na Rússia? O Putin flan.')
        st.write('Editada: Qual é a sobremesa mais popular na Rússia? O pudim flan.')
        st.divider()
        st.write('Original: Um parto não costuma demorar muito tempo. Mas para as grávidas parece maternidade.')
        st.write('Editada: Um parto não costuma demorar muito tempo. Mas para as grávidas parece uma eternidade.')
        st.divider()
        st.write('Original: Qual cantora superou seu deficit de atencao? Rita Li-na')
        st.write('Editada: Qual cantora superou seu deficit de atencao? Ana Carolina')
elif authentication_status == False:
    st.error('Usuário/senha incorreta')
