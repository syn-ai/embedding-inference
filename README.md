# Embedding Module

This module provides an embedding service for text using the tiktoken library. It's designed to be used as part of a larger system for natural language processing tasks.

## Features

- Text tokenization and embedding generation
- Token usage tracking
- Cosine similarity calculation between embeddings
- FastAPI-based API for embedding requests

## Local Installation

1. Ensure you have Python 3.10 or later installed.
2. Clone this repository.
3. Navigate to the `modules/embedding` directory.
4. Run the installation script:

   ```
   ./install_embedding.sh
   ```

   This script will create a virtual environment, install dependencies, and set up the `.env` file.

## Installing from the Module Registrar

1. make a get request to REGISTRAR_URL/modules/embedding and decode the base64 encoded json response and save it to modules/embedding/setup_embedding.py
```
import requests
import base64
import os

url = os.getenv("REGISTRAR_URL") + "/modules/embedding"

payload = {}
headers = {}

response = requests.request("GET", url, headers=headers, data=payload)

decoded_response = base64.b64decode(response.text).decode('utf-8')

os.makedirs("modules/embedding", exist_ok=True)

with open("modules/embedding/setup_embedding.py", "w", encoding="utf-8") as f:
    f.write(decoded_response)
```

2. run the setup_embedding.py file to unpack the files

```
python modules/embedding/setup_embedding.py
```

3. run the install_embedding.sh script to install the module

```
./install_embedding.sh
```

4. run the start_embedding.sh script to start the embedding service

```
./start_embedding.sh
```

## Configuration

The module uses environment variables for configuration. Copy the `.env.example` file to `.env` and adjust the values as needed:

