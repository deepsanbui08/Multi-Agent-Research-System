# 🧠 Multi-Agent Research System

An AI-powered research automation tool where multiple specialized agents collaborate in a pipeline to **search, read, write, and critique** research reports automatically — powered by Mistral AI, LangChain, and Tavily.

---

## 🚀 Live Demo

👉 **[multi-agent-research-system-deep.streamlit.app](https://multi-agent-research-system-deep.streamlit.app/)**

---

## ✨ How It Works

Instead of one AI doing everything, four specialized agents work together in sequence:

| Step | Agent | Role |
|------|-------|------|
| 1 | 🔍 **Search Agent** | Uses Tavily API to search the web for recent and reliable information on the topic |
| 2 | 📄 **Reader Agent** | Picks the most relevant URL and scrapes the webpage using BeautifulSoup for deeper content |
| 3 | ✍️ **Writer Agent** | Combines search results and scraped content to generate a structured research report |
| 4 | 🧠 **Critic Agent** | Reviews the report, gives a score out of 10, and provides strengths and areas to improve |

> **In short:** You give it a topic → it searches → reads → writes → self-critiques → gives you a complete research report.

---

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| Python | Core language |
| LangChain | Agent orchestration framework |
| Mistral AI | Underlying LLM for all agents |
| Tavily API | Real-time web search |
| BeautifulSoup | Web scraping and content extraction |
| Streamlit | UI for running the pipeline and viewing results |

---

## 📁 Project Structure

```
Multi-Agent-Research-System/
├── agents.py          # Defines all four agents and writer/critic chains
├── pipeline.py        # Core pipeline logic connecting all agents
├── tools.py           # web_search (Tavily) and scrape_url (BeautifulSoup) tools
├── app.py             # Streamlit UI
├── .env               # API keys (never commit!)
├── requirements.txt   # Dependencies
└── README.md
```

---

## ⚙️ Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/deepsanbui08/Multi-Agent-Research-System.git
cd Multi-Agent-Research-System
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
.venv\Scripts\activate      # Windows
source .venv/bin/activate   # Mac/Linux
```

### 3. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the root directory:

```env
MISTRAL_API_KEY=your_mistral_api_key
TAVILY_API_KEY=your_tavily_api_key
```

- Get your Mistral API key at: https://console.mistral.ai
- Get your Tavily API key at: https://app.tavily.com

### 5. Run the App

**Streamlit UI (recommended):**
```bash
python -m streamlit run app.py
```

**Terminal only:**
```bash
python pipeline.py
```

---

## 🖥️ UI Features

- 📥 Topic input with a single run button
- ⚙️ Live step status indicators for each agent
- 📑 4 tabs — Final Report, Critic Feedback, Search Results, Scraped Content
- ⬇️ Download the final report as a `.md` file

---

## 📊 Output Format

The Writer Agent structures the report as:

- **Introduction**
- **Key Findings** (minimum 3 well-explained points)
- **Conclusion**
- **Sources** (URLs found during research)

The Critic Agent responds in this format:

```
Score: X/10
Strengths:
- ...
Areas to Improve:
- ...
One line verdict:
...
```

---

## ⚠️ Note on Rate Limits

If you are on Mistral's free tier, you may encounter **429 Rate Limit** errors. The pipeline includes automatic delays between steps to handle this. If errors persist, switch to a smaller model in `agents.py`:

```python
llm = ChatMistralAI(model="open-mistral-7b", temperature=0, max_retries=3)
```

---

## 👨‍💻 Author

**Deep Sanbui**
[GitHub](https://github.com/deepsanbui08) | [LinkedIn](https://www.linkedin.com/in/deep-sanbui-699814254)

