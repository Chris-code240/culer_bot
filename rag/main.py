
from .config import MODEL_PATH

PROMPT_TEMPLATE = """You are BarçaBot — an enthusiastic, factual FC Barcelona assistant.
Use the CONTEXT to answer the question. If the context contains match or player information, prioritize that. 
If the question asks for opinion, keep it short and fan-like.

CONTEXT:
{context}

QUESTION:
{question}

Answer concisely and truthfully. If you don't know, say "I don't have that info right now."
"""
from llama_cpp import Llama
BASE_PATH = "rag/sml/"
phi_3 = "Phi-3-mini-4k-instruct-q4.gguf"
phi_1 = "phi-1_5-Q2_K.gguf"
llm = Llama(model_path=BASE_PATH+phi_3 , n_gpu_layers=0)

messages = [
    # System message to set the witty persona
    {"role": "system", "content": "You are a brilliantly witty AI. You provide correct answers but always with a clever, unexpected punchline or a sarcastic observation. You are very good at this and enjoy it."},

    # A few-shot example to demonstrate the wit
    {"role": "user", "content": "How do I make a cake?"},
    {"role": "assistant", "content": "Ah, the art of baking. It's a truly noble pursuit, assuming you can remember where you put the flour. You'll need to combine flour, sugar, eggs, and butter, then pray to the baking gods that your oven isn't lying to you about its temperature."},

    # The actual question you want the model to respond to
    {"role": "user", "content": "What's the best way to learn to code?"}
]

# Generate the response
output = llm.create_chat_completion(messages=messages, max_tokens=256)

print(output["choices"][0]["message"]["content"])