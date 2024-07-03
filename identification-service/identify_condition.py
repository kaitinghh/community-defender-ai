import cohere
import os
from dotenv import load_dotenv

load_dotenv()

co = cohere.Client(os.getenv("COHERE_API_KEY_1"))

prompt = """You are given a transcript where you need to choose the most applicable condition from the list below. 
Conditions: 1.breathing problems 2.cardiac arrest/death 3.chest pain 4.seizure 4.traumatic injury 5.unconscious/fainting  6.non-critical.

Give the output in this format: cardiac arrest
"""

def identify_condition(transcript):
    condition = co.chat(
        message=prompt + transcript,
        # perform web search before answering the question. You can also use your own custom connector.
        # connectors=[{"id": "web-search"}],
    )
    return condition.text

if __name__ == "__main__":
    transcript = """Operator: 995, what's your emergency?
    Caller: My friend just collapsed! I think he's having a heart attack!
    Operator: Okay, stay calm. Where are you located?
    Caller: We're at 456 Oak Drive, apartment 2A.
    Operator: Thank you. Help is on the way. Is your friend conscious?
    Caller: No, he's not responding at all!
    Operator: Alright, is he breathing?
    Caller: No, I don't think so. I can't see his chest moving."""
    print(identify_condition(transcript))