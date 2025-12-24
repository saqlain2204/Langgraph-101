from dotenv import load_dotenv
load_dotenv()


from src.workflow import Workflow


if __name__ == "__main__":
    workflow = Workflow()
    # Print ASCII representation of the workflow graph
    workflow.workflow.get_graph().draw_mermaid_png(
        output_file_path="graph.png"
    )
    result_state = workflow.run(query="")
    print("The result is:", result_state.result)