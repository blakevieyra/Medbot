import sys
import random
import speech_recognition as sr
import pyttsx3
import openai
import time
from textblob import TextBlob
from transformers import pipeline
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton

r = sr.Recognizer()
engine = pyttsx3.init(driverName='sapi5')
openai.api_key = "YOUR_OPENAI_KEY"
classifier = pipeline("text-classification", model="distilbert-base-uncased")

def generate_chief_complaint():
    complaints = [
    "I have a headache that won't go away.",
    "I've been feeling nauseous and dizzy all day.",
    "I've had a sore throat and a cough for the past few days.",
    "I’m having trouble breathing, and it's getting worse.",
    "I've been experiencing chest pain when I breathe.",
    "I have a sharp pain in my lower back that won't subside.",
    "My stomach hurts, and I feel bloated after eating.",
    "I've been feeling very fatigued and can't seem to get enough rest.",
    "I have frequent urination and some discomfort in my lower abdomen.",
    "I’ve noticed a rash developing on my skin that’s itchy and spreading.",
    "I’m having pain in my joints, especially in my knees and elbows.",
    "I’m having difficulty concentrating and feeling foggy-headed.",
    "My skin is turning yellow, and I feel very weak.",
    "I have a high fever and chills that have lasted for days.",
    "I’m experiencing a constant ringing in my ears.",
    "I have a persistent cough and a tight feeling in my chest.",
    "My vision is blurry, and I have difficulty seeing clearly.",
    "I've been feeling unusually thirsty and needing to urinate a lot.",
    "I've been coughing up blood, and I'm worried.",
    "I’ve noticed that my hands are shaking uncontrollably.",
    "I’ve been having heart palpitations and lightheadedness.",
    "I’m feeling unusually short of breath even when resting.",
    "I've had unexplained weight loss and loss of appetite.",
    "I've been feeling anxious and having trouble sleeping.",
    "I have pain when swallowing and some difficulty breathing.",
    "My legs feel weak, and I have difficulty walking.",
    "I’ve been feeling nauseous every morning and have trouble eating.",
    "I’ve been experiencing severe headaches that last for hours.",
    "I’ve been coughing up yellow mucus for the last few days.",
    "I’ve had diarrhea for the past two days and feel very dehydrated."
]

    return random.choice(complaints)


def speak(text):
    try:
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"Error in speak function: {e}")

def recognize_speech():
    with sr.Microphone() as source:
        print("Speak:")
        audio = r.listen(source)
    try:
        text = r.recognize_google(audio)
        print(f"You said: {text}")
        return text
    except sr.UnknownValueError:
        print("Sorry, I did not get that")
        return None
    except sr.RequestError:
        print("Request Error from Google Speech Recognition service")
        return None

def get_gpt_response(prompt, chief_complaint, retries=5, wait_time=1, max_wait_time=32):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": f"You are a simulated patient with the following chief complaint: {chief_complaint}. Respond in a way that feels human, natural, and realistic to a medical student questioning you about your chief complaint."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message['content'].strip()
    except openai.error.AuthenticationError:
        return "Authentication Error: Please check your API key."
    except openai.error.RateLimitError:
        if retries > 0:
            time.sleep(wait_time)
            return get_gpt_response(prompt, chief_complaint, retries - 1, wait_time * 2, max_wait_time)
        else:
            return "Rate limit exceeded. Please try again later."
    except Exception as e:
        return f"An error occurred: {str(e)}"

def local_fallback_response(prompt):
    return "I'm currently unable to process your request. Please try again later."

def analyze_sentiment(response):
    analysis = TextBlob(response)
    polarity = analysis.sentiment.polarity
    subjectivity = analysis.sentiment.subjectivity
    
    if polarity > 0.1:
        sentiment = "Positive"
    elif polarity < -0.1:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"

    if subjectivity > 0.5:
        sentiment_detail = f"Patient is quite subjective, potentially emotional."
    else:
        sentiment_detail = f"Patient's response is more objective."

    return sentiment, sentiment_detail

def evaluate_question_quality(question, context=""):
    if len(question.split()) < 3: 
        return 3
    elif len(question.split()) > 50:  
        return 5
    
    if context:
        context_keywords = set(context.lower().split())
        question_keywords = set(question.lower().split())
        relevance_score = len(context_keywords.intersection(question_keywords)) / len(context_keywords)
    else:
        relevance_score = 0.5  

    try:
        result = classifier(question)
        quality_score = result[0]['score']  
    except Exception as e:
        print(f"Error during quality evaluation: {e}")
        quality_score = 0.5  

    final_score = (relevance_score * 0.4 + quality_score * 0.6) * 10  
    final_score = min(max(final_score, 1), 10)
    return round(final_score, 2)

def get_guidance(context, chief_complaint):
    try:
        prompt = f"Based on the following conversation: {context}, with the patient's chief complaint being: {chief_complaint}, what should be asked next to further the investigation and reach a diagnosis?"
        guidance_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a experienced doctor giving guidance for the next question to ask to a medical student in a simulated medical consultation."},
                {"role": "user", "content": prompt}
            ]
        )
        return guidance_response.choices[0].message['content'].strip()
    except Exception as e:
        return f"An error occurred while providing guidance: {str(e)}"

class ChatBotApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.conversation_context = []
        self.chief_complaint = generate_chief_complaint()  
        print(f"Generated Chief Complaint: {self.chief_complaint}") 

    def initUI(self):
        self.setWindowTitle('AI Medical Chatbot')

        self.layout = QVBoxLayout()

        self.input_label = QLabel("User Input:")
        self.layout.addWidget(self.input_label)

        self.input_box = QTextEdit()
        self.input_box.setFixedHeight(150)  
        self.layout.addWidget(self.input_box)

        self.response_label = QLabel("AI Response:")
        self.layout.addWidget(self.response_label)

        self.response_box = QTextEdit()
        self.response_box.setFixedHeight(150)
        self.response_box.setReadOnly(True)
        self.layout.addWidget(self.response_box)

        self.guidance_label = QLabel("Guidance:")
        self.layout.addWidget(self.guidance_label)

        self.guidance_box = QTextEdit()
        self.guidance_box.setFixedHeight(100)  
        self.guidance_box.setReadOnly(True)
        self.layout.addWidget(self.guidance_box)

        self.recognize_button = QPushButton('Speak')
        self.recognize_button.clicked.connect(self.handle_conversation)
        self.layout.addWidget(self.recognize_button)

        self.guidance_button = QPushButton('Get Guidance')
        self.guidance_button.clicked.connect(self.provide_guidance)
        self.layout.addWidget(self.guidance_button)

        self.rating_label = QLabel("Question Quality: N/A | Patient Sentiment: N/A")
        self.layout.addWidget(self.rating_label)

        self.setLayout(self.layout)


    def handle_conversation(self):
        user_input = recognize_speech()
        if user_input:
            self.input_box.append(f"You: {user_input}")
            gpt_response = get_gpt_response(user_input, self.chief_complaint)

            if "Rate limit exceeded" in gpt_response or "Authentication Error" in gpt_response:
                gpt_response = local_fallback_response(user_input)

            self.response_box.append(f"Bot: {gpt_response}")
            speak(gpt_response)

            question_quality = evaluate_question_quality(user_input, " ".join(self.conversation_context))
            sentiment, sentiment_detail = analyze_sentiment(gpt_response)

            self.rating_label.setText(f"Question Quality: {question_quality}/10 | Patient Sentiment: {sentiment} - {sentiment_detail}")

            self.conversation_context.append(f"You: {user_input}")
            self.conversation_context.append(f"Patient: {gpt_response}")

    def provide_guidance(self):
        guidance = get_guidance(" ".join(self.conversation_context), self.chief_complaint)
        self.guidance_box.setText(guidance)
        speak(guidance)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = ChatBotApp()
    ex.show()
    sys.exit(app.exec_())
