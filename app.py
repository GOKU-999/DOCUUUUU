"""
DocuBot - AI Document Q&A Assistant
Main Streamlit application file
"""

import streamlit as st
import google.generativeai as genai
from utils.pdf_processor import extract_text_from_pdf, validate_pdf
import os
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="DocuBot - AI Document Q&A",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS with proper dark mode support
def load_css():
    """Load custom CSS styling with dark mode support"""
    st.markdown("""
    <style>
    /* Force dark mode background */
    .stApp {
        background-color: #0e1117 !important;
    }
    
    /* Main container */
    .main {
        padding: 0rem 1rem;
    }
    
    /* ALL text should be white in dark mode */
    .stMarkdown, .stMarkdown p, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, 
    .stMarkdown h4, .stMarkdown h5, .stMarkdown h6, .stMarkdown li, .stMarkdown span,
    .stAlert, .stAlert p, .stAlert div, .stAlert span,
    .stInfo, .stInfo p, .stInfo div,
    .stSuccess, .stSuccess p, .stSuccess div,
    .stWarning, .stWarning p, .stWarning div,
    .stError, .stError p, .stError div,
    .stCaption, .stCaption p,
    label, .stTextInput label, .stFileUploader label,
    .stChatMessage, .stChatMessage p, .stChatMessage div,
    [data-testid="stMarkdownContainer"] p,
    [data-testid="stMarkdownContainer"] div,
    .css-1d391kg, .css-1d391kg p, .css-1d391kg div,
    .sidebar .sidebar-content, .sidebar .sidebar-content p {
        color: #ffffff !important;
    }
    
    /* Chat messages */
    [data-testid="stChatMessage"] {
        background-color: #1e1e1e !important;
        border: 1px solid #333333 !important;
        border-radius: 0.5rem !important;
        padding: 1rem !important;
        margin-bottom: 0.5rem !important;
    }
    
    [data-testid="stChatMessage"][data-role="user"] {
        background-color: #2d2d2d !important;
        border-left: 3px solid #4CAF50 !important;
    }
    
    [data-testid="stChatMessage"][data-role="assistant"] {
        background-color: #1a1a1a !important;
        border-left: 3px solid #2196F3 !important;
    }
    
    [data-testid="stChatMessage"] p {
        color: #ffffff !important;
    }
    
    /* Sidebar */
    .stSidebar, .css-1d391kg {
        background-color: #0e1117 !important;
        border-right: 1px solid #333333 !important;
    }
    
    .stSidebar p, .stSidebar div, .stSidebar span, .stSidebar label {
        color: #ffffff !important;
    }
    
    /* Input fields */
    .stTextInput > div > div > input {
        background-color: #1e1e1e !important;
        color: #ffffff !important;
        border: 1px solid #444444 !important;
        border-radius: 0.5rem !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #4CAF50 !important;
        box-shadow: 0 0 0 2px rgba(76, 175, 80, 0.2) !important;
    }
    
    .stTextArea > div > div > textarea {
        background-color: #1e1e1e !important;
        color: #ffffff !important;
        border: 1px solid #444444 !important;
        border-radius: 0.5rem !important;
    }
    
    /* Buttons */
    .stButton > button {
        background-color: #2d2d2d !important;
        color: #ffffff !important;
        border: 1px solid #444444 !important;
        border-radius: 0.5rem !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button:hover {
        background-color: #3d3d3d !important;
        border-color: #666666 !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 8px rgba(0,0,0,0.3) !important;
    }
    
    /* Alerts - make text visible */
    .stAlert {
        background-color: #1e1e1e !important;
        border-color: #444444 !important;
        border-radius: 0.5rem !important;
        color: #ffffff !important;
    }
    
    .stAlert > div {
        color: #ffffff !important;
    }
    
    .stAlert p, .stAlert div, .stAlert span {
        color: #ffffff !important;
    }
    
    .stAlert[data-baseweb="notification"][kind="success"] {
        border-left: 4px solid #4CAF50 !important;
    }
    
    .stAlert[data-baseweb="notification"][kind="error"] {
        border-left: 4px solid #f44336 !important;
    }
    
    .stAlert[data-baseweb="notification"][kind="warning"] {
        border-left: 4px solid #ff9800 !important;
    }
    
    .stAlert[data-baseweb="notification"][kind="info"] {
        border-left: 4px solid #2196F3 !important;
    }
    
    /* File uploader */
    [data-testid="stFileUploader"] {
        background-color: #1e1e1e !important;
        border: 1px dashed #444444 !important;
        border-radius: 0.5rem !important;
        padding: 1rem !important;
        color: #ffffff !important;
    }
    
    [data-testid="stFileUploader"]:hover {
        border-color: #4CAF50 !important;
    }
    
    [data-testid="stFileUploader"] p, [data-testid="stFileUploader"] div {
        color: #ffffff !important;
    }
    
    /* Chat input */
    [data-testid="stChatInput"] > div > div > textarea {
        background-color: #1e1e1e !important;
        color: #ffffff !important;
        border: 1px solid #444444 !important;
        border-radius: 0.5rem !important;
    }
    
    [data-testid="stChatInput"] > div > div > textarea:focus {
        border-color: #4CAF50 !important;
        box-shadow: 0 0 0 2px rgba(76, 175, 80, 0.2) !important;
    }
    
    [data-testid="stChatInput"] > div > div > textarea::placeholder {
        color: #888888 !important;
    }
    
    /* Info boxes */
    .stInfo, .stSuccess, .stWarning, .stError {
        background-color: #1e1e1e !important;
        border-radius: 0.5rem !important;
        padding: 0.5rem !important;
    }
    
    .stInfo p, .stSuccess p, .stWarning p, .stError p {
        color: #ffffff !important;
    }
    
    /* Caption */
    .stCaption, .stCaption p {
        color: #aaaaaa !important;
    }
    
    /* Divider */
    hr {
        border-color: #333333 !important;
        margin: 1rem 0 !important;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 8px !important;
        height: 8px !important;
    }
    
    ::-webkit-scrollbar-track {
        background: #1a1a1a !important;
        border-radius: 4px !important;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #444444 !important;
        border-radius: 4px !important;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #555555 !important;
    }
    
    /* Code blocks */
    code {
        background-color: #1e1e1e !important;
        color: #e0e0e0 !important;
        padding: 2px 6px !important;
        border-radius: 4px !important;
    }
    
    /* Spinner */
    .stSpinner > div {
        border-color: #4CAF50 !important;
    }
    
    /* Animation */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .stChatMessage {
        animation: fadeIn 0.3s ease-in-out !important;
    }
    
    /* Fix for all text elements in sidebar */
    .css-1d391kg .stMarkdown p,
    .css-1d391kg .stMarkdown div,
    .css-1d391kg p,
    .css-1d391kg div {
        color: #ffffff !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state variables
def init_session_state():
    """Initialize all session state variables"""
    if 'extracted_text' not in st.session_state:
        st.session_state.extracted_text = ""
    if 'file_name' not in st.session_state:
        st.session_state.file_name = ""
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'api_key_configured' not in st.session_state:
        st.session_state.api_key_configured = False
    if 'total_tokens' not in st.session_state:
        st.session_state.total_tokens = 0

# Configure Gemini API
def configure_gemini(api_key):
    """Configure Gemini API with the provided key"""
    try:
        genai.configure(api_key=api_key)
        st.session_state.api_key_configured = True
        return True
    except Exception as e:
        st.error(f"Error configuring API: {str(e)}")
        st.session_state.api_key_configured = False
        return False

# Get Gemini response - FIXED model name
def get_gemini_response(question, context):
    """Get response from Gemini API based on document context"""
    try:
        # Use the correct model name - gemini-1.5-flash or gemini-pro
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = f"""
        You are DocuBot, an AI assistant that answers questions strictly based on the provided document.
        
        DOCUMENT CONTENT:
        {context[:300000]}
        
        USER QUESTION: {question}
        
        INSTRUCTIONS:
        1. Answer based ONLY on the information in the document above
        2. If the answer is not found in the document, say: "I couldn't find relevant information in the uploaded document."
        3. Be concise, accurate, and helpful
        4. Use quotes if citing directly from the document
        
        ANSWER:
        """
        
        response = model.generate_content(prompt)
        return response.text
        
    except Exception as e:
        error_msg = str(e)
        # If model not found, try alternative model name
        if "404" in error_msg or "not found" in error_msg:
            try:
                # Try using gemini-pro as fallback
                model = genai.GenerativeModel('gemini-pro')
                prompt = f"""
                You are DocuBot, an AI assistant that answers questions strictly based on the provided document.
                
                DOCUMENT CONTENT:
                {context[:300000]}
                
                USER QUESTION: {question}
                
                INSTRUCTIONS:
                1. Answer based ONLY on the information in the document above
                2. If the answer is not found in the document, say: "I couldn't find relevant information in the uploaded document."
                3. Be concise, accurate, and helpful
                4. Use quotes if citing directly from the document
                
                ANSWER:
                """
                response = model.generate_content(prompt)
                return response.text
            except Exception as e2:
                return f"⚠️ Error: Both gemini-1.5-flash and gemini-pro models failed. Please check your API key and model availability. Details: {str(e2)}"
        return f"⚠️ Error generating response: {error_msg}"

# Process uploaded PDF
def process_uploaded_file(uploaded_file):
    """Process uploaded PDF and extract text"""
    if uploaded_file and uploaded_file.name != st.session_state.file_name:
        with st.spinner("📑 Extracting text from PDF..."):
            extracted_text = extract_text_from_pdf(uploaded_file)
            
            if extracted_text and extracted_text.strip():
                st.session_state.extracted_text = extracted_text
                st.session_state.file_name = uploaded_file.name
                
                # Add welcome message
                st.session_state.messages = [{
                    "role": "assistant",
                    "content": f"✅ **Document Processed Successfully!**\n\n📄 **File:** {uploaded_file.name}\n📊 **Characters:** {len(extracted_text):,}\n\nAsk me anything about this document!"
                }]
                return True
            else:
                st.error("❌ No text found in PDF. Make sure it contains selectable text (not scanned images).")
                return False
    return False

# Display chat messages
def display_chat_messages():
    """Display all chat messages in the conversation"""
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Add message to chat
def add_message(role, content):
    """Add a new message to the chat"""
    st.session_state.messages.append({
        "role": role,
        "content": content,
        "timestamp": datetime.now().strftime("%H:%M:%S")
    })

# Clear chat history
def clear_chat():
    """Clear all chat messages"""
    st.session_state.messages = []
    if st.session_state.extracted_text:
        add_message("assistant", f"🧹 Chat cleared! You can continue asking questions about '{st.session_state.file_name}'.")
    else:
        add_message("assistant", "🧹 Chat cleared! Upload a document to start asking questions.")

# Main application
def main():
    # Load custom CSS
    load_css()
    
    # Initialize session state
    init_session_state()
    
    # Sidebar
    with st.sidebar:
        st.markdown("## 📄 DocuBot")
        st.markdown("*AI-powered Document Q&A*")
        st.divider()
        
        # API Key Configuration
        st.markdown("### 🔑 API Configuration")
        api_key = st.text_input(
            "Google Gemini API Key",
            type="password",
            placeholder="Enter your Gemini API key",
            help="Get your free API key from [Google AI Studio](https://aistudio.google.com/app/apikey)"
        )
        
        if api_key:
            if configure_gemini(api_key):
                st.success("✅ API Key Configured")
            else:
                st.error("❌ Invalid API Key")
        elif st.session_state.api_key_configured:
            st.success("✅ API Key Already Configured")
        else:
            st.warning("⚠️ Please enter your API key")
        
        st.divider()
        
        # Document Upload Section
        st.markdown("### 📁 Document Upload")
        uploaded_file = st.file_uploader(
            "Upload a PDF document",
            type=['pdf'],
            help="Upload PDF files containing selectable text"
        )
        
        if uploaded_file:
            if process_uploaded_file(uploaded_file):
                st.success(f"✅ Ready: {uploaded_file.name}")
                st.info(f"📊 Text extracted: {len(st.session_state.extracted_text):,} characters")
        
        # Document Info
        if st.session_state.extracted_text:
            st.divider()
            st.markdown("### 📊 Document Info")
            st.info(f"**File:** {st.session_state.file_name}")
            st.info(f"**Size:** {len(st.session_state.extracted_text):,} chars")
            st.info(f"**Status:** ✅ Ready for Q&A")
        
        st.divider()
        
        # Actions
        st.markdown("### 🛠️ Actions")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🗑️ Clear Chat", use_container_width=True):
                clear_chat()
                st.rerun()
        with col2:
            if st.button("🔄 Reset Document", use_container_width=True):
                st.session_state.extracted_text = ""
                st.session_state.file_name = ""
                st.session_state.messages = []
                st.rerun()
        
        st.divider()
        
        # Footer
        st.markdown("---")
        st.markdown("""
        <div style='text-align: center; font-size: 12px; color: #888888;'>
            Powered by Google Gemini AI<br>
            Made with ❤️ using Streamlit
        </div>
        """, unsafe_allow_html=True)
    
    # Main content area
    st.markdown("## 💬 Document Q&A")
    
    # Display chat messages
    display_chat_messages()
    
    # Chat input
    if prompt := st.chat_input("Ask a question about your document..."):
        # Check prerequisites
        if not st.session_state.api_key_configured:
            st.error("⚠️ Please configure your Gemini API key in the sidebar first!")
        elif not st.session_state.extracted_text:
            st.error("📄 Please upload a PDF document first!")
        else:
            # Add user message
            add_message("user", prompt)
            
            # Display user message
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Generate and display assistant response
            with st.chat_message("assistant"):
                with st.spinner("🤔 Thinking..."):
                    response = get_gemini_response(prompt, st.session_state.extracted_text)
                    st.markdown(response)
                    
                    # Add assistant message to history
                    add_message("assistant", response)
                    
                    # Update token count (rough estimate)
                    st.session_state.total_tokens += len(prompt.split()) + len(response.split())
    
    # Display usage info if available
    if st.session_state.total_tokens > 0 and st.session_state.extracted_text:
        st.markdown("---")
        st.caption(f"📊 Session tokens: ~{st.session_state.total_tokens:,} | 💡 Answers are based strictly on your uploaded document")

if __name__ == "__main__":
    main()
