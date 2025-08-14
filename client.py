# from openai import OpenAI

# # pip install openai
# # if you saved the key under a different environment variable name, you can do something like:
# client = OpenAI(
#     api_key="<Your Key Here>",
# )

# completion = client.chat.completions.create(
#     model="gpt-3.5-turbo",
#     messages=[
#         {
#             "role": "system",
#             "content": "You are a virtual assistant named jarvis skilled in general tasks like Alexa and Google Cloud",
#         },
#         {"role": "user", "content": "what is coding"},
#     ],
# )

# print(completion.choices[0].message.content)


import requests


def ollama_chat(prompt, model="llama3.1"):
    url = "http://localhost:11434/api/chat"
    payload = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": "You are a virtual assistant named Jarvis skilled in general tasks like Alexa and Google Cloud",
            },
            {"role": "user", "content": prompt},
        ],
        "stream": False,
    }

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        data = response.json()
        return data["message"]["content"]
    except requests.exceptions.ConnectionError:
        return "Error: Could not connect to Ollama. Make sure it's running."
    except Exception as e:
        return f"Error: {e}"


# Example usage
if __name__ == "__main__":
    answer = ollama_chat("what is coding")
    print(answer)
