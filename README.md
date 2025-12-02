# Wazuh AI Threat Analysis

This is an example program to explore about the capability of AI in analyzing security logs, especially Wazuh.

## Requirements
- Python 3
- Ollama. [reference](https://ollama.com/)
- Wazuh archive logs. [reference](https://documentation.wazuh.com/current/user-manual/manager/event-logging.html#archiving-event-logs)

## Setup
1. Clone this repo
2. Create virtual environment
```
python3 -m venv .venv
```
3. Activate the venv
```
source .venv/bin/activate
```
4. Install dependencies
```
pip install -r requirements
```
5. Download the Wazuh archive log files to `./logs/archives.json`

## How to Use
1. If it is the first time to run the code or you want to update the vector database, set the `INIT_VECTOR` environment variable to `1`
```
INIT_VECTOR=1 python assistant.py
```
2. Enjoy the chat session!
3. Next time you want to chat with the assistant, run without `INIT_VECTOR=1`
```
python assistant.py
```

## Notes
Please feel free to update the LLM or Embedding model in the code!
