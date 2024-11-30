# LightRAG Query Interface

A Streamlit-based web interface for querying text using LightRAG (Retrieval-Augmented Generation) with Jina AI embeddings. This application provides an intuitive way to perform various types of semantic searches on your text corpus.

## Features

- Multiple query modes:
  - Hybrid (combines local and global search)
  - Naive (simple text matching)
  - Local (context-aware search)
  - Global (semantic search)
- Interactive web interface
- Collapsible context sections showing:
  - Entities
  - Relationships
  - Source documents
- Environment variable support for both local development and cloud deployment

## Prerequisites

- Python 3.11 or higher
- A Jina AI API key
- A Naga API key

## Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd light-rag-ui
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root with your API keys:
```env
JINA_API_KEY=your_jina_api_key_here
NAGA_API_KEY=your_naga_api_key_here
```

## Usage

### Local Development

Run the Streamlit app locally:
```bash
streamlit run app.py
```

The app will be available at `http://localhost:8501`

### Cloud Deployment

1. Push your code to GitHub
2. Go to [Streamlit Cloud](https://share.streamlit.io)
3. Deploy your app by connecting to your GitHub repository
4. Add your environment variables in Streamlit Cloud's secrets management:
```toml
JINA_API_KEY = "your_jina_api_key"
NAGA_API_KEY = "your_naga_api_key"
```

## Project Structure

```
light-rag-ui/
├── app.py              # Streamlit web interface
├── query.py            # LightRAG and embedding configuration
├── requirements.txt    # Project dependencies
├── .env               # Local environment variables (not in repo)
├── .gitignore         # Git ignore rules
└── bible/             # Working directory for LightRAG (created automatically)
```

## Query Modes

- **Hybrid**: Combines both local and global search strategies for comprehensive results
- **Naive**: Simple text matching without semantic understanding
- **Local**: Searches within specific context windows
- **Global**: Semantic search across the entire corpus

## Environment Variables

The application uses two main environment variables:

- `JINA_API_KEY`: Your Jina AI API key for embeddings
- `NAGA_API_KEY`: Your Naga API key for LLM completions

These can be set either in a local `.env` file for development or in Streamlit Cloud's secrets management for deployment.

## Acknowledgments

- [LightRAG](https://github.com/HKUDS/LightRAG) for the RAG implementation
- [Jina AI](https://jina.ai/) for embeddings
- [Streamlit](https://streamlit.io/) for the web interface