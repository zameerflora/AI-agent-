from crewai import Task
from Agents import recommendation_expert

def recommendation_task(agent, query):
    return Task(
        description=f"""
        Answer the user's questions about sustainability and travels
        based on the following: {query}
        Answer the user query. Avoid unnecessary tool use.
        """,
        expected_output="A clean, final answer without Thought/Action formats.",
        agent=recommendation_expert
    )