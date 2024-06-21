import cohere
import os
from dotenv import load_dotenv

load_dotenv()

co = cohere.Client(os.getenv("COHERE_API_KEY"))

first_prompt = """You are given a transcript between an emergency call operator and the caller. 
Extract only key phrases from the transcript, include important details such as symptoms, personal details, location. """

subsequent_prompt = """The call continues, with the transcript as follows. Extract only key phrases from the transcript, 
include important details such as symptoms, personal details, location."""

def first_summarize(transcript):
    response = co.chat(
        message=first_prompt + transcript,
    )
    return response.text

def subsequent_summarize(transcript):
    response = co.chat(
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

