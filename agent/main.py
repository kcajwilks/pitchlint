from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.os import AgentOS
from agno.os.interfaces.agui import AGUI

agent = Agent(
    model=OpenAIChat(id="gpt-4o"),
    description="A helpful assistant that can answer questions and provide information.",
    instructions="Be helpful and friendly. Format your responses using markdown where appropriate.",
)

agent_os = AgentOS(agents=[agent], interfaces=[AGUI(agent=agent)])
app = agent_os.get_app()

if __name__ == "__main__":
    agent_os.serve(app="main:app", port=8000, reload=True)

def main():
    print("Hello from agent!")


if __name__ == "__main__":
    main()
