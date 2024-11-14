import streamlit as st #Avisamos del uso de libreria
from groq import Groq #Importamos la libreria

#Configuración de la venntana de la web
st.set_page_config(page_title='Mi chat de IA', page_icon='🤖') #Window + punto se ponen inconos
MODELOS = ['llama3-8b-8192', 'llama 70b-8192', 'mixtral-8x7b-32768']
#Nos conectamos con la API, creando un usuario
def crear_usuario_groq():
    #Obtenemos la clave API
    clave_secreta = st.secrets['CLAVE_API']
    return Groq(api_key = clave_secreta) #Conectamos a la API

#Seleccionamos el modelo de la IA
def configurar_modelo(cliente, modelo, mensajeDeEntrada):
    return cliente.chat.completions.create(
        model = modelo, #Selección el modelo IA
        messages = [{'role':'user', 'content' : mensajeDeEntrada}],
        stream = True #Funcionalidad para IA, responde a tiempo real
    ) #Devuelve la respuesta que manda la IA

#Historial del mensaje
def inicializar_estado():
    #Si no existe 'mensajes' entonces creamos un historial
    if 'mensajes' not in st.session_state:
        st.session_state.mensajes = [] #Historial vacío

def configurar_pagina():
    st.title('Mi chat de IA') #Titulo
    st.sidebar.title('Configuración') #Titulo
    opcion = st.sidebar.selectbox(
        'Elegí modelo', #Titulo
        options = MODELOS, #Opciones deben estar en una lista
        index = 0 #ValorPorDefecto
    )
    return opcion #! AGREGAMOS ESTO PARA OBTENER EL NOMBRE DEL MODELO

def actualizar_historial(rol, contenido, avatar):
    #El metodo append(dato) Agrega datos a la lista
    st.session_state.mensajes.append(
        {'role': rol, 'content': contenido, 'avatar': avatar}
    )

def mostrar_historial(): #Guarda la estructura visual del mensaje
    for mensaje in st.session_state.mensajes:
        with st.chat_message(mensaje['role'], avatar=mensaje['avatar']):
            st.markdown(mensaje['content'])

def area_chat():
    contenedorDelChat = st.container(height= 400, border= True)
    with contenedorDelChat : mostrar_historial()

#! NUEVA FUNCIÓN
def generar_respuesta(chat_completo):
    respuesta_completa = '' #Variable vacía
    for frase in chat_completo:
        if frase.choices[0].delta.content: #Evitamos el dato NONE
            respuesta_completa += frase.choices[0].delta.content
            yield frase.choices[0].delta.content
    
    return respuesta_completa

def main():
    #? INVOVACIÓN DE FUNCIONES
    modelo = configurar_pagina() #Agarramos el modelo seleccionado
    clienteUsuario = crear_usuario_groq() #Conecta con la API GROG
    inicializar_estado() #Se crea en memoria el historial vacío
    area_chat() #Se crea el contenedor de los mensajes
    mensaje = st.chat_input('Escribí un mensaje...')
    #! MODIFICAMOS EL CODIGO DEL IF
    if mensaje:
        actualizar_historial('user', mensaje, '🤩') #Mostramos el mensaje en el chat
        chat_completo = configurar_modelo(clienteUsuario, modelo, mensaje) #Obtenemos la respuesta de IA
        if chat_completo: #Verificamos que la variable tenga algo
            with st.chat_message('assistant') :
                respuesta_completa = st.write_stream(generar_respuesta(chat_completo))
                actualizar_historial('assistant', respuesta_completa, '🤖')
                st.rerun() #Actualizar
            
if __name__ == '__main__':
    main()