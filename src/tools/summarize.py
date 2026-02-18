import os
from groq import Groq

def summarize_page(content: str) -> str:
    """
    Summarizes the given text content using an LLM.
    
    Args:
        content: The text content to summarize.
        
    Returns:
        A concise summary of the content.
    """
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return "Error: GROQ_API_KEY not found in environment variables."
        
    client = Groq(api_key=api_key)
    
    try:
        completion = client.chat.completions.create(
            model="llama3-8b-8192", # Using a fast, free model
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that summarizes text. Keep it concise and capture the main points."
                },
                {
                    "role": "user",
                    "content": f"Summarize the following text:\n\n{content[:10000]}" # Limit context window
                }
            ],
            temperature=0.7,
            max_tokens=500,
            top_p=1,
            stream=False,
            stop=None,
        )
        
        return completion.choices[0].message.content
    except Exception as e:
        return f"Error gathering summary: {str(e)}"

if __name__ == "__main__":
    # Test requires GROQ_API_KEY in .env or environment
    from dotenv import load_dotenv
    load_dotenv()
    print(summarize_page("Python is a high-level, general-purpose programming language. Its design philosophy emphasizes code readability with the use of significant indentation."))
