## LlamaIndex RAG agent

Answers questions based on Obsidian folder.

### How to run:

1. Install Ollama

2. Pull model
```
ollama pull llama3.2:3b

ollama serve
```
3. Install the uv package manager

```
pip install uv
```
4. Install dependencies
```
uv add -r requirements.txt
```
5. Run agent!
```
python3 main.py
```
