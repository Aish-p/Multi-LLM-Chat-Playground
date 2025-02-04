import streamlit as st
from litellm import completion

st.set_page_config(layout="wide")

st.title("Multi-LLM Chat Playground")

# Get API keys from the user
openai_api_key = st.text_input("Enter your OpenAI API Key:", type="password")
anthropic_api_key = st.text_input("Enter your Anthropic API Key:", type="password")
cohere_api_key = st.text_input("Enter your Cohere API Key:", type="password")

# Check if all API keys are provided
if openai_api_key and anthropic_api_key and cohere_api_key:

    system_prompt = st.text_area(
        "💡 Test your custom prompts (e.g., 'You are a creative writing assistant who writes in a poetic style.')",
        value="You are a helpful AI assistant that provides clear and concise responses."
    )
    if not system_prompt.strip():
        system_prompt = "You are a helpful AI assistant that provides clear and concise responses."

    def get_llm_response(model_name, api_key, user_input):
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ]
        try:
            response = completion(model=model_name, messages=messages, api_key=api_key)
            return response.choices[0].message.content
        except Exception as e:
            return f"Error: {str(e)}"

    user_input = st.text_area("💬 Enter your message:", height=68)

    if st.button("Send to All LLMs"):
        if user_input:
            st.subheader("Responses from LLMs")
            
            # Create three columns for side-by-side display
            col1, col2, col3 = st.columns(3)
            
            # GPT-4o response
            with col1:
                st.subheader("GPT-4o")
                try:
                    gpt_response = get_llm_response("gpt-4o", openai_api_key, user_input)
                    st.write(gpt_response)
                except Exception as e:
                    st.error(f"Error with GPT-4o: {str(e)}")
            
            # Claude-3-sonnet response
            with col2:
                st.subheader("Claude 3.5 Sonnet")
                try:
                    claude_response = get_llm_response("claude-3-5-sonnet-20240620", anthropic_api_key, user_input)
                    st.write(claude_response)
                except Exception as e:
                    st.error(f"Error with Claude 3.5 Sonnet: {str(e)}")
            
            # Cohere response
            with col3:
                st.subheader("Cohere")
                try:
                    cohere_response = get_llm_response("command-r-plus", cohere_api_key, user_input)
                    st.write(cohere_response)
                except Exception as e:
                    st.error(f"Error with Cohere: {str(e)}")
        else:
            st.warning("Please enter a message.")
else:
    st.warning("Please enter all API keys to use the chat.")

st.sidebar.title("About this app")

st.sidebar.write(
    "This app compares responses from multiple Large Language Models (LLMs) "
    "using the LiteLLM library."
)

st.sidebar.subheader("Key features:")
st.sidebar.markdown(
    """
    - Uses **GPT-4o**, **Claude 3.5 Sonnet**, and **Cohere Command R Plus**
    - Allows users to test **custom prompts**
    - Sends the same user input to all models
    - Displays responses **side by side for easy comparison**
    - Helps analyze how different LLMs behave based on varied prompts
    """
)

st.sidebar.write(
    "💡 Try different prompts and see how LLM responses change!"
)
