import cohere
import os
from dotenv import load_dotenv

load_dotenv()

co1 = cohere.Client(os.getenv("COHERE_API_KEY_1"))
co2 = cohere.Client(os.getenv("COHERE_API_KEY_2"))

first_prompt = """You are given a transcript of a conversation between an emergency call operator and a caller. 
Your task is to extract key phrases that include important details such as location, personal details and symptoms. 
Ensure that the extracted key phrases are concise and accurately reflect the critical information from the conversation.
If the transcript given is not in English, there is no need to provide an additional translation of the transcript, 
just return the key phrases in English. 

Requirements:
Location: Specify the location details provided, such as address, landmarks, or surroundings.
Personal Details: Include relevant personal information such as the caller's name, age, or relationship to the person in need.
Symptoms: Describe any medical symptoms or conditions mentioned by the caller.

Output Format:
Location: Location details \n
Personal Details: List of personal details \n
Symptoms: List of key symptoms

Example:
Transcript:
Operator: "911, what's your emergency?"
Caller: "Hi, I need help! There's been a car accident on Maple Street."
Operator: "Okay, I understand. Are you or anyone else injured?"
Caller: "Yes, there's a woman who looks seriously hurt. She's not responding."
Operator: "I'm dispatching emergency services to your location. Can you tell me if she's breathing?"
Caller: "I'm not sure. I don't think she is."
Operator: "Alright, can you check her pulse or see if her chest is moving?"
Caller: "Hold on... No, I don't see any movement. What should I do?"
Operator: "Stay calm. Help is on the way. Do you know CPR?"
Caller: "Yes, but it's been a while since I learned."
Operator: "That's okay. I can guide you through it. First, tilt her head back slightly to open her airway."

Extracted Key Phrases:
Location: car accident on Maple Street \n
Personal Details: woman \n
Symptoms: seriously hurt, not responding, not breathing, no pulse, no chest movement

The transcript given to you is: 
"""

subsequent_prompt = """The call continues, with the transcript as follows. Extract only key phrases from the transcript, 
include important details such as symptoms, personal details, location."""

def first_summarize(transcript, api):
    if api == 0:
        response = co1.chat(
            message=first_prompt + transcript,
        )
    else: 
        response = co2.chat(
            message=first_prompt + transcript,
        )
    return response.text

def subsequent_summarize(transcript):
    response = co1.chat(
        message=subsequent_prompt + transcript,
    )
    return response.text

# if __name__ == "__main__":
#     transcript = """Operator: 995, what's your emergency?
#     Caller: My friend just collapsed! I think he's having a heart attack!
#     Operator: Okay, stay calm. Where are you located?
#     Caller: We're at 456 Oak Drive, apartment 2A.
#     Operator: Thank you. Help is on the way. Is your friend conscious?
#     Caller: No, he's not responding at all!
#     Operator: Alright, is he breathing?
#     Caller: No, I don't think so. I can't see his chest moving."""
#     print(first_summarize(transcript))

# from summarizer import Summarizer
# from dg3 import transcribe

# def extractive_summarize(text, ratio=0.2):
#     """
#     Summarize the text using extractive summarization.
#     text: The text to be summarized.
#     ratio: The ratio of sentences to include in the summary.
#     :return: The summarized text.
#     """
#     model = Summarizer()
#     return model(text, ratio=ratio)

# def main():
#     print('hi')
#     print(extractive_summarize(transcribe()))

# if __name__ == "__main__":
#     print('hii')
#     main()

