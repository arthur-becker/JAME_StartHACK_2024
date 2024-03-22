import requests




NOTION_TOKEN = "secret_7RzkbGjr3Z3gvzozIVWissfF8IzBMTzDZaIjjZV0l2s"
DATABASE_ID = "092ca412-fb0a-4837-8964-eab011db9d2e"


def get_headers(notion_token):
    return {
        "Authorization": "Bearer " + notion_token,
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28",
    }
    




def create_entry(data: dict, database_id, headers):
    create_url = "https://api.notion.com/v1/pages"

    payload = {"parent": {"database_id": DATABASE_ID}, "properties": data}

    res = requests.post(create_url, headers=headers, json=payload)
    # print(res.status_code)
    return res

from datetime import datetime, timezone

title = "Test Title"
description = "Test Description"
published_date = datetime.now().astimezone(timezone.utc).isoformat()





def get_pages(num_pages, database_id, headers):
    
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

    results = data["results"]
    while data["has_more"] and get_all:
        payload = {"page_size": page_size, "start_cursor": data["next_cursor"]}
        url = f"https://api.notion.com/v1/databases/{database_id}/query"
        response = requests.post(url, json=payload, headers=headers)
        data = response.json()
        results.extend(data["results"])

    return results






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
#Students
#Class
#Assessment entries
#Learning Objectives
#Cycle
#Competence
#Exames





for DB_id in DBs:
    res=get_pages(database_id=DB_id)
    print(res[0]["properties"])

