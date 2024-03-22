import gradio as gr
from generator import generator_page
from diagram import diagram_page

def init_value(req: gr.Request):
    params = req.query_params

    if "type" in params.keys() and params["type"] == "generator":
        print("generator")
        return {
            generator: gr.Column(visible=True),
            diagram: gr.Column(visible=False)
        }
    else:
        print("diagram")
        return {
            generator: gr.Column(visible=False),
            diagram: gr.Column(visible=True)
        }

if __name__ == "__main__":
    with gr.Blocks() as main:
        with gr.Column(visible=False) as generator:
            generator_page()

        with gr.Column(visible=False) as diagram:
            diagram_page()
        
        main.load(init_value, [], [generator, diagram])

    main.launch()
