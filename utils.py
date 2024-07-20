import os
from dotenv import load_dotenv

def load_environment_variables():
    load_dotenv()
    hf_token = os.getenv("HF_TOKEN")
    return hf_token

def query_huggingface_api(prompt, api_url, headers):
    import requests
    response = requests.post(api_url, headers=headers, json={"inputs": prompt})
    if response.status_code == 200:
        generated_text = response.json()[0]['generated_text']
        # Extract only the final answer
        answer_start = generated_text.find("Answer: ")
        if answer_start != -1:
            answer = generated_text[answer_start + len("Answer: "):].strip()
        else:
            answer = generated_text
        return answer
    else:
        return f"Error {response.status_code}: {response.text}"

def chunk_text(text, chunk_size=1000):
    chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
    return chunks
