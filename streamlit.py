import streamlit as st
from main import *
import time

def display_latest_conversation():
    for message in st.session_state['latest_conversation']:
        if message['role'] == "user":
            st.chat_message("user").write(f"**You:** {message['message']}")
        elif message['role'] == "assistant":
            st.chat_message("assistant").write(f"**AI Assistant:** {message['message']}")

st.title("AI Search and Chat Assistant")

if 'latest_conversation' not in st.session_state:
    st.session_state['latest_conversation'] = []

query = st.text_input("You:", placeholder="Type a question...")

if st.button("Send"):
    
    if query:
        st.session_state['latest_conversation'] = []
        st.session_state['latest_conversation'].append({"role": "user", "message": query})
        display_latest_conversation()
        with st.spinner("Fetching web results..."):
            search_results = google_search(query, GOOGLE_API_KEY, GOOGLE_CSE_ID, num=5)

        if search_results:
            clean_results, clean_urls = clean_search_results(search_results)
            st.chat_message("system").write("Here are some relevant search results:")
            for idx, (result, url) in enumerate(zip(clean_results, clean_urls), 1):
                st.markdown(f"**[{idx}. {url.split('//')[1]}]({url})**")  
                st.write(f"{result}")  
                st.markdown("---")  

        
        with st.spinner("AI Assistant is thinking..."):
            st.session_state['latest_conversation'] = []
            context = prepare_context(clean_results)
            model_id = 'arn:aws:bedrock:us-west-2::foundation-model/meta.llama3-1-405b-instruct-v1:0'
            ai_response = invoke_llama_with_context(model_id, context, query)
            st.session_state['latest_conversation'].append({"role": "assistant", "message": ai_response})

    else:
        st.error("Please enter a question.")
display_latest_conversation()
