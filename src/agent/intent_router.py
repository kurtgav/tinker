import os
from groq import Groq
from typing import Literal

IntentType = Literal["search", "chat", "unknown"]

class IntentRouter:
    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY not found.")
        self.client = Groq(api_key=api_key)

    def classify(self, message: str) -> IntentType:
        """
        Classifies the user message into an intent.
        """
        prompt = f"""
        Classify the intent of the following user message sent to a bot named 'Tinker'.
        
        Intents:
        - 'search': The user wants to find information, look something up, or asks a question that requires external knowledge.
        - 'chat': The user is greeting, thanking, or making small talk.
        - 'unknown': The intent is unclear.

        Message: "{message}"
        
        Respond ONLY with the intent label (search, chat, unknown). Do not add punctuation or explanation.
        """
        
        try:
            completion = self.client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.0,
                max_tokens=10
            )
            intent = completion.choices[0].message.content.strip().lower()
            if intent in ["search", "chat", "unknown"]:
                return intent
            return "unknown"
        except Exception as e:
            print(f"Error in intent classification: {e}")
            return "unknown"
