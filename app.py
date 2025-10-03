"""
Daily AI Report System - Workflow Edition
Simple, deterministic daily report generation
"""
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from agno.tools.hackernews import HackerNewsTools
from agno.tools.file import FileTools
from agno.tools.reddit import RedditTools
from agno.tools.arxiv import ArxivTools
from agno.db.sqlite import SqliteDb
from agno.vectordb.lancedb import LanceDb
from agno.knowledge.embedder.sentence_transformer import SentenceTransformerEmbedder
from agno.knowledge.knowledge import Knowledge
from agno.os import AgentOS
from agno.workflow import Workflow, Step
from agno.team import Team

# Get today's date
TODAY = datetime.now().strftime("%Y-%m-%d")

# Create directories
reports_dir = Path("reports")
research_dir = Path("research")
trends_dir = Path("trends")
reports_dir.mkdir(exist_ok=True)
research_dir.mkdir(exist_ok=True)
trends_dir.mkdir(exist_ok=True)

# Single shared database to avoid ID conflicts
shared_db = SqliteDb(
    db_file="ai_system.db",
    memory_table="agent_memories",
    session_table="workflow_sessions"
)

knowledge_db = SqliteDb(db_file="ai_knowledge.db")

# Knowledge base
knowledge = Knowledge(
    name="AI News Knowledge Base",
    contents_db=knowledge_db,
    vector_db=LanceDb(
        uri="ai_vectors",
        table_name="knowledge_vectors",
        embedder=SentenceTransformerEmbedder(id="all-MiniLM-L6-v2", dimensions=384),
    ),
)

# Knowledge base builds dynamically as agents create content
print("🚀 Initializing Daily AI Report System...")

# Step 1: HN Reddit Researcher
hn_researcher = Agent(
    name="HN Reddit Researcher",
    model=OpenRouter(id="x-ai/grok-4-fast:free"),
    tools=[HackerNewsTools(), RedditTools(), FileTools(base_dir=research_dir)],
    db=shared_db,
    knowledge=knowledge,
    user_id="test@example.com",
    session_id=f"session_{TODAY}",
    enable_user_memories=True,
    search_knowledge=False,
    update_knowledge=True,
    instructions=f"""Get AI news from HackerNews and Reddit r/artificial for {TODAY}.

Steps:
1. Use get_top_hackernews_stories tool to get AI/ML stories from HackerNews
2. Use get_top_posts tool to get posts from Reddit subreddit r/artificial only
3. Use save_file tool to save results to EXACTLY this filename: "hn_reddit_{TODAY}.md"
4. Use add_to_knowledge tool to add file to knowledge base

CRITICAL: File must be named exactly "hn_reddit_{TODAY}.md" - do not change this filename.
ALWAYS create output file and add to knowledge base, even if no results found.

Output format:
# HackerNews AI Stories
- [Title](link) - Brief summary

# Reddit r/artificial Posts  
- [Title](link) - Brief summary""",
)

# Step 2: ArXiv Researcher
arxiv_researcher = Agent(
    name="ArXiv Researcher",
    model=OpenRouter(id="x-ai/grok-4-fast:free"),
    tools=[ArxivTools(), FileTools(base_dir=research_dir)],
    db=shared_db,
    knowledge=knowledge,
    user_id="test@example.com",
    session_id=f"session_{TODAY}",
    enable_user_memories=True,
    search_knowledge=False,
    update_knowledge=True,
    instructions=f"""Search ArXiv for AI research papers from last 2 days including {TODAY}:

Steps:
1. Use search_arxiv_and_return_articles tool to search categories cs.AI, cs.CL, cs.LG with query "artificial intelligence OR machine learning OR neural network"
2. Use save_file tool to save results to EXACTLY this filename: "arxiv_{TODAY}.md"
3. Use add_to_knowledge tool to add file to knowledge base

CRITICAL: File must be named exactly "arxiv_{TODAY}.md" - do not change this filename.
ALWAYS create output file and add to knowledge base, even if no results found.

Output format:
# Latest AI Research Papers
- [Title](arxiv_link) - Brief summary""",
)

# Step 3: Report Writer
writer = Agent(
    name="Report Writer",
    model=OpenRouter(id="x-ai/grok-4-fast:free"),
    tools=[FileTools(base_dir=research_dir), FileTools(base_dir=reports_dir)],
    db=shared_db,
    knowledge=knowledge,
    user_id="test@example.com",
    session_id=f"session_{TODAY}",
    enable_user_memories=True,
    search_knowledge=False,
    update_knowledge=True,
    instructions=f"""Create daily AI report for {TODAY}.

Steps:
1. Try to read file "hn_reddit_{TODAY}.md" - if not found, look for any .md file containing "{TODAY}" in research directory
2. Try to read file "arxiv_{TODAY}.md" - if not found, look for any .md file containing "{TODAY}" and "arxiv" in research directory
3. Create summary report from the content found
4. Use save_file tool to save as EXACTLY this filename: "daily_report_{TODAY}.md"
5. Use add_to_knowledge tool to add file to knowledge base

CRITICAL: Report file must be named exactly "daily_report_{TODAY}.md" - do not change this filename.
ALWAYS create output file and add to knowledge base, even if source files are missing.

Output format:
# Daily AI Report - {TODAY}

## Industry News
- [Title] - [Description] - [Link]

## Research Papers
- [Title] - [Description] - [Link]

## Summary
Brief overview of today's AI developments.""",
)

# Step 4: Trend Analyst
trend_analyst = Agent(
    name="Trend Analyst",
    model=OpenRouter(id="x-ai/grok-4-fast:free"),
    tools=[FileTools(base_dir=trends_dir)],
    db=shared_db,
    knowledge=knowledge,
    user_id="test@example.com",
    session_id=f"session_{TODAY}",
    enable_user_memories=True,
    search_knowledge=True,
    add_knowledge_to_context=True,
    update_knowledge=True,
    instructions=f"""Analyze long-term AI trends using accumulated knowledge:

🔍 KNOWLEDGE ANALYSIS:
1. Search knowledge base for historical AI development patterns
2. Identify recurring themes across multiple reports
3. Track technology evolution (LLMs, transformers, etc.)
4. Spot emerging research directions
5. Note market and industry shifts

📈 TREND ANALYSIS FOCUS:
- Model architecture evolution
- Performance improvements over time
- Emerging application areas
- Research methodology trends
- Industry adoption patterns
- Regulatory and ethical developments

📝 COMPREHENSIVE ANALYSIS FORMAT:
# AI Trend Analysis - {TODAY}

## 🔄 Recurring Themes
[Patterns appearing across multiple time periods]

## 📈 Technology Evolution
[How AI capabilities have progressed]

## 🆕 Emerging Directions
[New research areas gaining momentum]

## 🏭 Industry Shifts
[Changes in commercial AI adoption]

## 🔮 Future Implications
[Predictions based on observed patterns]

💾 SAVE & STORE:
1. Create "trends_{TODAY}.md" with comprehensive analysis
2. Use update_knowledge tool to add insights to knowledge base""",
)

# Daily Report Team (for memory creation)
daily_team = Team(
    name="Daily AI Report Team",
    members=[hn_researcher, arxiv_researcher, writer],
    model=OpenRouter(id="x-ai/grok-4-fast:free"),
    db=shared_db,
    knowledge=knowledge,
    user_id="test@example.com",
    session_id=f"session_{TODAY}",
    enable_user_memories=True,
    add_memories_to_context=True,
    instructions=f"""Execute daily AI report workflow for {TODAY} in SEQUENTIAL order:

STEP 1: HN Reddit Researcher must complete first
- Get AI news from HackerNews and Reddit
- Create file "hn_reddit_{TODAY}.md"
- Wait for completion before next step

STEP 2: ArXiv Researcher executes after Step 1 completes
- Get AI papers from ArXiv  
- Create file "arxiv_{TODAY}.md"
- Wait for completion before next step

STEP 3: Report Writer executes after Steps 1 and 2 complete
- Read research files from Steps 1 and 2
- Create daily report "daily_report_{TODAY}.md"

Each agent must complete fully before the next agent starts.""",
)

# Daily Report Workflow (stops at report, no trend analysis)
daily_workflow = Workflow(
    name="Daily AI Report Workflow", 
    description="Sequential AI intelligence report generation",
    db=shared_db,
    user_id="test@example.com",
    session_id=f"workflow_session_{TODAY}",
    steps=[
        hn_researcher,    # Step 1: HN Reddit research
        arxiv_researcher, # Step 2: ArXiv research  
        writer           # Step 3: Report writing
    ]
)

# AgentOS with team, individual agents, and workflow
agent_os = AgentOS(
    name="Daily AI Report System",
    agents=[hn_researcher, arxiv_researcher, writer, trend_analyst],
    teams=[daily_team],
    workflows=[daily_workflow]
)

app = agent_os.get_app()

if __name__ == "__main__":
    print(f"\n🤖 Daily AI Report System - {TODAY}")
    print("🔄 Workflow Edition - Deterministic Daily Reports")
    print(f"🔗 Dashboard: http://localhost:7777")
    print(f"📁 Outputs:")
    print(f"   Research: {research_dir}/")
    print(f"   Reports: {reports_dir}/")
    print(f"   Trends: {trends_dir}/")
    print(f"💾 Databases:")
    print(f"   System: ai_system.db (memories + workflow sessions)")
    print(f"   Knowledge: ai_knowledge.db + ai_vectors/")
    
    print(f"\n🌅 Morning Workflow (Daily AI Report Workflow):")
    print(f"   1. HN Reddit Research → research/hn_reddit_{TODAY}.md")
    print(f"   2. ArXiv Research → research/arxiv_{TODAY}.md")
    print(f"   3. Report Writing → reports/daily_report_{TODAY}.md")
    print(f"   4. All files → Knowledge Base")
    
    print(f"\n📈 Standalone Chat (Trend Analyst):")
    print(f"   - Ask trend questions anytime")
    print(f"   - Uses accumulated knowledge for analysis")
    print(f"   - Creates trends/trends_{TODAY}.md when requested")
    
    print(f"\n🚀 Ready!")
    print(f"   Morning: Trigger 'Daily AI Report Workflow'")
    print(f"   Anytime: Chat with 'Trend Analyst' for trend analysis")
    
    agent_os.serve(app="app:app", reload=True, port=7777)