# ResearchMind - Multi-Agent AI Research System

A sophisticated, production-ready research automation system powered by Google Gemini and LangChain. Leverages multiple AI agents to conduct comprehensive research, synthesize findings, and provide quality feedback—all with a premium dark-themed interface.

[![Live Demo on Hugging Face](https://img.shields.io/badge/🤗-Live%20Demo-blue)](https://huggingface.co/spaces/kaifyyy06/research-mind)

![ResearchMind Banner](https://img.shields.io/badge/AI-Research-orange) ![Python](https://img.shields.io/badge/Python-3.9+-blue) ![FastAPI](https://img.shields.io/badge/FastAPI-Latest-green) ![Gemini](https://img.shields.io/badge/Google%20Gemini-API-red)

## ⚡ Quick Start

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/kaifm9427-wq/MULTI-AGENT-RESARCH-SYSTEM.git
    cd "MULTI-AGENT-RESARCH-SYSTEM"
    ```

2.  **Set up the environment:**
    Create a virtual environment and install the dependencies.
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r backend/requirements.txt
    ```

3.  **Add your API keys:**
    Create a `.env` file in the `backend` directory and add your `GEMINI_API_KEY` and `TAVILY_API_KEY`.
    ```
    GEMINI_API_KEY="your_gemini_api_key"
    TAVILY_API_KEY="your_tavily_api_key"
    ```

4.  **Run the application:**
    ```bash
    python start.py
    ```
    Now, open your browser and go to `http://localhost:8000`.

## 🚀 Key Features

- **Multi-Agent Pipeline**: Search → Read → Write → Critique workflow
- **AI-Powered Research**: Google Gemini 1.5 Flash
- **Web Integration**: Real-time web search via Tavily API
- **Modern UI**: Clean and responsive interface.
- **Production Ready**: Built with FastAPI.

## 📁 Project Structure

```
.
├── Dockerfile
├── README.md
├── backend
│   ├── __init__.py
│   ├── agents.py
│   ├── pipeline.py
│   ├── requirements.txt
│   ├── server.py
│   └── tools.py
├── frontend
│   ├── app.js
│   ├── index.html
│   ├── package.json
│   └── styles.css
└── start.py
```

## 🛠️ Installation

### Prerequisites
- Python 3.9 or higher
- [Google Gemini API key](https://aistudio.google.com/app/apikey)
- [Tavily API key](https://tavily.com/)

### Step 1: Clone the Repository
```bash
git clone https://github.com/kaifm9427-wq/MULTI-AGENT-RESARCH-SYSTEM.git
cd MULTI-AGENT-RESARCH-SYSTEM
```

### Step 2: Set Up Python Environment
Create and activate a virtual environment.
```bash
python3 -m venv .venv
source .venv/bin/activate  # For macOS/Linux
# .venv\Scripts\activate  # For Windows
```

### Step 3: Install Dependencies
```bash
pip install -r backend/requirements.txt
```

### Step 4: Configure API Keys
Create a `.env` file in the `backend` directory.
```bash
touch backend/.env
```
Now, open `backend/.env` and add your API keys in the following format:
```
GEMINI_API_KEY="your_gemini_api_key"
TAVILY_API_KEY="your_tavily_api_key"
```

### Step 5: Run the Application
```bash
python start.py
```
The application will be available at `http://localhost:8000`.

## 🐳 Docker
You can also run this project using Docker.

1.  **Build the Docker image:**
    ```bash
    docker build -t multi-agent-research-system .
    ```

2.  **Run the Docker container:**
    Make sure to replace the placeholder API keys with your actual keys.
    ```bash
    docker run -p 8000:8000 
      -e GEMINI_API_KEY="your_gemini_api_key" 
      -e TAVILY_API_KEY="your_tavily_api_key" 
      multi-agent-research-system
    ```
The application will be available at `http://localhost:8000`.

# ResearchMind - Multi-Agent AI Research System

A sophisticated, production-ready research automation system powered by Google Gemini and LangChain. Leverages multiple AI agents to conduct comprehensive research, synthesize findings, and provide quality feedback—all with a premium dark-themed interface.

![ResearchMind Banner](https://img.shields.io/badge/AI-Research-orange) ![Python](https://img.shields.io/badge/Python-3.9+-blue) ![FastAPI](https://img.shields.io/badge/FastAPI-Latest-green) ![Gemini](https://img.shields.io/badge/Google%20Gemini-API-red)

## ⚡ Quick Start (30 Seconds)



```bash
cd "multi agent system"
python start.py
# Open: http://localhost:8000
```

## 🚀 Key Features

- **Multi-Agent Pipeline**: Search → Read → Write → Critique workflow
- **AI-Powered Research**: Google Gemini 1.5 Flash with auto-fallback for free tier
- **Web Integration**: Real-time web search via Tavily API
- **Premium UI**: Dark theme with glassmorphism effects, smooth animations
- **Production Ready**: Error handling, retry logic, rate limit management
- **Fully Responsive**: Desktop-optimized two-column layout


## 📁 Project Structure

```
researchmind/
├── start.py                     # 🚀 Run this to start server
├── start.sh                     # 🚀 Or run this (bash)
├── QUICKSTART.md                # ⚡ Quick start guide
├── frontend/                    # Frontend assets
│   ├── index.html              # Premium dark-themed UI
│   ├── app.js                  # JavaScript logic & animations
│   ├── styles.css              # Custom CSS + Tailwind
│   └── package.json            # Frontend metadata
├── backend/                     # Python backend
│   ├── server.py               # FastAPI application
│   ├── pipeline.py             # 4-agent orchestration
│   ├── agents.py               # LLM configuration
│   ├── tools.py                # Web search & scraping
│   ├── requirements.txt         # Python dependencies
│   ├── .env                    # API credentials (git-ignored)
│   └── tests/
│       └── test_premium_ui.py  # Comprehensive test suite
├── config/
│   └── .env.example            # Environment template
├── scripts/
│   └── RUN_ME.sh               # Convenient startup script
├── vercel.json                 # Vercel deployment config
├── pyproject.toml              # Python project metadata
└── .gitignore                  # Git exclusions
```

## 🛠️ Installation

### Prerequisites
- Python 3.9 or higher
- Gemini API key (free tier available)
- Tavily API key (free tier available)

### Step 1: Clone & Navigate
```bash
git clone https://github.com/yourusername/researchmind.git
cd researchmind
```

### Step 2: Setup Python Environment
```bash
# Create virtual environment
python3 -m venv .venv

# Activate it
source .venv/bin/activate  # macOS/Linux
# or
.venv\Scripts\activate  # Windows
```

### Step 3: Install Dependencies
```bash
pip install -r backend/requirements.txt
```

### Step 4: Configure API Keys
```bash
# Copy template
cp config/.env.example backend/.env

# Edit with your keys
nano backend/.env
```

Get your keys:
- **Gemini API**: https://makersuite.google.com/app/apikey
- **Tavily API**: https://tavily.com

### Step 5: Verify Installation
```bash
# Optional: Run test suite
python backend/tests/test_premium_ui.py
```

## 🚀 Running the System

### Quick Start
```bash
bash scripts/RUN_ME.sh
```

### Manual Start
```bash
cd backend
uvicorn server:app --host 0.0.0.0 --port 8000 --reload
```

Then open your browser to: **http://localhost:8000**

## 📝 Usage

1. **Enter Topic**: Type a research topic in the input field
2. **Run Pipeline**: Click "Run Research Pipeline"
3. **Watch Progress**: See animated agent cards complete sequentially
4. **Review Results**: Read synthesized report with source links
5. **Get Feedback**: View AI quality critique of the research

### Example Queries
- "Latest breakthroughs in quantum computing 2025"
- "AI regulatory changes in Europe"
- "Sustainable energy solutions for developing nations"

### Example Queries
- "Latest breakthroughs in quantum computing 2025"
- "AI regulatory changes in Europe"
- "Sustainable energy solutions for developing nations"

## 🔧 API Reference

### Base URL
```
http://localhost:8000
```

### Endpoints

#### `GET /`
Serves the premium frontend UI.

**Response**: HTML page

---

#### `GET /health`
Health check endpoint for server status.

**Response**:
```json
{
  "status": "ok"
}
```

---

#### `POST /api/run`
Execute the multi-agent research pipeline.

**Request Body**:
```json
{
  "query": "Your research topic",
  "use_gemini": false
}
```

**Response**:
```json
{
  "steps_completed": "completed",
  "sources": [
    {
      "title": "Source title",
      "url": "https://example.com",
      "snippet": "Relevant excerpt..."
    }
  ],
  "report": "Comprehensive synthesized research report...",
  "sources_list": ["url1", "url2", "url3"],
  "feedback": "Quality assessment of the research..."
}
```

---

#### `GET /styles.css`
Frontend stylesheet with Tailwind CSS and custom animations.

---

#### `GET /app.js`
Frontend JavaScript with API integration and animations.

## 🎨 UI Design

### Color Scheme
- **Primary**: `#0a0a0a` (Deep black)
- **Cards**: `#1a1a1a` (Dark gray)
- **Accent**: `#ff8c42` (Vibrant orange)
- **Success**: `#10b981` (Emerald green)

### Features
- **Glassmorphism**: Frosted glass effect on cards
- **Animations**: Smooth transitions, staggered agent reveals
- **Responsive**: Works on all modern browsers
- **Dark Theme**: Easy on the eyes, modern aesthetic

## ⚙️ How It Works

### 4-Agent Pipeline

1. **Search Agent** 📡
   - Queries Tavily API for relevant sources
   - Returns top 3 articles

2. **Reader Agent** 📖
   - Scrapes content from URLs
   - Extracts key information

3. **Writer Agent** ✍️
   - Synthesizes research into coherent report
   - Uses Gemini 1.5 Flash with 2048 token limit

4. **Critic Agent** 🎯
   - Reviews report quality
   - Provides constructive feedback

### Error Handling
- **Auto-retry** with exponential backoff
- **Free-tier fallback**: Uses local synthesis if API rate limited
- **Timeout protection**: 5-second scrape limit
- **Input validation**: Empty query checks

## 🔑 Environment Variables

```env
# Google Gemini API (free tier)
GEMINI_API_KEY=your_key_here

# Tavily Web Search API
TAVILY_API_KEY=your_key_here
```

## 🐛 Troubleshooting

### "API Key not found"
- Check `.env` file exists in `backend/` directory
- Verify keys are correctly pasted (no extra spaces)
- Run `echo $GEMINI_API_KEY` to test

### "Port 8000 already in use"
```bash
# Find process using port 8000
lsof -i :8000

# Kill it
kill -9 <PID>

# Or use different port
uvicorn backend.server:app --port 8001
```

### "Frontend not loading"
- Ensure server is running (`http://localhost:8000`)
- Check browser console for errors (F12)
- Clear browser cache (Ctrl+Shift+Delete)

### "Research pipeline timing out"
- Check internet connection
- Verify Tavily API key is valid
- Try simpler query
- Check rate limits on API dashboard

## 📦 Technology Stack

| Component | Technology |
|-----------|-----------|
| Frontend | HTML5, Tailwind CSS, Vanilla JavaScript |
| Backend | FastAPI, Uvicorn, Python 3.9+ |
| LLM | Google Gemini 1.5 Flash |
| Search | Tavily API |
| Parsing | BeautifulSoup4, lxml |
| Framework | LangChain |

## 🚀 Deployment

### Vercel (Recommended for Frontend)
```bash
vercel deploy
```

### Railway
```bash
railway up
```

### Heroku
```bash
heroku login
heroku create researchmind
git push heroku main
```

### AWS EC2
```bash
# Connect via SSH
ssh -i key.pem ubuntu@your-instance.aws.com

# Install and run
git clone <repo>
cd researchmind
bash scripts/RUN_ME.sh
```

## 📄 Configuration Files

### `pyproject.toml`
Python project metadata, dependencies, and tool configurations.

### `vercel.json`
Vercel deployment settings for frontend hosting.

### `.gitignore`
Specifies files to exclude from version control (.env, __pycache__, .venv, etc.)

## 🧪 Testing

Run comprehensive verification:
```bash
python backend/tests/test_premium_ui.py
```

Tests include:
- ✅ Project structure validation
- ✅ Dependency checks
- ✅ Environment configuration
- ✅ Server startup
- ✅ API endpoints
- ✅ Frontend rendering
- ✅ CSS/JS loading
- ✅ Research pipeline
- ✅ Integration tests

## 📚 Documentation

- **API Documentation**: Run server, visit `http://localhost:8000/docs`
- **Code Comments**: Extensively documented Python modules
- **Examples**: See usage queries above

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing`)
3. Commit changes (`git commit -m "Add amazing feature"`)
4. Push to branch (`git push origin feature/amazing`)
5. Open Pull Request

## 📋 License

MIT License - See LICENSE file for details

## 🙋 Support

- **Issues**: GitHub Issues
- **Documentation**: Check README and inline code comments
- **Questions**: Open a Discussion on GitHub

## 🔗 Links

- **Homepage**: https://researchmind.dev
- **Repository**: https://github.com/yourusername/researchmind
- **API Keys**:
  - [Gemini API](https://makersuite.google.com/app/apikey)
  - [Tavily API](https://tavily.com)

---

## ✍️ Author

Made with ❤️ by **Mohammed Kaif**
*Galgotias University, B.TECH CSE*

**Built with ❤️ by MOHAMMED KAIF**

*Transform research with AI. No more manual searching—just instant, synthesized insights.*
Results Display → Report + Sources + Assessment

