# For example: http://127.0.0.1:7860/?__theme=light&type=scatter&x=aaa&y=bbb&database=students


import gradio as gr
import matplotlib.pyplot as plt
import numpy as np

def make_plot(req: gr.Request):

    # Get the parameters
    params = req.query_params
    type = "plot"
    if "type" in params.keys():
        type = params["type"]

    database = params["database"]
    x_column = params["x"]
    y_column = params["y"]
    api_key = params["api_key"]
    title = params["title"]
    
    print(f"\nDatabase: {database}")
    print(f"X: {x_column}")
    print(f"Y: {y_column}")
    print(f"API Key: {api_key}")
    print(f"Title: {title}")

    # TODO: retrieve data from database
    # For now: mock data
    x = np.linspace(0, 10, 100)
    y = np.sin(x)

    # Create a plot
    fig, ax = plt.subplots()
    
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title(title)

    # Plot types
    if type == "plot":
        ax.plot(x, y)
    elif type == "bar":
        ax.bar(x, y)
    elif type == "scatter":
        ax.scatter(x, y)
    elif type == "hist":
        ax.hist(y, bins=10)
    else:
        ax.plot(x, y)

    return fig

def diagram_page():
    with gr.Blocks() as block:
        plot = gr.Plot(label="Plot")
        block.load(make_plot, inputs=[], outputs=[plot])
    
    return block