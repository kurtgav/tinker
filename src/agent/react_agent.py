import os
import re
from groq import Groq
from src.agent.tool_registry import registry
from src.agent.intent_router import IntentRouter

# Import tools to register them
import src.tools.web_search
import src.tools.summarize

# Register tools explicitly
registry.register(src.tools.web_search.web_search)
registry.register(src.tools.summarize.summarize_page)

class ReactAgent:
    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
             # In a real app, handled more gracefully
             print("Warning: GROQ_API_KEY missing.")
        
        self.client = Groq(api_key=api_key)
        self.router = IntentRouter()
        self.max_steps = 5

    def process_message(self, message: str, history: list = None, user_id: str = "default_user") -> str:
        """
        Main entry point for processing a user message.
        """
        # Check Rate Limit
        from src.utils.rate_limiter import RateLimiter
        if not hasattr(self, 'rate_limiter'):
             self.rate_limiter = RateLimiter(max_requests=5, period_seconds=600)

        if not self.rate_limiter.is_allowed(user_id):
            return "You have reached the rate limit (5 requests per 10 minutes). Please try again later."

        # Set context var for memory tools
        from src.tools.memory_tools import set_current_user
        set_current_user(user_id)

        # 1. Classify Intent
        intent = self.router.classify(message)
        print(f"DEBUG: Intent detected: {intent}")

        if intent == "chat":
            return self._handle_chat(message, history)
        else:
            # For 'search' or 'unknown' (treat unknown as potential complex task), enter ReAct loop
            return self._run_react_loop(message, history)

    def _handle_chat(self, message: str, history: list = None) -> str:
        messages = [{"role": "system", "content": "You are Tinker, a helpful AI assistant. Be brief and friendly."}]
        
        # Inject short-term history if available
        if history:
            # Convert generic history format to Groq format if needed, 
            # but assuming history passed in is list of {"role": "user"/"assistant", "content": "..."}
            # We filter for only user/assistant messages
            clean_history = [
                {"role": msg["role"], "content": msg["content"]} 
                for msg in history 
                if msg["role"] in ["user", "assistant"]
            ]
            messages.extend(clean_history[-10:]) # Keep last 10 messages

        # Add current message
        messages.append({"role": "user", "content": message})

        completion = self.client.chat.completions.create(
            model="llama3-8b-8192",
            messages=messages
        )
        return completion.choices[0].message.content

    def _run_react_loop(self, task: str, history: list = None) -> str:
        """
        Executes the ReAct (Reasoning + Acting) loop.
        """
        tools_desc = registry.get_tools_description()
        
        system_prompt = f"""
You are Tinker, an autonomous agent.
You have access to the following tools:
{tools_desc}

Use the following format:
Task: the input task you must solve
Thought: you should always think about what to do
Action: the action to take, should be one of [{", ".join(registry.list_tools())}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input task

Begin!
        """
        
        agent_messages = [{"role": "system", "content": system_prompt}]
        
        # Inject short-term history for context (simplified)
        # For ReAct, we primarily want the *Task* context. 
        # If the user says "do it again", we need the previous messages.
        if history:
             # Add recent history as a context block or individual messages
             # For simplicity, let's just add them as previous user/assistant turns *before* the current task prompt
            clean_history = [
                {"role": msg["role"], "content": msg["content"]} 
                for msg in history 
                if msg["role"] in ["user", "assistant"]
            ]
            agent_messages.extend(clean_history[-5:])

        agent_messages.append({"role": "user", "content": f"Task: {task}"})

        for i in range(self.max_steps):
            print(f"DEBUG: Step {i+1}")
            
            # 1. LLM Generation
            completion = self.client.chat.completions.create(
                model="llama3-70b-8192", # Stronger model for reasoning
                messages=agent_messages,
                stop=["Observation:"] # Stop before generating observation
            )
            response = completion.choices[0].message.content
            print(f"DEBUG: LLM Response:\n{response}")
            
            # Append agent response to history
            agent_messages.append({"role": "assistant", "content": response})

            # 2. Check for Final Answer
            if "Final Answer:" in response:
                return response.split("Final Answer:")[-1].strip()

            # 3. Parse Action
            match = re.search(r"Action: (\w+)\nAction Input: (.+)", response, re.DOTALL)
            if not match:
                # If no strict action/input format, user might have just chatted or LLM hallucinated format
                return response

            tool_name = match.group(1).strip()
            tool_input = match.group(2).strip()

            # 4. Execute Tool
            tool_func = registry.get_tool(tool_name)
            observation = ""
            if tool_func:
                try:
                    # Simple arg parsing (assumes single string input mostly)
                    # For web_search(query, max_results), we might need smarter parsing if passing JSON
                    # But for now, let's treat input as the first arg string
                    observation = tool_func(tool_input)
                except Exception as e:
                    observation = f"Error executing {tool_name}: {e}"
            else:
                observation = f"Tool '{tool_name}' not found."

            print(f"DEBUG: Observation: {observation[:100]}...") # Log beginning

            # 5. Append Observation
            obs_message = f"Observation: {observation}"
            agent_messages.append({"role": "user", "content": obs_message})

        return "I processed the task but reached the maximum number of steps without a final answer."
