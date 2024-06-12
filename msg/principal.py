
import time

import streamlit as st

from utilidades import *

TEMPO_DE_RERUN = 3

# PÁGINAS =========================================

def pag_login():
    st.header('💬 Bem-vindo ao MSN Alfa', divider=True)
    tab1, tab2 = st.tabs(['Entrar', 'Cadastrar'])

    with tab1.form(key='login'):
        nome = st.text_input('Digite seu nome de usuario')
        senha = st.text_input('Digite sua senha')
        if st.form_submit_button('Entrar'):
            _login_usuario(nome, senha)
    
    with tab2.form(key='cadastro'):
        nome = st.text_input('Cadastre um novo nome de usuário')
        senha = st.text_input('Cadastre uma nova senha')
        if st.form_submit_button('Cadastrar'):
            _cadastrar_usuario(nome, senha) 

def _login_usuario(nome, senha):
    if validacao_de_senha(nome, senha):
        st.success('Login efetuado com sucesso')
        time.sleep(2)
        st.session_state['usuario_logado'] = nome.upper()
        mudar_pagina('chat')
        st.rerun()
    else:
        st.error('Dados inválidos, verifique sua senha ou cadastro')

def _cadastrar_usuario(nome, senha):
    if salvar_novo_usuario(nome, senha):
        st.success('Usuário cadastrado com sucesso')
        time.sleep(2)
        st.session_state['usuario_logado'] = nome.upper()
        mudar_pagina('chat')
        st.rerun()
    else:
        st.error('Erro ao cadastrar usuário')

def mudar_pagina(nome_pagina):
    st.session_state['pagina_atual'] = nome_pagina

def pagina_chat():
    st.title('💬 MSN ALFA')
    st.divider()

    usuario_logado = st.session_state['usuario_logado']
    conversando_com = st.session_state['conversando_com']
    mensagens = le_mensagens_armazendas(usuario_logado, conversando_com)

    container = st.container()
    for mensagem in mensagens:
        nome_usuario = 'user' if mensagem['nome_usuario'] == usuario_logado else mensagem['nome_usuario']
        avatar = None if mensagem['nome_usuario'] == usuario_logado else '😎'
        chat = container.chat_message(nome_usuario, avatar=avatar)
        chat.markdown(mensagem['conteudo'])
    
    nova_mensagem = st.chat_input('Digite uma mensagem')
    if nova_mensagem:
        if nova_mensagem != st.session_state['ultima_conversa_enviada']:
            st.session_state['ultima_conversa_enviada'] = nova_mensagem
            nova_dict_mensagem = {'nome_usuario': usuario_logado,
                                'conteudo': nova_mensagem}
            chat = container.chat_message('user')
            chat.markdown(nova_dict_mensagem['conteudo'])
            mensagens.append(nova_dict_mensagem)
            armazena_mensagens(usuario_logado, conversando_com, mensagens)

def inicializacao():
    if not 'pagina_atual' in st.session_state:
        mudar_pagina('login')
    if not 'usuario_logado' in st.session_state:
        st.session_state['usuario_logado'] = ''
    if not 'conversando_com' in st.session_state:
        st.session_state['conversando_com'] = ''
    if not 'ultima_conversa_enviada' in st.session_state:
        st.session_state['ultima_conversa_enviada'] = ''

def pagina_selecao_conversa(elemento):

    if not st.session_state['conversando_com'] == '':
        elemento.title(f"👋 Conversando com :blue[{st.session_state['conversando_com']}]")
        elemento.divider()
    usuarios = lista_usuarios()
    usuarios = [u for u in usuarios if u != st.session_state['usuario_logado']]
    conversando_com = elemento.selectbox('Selecione o usuário para conversar',
                                         usuarios)
    elemento.button('Iniciar conversa',
              on_click=_seleciona_conversa,
              args=(conversando_com, ))

def _seleciona_conversa(conversando_com):
    st.session_state['conversando_com'] = conversando_com
    st.success(f'Inciando conversa com {conversando_com}')
    time.sleep(1)
    mudar_pagina('chat')

def main():
    inicializacao()

    if st.session_state['pagina_atual'] == 'login':
        pag_login()
    elif st.session_state['pagina_atual'] == 'chat':
        if st.session_state['conversando_com'] == '':
            container = st.container()
            pagina_selecao_conversa(container)
        else:
            pagina_chat()
            container = st.sidebar.container()
            pagina_selecao_conversa(container)
            time.sleep(TEMPO_DE_RERUN)
            st.rerun()


if __name__ == '__main__':
    main()