from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv(r'D:\DoubtSolver\.env')

apikey = os.getenv("OPENAI_API_KEY")
class AgentLlm:
    repo = "gpt-4o"
    temperature = 0

    def __init__(self):
        self.llm = None
        pass

    def load_agent_llm(self):
        if self.llm == None:
            self.llm = ChatOpenAI(model=self.repo, temperature=self.temperature,api_key=apikey)
        return self.llm
    