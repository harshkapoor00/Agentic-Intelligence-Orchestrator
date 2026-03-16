import os
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI

# 1. Setup Models (Assuming environment variables are set)
# os.environ["OPENAI_API_KEY"] = "your_key"

llm = ChatOpenAI(model="gpt-4o", temperature=0.7)

def create_orchestrator():
    """
    Initializes and runs the Multi-Agent Orchestrator.
    """
    
    # 2. Define Specialized Agents
    researcher = Agent(
        role='Senior Technical Researcher',
        goal='Uncover groundbreaking developments in {topic}',
        backstory="""You are a world-class technical researcher. 
        Your expertise lies in identifying emerging trends and technical nuances in frontier AI.""",
        verbose=True,
        allow_delegation=False,
        llm=llm
    )

    writer = Agent(
        role='Technical Content Strategist',
        goal='Synthesize complex research into high-impact documentation',
        backstory="""You are a professional technical writer. 
        You excel at taking raw data and transforming it into professional, accessible, and structured reports.""",
        verbose=True,
        allow_delegation=False,
        llm=llm
    )

    # 3. Define Tasks
    research_task = Task(
        description="""Conduct a comprehensive search on {topic}. 
        Identify the top 3 key innovations and their architectural significance.""",
        expected_output="A detailed summary of the top 3 innovations in {topic}.",
        agent=researcher
    )

    writing_task = Task(
        description="""Using the research provided, create a professional technical report. 
        The report should include an Executive Summary, Technical Deep-Dive, and Future Outlook.""",
        expected_output="A complete Markdown-formatted technical report.",
        agent=writer
    )

    # 4. Form the Crew
    orchestrator_crew = Crew(
        agents=[researcher, writer],
        tasks=[research_task, writing_task],
        process=Process.sequential, # Sequential workflow
        verbose=True
    )

    # 5. Execute
    print("### Starting Agentic Orchestration ###")
    result = orchestrator_crew.kickoff(inputs={'topic': 'Agentic Workflows in Enterprise AI'})
    
    print("\n\n########################")
    print("## FINAL OUTPUT ##")
    print("########################\n")
    print(result)

if __name__ == "__main__":
    create_orchestrator()
