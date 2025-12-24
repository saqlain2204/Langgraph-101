from src.workflow import Workflow

if __name__ == "__main__":
    wf = Workflow()

    graph = wf.workflow.get_graph().draw_mermaid_png(
        output_file_path="graph.png"
    )

    while True:
        user_input = input("Enter your query (or 'exit' to quit): ")
        if user_input.lower() == "exit":
            break
        result = wf.run(user_input)
        print("Response:", result["messages"][-1].content)
