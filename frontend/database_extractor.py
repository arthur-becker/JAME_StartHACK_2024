from notion_client import Client

class DatabaseExtractor:
    def __init__(self, secret) -> None:
        self.notion = Client(auth=secret)

# Initialize the Notion client with your integration token


# Define the page ID
#page_id = "3ab56ccefa1c45f288245ef90d8820d9"

    def retrieve_blocks(self, page_id):
        """
        Recursively retrieves all blocks within a given page.
        """
        block_list = []
        next_cursor = None

        while True:
            response = self.notion.blocks.children.list(block_id=page_id, start_cursor=next_cursor)
            block_list.extend(response["results"])
            next_cursor = response["next_cursor"]
            if not next_cursor:
                break

        return block_list

    def find_potential_links(self, blocks):
        """
        Finds all text blocks that potentially contain hyperlinks.
        """
        link_blocks = []

        for block in blocks:
            print(block)
            link_blocks.append(block["id"])

        return link_blocks