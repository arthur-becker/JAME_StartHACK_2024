import gradio as gr
import pandas as pd
from enum import Enum

# TODO: get the databases name

class Step(Enum):
    ENTER_API_KEY = 1
    SELECT_DATABASE = 2
    SELECT_PROPERTIES = 3
    DONE = 4



class WidgetBuilder:
    def __init__(self):
        self._api_key = None
        self._database = None
        self._properties = None

    # Step 1
        
    def set_api_key(self, api_key: str):
        print("Setting API")

        self._api_key = api_key

        self._database = None # reset database
        self._properties = None # reset properties

    def get_api_key(self):
        return self._api_key
    
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
        


if __name__ == "__main__":
    builder = WidgetBuilder()

    with gr.Blocks() as demo:

        with gr.Column(visible=True) as api_key_input_page:
            api_key_input = gr.Textbox(label="API Key", placeholder="Enter your Notion API key")
            submit_btn_1 = gr.Button("Next")
        
            def submit1(api_key):
                print("Submit 1")
                return {
                    api_key_input_page: gr.Column(visible=False),
                    choose_database_page: gr.Column(visible=True),
                }
            
        
        with gr.Column(visible=False) as choose_database_page:
            gr.Dropdown(
                ["table1", "table2", "table3"], label="Database", info="Select a database to aggregate data from"
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
                    gr.Dropdown(
                        ["Type1", "Type2", "Type3"], label="Graph type", info="Select a graph type to display data"
                    ),
                    
                    gr.CheckboxGroup(
                        ["property1", "property2", "property3"], label="X-Axis", info="Select properties to aggregate"
                    ),

                    gr.CheckboxGroup(
                        ["property1", "property2", "property3"], label="Y-Axis", info="Select properties to aggregate"
                    ),
                with gr.Column(scale=2):
                    gr.BarPlot(
                        pd.DataFrame({"a": [1, 2, 3], "b": [10, 20, 30]}),
                        x="a",
                        y="b",
                        title="Simple Bar Plot with made up data",
                        tooltip=["a", "b"],
                        #y_lim=[20, 100],
                    ),
                    gr.Textbox(label="URL", placeholder="Create an embedding block in Notion and paste this URL"),

            submit_btn_3 = gr.Button("Generate")

            def submit3(properties):
                print("Submit 3")
                return {
                    choose_properties_page: gr.Column(visible=False),
                    #done_page: gr.Column(visible=True),
                }

        

       

        # Actions
        submit_btn_1.click(
            submit1,
            [api_key_input],
            [choose_database_page,api_key_input_page],
        )
        submit_btn_2.click(
            submit2,
            [],
            [choose_database_page, choose_properties_page],
        )
        


    demo.launch()