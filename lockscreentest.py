import flet as ft
from datetime import datetime
import time
import os
import threading
import subprocess
from typing import List, Dict

IsProduction = True  # 🔁 Toggle this to False for Windows paths
testing_mode = False

# Set paths based on IsProduction
if IsProduction:
    ICON_DIR = "/home/goober/breeze-main/icons"
    FONT_PATH = "/home/goober/breeze-main/SFPRODISPLAYBOLD.OTF"
    LOCK_WALLPAPER = "/home/goober/breeze-main/result.jpg"
    HOME_WALLPAPER = "/home/goober/breeze-main/result2.png"
else:
    ICON_DIR = r"C:\Users\danbo\Downloads\icons"
    FONT_PATH = r"C:\users\danbo\Downloads\sf-pro-display\SFPRODISPLAYBOLD.OTF"
    LOCK_WALLPAPER = r"C:\Users\danbo\Downloads\result.jpg"
    HOME_WALLPAPER = r"C:\Users\danbo\Downloads\result2.png"

apps: List[Dict[str, object]] = [
    {
        "name": "Phone",
        "icon": "phone.png",
        "exec": ["pkill", "weston"] if IsProduction else ["start", "notepad.exe"]
    },
    {
        "name": "Messages",
        "icon": "messages.png",
        "exec": ["firefox-esr", "--kiosk", "https://web.whatsapp.com"] if IsProduction else ["start", "notepad.exe"]
    },
    {
        "name": "Camera",
        "icon": "camera.png",
        "exec": ["thunar"] if IsProduction else ["start", "notepad.exe"]
    },
    {
        "name": "Photos",
        "icon": "photos.png",
        "exec": ["firefox-esr", "--kiosk", "https://photos.google.com"] if IsProduction else ["start", "notepad.exe"]
    },
    {
        "name": "YouTube",
        "icon": "youtube.png",
        "exec": ["firefox-esr", "--kiosk", "https://youtube.com"] if IsProduction else ["notepad.exe"]
    },
    {
        "name": "Music",
        "icon": "music.png",
        "exec": ["firefox-esr", "--kiosk", "https://spotify.com"] if IsProduction else ["start", "notepad.exe"]
    },
    {
        "name": "Settings",
        "icon": "settings.png",
        "exec": ["firefox-esr", "about:preferences"] if IsProduction else ["notepad.exe"]
    },
    {
        "name": "Maps",
        "icon": "maps.png",
        "exec": ["firefox-esr", "--kiosk", "https://maps.google.com"] if IsProduction else ["start", "notepad.exe"]
    },
    {
        "name": "Mail",
        "icon": "mail.png",
        "exec": ["firefox-esr", "--kiosk", "https://mail.google.com"] if IsProduction else ["start", "notepad.exe"]
    },
    {
        "name": "Browser",
        "icon": "browser.png",
        "exec": ["firefox-esr"] if IsProduction else ["notepad.exe"]
    },
]


def log(msg: str):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}")

class SafeTimer:
    def __init__(self, interval: float, callback):
        self.interval = interval
        self.callback = callback
        self.active = True
        self.thread = threading.Thread(target=self._run, daemon=True)
        self.thread.start()
        log(f"SafeTimer started with interval {interval:.2f}s")

    def _run(self):
        while self.active:
            time.sleep(self.interval)
            if self.active:
                try:
                    self.callback()
                except Exception as e:
                    log(f"SafeTimer callback error: {e}")

    def stop(self):
        self.active = False
        log("SafeTimer stopped")

def main(page: ft.Page):
    page.title = "Phone Home Screen Simulation"
    if testing_mode:
        width, height = 720, 1280
        time_font_size, date_font_size = 100, 25
        pill_width, pill_height, pill_bottom = 200, 6, 30
        gradient_height, swipe_threshold = 300, 200
        clock_top_padding = 150
        icon_size, icon_font_size = 70, 12
        grid_spacing, grid_padding, grid_columns = 4, 50, 4
        icon_shadow_blur = 15
        icon_shadow_offset = ft.Offset(0, 4)
        icon_shadow_color = "#80000000"
        icon_border_radius = 20
    else:
        width, height = 1080, 1920
        time_font_size, date_font_size = 150, 40
        pill_width, pill_height, pill_bottom = 300, 8, 40
        gradient_height, swipe_threshold = 400, 300
        clock_top_padding = 200
        icon_size, icon_font_size = 120, 18
        grid_spacing, grid_padding, grid_columns = 40, 100, 4
        icon_shadow_blur = 25
        icon_shadow_offset = ft.Offset(0, 6)
        icon_shadow_color = "#80000000"
        icon_border_radius = 25

    pill_left = (width - pill_width) / 2

    page.window_width = width
    page.window_height = height
    page.window_resizable = False
    page.padding = 0
    page.margin = 0
    page.bgcolor = "black"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    font_family = "SF Pro Display" if os.path.exists(FONT_PATH) else "Arial"
    if os.path.exists(FONT_PATH):
        page.fonts = {"SF Pro Display": FONT_PATH}
    text_color = "#FFFFFF"

    time_display = ft.Text(value="", size=time_font_size, color=text_color, weight=ft.FontWeight.W_100,
                           text_align=ft.TextAlign.CENTER, font_family=font_family, width=width)
    date_display = ft.Text(value="", size=date_font_size, color=text_color, weight=ft.FontWeight.W_300,
                           text_align=ft.TextAlign.CENTER, font_family=font_family, width=width)

    def update_time():
        now = datetime.now()
        time_display.value = now.strftime("%H:%M")
        date_display.value = now.strftime("%A, %B %d").upper()
        try:
            page.update()
        except Exception:
            timer.stop()
            log("Page update failed in update_time")

    timer = SafeTimer(60, update_time)
    update_time()

    lock_background = ft.Image(
        src=LOCK_WALLPAPER,
        width=width, height=height, fit=ft.ImageFit.COVER,
    )
    bottom_gradient = ft.Container(
        height=gradient_height,
        gradient=ft.LinearGradient(
            begin=ft.alignment.top_center,
            end=ft.alignment.bottom_center,
            colors=["#00000000", "#000000FF"],
            stops=[0.0, 0.8],
        ),
        bottom=0
    )
    pill = ft.Container(
        width=pill_width, height=pill_height, bgcolor="#FFFFFF",
        border_radius=50, bottom=pill_bottom, left=pill_left, opacity=0.6,
    )
    clock_column = ft.Column(
        controls=[time_display, date_display],
        spacing=0, horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        alignment=ft.MainAxisAlignment.START, expand=True,
    )
    clock_container = ft.Container(
        content=clock_column, padding=ft.padding.only(top=clock_top_padding),
        alignment=ft.alignment.top_center, width=width, height=height,
    )

    lock_screen_stack = ft.Stack(
        controls=[lock_background, bottom_gradient, clock_container, pill],
        width=width, height=height,
    )
    lock_screen_container = ft.Container(
        content=lock_screen_stack,
        width=width, height=height,
        left=0, top=0,
    )

    def launch_app(exec_cmd: List[str], app_name: str):
        try:
            log(f"🚀 Launching {app_name} -> {' '.join(exec_cmd)}")
            subprocess.Popen(exec_cmd)
        except Exception as e:
            log(f"❌ Launch failed for {app_name}: {e}")

    def create_app_grid():
        grid_items = []
        for app_info in apps:
            name = app_info["name"]
            icon_file = app_info["icon"]
            exec_cmd = app_info["exec"]
            icon_path = os.path.join(ICON_DIR, icon_file)

            icon_container = ft.Container(
                width=icon_size,
                height=icon_size,
                border_radius=icon_border_radius,
                shadow=ft.BoxShadow(
                    spread_radius=1,
                    blur_radius=icon_shadow_blur,
                    color=icon_shadow_color,
                    offset=icon_shadow_offset
                ),
                clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
            )

            if os.path.exists(icon_path):
                icon_container.content = ft.Image(
                    src=icon_path,
                    fit=ft.ImageFit.CONTAIN
                )
            else:
                icon_container.content = ft.Container(
                    width=icon_size,
                    height=icon_size,
                    bgcolor="#444444",
                    border_radius=icon_border_radius,
                    alignment=ft.alignment.center,
                    content=ft.Text(name[0], size=icon_size//2, color="white")
                )

            text = ft.Text(
                value=name, size=icon_font_size, color=text_color,
                text_align=ft.TextAlign.CENTER, font_family=font_family,
                width=icon_size + 20,
            )

            btn = ft.FilledButton(
                content=ft.Container(
                    content=ft.Column(
                        [icon_container, text],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=5
                    ),
                    alignment=ft.alignment.center,
                    padding=5,
                ),
                style=ft.ButtonStyle(
                    bgcolor="#00000000",
                    shadow_color="#00000000",
                    overlay_color="#20FFFFFF",
                    shape=ft.RoundedRectangleBorder(radius=10)
                ),
                on_click=lambda e, cmd=exec_cmd, nm=name: launch_app(cmd, nm),
            )
            grid_items.append(btn)

        return ft.GridView(
            controls=grid_items,
            runs_count=grid_columns,
            max_extent=icon_size + 80,
            spacing=grid_spacing,
            run_spacing=grid_spacing,
            padding=grid_padding,
        )

    home_background = ft.Image(
        src=HOME_WALLPAPER,
        width=width, height=height, fit=ft.ImageFit.COVER,
    )
    home_overlay = ft.Container(
        gradient=ft.LinearGradient(
            begin=ft.alignment.top_center, end=ft.alignment.bottom_center,
            colors=["#00000019", "#0000004D"],
        ),
        width=width, height=height,
    )

    app_grid = create_app_grid()

    home_screen_stack = ft.Stack(
        controls=[home_background, home_overlay, app_grid],
        visible=False,
    )
    home_screen_container = ft.Container(
        content=home_screen_stack, width=width, height=height,
    )

    def on_vertical_drag_update(e: ft.DragUpdateEvent):
        if e.delta_y < 0:
            lock_screen_container.top += e.delta_y
            lock_screen_container.opacity = max(0.1, 1 - abs(lock_screen_container.top) / height)
            lock_screen_container.update()

    def on_vertical_drag_end(e: ft.DragEndEvent):
        if lock_screen_container.top < -swipe_threshold:
            lock_screen_container.top = -height
            lock_screen_container.opacity = 0
            home_screen_stack.visible = True
            if gesture_detector in main_stack.controls:
                main_stack.controls.remove(gesture_detector)
                main_stack.update()
        else:
            lock_screen_container.top = 0
            lock_screen_container.opacity = 1
            lock_screen_container.update()
        page.update()

    gesture_detector = ft.GestureDetector(
        mouse_cursor=ft.MouseCursor.GRAB,
        drag_interval=5,
        on_vertical_drag_update=on_vertical_drag_update,
        on_vertical_drag_end=on_vertical_drag_end,
        content=ft.Stack(controls=[lock_screen_container], width=width, height=height)
    )

    main_stack = ft.Stack(
        controls=[home_screen_container, gesture_detector],
        width=width, height=height,
    )
    page.add(main_stack)

    debug_output = ft.Text("DEBUG", color="yellow", size=16)
    debug_container = ft.Container(
        content=debug_output,
        bgcolor="#40000000",
        padding=10,
        bottom=50,
        left=10,
        right=10,
        border_radius=5,
        visible=False
    )
    lock_screen_stack.controls.append(debug_container)

    def show_debug(e):
        debug_container.visible = not debug_container.visible
        debug_container.update()

    pill.on_long_press = show_debug

    def update_debug():
        while True:
            time.sleep(1)
            if debug_container.visible:
                now = datetime.now()
                debug_output.value = (
                    f"Last update: {now.strftime('%H:%M:%S')}\n"
                    f"Lock screen top: {lock_screen_container.top}\n"
                    f"Window: {page.window_width}x{page.window_height}"
                )
                try:
                    debug_output.update()
                except:
                    pass

    threading.Thread(target=update_debug, daemon=True).start()

    def on_window_event(e):
        if e.data == "close":
            timer.stop()
            log("Window closed")

    page.on_window_event = on_window_event

ft.app(target=main)
