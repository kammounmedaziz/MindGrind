import os
from typing import List, Dict
from dotenv import load_dotenv
from duckduckgo_search import DDGS
from openai import OpenAI

# Load environment variables
load_dotenv()

# function uses a query string and duckduckgo_search library to perform a web search
def perform_web_search(query: str, max_results: int = 6) -> List[Dict[str, str]]:
    """Perform a DuckDuckGo search and return a list of results.

    Each result contains: title, href, body.
    """
    results: List[Dict[str, str]] = []
    try:
        with DDGS() as ddgs:
            for result in ddgs.text(query, max_results=max_results):
                # result keys typically include: title, href, body
                if not isinstance(result, dict):
                    continue
                title = result.get('title') or ''
                href = result.get('href') or ''
                body = result.get('body') or ''
                if title and href:
                    results.append({
                        'title': title,
                        'href': href,
                        'body': body,
                    })
        return results
    except Exception as e:
        print(f"DuckDuckGo search error: {e}")
        return []

# A class that manages the interaction with the OpenRouter API (using Mistral model) and core agent logic 
class GeminiClient:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv('OPENROUTER_API_KEY')
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=self.api_key,
        )
        self.model = "mistralai/mistral-small-3.2-24b-instruct:free"
        self.history = []  # List of messages for chat history

    def generate_response(self, user_input: str) -> str:
        """Generate an AI response with optional web search when prefixed.

        To trigger web search, start your message with one of:
        - "search: <query>"
        - "/search <query>"
        Otherwise, the model responds directly using chat history.
        """
        if not self.api_key:
            return "AI service is not configured correctly. Please set OPENROUTER_API_KEY."

        try:
            text = user_input or ""
            lower = text.strip().lower()

            # Search trigger
            search_query = None
            if lower.startswith("search:"):
                search_query = text.split(":", 1)[1].strip()
            elif lower.startswith("/search "):
                search_query = text.split(" ", 1)[1].strip()

            if search_query:
                web_results = perform_web_search(search_query, max_results=6)
                if not web_results:
                    return "I could not retrieve web results right now. Please try again."

                # Build context with numbered references
                refs_lines = []
                for idx, item in enumerate(web_results, start=1):
                    refs_lines.append(f"[{idx}] {item['title']} — {item['href']}\n{item['body']}")
                refs_block = "\n\n".join(refs_lines)

                system_prompt = (
                    "You are an AI research assistant. Use the provided web search results to answer the user query. "
                    "Synthesize concisely, cite sources inline like [1], [2] where relevant, and include a brief summary."
                )
                messages = [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Query: {search_query}\n\nWeb Results:\n{refs_block}"}
                ]
            else:
                # Normal chat
                self.history.append({"role": "user", "content": text})
                messages = self.history.copy()

            # Make API request using OpenAI client
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                extra_headers={
                    "HTTP-Referer": "https://your-site-url.com",  # Replace with your actual site URL if needed
                    "X-Title": "Study Planner",  # Replace with your site name if needed
                },
                extra_body={}
            )
            ai_response = completion.choices[0].message.content

            # Add to history
            self.history.append({"role": "assistant", "content": ai_response})

            return ai_response
        except Exception as e:
            print(f"Error generating response: {e}")
            return "I'm sorry, I encountered an error processing your request."