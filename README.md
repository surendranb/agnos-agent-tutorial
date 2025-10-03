# Daily AI Report System

A multi-agent system built with AgentOS that demonstrates key concepts: workflows, teams, memory, and knowledge management. Agents research **AI news and research** from three sources (HackerNews, Reddit r/artificial, ArXiv), then generate daily reports and build searchable knowledge for trend analysis.

## How It Works

This system demonstrates core AgentOS concepts through a practical example:

1. **Data Collection** - Agents fetch AI news from 3 sources: HackerNews (top AI stories), Reddit r/artificial (AI discussions), ArXiv (AI research papers)
2. **LLM Processing** - OpenRouter models (Grok-4-fast) process and summarize the collected AI content  
3. **Knowledge Storage** - Each day's content gets chunked using SentenceTransformer embeddings and stored in LanceDB vector database
4. **Memory Creation** - Agents store coordination patterns and preferences in SQLite database
5. **Team Coordination** - Team orchestrates sequential agent execution with shared context
6. **File Generation** - Agents save daily research files and reports using FileTools
7. **Knowledge Accumulation** - Daily content builds searchable knowledge base for long-term trend analysis

## 🚀 Features

- **Workflow Execution** - Automated sequence of AI research tasks
- **Multi-Source AI Data** - HackerNews AI stories, Reddit r/artificial discussions, ArXiv AI papers
- **Team Memory** - Agents retain execution patterns and coordination preferences
- **Knowledge Accumulation** - Vector database builds searchable AI knowledge over time
- **Trend Analysis** - Historical data enables long-term AI trend identification
- **File Management** - Organized daily outputs in separate directories

## 📋 Prerequisites

- Python 3.8+
- OpenRouter API key (for AI model access)

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/surendranb/agnos-agent-tutorial.git
   cd agnos-agent-tutorial
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp .env.sample .env
   # Edit .env and add your OpenRouter API key
   ```

4. **Get your OpenRouter API key**
   - Visit [OpenRouter](https://openrouter.ai/keys)
   - Create an account and generate an API key
   - Add it to your `.env` file

## 🎯 Usage

### Start the System
```bash
python app.py
```

The system will start on `http://localhost:7777`

### Run Workflow
1. Open the dashboard at `http://localhost:7777`
2. Navigate to "Workflows"
3. Trigger "Daily AI Report Workflow"

### Chat with Trend Analyst
1. Go to "Agents" in the dashboard
2. Chat with "Trend Analyst" for AI trend insights

## 📁 Output Structure

```
reports/           # Final daily reports
research/          # Raw research data (HN, Reddit, ArXiv)
trends/            # Trend analysis reports (on-demand)
```

## 🤖 Agents

- **HN Reddit Researcher** - Gathers AI news from HackerNews and Reddit
- **ArXiv Researcher** - Finds latest AI research papers
- **Report Writer** - Creates concise daily intelligence reports
- **Trend Analyst** - Analyzes long-term AI trends (chat-based)

## 🔄 Workflow

1. **Daily Report Workflow**: Executes team of 3 agents sequentially to research AI developments
   - **HN Reddit Researcher**: Fetches top AI stories from HackerNews + AI discussions from Reddit r/artificial → `research/hn_reddit_YYYY-MM-DD.md`
   - **ArXiv Researcher**: Searches latest AI research papers from ArXiv → `research/arxiv_YYYY-MM-DD.md`  
   - **Report Writer**: Synthesizes AI research into daily report → `reports/daily_report_YYYY-MM-DD.md`

2. **Trend Analysis**: Individual agent available for chat-based AI trend analysis
   - Searches accumulated AI knowledge base for historical patterns
   - Identifies emerging AI themes, recurring topics, and technology evolution
   - Generates comprehensive trend analysis reports on request

## 🧠 AgentOS Concepts Demonstrated

- **Team Memory** - SQLite database stores agent coordination patterns and preferences
- **Knowledge Base** - LanceDB vector database with SentenceTransformer embeddings for content search
- **Workflow Orchestration** - Sequential execution of agent tasks with shared context
- **Tool Integration** - File operations, API calls, and database interactions
- **Memory Persistence** - Agent experiences retained across workflow executions

## 📈 Knowledge Accumulation System

This system demonstrates how daily data collection builds long-term analytical capabilities:

### **Daily Knowledge Building:**
- **Day 1**: Collects AI news → Stores in vector database → Creates searchable embeddings
- **Day 2**: Adds new AI content → Expands knowledge base → Links related concepts
- **Day N**: Accumulated knowledge enables pattern recognition across time periods

### **Long-term Trend Analysis:**
- **Trend Analyst** searches accumulated knowledge using vector similarity
- **Historical patterns** emerge from daily AI news and research data
- **Topic evolution** tracked across HackerNews discussions, Reddit conversations, and research papers
- **Emerging themes** identified by analyzing content clusters over time

### **Knowledge Sources:**
1. **HackerNews** - Industry AI news, product launches, company developments
2. **Reddit r/artificial** - Community discussions, AI tool reviews, trend observations  
3. **ArXiv** - Latest AI research papers, methodologies, academic breakthroughs

The longer the system runs, the more valuable the trend analysis becomes as it can identify patterns across weeks, months, and years of AI development data.

## 🛡️ Data Storage

- All databases and files stored locally
- External API calls: OpenRouter (LLM), HackerNews, Reddit, ArXiv
- Generated content based on publicly available information

## 📝 License

MIT License - see LICENSE file for details

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📞 Support

- Open an issue for bug reports
- Discussions for questions and ideas
- Check the AgentOS documentation for advanced configuration

---

**Tutorial Purpose**: This project demonstrates AgentOS capabilities including multi-agent workflows, team coordination, memory systems, and knowledge management. Use it as a template for building your own agent systems.

Built with [AgentOS](https://github.com/agnos-ai/agnos)
