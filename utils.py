# utils.py
# utils.py

import PyPDF2

def extract_text_from_pdf(uploaded_file):
    try:
        reader = PyPDF2.PdfReader(uploaded_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text
    except Exception as e:
        return f"Error extracting text: {e}"
import speech_recognition as sr

def convert_audio_to_text(audio_file):
    try:
        recognizer = sr.Recognizer()
        with sr.AudioFile(audio_file) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data)
            return text
    except Exception as e:
        return f"Error converting audio to text: {e}"

def generate_tech_questions(tech_stack):
    tech_stack = tech_stack.lower()
    questions = []

    if "python" in tech_stack:
        questions.extend([
            "What are Python decorators and how do you use them?",
            "Explain list comprehension with an example.",
            "What is the difference between deep copy and shallow copy?",
            "How does Python handle memory management?",
            "What is a lambda function? Where is it used?"
        ])
    
    if "django" in tech_stack:
        questions.extend([
            "What is Django ORM and how does it work?",
            "How does middleware work in Django?",
            "Explain Django’s request-response cycle.",
            "How do you implement authentication in Django?",
            "What are class-based views in Django?"
        ])
    
    if "react" in tech_stack:
        questions.extend([
            "What are React Hooks and give examples?",
            "How does React handle component lifecycle?",
            "Explain virtual DOM in React.",
            "What is Redux and when should it be used?",
            "How can you optimize performance in a React app?"
        ])
    
    if "sql" in tech_stack:
        questions.extend([
            "What is normalization? Explain different normal forms.",
            "What is the difference between WHERE and HAVING?",
            "Explain JOINs in SQL with examples.",
            "How do indexes work in SQL?",
            "What is ACID property in DBMS?"
        ])
    
    if "node" in tech_stack:
        questions.extend([
            "How does Node.js handle asynchronous operations?",
            "What are event loops in Node.js?",
            "What are streams in Node.js and how do they work?",
            "How do you manage packages in Node.js?",
            "Explain middleware in Express.js."
        ])
    
    if not questions:
        questions = [
            "Tell us about a complex technical problem you solved.",
            "How do you stay updated with new technologies?",
            "What was your most challenging coding experience?",
            "How do you handle tight deadlines in projects?",
            "Describe your favorite project and what made it successful."
        ]

    return questions[:7]  # Return first 7 relevant questions
