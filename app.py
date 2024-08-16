import streamlit as st
from dotenv import load_dotenv
import os
load_dotenv() # Load environment variables from .env file
import google.generativeai as genai

from youtube_transcript_api import YouTubeTranscriptApi


def extract_transcript_details(youtube_video_url):
    try:
        video_id = youtube_video_url.split("=")[1]
        print(video_id)
        transcript_text = YouTubeTranscriptApi.get_transcript(video_id)

        transcript = ""
        for i in transcript_text:
            transcript += " " + i['text'] 

        return transcript


    except Exception as e:
        raise e


# Getting the summary based on prompt from google gemini pro
genai.configure(api_key=os.getenv("GEMINI_API_KEY")) # Configure the Google AI platform

prompt= """You are a Youtube Video Summerizer. 
You will be taking the transcript text and summerize the 
entire video and providing the important summary in points within 250 words.
The transcript text will be appended here: """

def generate_gemini_content(transcript_text, prompt):
    model=genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt+transcript_text)
    return response.text

    

st.title("Youtube Video Summerizer")
youtube_link = st.text_input("Enter the youtube video link: ")

if youtube_link:
    video_id = youtube_link.split("=")[1]
    st.image(f"https://img.youtube.com/vi/{video_id}/0.jpg", width=300)


if st.button("Summarize"):
    transcript_text = extract_transcript_details(youtube_link)
    if transcript_text:
        summary = generate_gemini_content(transcript_text, prompt)
        st.markdown("### Summary")
        # st.write(summary)

        all_responses = []
        for response in summary:
            for part in response.parts:
                if part.text:
                    all_responses.append(part.text)

        st.write(all_responses)
    
    