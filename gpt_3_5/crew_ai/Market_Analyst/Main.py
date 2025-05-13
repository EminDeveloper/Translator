import os
from crewai import Agent, Task, Crew


os.environ["OPENAI_API_KEY"] = "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"  # replace with your actual key



agent = Agent(
    role="Tədqiqatçı",
    goal="Azərbaycan bazarında EdTech sahəsini analiz etmək",
    backstory="Təcrübəli bazar analitiki",
    verbose=True
)

task = Task(
    description="Azərbaycan üzrə təhsil texnologiyalarında inkişaf trendini analiz et.",
    agent=agent
)

crew = Crew(
    agents=[agent],
    tasks=[task],
    verbose=True
)

crew.kickoff()
