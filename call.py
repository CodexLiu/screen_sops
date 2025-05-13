from openai import OpenAI
from dotenv import load_dotenv
import os
import base64

def encode_docx(docx_path):
    """Encode a DOCX file as base64 string"""
    with open(docx_path, "rb") as file:
        return base64.b64encode(file.read()).decode('utf-8')

def ask_openrouter(prompt: str) -> str:
    """Send a text prompt to Gemini via OpenRouter and get the response"""
    load_dotenv()
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("OPENROUTER_API_KEY"),
    )
    completion = client.chat.completions.create(
        extra_headers={
            "HTTP-Referer": "<YOUR_SITE_URL>",  # Optional. Site URL for rankings on openrouter.ai.
            "X-Title": "<YOUR_SITE_NAME>",      # Optional. Site title for rankings on openrouter.ai.
        },
        extra_body={},
        model="google/gemini-2.5-pro-preview",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    }
                ]
            }
        ]
    )
    return completion.choices[0].message.content

def ask_openrouter_with_docx(prompt: str, docx_path: str) -> str:
    """Send a prompt with a base64-encoded DOCX file to Gemini via OpenRouter"""
    load_dotenv()
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("OPENROUTER_API_KEY"),
    )
    
    # Encode the DOCX file
    base64_docx = encode_docx(docx_path)
    
    # Get the file extension for MIME type
    file_ext = os.path.splitext(docx_path)[1].lower().replace('.', '')
    
    completion = client.chat.completions.create(
        extra_headers={
            "HTTP-Referer": "https://sop-processor.example.com",
            "X-Title": "SOP Document Processor",
        },
        extra_body={},
        model="google/gemini-2.5-pro-preview",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:application/{file_ext};base64,{base64_docx}"
                        }
                    }
                ]
            }
        ]
    )
    
    try:
        return completion.choices[0].message.content
    except Exception as e:
        print(f"Error getting response: {str(e)}")
        # Try to extract any available response content
        if hasattr(completion, 'choices') and len(completion.choices) > 0:
            if hasattr(completion.choices[0], 'message'):
                if hasattr(completion.choices[0].message, 'content'):
                    return completion.choices[0].message.content
        
        return f"Error processing document: {str(e)}"

if __name__ == "__main__":
    response = ask_openrouter("What is the capital of France?")
    print(response)