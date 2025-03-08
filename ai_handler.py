import ollama
import re
from config import MEMORY_LIMIT  # Absolute import

PROMPT_TEMPLATE = """
You are Miku, an AI VTuber known for deadpan humor and sarcasm.
- Stay playful, witty, and mischievous, but never be too aggressive.
- Never use asterisks (*) or stage directions
- Avoid dramatic pauses, sighs, or whispers
- Deliver information directly first, then add humor
- Keep responses concise (1-2 sentences max)
- Always remember numbers/names accurately

Conversation History:
{memory}

User: {prompt}
Miku:"""

def get_ai_response(prompt, memory):
    memory_str = "\n".join(memory[-MEMORY_LIMIT:])
    full_prompt = PROMPT_TEMPLATE.format(memory=memory_str, prompt=prompt)
    
    response = ollama.generate(model='llama3', prompt=full_prompt)
    return clean_ai_response(response['response'])

def clean_ai_response(text):
    text = re.sub(r'[*()]', '', text)
    text = re.sub(r'\.{2,}', '.', text)
    text = re.sub(r'\b(?:sigh|whisper|dramatic pause)\b', '', text, flags=re.IGNORECASE)
    return text.strip()