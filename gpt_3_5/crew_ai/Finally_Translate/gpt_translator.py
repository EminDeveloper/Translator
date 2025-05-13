import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew

# ✅ Load environment variables
load_dotenv()

# ✅ Validate key
api_key = os.getenv("OPENAI_API_KEY")
assert api_key, "❌ OPENAI_API_KEY is missing! Check your .env file."

# 🧠 CrewAI will automatically use OPENAI_API_KEY and OPENAI_MODEL if available

# ✅ Define translator agent (default model will be used)
translator_agent = Agent(
    role="Translator",
    goal="Translate English words to Azerbaijani and define them briefly.",
    backstory="You are a bilingual translator fluent in both English and Azerbaijani.",
    allow_delegation=False
)

# ✅ Translator function using CrewAI
def translate_with_crewai(word: str) -> str:
    prompt = (
        f'Translate the English word "{word}" into Azerbaijani and give a short English definition.\n'
        f'Return result in this JSON format:\n'
        f'{{"english_word": "{word}", "word_meaning": "...", "azerbaijani_word": "..."}}'
    )

    task = Task(
        description=prompt,
        expected_output='JSON with english_word, word_meaning, and azerbaijani_word',
        agent=translator_agent
    )

    crew = Crew(agents=[translator_agent], tasks=[task])
    result = crew.kickoff()
    return str(result)  # ✅ Important for JSON parsing later
