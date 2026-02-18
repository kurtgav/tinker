from duckduckgo_search import DDGS

def web_search(query: str, max_results: int = 5) -> str:
    """
    Performs a web search using DuckDuckGo and returns a formatted string of results.
    
    Args:
        query: The search query.
        max_results: The maximum number of results to return.
        
    Returns:
        A formatted string containing titles, URLs, and snippets of the search results.
    """
    print(f"DEBUG: Searching for '{query}'...")
    try:
        results = DDGS().text(query, max_results=max_results)
        if not results:
            return "No results found."
        
        formatted_results = []
        for i, res in enumerate(results, 1):
            title = res.get('title', 'No Title')
            href = res.get('href', '#')
            body = res.get('body', 'No description available.')
            formatted_results.append(f"{i}. [{title}]({href})\n   {body}")
            
        return "\n\n".join(formatted_results)
    except Exception as e:
        return f"Error performing web search: {str(e)}"

if __name__ == "__main__":
    # Test
    print(web_search("latest python version"))
