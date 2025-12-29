import os
from dotenv import load_dotenv
load_dotenv()

from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import MemorySaver

from .tools import hybrid_retriever_tool
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage

class Workflow:
    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        self.llm = ChatGroq(model="llama-3.3-70b-versatile", api_key=self.api_key)
        self.tools = [hybrid_retriever_tool]
        self.llm = self.llm.bind_tools(self.tools)
        self.tools = ToolNode(self.tools)
        self.workflow = self._build_workflow()
        
    
    def _build_workflow(self):
        graph = StateGraph(MessagesState)
        graph.add_node("agent", self._call_model)
        graph.add_node("tools", self.tools)
        
        graph.add_edge(START, "agent")
        graph.add_conditional_edges(
            "agent",
            self._should_continue,
            {
                "tools": "tools",
                "end": END,
            },
        )
        graph.add_edge("tools", "agent")
        checkpointer = MemorySaver()
        return graph.compile(checkpointer=checkpointer)
        

    def _call_model(self, state):
        messages = state['messages']
        response = self.llm.invoke(messages)
        return {"messages": [response]}

    def _should_continue(self, state):
        last_message = state["messages"][-1]
        if last_message.tool_calls:
            return "tools"
        return "end"

    def run(self, query):
        result_state = self.workflow.invoke({"messages": [HumanMessage(content=query)]},
            config={"configurable": {"thread_id": 42}}
        )
        print("\n--- Conversation Log ---")
        for i, msg in enumerate(result_state['messages']):
            print(f"Message {i}: {msg}")
            tool_calls = getattr(msg, 'tool_calls', None)
            if tool_calls is None and isinstance(msg, dict):
                tool_calls = msg.get('tool_calls', None)
            if tool_calls:
                print(f"  Tool Calls: {tool_calls}")
        print("--- End of Log ---\n")
        final_message = result_state['messages'][-1]
        if isinstance(final_message, dict):
            return final_message.get('content', '')
        return getattr(final_message, 'content', '')
        