import cohere
import os
from dotenv import load_dotenv

load_dotenv()

co = cohere.Client(os.getenv("COHERE_API_KEY"))

prompt = """You are given a transcript between an emergency call operator and the caller. 
I need you to return the caller's name and address, if given in the transcript. If the caller's name and address are
not given in the transcript, return "Unknown". 

Return in this format: 
Name: Unknown
Address: Ang Mo Kio Avenue Block 71

The transcript given to you is: 
"""

def identify_details(transcript):
    details = co.chat(
        message=prompt + transcript,
        # perform web search before answering the question. You can also use your own custom connector.
        # connectors=[{"id": "web-search"}],
    )
    return details.text