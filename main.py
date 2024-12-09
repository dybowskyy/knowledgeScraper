import customtkinter as ctk
import youtube_transcript_api
import os
from dotenv import load_dotenv
from googleapiclient.discovery import build
import openai
import re

load_dotenv()
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
openai.api_key = os.getenv("OPENAI_API_KEY")

class KnowledgeScraperUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("KnowledgeScraper")
        self.geometry("360x600")
        self.resizable(False, False)
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        # Configure the grid layout
        self.main_frame = ctk.CTkFrame(master=self)
        self.main_frame.grid(sticky="nsew", row=0, column=0, padx=20, pady=20)
        self.main_frame.rowconfigure((0, 5), weight=0)
        self.main_frame.rowconfigure((1, 2, 3, 4), weight=1)
        self.main_frame.columnconfigure(0, weight=1)
        # Title
        self.game_title = ctk.CTkLabel(master=self.main_frame, font=("Roboto", 30), text="KnowledgeScraper", width=320)
        self.game_title.grid(row=1, pady=30, sticky="nswe")
        # Input Field
        self.input_field = ctk.CTkEntry(master=self.main_frame, font=("Roboto", 20), width=320, corner_radius=10)
        self.input_field.grid(row=4, pady=5, sticky="nswe")
        self.input_field.bind("<Return>", lambda event: scrape(self.input_field.get()))
        # Button
        self.submit_button = ctk.CTkButton(master=self.main_frame, width=320, font=("Roboto", 20), text="Submit", corner_radius=10, command=lambda: scrape(self.input_field.get()))
        self.submit_button.grid(row=5, pady=5, sticky="nswe")

def get_video_id_from_url(url) -> str:
    if "v=" in url:
        return url.split("v=")[1].split("&")[0]
    elif "youtu.be/" in url:
        return url.split("youtu.be/")[1]
    else:
        raise ValueError("Invalid URL")

def get_video_title(video_id) -> str:
    youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
    request = youtube.videos().list(part="snippet", id=video_id)
    response = request.execute()

    if 'items' in response and len(response['items']) > 0:
        title = response['items'][0]['snippet']['title']
        return title
    else:
        print("Video not found")
def get_transcript(video_id) -> str:
    try:
        transcript = youtube_transcript_api.YouTubeTranscriptApi.get_transcript(video_id)
        return "\n".join([f"{item['text']}" for item in transcript])
    except youtube_transcript_api.TranscriptsDisabled:
        return "Transcripts are disabled for this video."
    except youtube_transcript_api.TooManyRequests:
        return "Too many requests"
    except youtube_transcript_api.CouldNotRetrieveTranscript:
        return "Could not retrieve transcript"

def scrape(url):
    video_id = get_video_id_from_url(url)
    transcript = get_transcript(video_id)

    with open(f'{get_video_title(get_video_id_from_url(url))}', "a") as file:
        file.write(str(create_note_from_transcript(transcript)))

def create_note_from_transcript(transcript):
    prompt = open(r'prompt.txt', 'r')

    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": "You make high quality notes"}, {"role": "user", "content": f'{prompt.read()}\n\nTranscript: {transcript}'}]
        ),
        prompt.close()

        return response

    except Exception as e:
        print(f"An error occurred: {e}")
        prompt.close()
        return None

#TODO: Add error handling for invalid URLs, YouTube API rate limits, and OpenAI API errors
#TODO: Sanitize user input & and video title to prevent vulnerabilities
#TODO: Display the notes in a UI OR display them in Obsidian
#TODO: Simplify the code
#TODO: Improve UI: add a progress bar, message box for errors, etc.


if __name__ == "__main__":
    app = KnowledgeScraperUI()
    app.mainloop()
