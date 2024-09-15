from googleapiclient.discovery import build
import pprint

def google_search(search_term, api_key, cse_id, **kwargs):
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
    
    # Check if 'items' exists to prevent KeyError
    if 'items' in res:
        return res['items']
    else:
        return []

results = google_search(
    'stackoverflow site:en.wikipedia.org', 
    "<*****>", 
    "135d9c12e6cef4053", num=10)

for result in results:
    pprint.pprint(result)
