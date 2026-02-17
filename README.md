# 🏠 Real Estate Research Tool

A powerful AI-powered research assistant that helps you analyze real estate information from web sources using RAG (Retrieval-Augmented Generation) technology.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://your-app-url.streamlit.app)

![product screenshot](resources/image.png)

## ✨ Features

- 🔍 **Web Scraping**: Extract content from multiple URLs simultaneously
- 🧠 **AI-Powered Answers**: Uses Groq's LLaMA 3.3 70B model for intelligent responses
- 📚 **Vector Database**: ChromaDB for efficient document storage and retrieval
- 🎯 **Semantic Search**: Find relevant information using HuggingFace embeddings
- 💬 **Interactive UI**: Clean Streamlit interface for easy interaction
- 🔗 **Source Citations**: Provides source URLs for transparency

## 🚀 Live Demo

**[Try it live here!](https://your-app-url.streamlit.app)** *(Update this link after deployment)*

## 🛠️ Tech Stack

- **LLM**: Groq (LLaMA 3.3 70B Versatile)
- **Framework**: LangChain 1.2.10
- **Vector Store**: ChromaDB 1.5.0
- **Embeddings**: HuggingFace (all-MiniLM-L6-v2)
- **Web Interface**: Streamlit 1.54.0
- **Python**: 3.13.5

## 📋 Prerequisites

- Python 3.8+
- Groq API Key ([Get one here](https://console.groq.com/keys))

## 🔧 Local Setup

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/REALESTATE-ASSISTANT.git
cd REALESTATE-ASSISTANT
```

### 2. Create Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root:

```bash
GROQ_API_KEY=your_groq_api_key_here
```

### 5. Run the Application

```bash
streamlit run main.py
```

The app will open in your browser at `http://localhost:8501`

## ☁️ Deploy to Streamlit Cloud

### Step 1: Push to GitHub

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/yourusername/REALESTATE-ASSISTANT.git
git push -u origin main
```

### Step 2: Deploy on Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with your GitHub account
3. Click **"New app"**
4. Select your repository: `REALESTATE-ASSISTANT`
5. Set main file path: `main.py`
6. Click **"Deploy"**

### Step 3: Configure Secrets

1. In Streamlit Cloud dashboard, go to **App settings** → **Secrets**
2. Add your API key:

```toml
GROQ_API_KEY = "your_groq_api_key_here"
```

3. Click **"Save"** and the app will restart automatically

## 📖 Usage

### Recommended URLs (Scraper-Friendly)

✅ **Wikipedia**
```
https://en.wikipedia.org/wiki/Real_estate
https://en.wikipedia.org/wiki/Mortgage_loan
```

✅ **Investopedia**
```
https://www.investopedia.com/terms/r/realestate.asp
```

### URLs to Avoid

❌ **News Sites with Paywalls** (will be blocked):
- Wall Street Journal, CNBC, Bloomberg, New York Times

### How to Use

1. **Enter URLs** in the sidebar (up to 3)
2. Click **"Process URLs"** to load and index the content
3. **Ask questions** in the text input
4. Get **AI-generated answers** with source citations

## 🐛 Troubleshooting

### "Access Denied" or "404 Error"

**Cause**: Website is blocking automated scraping  
**Solution**: Use scraper-friendly sites (Wikipedia, Investopedia, .gov sites)

### "Vector database is not initialized"

**Cause**: URLs haven't been processed yet  
**Solution**: Click "Process URLs" before asking questions

## 📁 Project Structure

```
REALESTATE-ASSISTANT/
├── main.py                 # Streamlit web interface
├── rag.py                  # RAG pipeline implementation
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (local only)
├── .gitignore             # Git ignore rules
├── .streamlit/
│   ├── config.toml        # Streamlit configuration
│   └── secrets.toml.example  # Secrets template
└── README.md              # This file
```

## 📄 License

This project is open source and available under the MIT License.

---

**Made with ❤️ using LangChain, Groq, and Streamlit**