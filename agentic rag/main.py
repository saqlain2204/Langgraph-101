from src.workflow import Workflow

if __name__ == "__main__":
    wf = Workflow()
    query = "What is reward hacking?"
    answer = wf.run(query)
    wf.workflow.get_graph().draw_mermaid_png(
        output_file_path="graph.png"
    )
    print("Final Answer:")
    print(answer)