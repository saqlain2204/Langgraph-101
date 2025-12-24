from typing import List, Annotated, TypedDict
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

class ResponseState(TypedDict):
    query: str
    messages: Annotated[List[BaseMessage], add_messages]