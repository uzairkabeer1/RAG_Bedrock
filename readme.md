# AI Search and Chat Assistant

An interactive AI assistant that combines web search and natural language processing. This project uses Google Custom Search API to retrieve search results and AWS Bedrock’s LLaMA model to generate contextual responses. The application is built with Python and Streamlit for a seamless web-based user experience.

## Features

- **Real-time Web Search**: Fetches and displays search results using Google Custom Search API.
- **Contextual AI Responses**: Utilizes AWS Bedrock's LLaMA model to generate responses based on search results.
- **Interactive Interface**: Built with Streamlit for an intuitive and user-friendly chat interface.

## Requirements

- **Python 3.7+**
- **Packages**: Use `requirements.txt` to install the necessary packages:
  - `google-api-python-client`
  - `boto3`
  - `requests`
  - `beautifulsoup4`
  - `python-dotenv`
  - `streamlit`

## Setup

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/RAG_Bedrock.git
cd RAG_Bedrock
```

### 2. Environment Variables

Create a `.env` file in the root directory with the following content:

```plaintext
GOOGLE_SEARCH_API_KEY=your_google_search_api_key
GOOGLE_CSE_ID=your_google_custom_search_engine_id
AWS_REGION=your_aws_region (e.g., 'us-west-2')
AWS_ACCESS_KEY_ID=your_aws_access_key_id
AWS_SECRET_ACCESS_KEY=your_aws_secret_access_key
```

### 3. Install Dependencies

Install the required Python packages:

```bash
pip install -r requirements.txt
```

### 4. Run the Streamlit Application

To start the Streamlit application, run:

```bash
streamlit run app.py
```

## Usage

1. **Open the Streamlit Application**: After running the above command, a web browser window will open with the Streamlit interface.
2. **Enter a Query**: Type your search query into the input box and click "Send."
3. **View Results**: The application will display search results and an AI-generated response based on those results.

## Code Overview

### Main Workflow (`main.py`)

- **Google Search Integration**: Fetches search results from Google Custom Search API.
- **Context Preparation**: Prepares the context for the AI model based on search results.
- **AI Response Generation**: Uses AWS Bedrock’s LLaMA model to generate responses.

### Streamlit Interface (`app.py`)

- **User Interface**: Provides an interactive chat interface for user input and displays responses.
- **Result Display**: Shows search results and AI-generated responses within the Streamlit app.
