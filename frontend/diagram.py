# For example: http://127.0.0.1:7860/?__theme=light&type=scatter&x=aaa&y=bbb&database=students


import gradio as gr
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import notion_api as na

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
    

    
    api=na.NotionAPI(api_key)
    y,x=api.retrieve_values(database, x_column, y_column)
    
    print(f"X: {x}")
    print(f"Y: {y}")

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
    elif type == "heat":
        # Example data
        criteria = y
        grades = x
        # Construct a frequency matrix
        unique_criteria = sorted(set(criteria)) 
        grade_scale = ["Does not succeed","Does succeed partially","That works well","That works great"]
        
        
        frequency_matrix = np.zeros((len(unique_criteria), len(grade_scale)))

        for criterion, grade in zip(criteria, grades):
            row = unique_criteria.index(criterion)
            col = grade_scale.index(grade)
            frequency_matrix[row, col] += 1

        # Create the heatmap
        #ax.figure(figsize=(8, 6))
        sns.heatmap(frequency_matrix, annot=True, fmt=".0f", cmap="Reds", xticklabels=grade_scale, yticklabels=unique_criteria,ax=ax,cbar=False)
        ax.set_yticklabels(ax.get_yticklabels(), rotation=0)
        plt.tight_layout()
        #plt.xlabel('Grades')
        #plt.ylabel('Evaluation Criteria')
        #plt.title('Grade Distribution by Evaluation Criteria')
        #plt.show()
    else:
        ax.plot(x, y)

    return fig

def diagram_page():
    with gr.Blocks() as block:
        plot = gr.Plot(label="Plot")
        block.load(make_plot, inputs=[], outputs=[plot])
    
    return block