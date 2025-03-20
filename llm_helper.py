from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

load_dotenv()

# Ensure the API key is loaded correctly
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    print("API key is not set. Please check your .env file.")
    exit(1)

# Initialize the LLM with the API key and model name
llm = ChatGroq(groq_api_key=api_key, model_name="llama3-8b-8192")

if __name__ == "__main__":
    try:
        response = llm.invoke("Two most important ingredients in samosa are ")
        print(response.content)
    except Exception as e:
        print(f"Error: {e}")
