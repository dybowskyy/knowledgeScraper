import customtkinter as ctk


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
        self.input_field.bind("<Return>", lambda event: self.fetch_yt_transcript())
        # Button
        self.submit_button = ctk.CTkButton(master=self.main_frame, width=320, font=("Roboto", 20), text="Submit", corner_radius=10, command=self.fetch_yt_transcript)
        self.submit_button.grid(row=5, pady=5, sticky="nswe")

    def fetch_yt_transcript(self):
        user_input = self.input_field.get()
        print(f"User Input: {user_input}")


if __name__ == "__main__":
    app = KnowledgeScraperUI()
    app.mainloop()
