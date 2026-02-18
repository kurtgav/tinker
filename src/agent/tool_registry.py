from typing import Callable, Dict, Any, List
from src.tools.browser import navigate, click, fill_form, extract_text, screenshot
from src.tools.memory_tools import remember, recall

class ToolRegistry:
    def __init__(self):
        self._tools: Dict[str, Callable] = {}
        # Auto-register browser tools
        self.register(navigate)
        self.register(click)
        self.register(fill_form)
        self.register(extract_text)
        self.register(screenshot)
        # Register memory tools
        self.register(remember)
        self.register(recall)

    def register(self, func: Callable):
        """Decorator to register a tool."""
        self._tools[func.__name__] = func
        return func

    def get_tool(self, name: str) -> Callable:
        return self._tools.get(name)

    def get_tools_description(self) -> str:
        """Returns a formatted string describing all registered tools."""
        descriptions = []
        for name, func in self._tools.items():
            doc = inspect.getdoc(func) or "No description provided."
            # Get signature (args)
            sig = inspect.signature(func)
            descriptions.append(f"- **{name}**{sig}: {doc}")
        return "\n".join(descriptions)

    def list_tools(self) -> List[str]:
        return list(self._tools.keys())

# Global registry instance
registry = ToolRegistry()
