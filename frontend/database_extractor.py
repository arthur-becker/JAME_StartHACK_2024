from notion_client import Client

# Initialize the Notion client with your integration token
#notion = Client(auth="secret_7RzkbGjr3Z3gvzozIVWissfF8IzBMTzDZaIjjZV0l2s")

# Define the page ID
#page_id = "3ab56ccefa1c45f288245ef90d8820d9"

def retrieve_blocks(page_id, notion):
    """
    Recursively retrieves all blocks within a given page.
    """
    block_list = []
    next_cursor = None

    while True:
        response = notion.blocks.children.list(block_id=page_id, start_cursor=next_cursor)
        block_list.extend(response["results"])
        next_cursor = response["next_cursor"]
        if not next_cursor:
            break

    return block_list

def find_potential_links(blocks, notion):
    """
    Finds all text blocks that potentially contain hyperlinks.
    """
    link_blocks = []

    for block in blocks:
        print(block)
        link_blocks.append(block["id"])

    return link_blocks

# Retrieve all blocks from the page
#blocks = retrieve_blocks(page_id, notion)

# Find all blocks that potentially contain links
#potential_link_blocks = find_potential_links(blocks, notion)

# Output the blocks that potentially contain links
#for block in potential_link_blocks:
#    print(block)