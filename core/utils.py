import requests
import traceback

LLAMA_API_URL = "http://csai01:8000/generate" 

def talk_llm(context,
             max_tokens=250,
             temperature=0.7,
             top_p=1.0,
             repetition_penalty=1.0,
             top_k=50,
             frequency_penalty=0.0,
             presence_penalty=0.0):
    payload = {
        "prompt": context,
        "max_tokens": max_tokens,
        "temperature": temperature,
        "top_p": top_p,
        "repetition_penalty": repetition_penalty,
        "top_k": top_k,
        "frequency_penalty": frequency_penalty,
        "presence_penalty": presence_penalty
    }

    try:
        response = requests.post(LLAMA_API_URL, json=payload)
        response.raise_for_status()
        response_json = response.json()
        clean_response = response_json.get("response", {})
        
        if isinstance(clean_response, dict):
            return clean_response.get("content", "")  
        else:
            return clean_response  
    except requests.exceptions.RequestException as e:
        traceback.print_exc()
        return {"error": "Failed to generate response", "details": str(e)}
