Rag API by Farbod Farhangfar

# RAG System

_By Farbod Farhangfar_

## Getting Started

To run the system, use Docker Compose in the same directory of the docker-compose.yaml:

```bash
docker compose up -d
```

Note: Make sure Docker is installed on your machine before running this.

Accessing the API
Once the system is running, open your browser and go to:
http://localhost:8000/docs

Here you will find the API documentation and can try out the available endpoints:

/eval — Answers questions based on the uploaded documents.

/eval (evaluation) — Runs the evaluation process to compare generated answers against the ground truth.

/uploadpdf — Allows you to upload PDF files as the source documents for answering questions.
