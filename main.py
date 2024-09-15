import os
from dotenv import load_dotenv
from googleapiclient.discovery import build
import boto3
import requests
from bs4 import BeautifulSoup
import re
import json

# Load environment variables from .env file
load_dotenv()

# Load Environment Variables (Google Custom Search API Key and CSE ID)
GOOGLE_API_KEY = os.getenv("GOOGLE_SEARCH_API_KEY")
GOOGLE_CSE_ID = os.getenv("GOOGLE_CSE_ID")
AWS_REGION = os.getenv("AWS_REGION", 'us-west-2')
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

# AWS Bedrock Client
bedrock_client = boto3.client(
    'bedrock-runtime',
    region_name=AWS_REGION,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)

# Google Search API integration
def google_search(search_term, api_key, cse_id, **kwargs):
    try:
        service = build("customsearch", "v1", developerKey=api_key)
        res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
        if 'items' in res:
            return res['items']
        else:
            print("No results found.")
            return []
    except Exception as e:
        print(f"An error occurred during the search: {e}")
        return []

# Function to capture user query
def capture_user_query():
    query = input("Enter your search query: ")
    return query

# Function to fetch real-time search results using Google Custom Search API
def fetch_search_results(query):
    return google_search(query, GOOGLE_API_KEY, GOOGLE_CSE_ID, num=5)

# Function to clean and extract snippets from search results
def clean_search_results(results):
    snippets = [item.get("snippet", "").strip() for item in results]
    urls = [item.get("link", "").strip() for item in results]
    return snippets, urls

# Function to fetch and parse URL content
def fetch_and_parse_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        page_content = soup.get_text()
        
        # Clean up the text
        page_content = re.sub(r'\s+', ' ', page_content).strip()  # Remove excessive whitespace and newlines
        return page_content
    except Exception as e:
        print(f"An error occurred while fetching or parsing the URL: {e}")
        return "Error fetching content"

# Prepare the context for AWS Bedrock (LLaMA model)
def prepare_context(search_results):
    context = "Search Results:\n"
    for idx, snippet in enumerate(search_results, 1):
        context += f"Result {idx}: {snippet}\n"
    return context

# AWS Bedrock - Invoke LLaMA model with context
def invoke_llama_with_context(model_id, context, user_query, temperature=0.7, top_p=0.9, max_gen_len=200):
    try:
        # Format the prompt using the LLaMA model's system prompt format
        prompt = f"<s>[INST] <<SYS>>\nYou are a helpful, respectful, and honest assistant. Always answer as helpfully as possible, while being safe. Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. Please ensure that your responses are socially unbiased and positive in nature.\nIf a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. If you don't know the answer to a question, please don't share false information.\n<</SYS>>\n\n{context}\n\nUser Question: {user_query} [/INST]"
        
        # Call the Bedrock model with the prompt and additional parameters
        response = bedrock_client.invoke_model(
            modelId=model_id,
            contentType="application/json",
            accept="application/json",
            body=json.dumps({
                "prompt": prompt,
                "temperature": temperature,
                "top_p": top_p,
                "max_gen_len": max_gen_len
            })
        )
        
        # Decode response body from bytes
        stream = response['body']
        chunks = []
        for chunk in stream.iter_chunks():
            chunks.append(chunk.decode('utf-8'))
        
        response_text = ''.join(chunks)
        
        # Attempt to extract relevant text from the response
        try:
            # Here, you might need to adjust the parsing logic depending on actual response format
            response_json = json.loads(response_text)
            generated_text = response_json.get('generation', "No response from the model.")
        except json.JSONDecodeError:
            # Fallback if the response is not valid JSON
            generated_text = response_text
        
        # Clean up the response text (removing unwanted tags)
        clean_response = re.sub(r'<<INST>>|<</INST>>|[/INST]', '', generated_text).strip()
        
        return clean_response
    
    except Exception as e:
        print(f"Error with AWS Bedrock: {str(e)}")
        return "An error occurred when processing the query with Bedrock."

# Main function to handle the entire workflow
def handle_user_query():
    # Step 1: Capture query
    user_query = capture_user_query()

    # Step 2: Fetch real-time web search results
    print("Fetching web results...")
    search_results = fetch_search_results(user_query)

    # Step 3: Clean up search results
    clean_results, clean_urls = clean_search_results(search_results)

    # Step 4: Optionally, fetch and parse content from URLs
    for url in clean_urls:
        page_content = fetch_and_parse_url(url)
        if page_content != "Error fetching content":
            clean_results.append(page_content)
            break

    # Step 5: Prepare the context for LLaMA
    context = prepare_context(clean_results)
    print("Prepared context for Bedrock:", context)

    # Step 6: Invoke LLaMA model with context
    print("Processing query with AWS Bedrock...")
    model_id = 'arn:aws:bedrock:us-west-2::foundation-model/meta.llama3-1-405b-instruct-v1:0'  # Updated model ID
    bedrock_response = invoke_llama_with_context(model_id, context, user_query)

    # Combine Bedrock response with content information
    return f"{bedrock_response}"

# Execute the search engine workflow
if __name__ == "__main__":
    result = handle_user_query()
    print(result)
