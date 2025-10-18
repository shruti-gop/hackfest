import streamlit as st
from openai import OpenAI

# Show title and description.
st.title("💬 Chatbot")
st.write(
    "This is a simple chatbot that uses OpenAI's GPT-3.5 model to generate responses. "
    "To use this app, you need to provide an OpenAI API key, which you can get [here](https://platform.openai.com/account/api-keys). "
    "You can also learn how to build this app step by step by [following our tutorial](https://docs.streamlit.io/develop/tutorials/llms/build-conversational-apps)."
)

# Ask user for their OpenAI API key via `st.text_input`.
# Alternatively, you can store the API key in `./.streamlit/secrets.toml` and access it
# via `st.secrets`, see https://docs.streamlit.io/develop/concepts/connections/secrets-management
openai_api_key = st.text_input("OpenAI API Key", type="password")
if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
else:

    # Create an OpenAI client.
    client = OpenAI(api_key=openai_api_key)

    # Create a session state variable to store the chat messages. This ensures that the
    # messages persist across reruns.
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display the existing chat messages via `st.chat_message`.
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Create a chat input field to allow the user to enter a message. This will display
    # automatically at the bottom of the page.
    if prompt := st.chat_input("What is up?"):

        # Store and display the current prompt.
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate a response using the OpenAI API.
        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )

        # Stream the response to the chat using `st.write_stream`, then store it in 
        # session state.
        with st.chat_message("assistant"):
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})

import streamlit as st
from openai import OpenAI

client = OpenAI(api_key="YOUR_KEY")

st.title("HepAware: Hepatitis B Awareness Copilot")

tab1, tab2, tab3 = st.tabs(["💬 Ask", "🚫 Myths", "📣 Post Generator"])

# --- Chat Tab ---
with tab1:
    q = st.text_input("Ask about Hepatitis B:")
    if q:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a public health educator about Hepatitis B."},
                {"role": "user", "content": q}
            ]
        )
        st.write(response.choices[0].message.content)

# --- Myth-Buster Tab ---
with tab2:
    myths = {
        "Only drug users get Hepatitis B":
            "False — Hep B can spread through birth, sexual contact, or unsterile medical tools.",
        "You can’t get Hepatitis B vaccine as an adult":
            "Adults can absolutely get vaccinated — it's safe and effective at any age."
    }
    choice = st.selectbox("Choose a myth:", list(myths.keys()))
    st.write(myths[choice])

# --- Awareness Post Generator ---
with tab3:
    audience = st.text_input("Who is this post for?")
    tone = st.selectbox("Tone", ["Friendly", "Educational", "Urgent"])
    if st.button("Generate Post"):
        prompt = f"Write a {tone.lower()} social media post to raise Hepatitis B awareness for {audience}."
        post = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        st.success(post.choices[0].message.content)
