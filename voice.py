import tkinter as tk
from tkinter import messagebox
import speech_recognition as sr
import pyttsx3
import requests
from bs4 import BeautifulSoup

class VoiceAssistantApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Voice Assistant")
        self.geometry("400x300")
        
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()

        self.create_widgets()

    def create_widgets(self):
        self.label = tk.Label(self, text="Press the mic button and speak", font=("Helvetica", 14))
        self.label.pack(pady=20)
        
        self.mic_button = tk.Button(self, text="🎙️", font=("Helvetica", 48), command=self.listen)
        self.mic_button.pack(pady=20)
        
        self.answer_label = tk.Label(self, text="", font=("Helvetica", 14), wraplength=380)
        self.answer_label.pack(pady=20)
    
    def listen(self):
        with sr.Microphone() as source:
            self.label.config(text="Listening...")
            try:
                audio_data = self.recognizer.listen(source, timeout=5)
                self.label.config(text="Processing...")
                question = self.recognizer.recognize_google(audio_data)
                self.process_input(question)
            except sr.UnknownValueError:
                messagebox.showerror("Error", "Could not understand audio")
            except sr.RequestError:
                messagebox.showerror("Error", "Could not request results; check your network connection")
            except sr.WaitTimeoutError:
                messagebox.showerror("Error", "Listening timed out while waiting for phrase to start")
    
    def process_input(self, question):
        # Display the question
        self.answer_label.config(text=f"Question: {question}")

        # Generate dynamic answer
        spoken_answer, text_answer = self.generate_answer(question)

        # Speak the question
        self.speak(question)

        # Speak the answer
        self.speak(spoken_answer)

        # Display the answer
        self.answer_label.config(text=f"Question: {question}\nAnswer: {text_answer}")

    def generate_answer(self, question):
        try:
            # Perform a web search using the question as the query
            search_url = f"https://www.google.com/search?q={question}"
            response = requests.get(search_url)
            soup = BeautifulSoup(response.text, 'html.parser')

            # Extract relevant information from the search results
            answer_text = ""
            for snippet in soup.find_all('div', class_='BNeawe'):
                if snippet.text:
                    answer_text += snippet.text + "\n"
            
            if answer_text:
                return answer_text, answer_text
            else:
                return "Sorry, I couldn't find an answer to that question.", ""
        except Exception as e:
            print(f"Error fetching answer: {e}")
            return "Sorry, an error occurred while fetching the answer.", ""

    def speak(self, text):
        # Speak the provided text
        self.engine.say(text)
        self.engine.runAndWait()

if __name__ == "__main__":
    app = VoiceAssistantApp()
    app.mainloop()
