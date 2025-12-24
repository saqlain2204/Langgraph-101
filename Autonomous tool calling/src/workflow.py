import os
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langgraph.graph import END, START, StateGraph, MessagesState
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.prebuilt import ToolNode

from .models import ResponseState
from .tools import get_weather, saqlain_formula

load_dotenv()

class Workflow:
    def __init__(self, model_name: str = "llama-3.3-70b-versatile"):
        self.api_key = os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("GROQ_API_KEY not found in environment variables.")
            
        self.model_name = model_name
        self.llm = ChatGroq(api_key=self.api_key, model=self.model_name)
        self.tool_list = [get_weather, saqlain_formula]
        self.llm_with_tools = self.llm.bind_tools(self.tool_list)
        self.tool_node = ToolNode(self.tool_list)
        self.workflow = self._build_workflow()
        
    
    def _build_workflow(self):
        graph = StateGraph(ResponseState)
        
        graph.add_node("agent", self._call_model)
        graph.add_node("tools", self.tool_node)
        
        graph.add_edge(START, "agent")
        graph.add_conditional_edges(
            "agent", 
            self._should_continue,
            {
                "tools": "tools",
                END: END
            }
        )
        graph.add_edge("tools", "agent")
    
        return graph.compile()
    

    def _call_model(self, state: MessagesState):
        messages = state["messages"]
        response = self.llm_with_tools.invoke(messages)
        return {"messages": [response]}

    def _should_continue(self, state: MessagesState):
        messages = state["messages"]
        last_message = messages[-1]
        if last_message.tool_calls:
            return "tools"
        return END

    def run(self, query):
        initial_messages = [
            SystemMessage(content="You are a helpful AI assistant with access to tools. When you use a tool, report the EXACT value returned by the tool - do not calculate or modify it."),
            HumanMessage(content=query)
        ]
        return self.workflow.invoke({"messages": initial_messages})
