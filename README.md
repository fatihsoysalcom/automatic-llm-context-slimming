# Automatic LLM Context Slimming

This example demonstrates the concept of 'context bloat' in Large Language Model (LLM) interactions and a simple automatic slimming strategy. It simulates an LLM conversation where messages accumulate, increasing the context size. A `LLMContextManager` class automatically truncates older messages to keep the total context within a predefined character limit, preventing performance degradation and increased costs.

## Language

`python`

## How to Run

Save the code as `main.py` and run it from your terminal:
`python main.py`

## Original Article

This example accompanies the Turkish article: [Claude Kod Kurulumunuz Neden Şişmanlar ve Otomatik Zayıflama Yöntemleri Nelerdir?](https://fatihsoysal.com/blog/claude-kod-kurulumunuz-neden-sismanlar-ve-otomatik-zayiflama-yontemleri-nelerdir/).

## License

MIT — see [LICENSE](LICENSE).
