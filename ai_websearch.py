from googleapiclient.discovery import build
import pandas as pd


def google_search(search_term, api_key, cse_id, **kwargs):
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()

    return res['items']


def search(search_term):
    api_key = ""  # Замените на ваш ключ API
    cse_id = "" # Замените на ваш ID настроенного поиска

    results = google_search(search_term, api_key, cse_id, num=10)

    if results:
        formatted_results = []
        for result in results:
            formatted_results.append({
                "title": result.get("title"),
                "link": result.get("link"),
                "snippet": result.get("snippet")
            })

        # df = pd.DataFrame(formatted_results)
        # df.to_csv('search_results.csv', index=False)
        print("Результаты успешно сохранены в search_results.csv")

        return formatted_results
    else:
        return ""
