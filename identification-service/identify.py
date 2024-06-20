import cohere
import os

load_dotenv()

co = cohere.Client(os.getenv("COHERE_API_KEY"))

prompt = """You are given a transcript where you need to choose the first applicable condition from the list below. If a condition is not applicable, you should consider the next one in the list. Choose the first option that meets the criteria.
Conditions: 1.cardiac arrest 2.severe bleeding 3.seizure 4.breathing problems 5.halted level of consciousness  6.non-critical."""

def identify_condition(transcript):
    condition = co.chat(
        message=prompt + transcript,
        # perform web search before answering the question. You can also use your own custom connector.
        # connectors=[{"id": "web-search"}],
    )
    return condition

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