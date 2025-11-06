import streamlit as st 
from langchain_core.messages import HumanMessage
from backend import workflow  # Not number at starting
user_input= st.chat_input('What you want to explore today ?')
CONFIG= {'configurable': {'thread_id': '1'}}


# This list will not refresh when user Press Enter in Chat_input

if 'message_history' not in st.session_state:
    st.session_state['message_history'] = [] # Normal list also get refreshed each time 

for message in st.session_state['message_history']:
    with st.chat_message(message['By']):
        st.text(message['content'])
        

# First Time Response Generation
if user_input:
    st.session_state['message_history'].append({'By':'user', 'content':user_input})
    with st.chat_message('user'):
        st.text(user_input)
    
    initial_graphs= {'messages': [HumanMessage(content= user_input)]}
    final_graph= workflow.invoke(initial_graphs , config= CONFIG)
    ai_message= final_graph['messages'][-1].content
    st.session_state['message_history'].append({'By':'assistant', 'content': ai_message})
    with st.chat_message('assistant'):
        st.text(ai_message)
        

