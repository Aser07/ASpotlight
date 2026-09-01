import flet as ft

# 앱 창 크기 설정
app_width = 1000
app_height = 80
app_expanded_height = 170



def create_ui(page:ft.Page, search_handler, onclick_handler, prev_meaning_handler, next_meaning_handler):

    

    # 2. UI 위젯 구성

    # 수식 계산 결과 표시
    calc_suffix = ft.Text("", color=ft.Colors.BLUE_GREY_400, italic=True,)

    search_field = ft.TextField(
        hint_text="Type anything...",
        suffix=calc_suffix,
        text_size=20,
        height=app_height,
        content_padding=20,
        border_color=ft.Colors.TRANSPARENT,
        focused_border_color=ft.Colors.TRANSPARENT,
        on_change=search_handler,  # 타이핑 즉시 호출 
        autofocus=True,
        expand=True,
        
    )
    # 단어 뜻 표시
    dict_title_text = ft.Text(
        value="검색 결과 없음",   
        max_lines=1,
        overflow=ft.TextOverflow.ELLIPSIS,
        size=15,)

    # 하단 단어 개수 넘버링
    dict_index_text = ft.Text("0/0", size=12, color=ft.Colors.GREY_400) # 현재 인덱스 표시용 텍스트

    results = ft.Column(
        visible=False,
        # 반복되는 부분이 있으니 class로 따로 만들어서 써도 괜찮을듯
        controls=[
            ft.ListTile(
                key = "file",
                leading=ft.Icon(ft.Icons.FILE_PRESENT_ROUNDED,),
                title=ft.Text(
                                value="검색 결과 없음",
                                max_lines=1,
                                overflow=ft.TextOverflow.ELLIPSIS,
                                size=15,
                            ),
                on_click=onclick_handler,
                
            ),
                        
            ft.ListTile(
                key = "web",
                leading=ft.Icon(ft.Icons.LANGUAGE),
                title=ft.Text(
                            value="검색 결과 없음",              
                            max_lines=1,
                            overflow=ft.TextOverflow.ELLIPSIS,
                            size=15,), 
                url="",
                on_click=onclick_handler,
                        ),

            ft.ListTile(
                key="dictionary",
                leading=ft.Icon(ft.Icons.FILE_OPEN_ROUNDED),
                title=dict_title_text, 
                trailing=ft.Row(
                    [
                        ft.IconButton(
                            icon=ft.Icons.CHEVRON_LEFT,
                            icon_size=18,
                            tooltip="이전 뜻",
                            on_click=prev_meaning_handler, # 별도의 핸들러 연결 가능
                        ),
                        dict_index_text,
                        ft.IconButton(
                            icon=ft.Icons.CHEVRON_RIGHT,
                            icon_size=18,
                            tooltip="다음 뜻",
                            on_click=next_meaning_handler, # 별도의 핸들러 연결 가능
                        ),
                    ],
                    tight=True,
                    spacing=0,
                ),
                # on_click=onclick_handler,
                # 딕셔너리 창 따로 만들기
                        ),
        ],
    )

    # 메인 컨테이너 (Spotlight 박스)
    spotlight_box = ft.Container(
        content=ft.Column([search_field, results], spacing=0),
        bgcolor=ft.Colors.with_opacity(0.9, "#222222"), # 다크 모드 감성
        border=ft.Border.all(1, "#444444"),
        expand=True,
        border_radius=30
    )
    return spotlight_box, results, dict_title_text, dict_index_text, calc_suffix