# AI Medical Chatbot

## Introduction
This AI Medical Chatbot is a tool designed to simulate conversations between a medical student and a virtual patient. The bot helps medical students practice their questioning skills and diagnostic reasoning. It features speech recognition for user input, natural language processing for AI responses, and sentiment analysis for patient mood evaluation.

## Requirements
The following libraries and tools are required to run the AI Medical Chatbot:

- Python 3.x
- SpeechRecognition
- pyttsx3
- OpenAI API
- transformers
- PyQt5
- textblob

## Instructions
1. Install the required libraries using the following command:
   ```bash
   pip install SpeechRecognition pyttsx3 openai transformers PyQt5 textblob
   ```
2. Create an OpenAI account and obtain an API key. Replace the "YOUR_OPENAI_KEY" placeholder with your API key in the code.
3. Run the Python script. The GUI window will appear, where you can interact with the chatbot using speech. You can also request guidance based on the conversation.
4. The bot will generate a dynamic chief complaint that simulates a patient’s issue. The bot will respond to your questions, and the conversation will be analyzed for question quality and patient sentiment.

## Features
- Speech-to-Text and Text-to-Speech: You can speak to the chatbot, and it will respond using speech synthesis.
- Chief Complaint Generation: The bot generates a dynamic chief complaint for each interaction, mimicking a variety of common patient symptoms.
- GPT-3 Powered Responses: GPT-3 generates realistic responses based on the chief complaint and the user’s questions.
- Sentiment Analysis: The bot performs sentiment analysis on the AI responses, providing insights into the patient's emotional state.
- Question Quality Evaluation: The chatbot evaluates the quality of the questions you ask, providing feedback to help improve your medical questioning skills.
- Guidance for Medical Investigation: The bot offers guidance for the next questions to ask based on the conversation context and chief complaint.

##  Code Overview
The core functionality of the AI Medical Chatbot is built using Python and several libraries for natural language processing, speech recognition, and GUI creation. Below is an outline of the main components of the code:

- Speech Recognition: The recognize_speech function listens to the user's speech and converts it into text.
- Text-to-Speech: The speak function uses pyttsx3 to read out the bot's response.
- Chatbot Responses: The get_gpt_response function uses the OpenAI GPT-3 model to generate responses based on user input and a simulated chief complaint.
- Sentiment and Question Quality Evaluation: The analyze_sentiment function analyzes the sentiment of the bot's response, and the evaluate_question_quality function evaluates the user's question.
- GUI: The PyQt5 library is used to create a user-friendly graphical interface where users can interact with the chatbot.

## License
   ```bash
   This code is open source and available for public use.
   ```
