import webbrowser
import requests


def search(query:str):
    # # 구글 검색어 자동완성 데이터 가져오기
    # google_url = "https://www.google.com/complete/search"
    # params = {
    #     "q": query,  # 검색어
    #     "client": "gws-wiz-serp",  # 클라이언트 설정(데스크탑)
    # }

    # response = requests.get(google_url, params=params)
    # if response.status_code == 200:
    #     data = response.json()  # 응답 데이터를 JSON으로 변환
    #     print("구글 자동완성 결과:", data)
    # else:
    #     print("구글 요청 실패:", response.status_code)

    webbrowser.open(f"https://www.google.com/search?q={query}")

    return 0