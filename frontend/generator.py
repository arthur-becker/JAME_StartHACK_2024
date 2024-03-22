import gradio as gr
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from enum import Enum
from notion_client import Client
import database_extractor as de


# Initialize the Notion client with your integration token
# 3ab56ccefa1c45f288245ef90d8820d9
# secret_7RzkbGjr3Z3gvzozIVWissfF8IzBMTzDZaIjjZV0l2s


class Step(Enum):
    ENTER_API_KEY = 1
    SELECT_DATABASE = 2
    SELECT_PROPERTIES = 3
    DONE = 4



class WidgetBuilder:
    def __init__(self):
        self._api_key = None
        self._page_id = None
        self._database = None
        self._properties = None

    # Step 1
        
    def set_api_key(self, api_key: str, page_id: str):
        print("Setting API")

        self._api_key = api_key
        self._page_id = page_id

        self._database = None # reset database
        self._properties = None # reset properties

    def get_api_key(self):
        return self._api_key
    
    def get_page_id(self):
        return self._page_id
    
    # Step 2
    def set_database(self, database_name: str):
        self._database = database_name

        self._properties = None # reset properties
    
    def get_database(self):
        return self._database

    def set_properties(self, properties: list):
        self._properties = properties

    def get_properties(self):
        return self._properties

    
    def get_step(self):
        if self._api_key is None:
            return Step.ENTER_API_KEY
        elif self._database is None:
            return Step.SELECT_DATABASE
        elif len(self._properties) == 0:
            return Step.SELECT_PROPERTIES
        else:
            return Step.DONE
        


def generator_page():
    builder = WidgetBuilder()

    with gr.Blocks() as demo:

        with gr.Column(visible=True) as api_key_input_page:
            api_key_input = gr.Textbox("secret_7RzkbGjr3Z3gvzozIVWissfF8IzBMTzDZaIjjZV0l2s", label="API Key", placeholder="Enter your Notion API key")
            page_id_input = gr.Textbox("3ab56ccefa1c45f288245ef90d8820d9", label="Page ID", placeholder="Enter the ID the page with all databases")
            submit_btn_1 = gr.Button("Next")
        
            def submit1(api_key, page_id):
                builder.set_api_key(api_key, page_id)

                print("API Key: ", api_key)
                print("Page ID: ", page_id)

                # Retrieve databases
                notion = Client(auth=api_key)

                blocks = de.retrieve_blocks(page_id, notion)

                a = 0
                b = 0
                databases = []
                for block in blocks:
                    if "child_database" in block.keys():
                        a += 1
                        databases.append((block["id"],block["child_database"]["title"]))
                print("Databases: ", databases)
                # The data will be retrieved like here. On the other places, it just will be hardcoded
                # TODO: implement retreival for other blocks


                print("Databases: ", a)
                print("Other blocks: ", b)


                # Find all blocks that potentially contain links
                potential_link_blocks = de.find_potential_links(blocks, notion)

                return {
                    api_key_input_page: gr.Column(visible=False),
                    choose_database_page: gr.Column(visible=True)
                }
            
        
        with gr.Column(visible=False) as choose_database_page:
            databases_dropdown = gr.Dropdown(
                ["Students", "Class", "Assesment entries", "Learning Objectives", "Cycle", "Competence", "Exames"], label="Database", info="Select a database to aggregate data from"
            ),
            #database = gr.Textbox(label="Database", placeholder="Enter the database name")
            submit_btn_2 = gr.Button("Next")

            def submit2():
                print("Submit 2")
                return {
                    choose_database_page: gr.Column(visible=False),
                    choose_properties_page: gr.Column(visible=True),
                }
            
        with gr.Column(visible=False) as choose_properties_page:
            with gr.Row():
                with gr.Column(scale=4):
                    graph_type = gr.Dropdown(
                        ["plot", "bar", "scatter", "hist", "heat"], label="Graph type", info="Select a graph type to display data"
                    ),
                    
                    gr.CheckboxGroup(
                        ["Student", "Learning Objective", "Type of Participation", "Comment", "Date"], label="X-Axis", info="Select properties to aggregate"
                    ),

                    gr.CheckboxGroup(
                        ["Student", "Learning Objective", "Type of Participation", "Comment", "Date"], label="Y-Axis", info="Select properties to aggregate"
                    ),
                with gr.Column(scale=2):
                    gr.BarPlot(
                        pd.DataFrame({"X": [1, 2, 3], "Y": [10, 20, 30]}),
                        x="X",
                        y="Y",
                        title="Bar Plot",
                        tooltip=["X", "Y"],
                        #y_lim=[20, 100],
                    ),
                    url = gr.Textbox("http://hardcoded.sorry:7860/?__theme=light&type=scatter&x=aaa&y=bbb&database=students", label="URL", placeholder="Create an embedding block in Notion and paste this URL"),

            submit_btn_3 = gr.Button("Generate")

            submit_btn_3.click(
                lambda: "Test",
                inputs=[],
                outputs=[]
            )

            """def submit3(graph_type):
                print("Submit 3")

                # TODO: retrieve data from database
                # For now: mock data
                x = np.linspace(0, 10, 100)
                y = np.sin(x)

                # Create a plot
                fig, ax = plt.subplots()
                
                ax.set_xlabel("x")
                ax.set_ylabel("y")
                ax.set_title("Title")

                # Plot types
                if graph_type == "plot":
                    ax.plot(x, y)
                elif graph_type == "bar":
                    ax.bar(x, y)
                elif graph_type == "scatter":
                    ax.scatter(x, y)
                elif graph_type == "hist":
                    ax.hist(y, bins=10)
                else:
                    ax.plot(x, y)

                return {
                    plotted: fig,
                }"""

        

       

        # Actions
        submit_btn_1.click(
            submit1,
            [api_key_input, page_id_input],
            [choose_database_page,api_key_input_page],
        )
        submit_btn_2.click(
            submit2,
            [],
            [choose_database_page, choose_properties_page],
        )
        


    return demo