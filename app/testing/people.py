import httpx


def get_people_with_pagination(client: httpx.Client):
    """Get all people with pagination"""
    page_number = 0
    people = []
    while True:
        get_all_response = client.get(
            f"/v0/people",
            params={"page[size]": 10, "page[number]": page_number},
        )
        get_all_response.raise_for_status()
        jon_response = get_all_response.json()
        meta = jon_response["meta"]
        if page_number >= meta["pagination"]["page[total]"]:
            break
        people += jon_response["data"]
        page_number += 1
    return people
