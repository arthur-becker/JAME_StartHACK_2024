import gradio as gr


if __name__ == "__main__":
    with gr.Blocks() as demo:
        with gr.Tab("Lion"):
            gr.Button("New Lion")
        with gr.Tab("Tiger"):
            gr.Button("New Tiger")

    demo.launch()