import streamlit as st
import requests
from datetime import datetime
import toml

# Load config
config = toml.load("config.toml")
url = config["webhook"]["url"]

# ... rest of your code ...


# Page configuration
st.set_page_config(
    page_title="HDB AI Agent",
    page_icon="🏠",
    layout="centered",
    initial_sidebar_state="expanded"
)

def load_css():
    # Custom CSS for better styling
    st.markdown("""
    <style>
        .main-header {
            font-size: 2.5rem;
            font-weight: bold;
            color: #1f77b4;
            text-align: center;
            margin-bottom: 2rem;
        }

        .sidebar-info {
            background-color: #f8f9fa;
            padding: 1rem;
            border-radius: 5px;
            margin-bottom: 1rem;
        }

        .sidebar-title {
            font-size: 1.5rem;
            font-weight: bold;
            color: #1f77b4;
            margin-bottom: 1rem;
            text-align: center;
        }

    </style>
    """, unsafe_allow_html=True)



def display_chat_history():
    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message['role']):
            st.markdown(f"{message['content']}\n\n*{message['timestamp']}*")

def main():
    # Main app
    load_css()
    st.markdown('<h1 class="main-header">🏠 HDB AI Agent</h1>', unsafe_allow_html=True)
    st.divider()


    # Examples questions
    st.markdown("#### 💡 Example Questions You Can Ask:")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        - What requirements must be met to purchase an HDB flat?
        - What is the application process for a resale HDB flat?
        - How does the HDB resale procedure work?
        """)

    with col2:
        st.markdown("""
        - What loan options does HDB offer?
        - What is the HDB Loan-to-Value ratio?
        - Send the previous chat message to ("your email address") via email.
        """)

    st.divider()

    #with st.chat_message("ai"):
    #    st.write("Hello! I am your HDB AI Agent 👋")

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    display_chat_history()

    prompt = st.chat_input("What's up?")

    if prompt:
        # Define timestamp for messages
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with st.chat_message("user"):
            st.write(f"{prompt}\n\n*{timestamp}*")

        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt, "timestamp": timestamp})

        try:
            response = requests.post(url, data={"chat_input": prompt})

            with st.chat_message("ai"):
                st.write(f"{response.text}\n\n*{timestamp}*")

            # Add ai response to chat history
            st.session_state.messages.append({"role": "ai", "content": response.text, "timestamp": timestamp})

        except requests.Timeout:
            st.error("The request timed out. Please try again.")
        except requests.ConnectionError:
            st.error("Failed to connect to the server. Check your internet connection.")
        except requests.HTTPError:
            st.error("An HTTP error occurred. Please check the request and try again.")
        except requests.RequestException as e:
            st.error(f"An error occurred: {str(e)}")


    if st.button("Clear Chat History"):
        st.session_state.messages = []
        if hasattr(st, "experimental_rerun"):
            st.experimental_rerun()
        else:
            st.rerun()

    # Sidebar configuration
    with st.sidebar:
        st.markdown('<h2 class="sidebar-title">ℹ️ About HDB AI AGENT</h2>', unsafe_allow_html=True)

        # Information section
        st.markdown("""
        <div class="sidebar-info">
        <p>This is an AI-driven retrieval-augmented generation (RAG) chatbot designed to assist with:</p>
        <ul>
            <li>Information on purchasing and selling HDB resale flats</li>
            <li>Details about HDB financing options</li>
            <li>CPF loan eligibility and requirements</li>
            <li>General HDB housing inquiries</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

        # Footer
        st.markdown("---")
        st.markdown("""
        <div style="text-align: center; color: #666; font-size: 0.9rem;">
            <p>HDB AI Agent powered by n8n workflow | Made with Streamlit</p>
            <p>For the most accurate and up-to-date information, please visit the official HDB website.</p>
        </div>
        """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
