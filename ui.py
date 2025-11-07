import streamlit as st 
from backend import workflow  # This is our backend code
from langchain_core.messages import HumanMessage
import uuid


user= st.chat_input('Ask Question')

# -------------------------------------------------------------Utility Function----------------------------------------------
def generating():
    unique_id= uuid.uuid4()
    return unique_id

def button():
    thread_id= generating()
    st.session_state['messages']=[]
    st.session_state['all_thread_ids'].append(thread_id)

def developing_connects(thread_id):
    thread= workflow.get_state(config= {'configurable': {'thread_id': thread_id }})
    return thread.values.get('messages', [])

#------------------------------------------------------------Session_State-s=================================================

if 'threads_id' not in st.session_state: ######################## Percesting threads id (single time)
    st.session_state['threads_id']= generating()


if 'messages' not in st.session_state:  ################## For Messages Percesting
    st.session_state['messages']=[]


if 'all_thread_ids' not in st.session_state:
    st.session_state['all_thread_ids']= []

# Collecting threading ids from two places 
if st.session_state['threads_id'] not in st.session_state['all_thread_ids']:
    st.session_state['all_thread_ids'].append(st.session_state['threads_id'])


for msg in st.session_state['messages']:
    with st.chat_message(msg['role']):
        st.text(msg['content'])
#-------------------------------------------------------- SideBar Streamlet -------------------------------------------------
st.sidebar.title('Chat with LLM')
st.sidebar.header('Chat History')

if st.sidebar.button('Add Chats'):
    button()

# This may disturb the flow of streamlit but it is necessary
for threads in st.session_state['all_thread_ids'][::-1]: 
    if st.sidebar.button(str(threads)):
        same_datastructure= []
        st.session_state['threads_id']= threads

        generated_data= developing_connects(threads)
        for data in generated_data:
            if  isinstance(data , HumanMessage):
                role= 'user'
            else:
                role= 'assistant'
            same_datastructure.append({'role': role , 'content':data.content})
        st.session_state['messages']= same_datastructure
#-------------------------------------------------- Generating Part ---------------------------------------------------------
CONFIG= {'configurable': {'thread_id': st.session_state['threads_id'] }}  ########### Config with thread_id (single for one)

if user:
    st.session_state['messages'].append({'role': 'user', 'content': HumanMessage(content= user)})
    with st.chat_message('user'):
        st.text(user)

    
    with st.chat_message('assistant'):
        ai_message= st.write_stream(chunk.content for chunk , metadata in workflow.stream({'messages': [HumanMessage(content= user)]},config=CONFIG , stream_mode= 'messages'))

    st.session_state['messages'].append({'role': 'assistant', 'content': ai_message})