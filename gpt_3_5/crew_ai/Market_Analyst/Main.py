import os
from crewai import Agent, Task, Crew



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
