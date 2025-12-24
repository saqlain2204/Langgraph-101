from .prompts import TestingPrompts
from .models import AdditionState, NumberState

from langgraph.graph import StateGraph, END

class Workflow:
    def __init__(self):
        self.llm = None
        self.prompts = TestingPrompts()
        self.workflow = self._build_workflow()
    
    def _build_workflow(self):
        graph = StateGraph(AdditionState)
        graph.add_node("first_num", self._input_num1)
        graph.add_node("check_num1", self._check_num1)
        graph.add_node("second_num", self._input_num2)
        graph.add_node("check_num2", self._check_num2)
        graph.add_node("result", self._result)

        graph.set_entry_point("first_num")
        graph.add_edge("first_num", "check_num1")
        graph.add_conditional_edges(
            "check_num1",
            self._route_after_check_num1,
            {
                "ok": "second_num",
                "retry": "first_num"
            }
        )
        graph.add_edge("second_num", "check_num2")
        graph.add_conditional_edges(
            "check_num2",
            self._route_after_check_num2,
            {
                "ok": "result",
                "retry": "second_num"
            }
        )
        graph.add_edge("result", END)
        return graph.compile()
    

    def _check_num(self, value):
        return value is not None and value >= 0

    def _check_num1(self, state: AdditionState):
        value = state.num1.value
        valid = self._check_num(value)
        if not valid:
            print("num1 must be non-negative. Please re-enter.")
        return {"num1": {"value": value, "valid": valid}}

    def _route_after_check_num1(self, state):
        return "ok" if getattr(state.num1, "valid", False) else "retry"

    def _check_num2(self, state: AdditionState):
        value = state.num2.value
        valid = self._check_num(value)
        if not valid:
            print("num2 must be non-negative. Please re-enter.")
        return {"num2": {"value": value, "valid": valid}}

    def _route_after_check_num2(self, state):
        return "ok" if getattr(state.num2, "valid", False) else "retry"

    def _input_num1(self, state: AdditionState):
        num1 = int(input("Enter the num1: "))
        return {"num1": {"value": num1}}

    def _input_num2(self, state: AdditionState):
        num2 = int(input("Enter the num2: "))
        return {"num2": {"value": num2}}

    def _result(self, state: AdditionState):
        v1 = state.num1.value if state.num1 and state.num1.value is not None else 0
        v2 = state.num2.value if state.num2 and state.num2.value is not None else 0
        return {"result": v1 + v2}


    def run(self, query: str):
        initial_state = AdditionState(query=query)
        final_state = self.workflow.invoke(initial_state)
        return AdditionState(**final_state)
    
        
        
        