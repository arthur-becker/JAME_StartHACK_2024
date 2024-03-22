import requests
from notion_client import Client
NOTION_TOKEN = "secret_7RzkbGjr3Z3gvzozIVWissfF8IzBMTzDZaIjjZV0l2s"
headers = {
    "Authorization": "Bearer " + NOTION_TOKEN,
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
}

class NotionAPI :
    def __init__(self, token):
        self.notion = Client(auth=token)
        self.database_ids = ["092ca412-fb0a-4837-8964-eab011db9d2e",
            "06bc83f4-828a-4df7-9767-6ab2abe39042",
            "25f56073-cb64-45db-b27f-5425df4ae823",
            "5cde0f29-e7f5-434c-ab40-a0a5e1d75f90",
            "4f184c41-3a1a-4970-be8f-86d327bba6c9",
            "7f2455c2-4915-413d-a437-a313d2044d33",
            "f9e92087-bcab-4249-a19c-982f578400a7"]
        


    def create_entry(self,data: dict, database_id=None):
        create_url = "https://api.notion.com/v1/pages"

        payload = {"parent": {"database_id": database_id}, "properties": data}

        res = requests.post(create_url, headers=headers, json=payload)
        # print(res.status_code)
        return res

    def get_pages(self,num_pages=None, database_id=None):
        
        """If num_pages is None, get all pages, otherwise just the defined number."""

        url = f"https://api.notion.com/v1/databases/{database_id}/query"

        get_all = num_pages is None
        page_size = 100 if get_all else num_pages

        payload = {"page_size": page_size}
        response = requests.post(url, json=payload, headers=headers)

        data = response.json()

        # Comment this out to dump all data to a file
        # import json
        # with open('db.json', 'w', encoding='utf8') as f:
        #    json.dump(data, f, ensure_ascii=False, indent=4)
    # print(data.keys())
        results = data["results"]
        while data["has_more"] and get_all:
            payload = {"page_size": page_size, "start_cursor": data["next_cursor"]}
            url = f"https://api.notion.com/v1/databases/{database_id}/query"
            response = requests.post(url, json=payload, headers=headers)
            data = response.json()
            
            results.extend(data["results"])

        return results

    def get_page(self,page_id):
        return self.notion.pages.retrieve(page_id=page_id)
    
    def retrieve_values(self,database_id, column1_name,column2_name):
        rows=self.get_pages(database_id=database_id)
        data=[]
        data2=[]
        for block in rows:
            page=block["properties"]
            data_value=self.resolve_value(page,column1_name)
            data2_value=self.resolve_value(page,column2_name)
            data.append(data_value)
            data2.append(data2_value)
        return data,data2
            
       
    def resolve_value(self,page, column):
    
        if page[column]["type"] == "select":
            return page[column]["select"]["name"]
        elif page[column]["type"] == "number":
            return page[column]["number"]
        elif page[column]["type"] == "multi_select":
            return [item["name"] for item in page[column]["multi_select"]]
        elif page[column]["type"] == "title":
            return page[column]["title"][0]["text"]["content"]
        elif page[column]["type"] == "text":
            return page[column]["text"][0]["plain_text"]
        elif page[column]["type"] == "relation":
            page = self.get_page(page[column]["relation"][0]["id"])
            page=page["properties"]
            
            for key in page.keys():
                if page[key]["type"] == "title":
                    return page[key]["title"][0]["text"]["content"]
        else:
            return None
    
    
    
    

if __name__ == "__main__":
    #data = {
    #    "Name": {"title": [{"text": {"content": "Bernöad"}}]},
    #    'Tags': {'id': 'DTqG', 'type': 'multi_select', 'multi_select': [{'name': 'vmfds'}, {'name': 'nvdsn'}]},
    #    'ID': {'id': 'title'},
    #    "Number4": {"number": 4}
    #    }

    #create_entry(data)
    DBs=["092ca412-fb0a-4837-8964-eab011db9d2e",
        "06bc83f4-828a-4df7-9767-6ab2abe39042",
        "25f56073-cb64-45db-b27f-5425df4ae823",
        "5cde0f29-e7f5-434c-ab40-a0a5e1d75f90",
        "4f184c41-3a1a-4970-be8f-86d327bba6c9",
        "7f2455c2-4915-413d-a437-a313d2044d33",
        "f9e92087-bcab-4249-a19c-982f578400a7"]
    handler=notion_api(NOTION_TOKEN)
    print(handler.retrieve_values(DBs[2],"Type of Participation","Weight"))
#Students
#Class
#Assessment entries
#Learning Objectives
#Cycle
#Competence
#Exames



