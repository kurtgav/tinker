from dotenv import load_dotenv
from src.agent.react_agent import ReactAgent

load_dotenv()

def test_agent():
    print("Initializing Agent...")
    try:
        agent = ReactAgent()
    except Exception as e:
        print(f"Failed to initialize agent: {e}")
        return

    test_queries = [
        "Hello Tinker!",
        "Search for the latest SpaceX launch and summarize it."
    ]

    for query in test_queries:
        print(f"\n--- Testing Query: {query} ---")
        try:
            response = agent.process_message(query)
            print(f"Response:\n{response}")
        except Exception as e:
            print(f"Error processing message: {e}")

if __name__ == "__main__":
    test_agent()
