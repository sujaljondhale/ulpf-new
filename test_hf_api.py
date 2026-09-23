import os
import json
import urllib.request
from urllib.error import HTTPError, URLError

# Check if dotenv is installed, and load .env if it is
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("Loaded environment variables from .env file.")
except ImportError:
    print("python-dotenv not installed, assuming HF_TOKEN is exported in the environment.")

api_key = os.getenv('HF_TOKEN') or os.getenv('HUGGINGFACE_API_KEY')

if not api_key:
    print("❌ Error: No HF_TOKEN or HUGGINGFACE_API_KEY found in the environment!")
    exit(1)
    
print(f"Using Token: {api_key[:8]}...{api_key[-4:] if len(api_key) > 12 else ''}")

try:
    from huggingface_hub import InferenceClient
except ImportError:
    print("❌ Error: huggingface_hub is not installed. Run 'pip install huggingface_hub'")
    exit(1)

model_name = 'Qwen/Qwen2.5-Coder-7B-Instruct'
print(f"Sending request to {model_name} via huggingface_hub InferenceClient...")

client = InferenceClient(token=api_key, timeout=10.0)

messages = [
    {"role": "user", "content": "Hello, are you online? Respond with a very short 'Yes'."}
]

try:
    response = client.chat_completion(
        model=model_name,
        messages=messages,
        temperature=0.1,
        max_tokens=10
    )
    print("\n✅ SUCCESS! Response from model:")
    print(response.choices[0].message.content)
except Exception as e:
    print(f"\n❌ API or Network Error: {e}")
