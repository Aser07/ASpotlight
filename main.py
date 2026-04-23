from modules import web_search
from modules import explorer
from modules import dictionary
import flet as ft
import ctypes # 윈도우 해상도를 가져오기 위해 사용
import asyncio
from UI import create_ui
from pynput import keyboard
import threading

# settings 기능도 있으면 좋음 - 유명한 파일 확장자만 검색 같은거

options = ['web', 'dictonary', 'on device']
web_flag = False
dictionary_flag = False
onDevice_flag = True

# 앱 창 크기 설정
app_width = 1000
app_height = 80
app_expanded_height = 250

# 모니터 해상도 가져오기 (Windows 기준)
user32 = ctypes.windll.user32
screen_width = user32.GetSystemMetrics(0)
screen_height = user32.GetSystemMetrics(1)

# 3. 중앙 위치 계산
pos_x = int((screen_width-app_width) / 2)
pos_y = int((screen_height- app_height) / 3) 
# #----------------------------------------------------------------------------------------------------


# UI
async def main(page: ft.Page):

        
    # 1. 창 설정 (Spotlight 스타일)
    page.window.title_bar_hidden = True  # 타이틀바 제거
    page.window.title_bar_buttons_hidden = True
    page.window.width = app_width
    page.window.height = app_height  # 처음엔 입력창만 보이게
    page.window.left = pos_x
    page.window.top = pos_y
    page.window.resizable = False
    page.window.always_on_top = True
    page.bgcolor = ft.Colors.TRANSPARENT  # 배경 투명
    page.window.bgcolor = ft.Colors.TRANSPARENT
    page.padding = 0
    page.window.frameless = True
    # page.window.visible = False
    page.fonts = {
        "Pretendard": "/Fonts/Pretendard-Regular.otf"
    }
    page.theme = ft.Theme(font_family="Pretendard")
    page.title = "ASpotlight"


    # --------기능 구현 부분-----------
    
    # esc 종료
    async def escape(e: ft.KeyboardEvent):
        if e.key == "Escape":
            page.window.visible = False
            page.update()
    
    # 창 토글
    async def toggle_window():
        page.window.visible = not page.window.visible
        if page.window.visible:
            page.window.focused = True
            page.update()

    


    # 입력이 바뀔때마다 함수가 실행되는 비효율을 방지하기 위해 필요한 설정
    state = {
        "search_task": None
    }

    # 입력 시 결과 창 표시
    async def on_search(e):
        search_query = e.control.value
        if state["search_task"]:
            state["search_task"].cancel()
        

        if search_query:            
            state["search_task"] = asyncio.create_task(search(search_query))
            # 검색어가 있으면 창 높이를 늘려 결과창 표시
            page.window.height = app_expanded_height
            results.visible = True
        else:
            page.window.height = app_height
            results.visible = False
        page.update()

    

    ui_layout, results = create_ui(page=page,
                                   search_handler=on_search,
                                    )
    # 검색 - url 변환 최적화 필요
    async def search(query):
        try:
            await asyncio.sleep(0.2)
            file_data = explorer.file_search(query)
            url = f"https://www.google.com/search?q={str(query).strip().replace(" ", "+")}"
            response = dictionary.look_up(query)

            for control in results.controls:
                if control.key == "file" and file_data:
                    control.title.value = f"{file_data["name"][0]}: {file_data["path"][0]}"
                    control.url = file_data["path"][0]
                elif control.key =="file" and not file_data:
                    control.title.value = "file not found"

                elif control.key == "web":
                    # url_query = str(query).replace(" ", "+")
                    control.title.value = f"Web에서 검색: {query}"
                    control.url = url
                    

                elif control.key == "dictionary":
                    control.title.value = "검색 결과 없음"
                    if response == "error":
                        continue
                    if response:
                        control.title.value = f"{response["type"]}: {response["meaning"]}"
            # search_result = results.controls["file"].title.value = query
            control.update()
        except asyncio.CancelledError:
            pass

    # Hot key 설정
    def call():
        page.run_task(toggle_window)

    hotkey_manager = keyboard.GlobalHotKeys({
        '<ctrl>+<alt>+<space>': call
    })
    hotkey_manager.start()

    page.add(ui_layout)

    page.on_keyboard_event = escape
    page.update()



# 앱 실행 (view 매개변수로 창 모드 설정)
ft.run(main=main, assets_dir="Fonts")