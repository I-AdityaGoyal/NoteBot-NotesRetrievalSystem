
# NoteBot - Notes Retrieval System 🚀

Imagine joining a company as a fresher or a working professional and needing to know about meeting details, projects, and other important company information. Asking one by one about the process can be tedious and time-consuming.

**NoteBot - Notes Retrieval System solves this problem by acting as a personalized chatbot for your uploaded PDFs, and YouTube video transcripts, making information retrieval seamless and efficient.

## Project Live at Hugging Face Spaces 🤗
```
https://huggingface.co/spaces/I-AdityaGoyal/NoteBot

```

## Project Structure 📁

```plaintext
NoteBot-NotesRetrievalSystem/
│
├── app.py                # Main application file
├── pdf_processing.py     # PDF text extraction
├── youtube_processing.py # YouTube transcript extraction
├── faiss_indexing.py     # FAISS indexing and querying
├── utils.py              # Utility functions for environment variables, API querying, etc.
├── pdf_generator.py      # PDF generation from responses
├── text_to_speech.py     # Text-to-speech functionality
├── requirements.txt      # Python dependencies
├── .env                  # Environment variables file
└── .gitignore             # Git ignore file

```

## Getting Started 🛠️

### Prerequisites

1. Python 3.6 or higher
2. Streamlit
3. Hugging Face API key (available for free on the [Hugging Face website](https://huggingface.co/))

### Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/I-AdityaGoyal/NoteBot-NotesRetrievalSystem.git
    cd NoteBot-NotesRetrievalSystem
    ```

2. Create a virtual environment and activate it:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Replace your Hugging Face API key in the `.env` file. You can get a free key from the [Hugging Face website](https://huggingface.co/).

### Running the Application

To run the Streamlit application, use the following command:
```bash
streamlit run app.py
```

## Acknowledgements 🙏

- Special thanks to my mentor, Harsh Sir, for the idea and guidance.
