# PDFChat — RAG-Powered Document Chat

PDFChat is a document question-answering application that lets users upload files and ask questions about their content. It combines a **Django web application** with a separate **FastAPI service** that executes the Retrieval-Augmented Generation (RAG) pipeline.

The system loads and chunks documents, retrieves relevant passages using a configurable search strategy, and uses a text-generation model to produce context-aware answers. Text generation can use a local Hugging Face model or a supported API provider such as **OpenRouter**.

## Features

- **User authentication:** Users can register, sign in, and work with their own documents and conversations.
- **Multiple file formats:** Supports PDF (`.pdf`), Markdown (`.md`), plain text (`.txt`), and CSV (`.csv`) files.
- **Configurable chunking:** Configure chunk size and overlap to control how documents are split before retrieval.
- **Configurable retrieval:** Choose **BM25**, **semantic search**, or **hybrid search**.
- **BM25 retrieval:** Finds relevant passages through keyword-based ranking.
- **Semantic retrieval:** Uses sentence embeddings to find passages with similar meaning.
- **Hybrid retrieval:** Combines lexical and semantic retrieval.
- **Flexible text generation:** Generate answers with a local Hugging Face model or through a supported API such as OpenRouter.
- **Admin RAG controls:** Administrators can configure chunk size, chunk overlap, and the retrieval strategy from the admin interface.
- **FastAPI RAG service:** Exposes an API endpoint for sending a query and file information to the RAG pipeline and receiving a generated answer.
- **Django web application:** Handles users, uploaded documents, conversations, and the web interface.
- **Document-grounded answers:** Retrieved passages are supplied as context to help the generator answer questions about the uploaded files.

## Architecture

PDFChat separates the user-facing application from the RAG execution service.

```text
                 User
                   |
                   v
           Django Web Application
      Authentication / Files / Chat UI
                   |
                   v
             FastAPI Service
              RAG API Request
                   |
                   v
            Load Documents
        PDF / TXT / Markdown / CSV
                   |
                   v
          Split into Chunks
       Configurable Size and Overlap
                   |
                   v
          Select Retrieval Strategy
          /          |          \
         v           v           v
       BM25       Semantic      Hybrid
                    Search    BM25 + Semantic
          \          |          /
                   v
           Relevant Passages
                   |
                   v
          Build Prompt + Context
                   |
                   v
          Text Generation Model
          /                    \
         v                      v
  Local Hugging Face       OpenRouter API
          \                    /
                   v
             Generated Answer
                   |
                   v
          Return Answer to Django
```

## RAG Pipeline

### 1. Document loading

The application supports the following formats:

| Format | Typical use |
|---|---|
| `.pdf` | Reports, guides, and other PDF documents |
| `.txt` | Plain-text notes and logs |
| `.md` | Markdown documentation and README files |
| `.csv` | Tabular data stored as comma-separated values |

CSV files require appropriate parsing so their rows and column values can be used as retrieval context. The usefulness of answers depends on the structure and content of the uploaded data.

### 2. Chunking

Loaded document content is split into smaller, overlapping chunks before retrieval. Chunk size affects how much text is stored in each chunk, while overlap preserves some surrounding context between neighboring chunks.

Administrators can change the chunk size and overlap through the RAG settings page. The exact values should be chosen based on the document types and retrieval quality you need.

### 3. Retrieval strategies

PDFChat supports three retrieval modes:

- **BM25:** Keyword-based retrieval. Useful when queries include exact terms, names, identifiers, or technical vocabulary.
- **Semantic search:** Embedding-based retrieval. Useful when the query and relevant passage express similar ideas using different words.
- **Hybrid search:** Combines BM25 and semantic retrieval to benefit from both keyword matching and semantic similarity.

The active strategy can be selected by an administrator through the RAG configuration interface.

### 4. Prompt construction

The retrieved passages are included in a prompt with the user's question and system instructions. This gives the generation model document context to use when answering.

### 5. Text generation

PDFChat can generate responses using either:

- **Local model:** A compatible Hugging Face Transformers model. The original configuration uses `Qwen/Qwen3-0.6B` as the default.
- **API model:** A supported text-generation API, including OpenRouter, when the required API configuration is provided.

The selected model/provider determines generation requirements, including internet access, credentials, hardware, and potential API costs. Keep API keys in environment variables rather than committing them to source control.

## Application Screenshots

PDFChat provides a document-based AI chat experience powered by Retrieval-Augmented Generation (RAG). The following screenshots showcase the application's user interface, document management features, conversational workflow, and administrative dashboard.

### 1. Home Page

The landing page introduces PDFChat and provides access to its core features.

**User View**

![User Home Page](assets/home_page.png)

**Admin View**

![Admin Home Page](assets/admin_home_page.png)

---

### 2. Authentication

PDFChat provides user authentication to give each user access to their own workspace.

#### Login

Existing users can sign in to access their documents and conversations.

![Login Page](assets/login_page.png)

#### Registration

New users can create an account to start using the application.

![Registration Page](assets/register_page.png)

---

### 3. Document Management

Users can upload and manage documents that serve as the knowledge base for their AI conversations.

#### Upload Documents

Upload supported document formats, including PDF, Markdown, plain-text (TXT), and CSV files.

![Upload Documents](assets/upload_file.png)

#### Uploaded Files

View the documents associated with your account and manage your personal document collection.

![Uploaded Files](assets/uploaded_files.png)

---

### 4. AI Conversations

PDFChat enables users to interact with their uploaded documents through a Retrieval-Augmented Generation (RAG) pipeline.

#### Conversations

Access and manage previous conversations in one place.

![Conversations](assets/conversations.png)

#### Chat with Your Documents

Ask questions about your uploaded documents and receive AI-generated answers based on the retrieved document context.

![Chat Interface](assets/chat.png)

---

### 5. Administration

The administration interface provides tools for managing and monitoring the application.

#### RAG Control Panel

Access the application's RAG management interface.

![RAG Control Panel](assets/controle_rag.png)

#### Admin Dashboard

View the administrative dashboard and its available management features.

![Admin Dashboard](assets/controle.png)

---

**Note:** Ensure that all screenshot files exist in the `assets/` directory and that their filenames match the paths referenced above. Adjust the descriptions if any feature is not yet implemented.


> Add a screenshot of the admin RAG settings page here when available.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Django | Web backend, authentication, document management, and conversations |
| FastAPI | API service for executing the RAG pipeline |
| LangChain | Document loading, text splitting, and retrieval components |
| Hugging Face Transformers | Local prompt formatting and text generation |
| Sentence Transformers | Text embeddings for semantic retrieval |
| BM25 | Keyword-based retrieval |
| OpenRouter API | API-based text generation |
| Qwen3-0.6B | Original default local generation model |
| HTML / CSS | Web interface |
| `uv` and Make | Dependency and development-command management |

## Getting Started

### Prerequisites

Install the following:

- Python version compatible with the project's dependencies
- `uv`
- Git
- Make

For local Hugging Face inference, ensure that your machine has enough memory for the selected model and an internet connection for initial model downloads. For API-based generation, configure the relevant provider credentials.

### 1. Clone the repository

Replace the placeholder with your repository URL:

```bash
git clone https://github.com/MohamedKirate-hub/PDFChat.git
cd PDFChat
```

### 2. Install dependencies

```bash
make install
```

This project uses the provided Makefile to install and synchronize dependencies with `uv`.

Follow the prompts to configure the account.

### 5. Configure environment variables

Create a local `.env` file if the project configuration uses `python-dotenv`. Add the variables required by your implementation, for example:

```dotenv
# Example only — use the variable names expected by your code.
OPENROUTER_API_KEY=your_api_key_here
RAG_API_URL=http://127.0.0.1:8011/api/query
```

Do not commit `.env` files or real API keys. If your code uses different environment-variable names, use those names instead.

### 6. Start the Django application

```bash
cd pdfRAG
uv run python3 manage.py runserver 
```

Open [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser.

### 7. Start the FastAPI RAG service

Start the FastAPI application using the module and ASGI variable defined in your project. 

```bash
cd pdfRAG
uv run python3 -m api_system
```

## FastAPI RAG Endpoint

The FastAPI service exposes the RAG pipeline through an HTTP API. Django can send the user's question and the relevant file paths or identifiers to the service, then use the returned answer in the conversation interface.

The exact endpoint, request schema, and response fields depend on the implementation. The example below illustrates a typical request shape; adapt it to the Pydantic models and endpoint defined in your code.

```http
POST /api/query
Content-Type: application/json
```

Example request body:

```json
{
  "query": "Summarize the key points in these documents.",
  "file_paths": ["path/to/document.pdf"],
  "model_name": "Qwen/Qwen3-0.6B" or "nvidia/nemotron-3.5-super-vl:free"
}
```

A typical successful response could look like:

```json
{
  "answer": "The documents describe ..."
}
```

These JSON fields are illustrative, not a guarantee of the current API contract. Check the FastAPI request and response models in the repository for the exact fields accepted by your implementation.

For local development, FastAPI's interactive API documentation is commonly available at `/docs` when enabled, for example [http://127.0.0.1:8011/docs](http://127.0.0.1:8011/docs).

## Admin RAG Configuration

The admin interface provides controls for tuning the RAG pipeline without requiring code changes for each setting.

Administrators can configure:

- **Chunk size:** Number of characters used for each chunk, according to the configured splitter.
- **Chunk overlap:** Number of overlapping characters between neighboring chunks.
- **Retrieval strategy:** Choose BM25, semantic, or hybrid retrieval.

Chunk size and overlap affect what context is available to retrieval. Retrieval strategy affects how candidate passages are ranked. Test different configurations against representative questions and documents rather than assuming one setting will work best for every dataset.

## Available Make Commands

| Command | Description |
|---|---|
| `make install` | Install and synchronize project dependencies |
| `make clean` | Remove `__pycache__` directories |

## How to Use PDFChat

1. Register or sign in to the Django application.
2. Upload one or more supported PDF, Markdown, text, or CSV files.
3. Open the chatbot and choose or create a conversation.
4. Ask a question about the uploaded documents.
5. The application sends the query to the RAG service, retrieves relevant passages, and generates an answer.
6. An administrator can adjust chunking and retrieval settings from the admin interface.
7. Review the answer against the source documents, especially when working with structured CSV data.

## Project Structure

The following is an illustrative structure; adjust it to reflect the actual files and directories in your repository.

```text
├── assets
├── Makefile
├── pdfRAG
│   ├── admin_controle
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── templates
│   │   │   ├── logs.html
│   │   │   └── rag_settings.html
│   │   ├── urls.py
│   │   └── views.py
│   ├── api_system
│   │   ├── __main__.py
│   │   └── rag_api.py
│   ├── chatbot
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── templates
│   │   │   ├── chatbot.html
│   │   │   ├── conversations.html
│   │   │   └── home.html
│   │   ├── urls.py
│   │   └── views.py
│   ├── data
│   │   ├── logs
│   │   │   └── logs.txt
│   │   ├── parameters
│   │   │   └── paramerters.json
│   │   └── uploads
│   │       ├── Supervisor.pdf
│   │       └── titanic.csv
│   ├── db.sqlite3
│   ├── loading
│   │   ├── apps.py
│   │   ├── forms.py
│   │   ├── models.py
│   │   ├── templates
│   │   │   ├── uploaded.html
│   │   │   └── upload_file.html
│   │   ├── urls.py
│   │   └── views.py
│   ├── manage.py
│   ├── pdfRAG
│   │   ├── asgi.py
│   │   ├── __init__.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── rag_system
│   │   ├── api_gen.py
│   │   ├── augemntation.py
│   │   ├── base.py
│   │   ├── chunking.py
│   │   ├── generation.py
│   │   ├── retrieval.py
│   │   └── system.py
│   ├── static
│   │   ├── admin_controle
│   │   │   ├── logs.css
│   │   │   └── rag_config.css
│   │   ├── chatbot
│   │   │   ├── chat.css
│   │   │   ├── conversations.css
│   │   │   └── home.css
│   │   ├── core
│   │   │   └── base.css
│   │   ├── loading
│   │   │   ├── uploaded_files.css
│   │   │   └── upload_file.css
│   │   └── user_auth
│   │       └── auth.css
│   ├── templates
│   │   ├── admin
│   │   │   └── index.html
│   │   ├── footer.html
│   │   ├── main.html
│   │   └── navbar.html
│   ├── user_auth
│   │   ├── apps.py
│   │   ├── forms.py
│   │   ├── models.py
│   │   ├── templates
│   │   │   └── login_register.html
│   │   ├── urls.py
│   │   └── views.py
│   └── utils
│       └── utils.py
├── pyproject.toml
├── README.md
└── uv.lock

```

The FastAPI entry point may be located in a separate module or directory depending on how your project is organized.

## Configuration Notes

- Keep API keys and other secrets in environment variables.
- Ensure the Django service can reach the FastAPI service at the configured URL.
- Make sure file paths passed to FastAPI are valid and accessible to the process running the RAG service.
- If Django and FastAPI run in separate containers or on different machines, a path on one service may not exist on the other; use a shared volume or another explicit file-transfer mechanism.
- Local model inference requires sufficient compute resources. API-based generation requires provider credentials and may incur usage costs.
- Verify the API request schema and model/provider configuration against your current source code.

## Project Objective

PDFChat is a practical project for exploring Retrieval-Augmented Generation and integrating it into a web application. It brings together document loading, CSV support, configurable chunking, BM25 and semantic retrieval, prompt construction, local or API-based text generation, Django-based user workflows, and a FastAPI service for RAG execution.
