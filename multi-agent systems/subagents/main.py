import os
from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain.agents import create_agent
from langchain_groq import ChatGroq

load_dotenv()

model = ChatGroq(model="llama-3.3-70b-versatile")
print("Model loaded.")

summarizer_agent = create_agent(
    model=model,
    tools=[],
    system_prompt="You are a helpful summarization agent. Summarize any text given to you concisely."
)
print("Summarizer subagent created.")

@tool("summarize_with_subagent", description="Use the summarizer subagent to summarize text.")
def summarize_with_subagent(text: str) -> str:
    """Use the summarizer subagent to summarize the given text."""
    result = summarizer_agent.invoke({"messages": [{"role": "user", "content": f"Summarize this: {text}"}]})
    return result["messages"][-1].content

main_agent = create_agent(
    model=model,
    tools=[summarize_with_subagent],
    system_prompt="You are a helpful assistant. When asked to summarize, use the summarize_with_subagent tool."
)

text_to_summarize = "The importance of addressing reward hacking in AI systems cannot be overstated. As AI continues to evolve and become more integrated into our daily lives, the potential risks and consequences of reward hacking will only continue to grow. It is essential that we take proactive steps to prevent and mitigate the effects of reward hacking and ensure that AI is developed and used responsibly."

query = f"Summarize the following: {text_to_summarize}"
response = main_agent.invoke({"messages": [{"role": "user", "content": query}]})
print("Final Response from Main Agent:", response["messages"][-1].content)