import collections

class LLMContextManager:
    """
    Manages the conversational context for an LLM interaction, simulating context bloat
    and providing a method for automatic slimming based on character count.
    """
    def __init__(self, max_context_chars=1000):
        self.interactions = collections.deque() # Stores (role, message) tuples
        self.current_char_count = 0
        self.max_context_chars = max_context_chars
        print(f"Context Manager initialized with max_context_chars: {self.max_context_chars}")

    def add_interaction(self, role: str, message: str):
        """
        Adds a new interaction (message) to the context and triggers automatic slimming.
        """
        # Each interaction contributes to the context size, including role and newline
        interaction_str = f"{role}: {message}\n"
        self.interactions.append((role, message))
        self.current_char_count += len(interaction_str)
        print(f"\nAdded interaction. Current context size: {self.current_char_count} chars.")
        # Automatically slim if context exceeds limit after adding, preventing bloat.
        self._auto_slim()

    def _auto_slim(self):
        """
        Automatically slims the context if its character count exceeds the maximum limit.
        This simulates removing older, less relevant information to prevent context bloat.
        The oldest interactions are removed first.
        """
        if self.current_char_count <= self.max_context_chars:
            return

        print(f"Context bloat detected! Current size ({self.current_char_count} chars) "
              f"exceeds max ({self.max_context_chars} chars). Slimming...")

        # Keep removing the oldest interactions until the context is within limits
        while self.current_char_count > self.max_context_chars and len(self.interactions) > 1:
            oldest_role, oldest_message = self.interactions.popleft()
            oldest_interaction_str = f"{oldest_role}: {oldest_message}\n"
            self.current_char_count -= len(oldest_interaction_str)
            print(f"  - Removed oldest interaction: '{oldest_message[:30]}...' (new size: {self.current_char_count})")

        print(f"Context slimmed. New context size: {self.current_char_count} chars.")
        if self.current_char_count > self.max_context_chars:
            print("Warning: Context still exceeds max even after removing all but the latest interaction. "
                  "Consider increasing max_context_chars or shortening individual messages.")

    def get_full_context(self) -> str:
        """
        Returns the current full context as a single string, ready to be sent to an LLM.
        """
        if not self.interactions:
            return ""
        return "\n".join([f"{role}: {msg}" for role, msg in self.interactions])


# --- Simulation --- 
if __name__ == "__main__":
    # Initialize the context manager with a relatively small context limit (e.g., 300 characters)
    # to easily demonstrate bloat and slimming in action.
    context_manager = LLMContextManager(max_context_chars=300)

    print("\n--- Phase 1: Adding interactions, context grows and triggers initial slimming ---")
    context_manager.add_interaction("system", "You are a helpful assistant.")
    context_manager.add_interaction("user", "Hello, how are you today? I have a long question about Python programming and its best practices for large-scale applications. Specifically, I'm interested in design patterns, dependency injection, and asynchronous programming paradigms.")
    context_manager.add_interaction("assistant", "I'm doing well, thank you! Python is a great choice. For large-scale applications, you'll want to focus on modularity, clear interfaces, and maintainable code. Let's break down your interests.")

    print("\n--- Current Context (after initial additions, potentially slimmed) ---")
    print(f"Total characters: {context_manager.current_char_count}")
    print(context_manager.get_full_context())

    print("\n--- Phase 2: Adding more interactions, forcing more aggressive slimming ---")
    context_manager.add_interaction("user", "That's a good overview. Could you show a simple Python example for constructor injection without any specific framework? Just a couple of classes demonstrating the concept.")
    context_manager.add_interaction("assistant", "Certainly. Here's a basic example of constructor injection in Python. We'll define a 'Service' that depends on a 'Repository' to fetch data. The 'Repository' is injected into the 'Service' during its creation.")
    context_manager.add_interaction("user", "Okay, I understand. What about asynchronous programming? Can you give an example using `asyncio` for a simple web request?")
    context_manager.add_interaction("assistant", "Asynchronous programming in Python, often with `asyncio`, allows your program to perform multiple operations concurrently without blocking the main thread. This is great for I/O-bound tasks like network requests. Here's a simple `asyncio` example fetching a URL.")
    context_manager.add_interaction("user", "This is very helpful! I appreciate the clear explanations and examples. I'll try to implement these concepts in my project. Thank you for your time and detailed responses.")
    context_manager.add_interaction("assistant", "You're most welcome! I'm glad I could assist. Feel free to ask if you have more questions as you implement these patterns. Happy coding!")

    print("\n--- Final Context (after extensive interactions and slimming) ---")
    print(f"Total characters: {context_manager.current_char_count}")
    print(context_manager.get_full_context())

    print("\n--- Demonstrating context size after further small additions ---")
    context_manager.add_interaction("user", "Just one more quick question: what's the difference between `async` and `await` keywords?")
    context_manager.add_interaction("assistant", "`async` defines a coroutine function, and `await` pauses its execution until an awaitable (like another coroutine or a Future) completes.")
    print(f"\nFinal context size: {context_manager.current_char_count} chars.")
    print(context_manager.get_full_context())
