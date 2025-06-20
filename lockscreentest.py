import flet as ft
from datetime import datetime
import time
import os
import threading

def main(page: ft.Page):
    # Set window dimensions
    page.window_width = 320
    page.window_height = 480
    page.window_resizable = False
    page.padding = 0
    page.margin = 0
    page.bgcolor = "black"
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # Load custom font
    font_path = r"C:\users\danbo\Downloads\sf-pro-display\SFPRODISPLAYBOLD.OTF"
    if os.path.exists(font_path):
        page.fonts = {"SF Pro Display": font_path}
        font_family = "SF Pro Display"
    else:
        font_family = "Arial"

    # Pure white text
    text_color = "#FFFFFF"
    
    # Create time display
    time_display = ft.Text(
        value="",
        size=65,
        color=text_color,
        weight=ft.FontWeight.W_100,
        text_align=ft.TextAlign.CENTER,
        font_family=font_family,
        width=320
    )
    
    # Create date display
    date_display = ft.Text(
        value="",
        size=20,
        color=text_color,
        weight=ft.FontWeight.W_300,
        text_align=ft.TextAlign.CENTER,
        font_family=font_family,
        width=320
    )

    # Create bottom gradient
    bottom_gradient = ft.Container(
        height=200,
        gradient=ft.LinearGradient(
            begin=ft.alignment.top_center,
            end=ft.alignment.bottom_center,
            colors=["#00000000", "#000000FF"],
            stops=[0.0, 0.8]
        ),
        bottom=0,
        left=0,
        right=0,
    )

    # Create iPhone-style pill at bottom
    pill = ft.Container(
        width=140,
        height=5,
        bgcolor="#FFFFFF",
        border_radius=50,
        bottom=20,
        left=90,
        right=90,
        opacity=0.6
    )

    # Create clock column
    clock_column = ft.Column(
        [time_display, date_display],
        spacing=0,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        alignment=ft.MainAxisAlignment.START,
        expand=True
    )
    
    # Container for clock
    clock_container = ft.Container(
        content=clock_column,
        padding=ft.padding.only(top=50),
        alignment=ft.alignment.top_center,
        width=320,
        height=480
    )

    # Create lock screen stack
    lock_screen_stack = ft.Stack(
        [
            # Background image
            ft.Image(
                src=r"C:\Users\danbo\Downloads\result.png",
                width=320,
                height=480,
                fit=ft.ImageFit.COVER,
            ),
            
            # Bottom gradient
            bottom_gradient,
            
            # Clock container
            clock_container,
            
            # Pill indicator
            pill
        ],
        width=320,
        height=480
    )

    # Create home screen
    home_screen = ft.Image(
        src=r"C:\Users\danbo\Downloads\result2.jpg",
        width=320,
        height=480,
        fit=ft.ImageFit.COVER,
        visible=False
    )

    # Create container for lock screen with absolute positioning
    lock_screen_container = ft.Container(
        content=lock_screen_stack,
        top=0,
        left=0,
        width=320,
        height=480
    )

    # Create main stack
    main_stack = ft.Stack(
        [
            home_screen,
            lock_screen_container
        ],
        width=320,
        height=480
    )

    # Create gesture detector for swipe functionality
    def on_vertical_drag_update(e: ft.DragUpdateEvent):
        # Only allow upward dragging (negative delta_y)
        if e.delta_y < 0:
            lock_screen_container.top += e.delta_y
            # Calculate opacity based on position (fade out as it moves up)
            opacity = max(0.1, 1 - (abs(lock_screen_container.top) / 480))
            lock_screen_container.opacity = opacity
            lock_screen_container.update()

    def on_vertical_drag_end(e: ft.DragEndEvent):
        # If dragged beyond threshold, complete the unlock
        if lock_screen_container.top < -240:  # 220px threshold
            lock_screen_container.top = -480
            lock_screen_container.opacity = 0
            home_screen.visible = True
        else:
            # Return to original position
            lock_screen_container.top = 0
            lock_screen_container.opacity = 1
        lock_screen_container.update()
        page.update()

    # Create gesture detector
    gesture_detector = ft.GestureDetector(
        mouse_cursor=ft.MouseCursor.GRAB,
        drag_interval=5,
        on_vertical_drag_update=on_vertical_drag_update,
        on_vertical_drag_end=on_vertical_drag_end,
    )
    
    # Wrap the main stack with gesture detector
    content = ft.Stack([
        main_stack,
        gesture_detector
    ], expand=True)

    page.add(content)

    # Update time function
    def update_time():
        now = datetime.now()
        time_str = now.strftime("%H:%M")
        date_str = now.strftime("%A, %B %d").upper()
        
        time_display.value = time_str
        date_display.value = date_str
        
        try:
            page.update()
        except:
            # Page closed, stop timer
            timer.stop()

    # Initialize time
    update_time()
    
    # Create thread-safe timer
    class SafeTimer:
        def __init__(self, interval, callback):
            self.interval = interval
            self.callback = callback
            self.active = True
            self.thread = threading.Thread(target=self.run, daemon=True)
            self.thread.start()
            
        def run(self):
            while self.active:
                time.sleep(self.interval)
                if self.active:
                    self.callback()
        
        def stop(self):
            self.active = False

    timer = SafeTimer(60, update_time)
    
    # Clean up on close
    def on_window_event(e):
        if e.data == "close":
            timer.stop()
    
    page.on_window_event = on_window_event

ft.app(target=main)
