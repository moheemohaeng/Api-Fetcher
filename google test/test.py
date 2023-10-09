from googleapiclient.discovery import build
import json

my_api_key = 'AIzaSyBQ0upilA1EqXFA2pmsjbq3WLLkERP6MDM'
my_cse_id = '836130e7b9cf5e1fe'

def google_search(search_term, api_key, cse_id, **kwargs):
    service = build("customsearch", "v1", developerKey = api_key)
    res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
    return res


#구글로 검색
search_result = google_search("Python Google Custom Search", my_api_key, my_cse_id)

#결과 파일로쓰기
with open('search_result_all.json', 'w', encoding='utf-8') as f:
    json.dump(search_result, f, ensure_ascii=False, indent=4)

items = search_result['items']

for i in items:
    print(str(i['link']))