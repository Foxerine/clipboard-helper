import threading
import time
import os
import sys
import tkinter as tk
import tkinter.font as tkfont
import pyautogui
from pynput import keyboard, mouse
import darkdetect
import clipboard_monitor
from PIL import ImageGrab, Image
import idlelib.colorizer as idc
import idlelib.percolator as idp
import pystray
from pystray import MenuItem as item
import locale
import re
from urllib.parse import urlparse, urlunparse

# --- Language Strings ---
LANGUAGES = {
    'en': {
        'copy_button_text': '💾',
        'highlight_button_text': '🎨',
        'linenum_button_text': '🔢',
        'pin_button_text_pinned': '📍',
        'pin_button_text_unpinned': '📌',
        'close_button_text': '❌',
        'context_copy_selected': 'Copy Selected',
        'context_update_clipboard': 'Update Clipboard',
        'context_select_all': 'Select All',
        'context_close_window': 'Close Window',
        'title_copied_text': 'Copied Text',
        'title_copied_text_lines': 'Copied Text ({lines} lines)',
        'title_file_path': 'File Path: {filename}',
        'title_copied_files_single': 'Copied File: {filename}',
        'title_copied_files_multi': 'Copied {count} Files/Folders',
        'title_copied_image': 'Copied Image: {width}x{height} Pixels',
        'status_copied': ' - Copied!',
        'status_updated': ' - Updated!',
        'tray_tooltip': 'Clipboard Helper',
        'tray_exit': 'Exit',
        'clipboard_content_title': 'Clipboard Content',
        'font_error': "Failed to load preferred font: {e}, using system default (ugly)",
        'monitor_error': "Error getting monitor info: {e}",
        'pynput_error': "!! Error setting up pynput listeners (permissions may be needed): {e}",
        'clipboard_monitor_error': "Failed to set up clipboard monitor: {e}",
        'popup_error': "Error showing/updating popup: {e}",
        'update_content_error': "Error updating window content: {e}",
        'copy_text_error': "Error copying text: {e}",
        'select_all_error': "Error selecting all text: {e}",
        'copy_edited_error': "Error copying edited text: {e}",
        'update_lines_error': "Error updating line numbers: {e}",
        'apply_highlight_error': "Error applying syntax highlight: {e}",
        'remove_highlight_error': "Error removing syntax highlight: {e}",
        'mousewheel_error': "Error handling scroll wheel event: {e}",
        'scroll_update_error': "Error updating scroll: {e}",
        'close_window_error': "Error closing window: {e}",
        'key_press_error': "Error processing key press: {e}",
        'clipboard_show_error': "Error getting or showing clipboard content: {e}",
        'tray_setup_error': "Failed to set up system tray icon: {e}",
        'tray_load_error': "Pystray or PIL not loaded correctly. Cannot create tray icon.",
        'tray_image_missing': "Tray icon image not found at {path}, skipping tray setup.",
        'stop_keyboard_listener_error': "Error stopping keyboard listener: {e}",
        'stop_mouse_listener_error': "Error stopping mouse listener: {e}",
        'stop_tray_error': "Error stopping tray icon: {e}",
        'close_popup_on_exit_error': "Error closing popup during exit: {e}",
        'destroy_root_tcl_error': "TclError destroying root (might already be gone): {e}",
        'destroy_root_error': "Error destroying Tkinter root: {e}",
        'main_error': "Critical error during application startup or runtime: {main_e}",
        'exit_message': "Application exited.",
        'help_text_title': 'Clipboard Helper - Usage',
        'help_text_content': """Button Functions:
💾 Copy edited text to clipboard
🎨 Show syntax highlighting
🔢 Show line numbers
📍 Pin window (stays open)
❌ Close window

Hotkey: Ctrl+Shift+Z
 - If window open: Process text (e.g., remove URL params). 
 - If window closed: Show current clipboard; If clipboard is empty: Show this help. 
 
Hotkey: Ctrl+Enter
- When editing in text block, save the content to system clipboard immediately

Author: Foxerine (GitHub)""",
    },
    'zh': {
        'copy_button_text': '💾',
        'highlight_button_text': '🎨',
        'linenum_button_text': '🔢',
        'pin_button_text_pinned': '📍',
        'pin_button_text_unpinned': '📌',
        'close_button_text': '❌',
        'context_copy_selected': '复制选中',
        'context_update_clipboard': '更新剪贴板',
        'context_select_all': '全选',
        'context_close_window': '关闭窗口',
        'title_copied_text': '复制的文本',
        'title_copied_text_lines': '复制的文本 ({lines} 行)',
        'title_file_path': '文件路径: {filename}',
        'title_copied_files_single': '复制的文件: {filename}',
        'title_copied_files_multi': '复制了 {count} 个文件/夹',
        'title_copied_image': '复制的图片: {width}x{height} 像素',
        'status_copied': ' - 已复制!',
        'status_updated': ' - 已更新!',
        'tray_tooltip': '剪贴板助手',
        'tray_exit': '退出',
        'clipboard_content_title': '剪贴板内容',
        'font_error': "无法载入首选字体: {e}，使用系统默认字体（很丑）",
        'monitor_error': "获取显示器信息出错: {e}",
        'pynput_error': "!! 设置 pynput 事件监听器出错 (可能需要权限): {e}",
        'clipboard_monitor_error': "设置剪贴板监听器失败: {e}",
        'popup_error': "显示或更新弹窗时出错: {e}",
        'update_content_error': "更新窗口内容出错: {e}",
        'copy_text_error': "复制文本出错: {e}",
        'select_all_error': "全选文本出错: {e}",
        'copy_edited_error': "复制编辑后文本出错: {e}",
        'update_lines_error': "更新行号时出错: {e}",
        'apply_highlight_error': "应用语法高亮出错: {e}",
        'remove_highlight_error': "移除语法高亮出错: {e}",
        'mousewheel_error': "滚轮事件处理出错: {e}",
        'scroll_update_error': "滚动更新出错: {e}",
        'close_window_error': "关闭窗口时出错: {e}",
        'key_press_error': "处理按键事件时出错: {e}",
        'clipboard_show_error': "获取或显示剪贴板内容出错: {e}",
        'tray_setup_error': "设置系统托盘图标失败: {e}",
        'tray_load_error': "Pystray 或 PIL 未正确加载。无法创建托盘图标。",
        'tray_image_missing': "在 {path} 未找到托盘图标图像，跳过托盘设置。",
        'stop_keyboard_listener_error': "停止键盘监听器时出错: {e}",
        'stop_mouse_listener_error': "停止鼠标监听器时出错: {e}",
        'stop_tray_error': "停止托盘图标时出错: {e}",
        'close_popup_on_exit_error': "退出时关闭弹窗出错: {e}",
        'destroy_root_tcl_error': "销毁根窗口时 TclError (可能已消失): {e}",
        'destroy_root_error': "销毁 Tkinter 根窗口时出错: {e}",
        'main_error': "应用程序启动或运行时发生严重错误: {main_e}",
        'exit_message': "应用程序已退出。",
        'help_text_title': '剪贴板助手 - 用法',
        'help_text_content': """按钮功能:
💾 保存内容到系统剪贴板
🎨 切换语法高亮
🔢 切换显示行号
📍 固定窗口 (保持打开) 
❌ 关闭窗口

快捷键: Ctrl+Shift+Z
 - 如果窗口已开启: 对文本框中的文字进行快速处理 (如去掉所有的URL参数)。 
 - 如果窗口未开启: 显示剪贴板内容； 如果剪贴板为空: 显示这个帮助信息。 
 
热键: Ctrl+Enter
- 当在文本框内编辑时，立即保存内容到系统剪贴板

作者: 沙糖橘(Foxerine at GitHub)""",
    }
}
# --- End Language Strings ---

class ThemeManager:
    """管理应用程序的主题和字体"""
    def __init__(self, lang_strings):
        self.lang_strings = lang_strings
        self.init_fonts()
        self.set_theme_colors()

    def init_fonts(self):
        try:
            self.font = tkfont.Font(family="Maple Mono Normal NL NF CN", size=10)
            self.title_font = tkfont.Font(family="Maple Mono Normal NL NF CN", size=11, weight="bold")
            self.italic_bold_font = tkfont.Font(family="Maple Mono Normal NL NF CN", size=10, weight="bold", slant="italic")
        except Exception as e:
            print(self.lang_strings['font_error'].format(e=e))
            self.font = tkfont.Font(family="TkDefaultFont", size=10)
            self.title_font = tkfont.Font(family="TkDefaultFont", size=11, weight="bold")
            self.italic_bold_font = tkfont.Font(family="TkDefaultFont", size=10, weight="bold", slant="italic")

    def set_theme_colors(self):
        if self.detect_dark_mode():
            self.bg_color = "#2d2d2d"
            self.fg_color = "#f0f0f0" # Normal text
            self.border_color = "#4d4d4d"
            self.select_bg = "#505050"
            self.select_fg = "#ffffff"
            self.insert_bg = "#FFFFFF"
            self.scrollbar_active_bg = "#777777"
            self.scrollbar_bg = "#555555"
            # Syntax highlight colors (Dark Mode)
            self.syntax_comment_fg = '#6a9955'
            self.syntax_keyword_fg = '#569cd6'
            self.syntax_builtin_fg = '#4ec9b0'
            self.syntax_string_fg = '#ce9178'
            self.syntax_definition_fg = '#dcdcaa'
            # Add more if needed, e.g., numbers, operators
        else:
            self.bg_color = "#f0f0f0"
            self.fg_color = "#1e1e1e" # Normal text
            self.border_color = "#c0c0c0"
            self.select_bg = "#add8e6"
            self.select_fg = "#000000"
            self.insert_bg = "#000000"
            self.scrollbar_active_bg = "#cccccc"
            self.scrollbar_bg = "#dddddd"
            # Syntax highlight colors (Light Mode)
            self.syntax_comment_fg = '#008000'
            self.syntax_keyword_fg = '#0000FF'
            self.syntax_builtin_fg = '#008080'
            self.syntax_string_fg = '#a31515'
            self.syntax_definition_fg = '#795E26'
            # Add more if needed

    def detect_dark_mode(self):
        return darkdetect.isDark()

class MonitorManager:
    """管理多显示器配置和窗口定位"""
    def __init__(self, root, lang_strings):
        self.root = root
        self.lang_strings = lang_strings
        self.monitors = self.get_monitor_info()

    def get_monitor_info(self):
        monitors = []
        try:
            temp_win = tk.Toplevel(self.root)
            temp_win.withdraw()
            primary = {
                'left': 0, 'top': 0, 'right': temp_win.winfo_screenwidth(), 'bottom': temp_win.winfo_screenheight(),
                'width': temp_win.winfo_screenwidth(), 'height': temp_win.winfo_screenheight()
            }
            monitors.append(primary)
            vwidth = temp_win.winfo_vrootwidth()
            vheight = temp_win.winfo_vrootheight()
            if vwidth > primary['width']:
                secondary = {
                    'left': primary['width'], 'top': 0, 'right': vwidth, 'bottom': primary['height'],
                    'width': vwidth - primary['width'], 'height': primary['height']
                }
                monitors.append(secondary)
            if vheight > primary['height']:
                tertiary = {
                    'left': 0, 'top': primary['height'], 'right': primary['width'], 'bottom': vheight,
                    'width': primary['width'], 'height': vheight - primary['height']
                }
                monitors.append(tertiary)
            temp_win.destroy()
        except Exception as e:
            print(self.lang_strings['monitor_error'].format(e=e))
            if not monitors:
                monitors.append({
                    'left': 0, 'top': 0, 'right': self.root.winfo_screenwidth(), 'bottom': self.root.winfo_screenheight(),
                    'width': self.root.winfo_screenwidth(), 'height': self.root.winfo_screenheight()
                })
        return monitors

    def get_current_monitor(self, x, y):
        for monitor in self.monitors:
            if (monitor['left'] <= x < monitor['right'] and monitor['top'] <= y < monitor['bottom']):
                return monitor
        return self.monitors[0] if self.monitors else None

    def position_window(self, window, x, y):
        current_monitor = self.get_current_monitor(x, y)
        if not current_monitor:
            return x, y
        window.update_idletasks()
        popup_width = window.winfo_width()
        popup_height = window.winfo_height()
        if x + popup_width + 10 > current_monitor['right']:
            x = current_monitor['right'] - popup_width - 10
        if y + popup_height + 10 > current_monitor['bottom']:
            y = current_monitor['bottom'] - popup_height - 10
        if x < current_monitor['left']:
            x = current_monitor['left'] + 10
        if y < current_monitor['top']:
            y = current_monitor['top'] + 10
        return x, y

class PopupWindow:
    """弹出窗口及其组件和交互管理"""
    def __init__(self, app, text, title, position, show_line_numbers_init, is_syntax_highlight_init, lang_strings):
        self.app = app
        self.theme = app.theme
        self.monitor_manager = app.monitor_manager
        self.lang_strings = lang_strings # Store language strings
        self.is_pinned = False
        self.is_dragging = False
        self.resize_edge = None
        self.is_resizing = False
        # Initialize state from app
        self.show_line_numbers = show_line_numbers_init
        self.is_syntax_highlight = is_syntax_highlight_init
        self.mouse_pressed_in_window = False
        self.close_timer = None
        self.percolator = None
        self.color_delegator = None
        self.create_window(text, title, position)

    def create_window(self, text, title, position):
        self.window = tk.Toplevel(self.app.root)
        self.window.withdraw()
        self.window.overrideredirect(True)
        self.window.attributes("-topmost", True)
        self.resize_edge = None
        self.is_resizing = False
        self.theme.set_theme_colors()
        self.frame = tk.Frame(
            self.window, bg=self.theme.bg_color, highlightbackground=self.theme.border_color, highlightthickness=2
        )
        self.frame.pack(fill=tk.BOTH, expand=True)
        self.create_title_bar(title)
        separator = tk.Frame(self.frame, height=1, bg=self.theme.border_color)
        separator.grid(row=1, column=0, sticky="ew", padx=15, pady=2)
        self.create_content_area(text)
        self.bind_resize_events()
        self.position_window(position)
        self.window.deiconify()

        # Apply initial state after window creation
        if self.show_line_numbers:
            self.line_numbers_button.config(relief=tk.SUNKEN)
            self.show_line_number_area()
        if self.is_syntax_highlight:
            self.highlight_button.config(relief=tk.SUNKEN)
            self.apply_syntax_highlight()

        self.reset_close_timer()


    def create_title_bar(self, title):
        title_frame = tk.Frame(self.frame, bg=self.theme.bg_color)
        title_frame.grid(row=0, column=0, sticky="ew")
        title_frame.columnconfigure(0, weight=1)
        for i in range(1, 6):
            title_frame.columnconfigure(i, weight=0)
        self.title_label = tk.Label(
            title_frame, text=title, bg=self.theme.bg_color, fg=self.theme.fg_color,
            font=self.theme.title_font, anchor="w", padx=15, pady=8
        )
        self.title_label.grid(row=0, column=0, sticky="w")
        self.title_label.bind("<ButtonPress-1>", self.start_move)
        self.title_label.bind("<ButtonRelease-1>", self.stop_move)
        self.title_label.bind("<B1-Motion>", self.do_move)
        title_frame.bind("<ButtonPress-1>", self.start_move)
        title_frame.bind("<ButtonRelease-1>", self.stop_move)
        title_frame.bind("<B1-Motion>", self.do_move)
        self.create_title_buttons(title_frame)

    def create_title_buttons(self, parent):
        button_params = {'bg': self.theme.border_color, 'fg': self.theme.fg_color,
                         'font': self.theme.font, 'relief': tk.FLAT, 'padx': 5, 'pady': 2}
        # Use lang_strings for button text (emojis retained)
        copy_button = tk.Button(parent, text=self.lang_strings['copy_button_text'], command=self.copy_edited_text, **button_params)
        copy_button.grid(row=0, column=1, sticky="e", padx=(0, 5))
        self.highlight_button = tk.Button(parent, text=self.lang_strings['highlight_button_text'], command=self.toggle_syntax_highlight, **button_params)
        self.highlight_button.grid(row=0, column=2, sticky="e", padx=(0, 5))
        self.line_numbers_button = tk.Button(parent, text=self.lang_strings['linenum_button_text'], command=self.toggle_line_numbers, **button_params)
        self.line_numbers_button.grid(row=0, column=3, sticky="e", padx=(0, 5))
        # Initial pin state text
        pin_text = self.lang_strings['pin_button_text_unpinned']
        self.pin_button = tk.Button(parent, text=pin_text, command=self.toggle_pin, **button_params)
        self.pin_button.grid(row=0, column=4, sticky="e", padx=(0, 5))
        close_button = tk.Button(parent, text=self.lang_strings['close_button_text'], command=self.close, **button_params)
        close_button.grid(row=0, column=5, sticky="e", padx=(0, 15))

    def create_content_area(self, text):
        text_container = tk.Frame(self.frame, bg=self.theme.bg_color)
        text_container.grid(row=2, column=0, sticky="nsew")
        self.frame.rowconfigure(2, weight=1)
        self.frame.columnconfigure(0, weight=1)
        scrollbar = tk.Scrollbar(text_container)
        scrollbar.config(
            troughcolor=self.theme.bg_color, activebackground=self.theme.scrollbar_active_bg,
            background=self.theme.scrollbar_bg, highlightbackground=self.theme.bg_color,
            highlightcolor=self.theme.bg_color, relief=tk.FLAT, command=self.yview_scroll_and_update,
        )
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        lines = text.split('\n')
        total_lines = len(lines)
        self.content_text = tk.Text(
            text_container, bg=self.theme.bg_color, fg=self.theme.fg_color, font=self.theme.font,
            wrap=tk.WORD, padx=15, pady=8, width=min(80, 600 // 7), height=min(25, max(5, total_lines)),
            relief=tk.FLAT, selectbackground=self.theme.select_bg, selectforeground=self.theme.select_fg,
            insertbackground=self.theme.insert_bg, yscrollcommand=scrollbar.set, state='normal',
        )
        self.content_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.content_text.insert("1.0", text)
        self.bind_content_events()

    def on_window_press(self, event):
        self.mouse_pressed_in_window = True
        self.reset_close_timer()
        return None

    def on_window_release(self, event):
        was_pressed = self.mouse_pressed_in_window
        self.mouse_pressed_in_window = False
        if was_pressed:
            self.reset_close_timer()
        return None

    def bind_content_events(self):
        self.create_context_menu()
        self.content_text.bind("<Control-Return>", lambda e: self.copy_edited_text())
        self.content_text.bind("<Button-3>", lambda e: self.show_context_menu(e))
        self.frame.bind("<Button-3>", lambda e: self.show_context_menu(e))
        self.window.bind("<Button-3>", lambda e: self.show_context_menu(e))
        self.title_label.bind("<Button-3>", lambda e: self.show_context_menu(e))
        self.window.bind("<ButtonPress-1>", self.on_window_press, add='+')
        self.window.bind("<ButtonRelease-1>", self.on_window_release, add='+')
        self.content_text.bind("<MouseWheel>", self.on_mousewheel)
        if sys.platform.startswith('linux'):
            self.content_text.bind("<Button-4>", self.on_mousewheel)
            self.content_text.bind("<Button-5>", self.on_mousewheel)
        self.content_text.bind("<B1-Motion>", self._on_content_drag_scroll, add='+')

    def create_context_menu(self):
        self.context_menu = tk.Menu(
            self.window, tearoff=0, bg=self.theme.bg_color, fg=self.theme.fg_color,
            activebackground=self.theme.select_bg, activeforeground=self.theme.select_fg
        )
        # Use lang_strings for context menu labels
        self.context_menu.add_command(label=self.lang_strings['context_copy_selected'], command=self.copy_selected_text)
        self.context_menu.add_command(label=self.lang_strings['context_update_clipboard'], command=self.copy_edited_text)
        self.context_menu.add_command(label=self.lang_strings['context_select_all'], command=self.select_all)
        self.context_menu.add_separator()
        self.context_menu.add_command(label=self.lang_strings['context_close_window'], command=self.close)

    def show_context_menu(self, event):
        try:
            self.context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.context_menu.unpost()

    def position_window(self, position):
        x, y = position
        adjusted_x, adjusted_y = self.monitor_manager.position_window(self.window, x + 10, y + 10)
        self.window.geometry(f"+{adjusted_x}+{adjusted_y}")

    def bind_resize_events(self):
        """为窗口添加调整大小功能 (禁止顶部和左侧)"""
        self.resize_edge = None
        self.start_x = None
        self.start_y = None
        self.start_width = None
        self.start_height = None
        self.is_resizing = False
        edge_size = 15
        ALLOWED_RESIZE_EDGES = ["right", "bottom", "topright", "bottomleft", "bottomright"]
        CURSOR_MAP = {"right": "sb_h_double_arrow", "bottom": "sb_v_double_arrow",
                      "topright": "size_ne_sw", "bottomleft": "size_ne_sw", "bottomright": "size_nw_se"}

        def get_edge(event):
            x, y = event.x_root, event.y_root
            wx, wy = self.window.winfo_rootx(), self.window.winfo_rooty()
            w, h = self.window.winfo_width(), self.window.winfo_height()
            left = wx <= x <= wx + edge_size
            right = wx + w - edge_size <= x <= wx + w
            top = wy <= y <= wy + edge_size
            bottom = wy + h - edge_size <= y <= wy + h
            if top and left: return "topleft"
            elif top and right: return "topright"
            elif bottom and left: return "bottomleft"
            elif bottom and right: return "bottomright"
            elif top: return "top"
            elif left: return "left"
            elif bottom: return "bottom"
            elif right: return "right"
            else: return ""

        def on_window_motion(event):
            if self.is_resizing or self.is_dragging: return
            edge = get_edge(event)
            cursor = CURSOR_MAP.get(edge, "") if edge in ALLOWED_RESIZE_EDGES else ""
            self.window.configure(cursor=cursor)

        def on_border_press(event):
            edge = get_edge(event)
            if edge in ALLOWED_RESIZE_EDGES:
                self.resize_edge = edge
                self.start_x, self.start_y = event.x_root, event.y_root
                self.start_width, self.start_height = self.window.winfo_width(), self.window.winfo_height()
                self.is_resizing = True
                self.is_dragging = False
                self.reset_close_timer()
                return "break"

        def on_border_motion(event):
            if self.is_resizing and self.resize_edge:
                dx = event.x_root - self.start_x
                dy = event.y_root - self.start_y
                x, y = self.window.winfo_x(), self.window.winfo_y()
                w, h = self.start_width, self.start_height
                new_w, new_h, new_x, new_y = w, h, x, y
                if "right" in self.resize_edge: new_w = max(200, w + dx)
                if "bottom" in self.resize_edge: new_h = max(100, h + dy)
                self.window.geometry(f"{int(new_w)}x{int(new_h)}+{int(new_x)}+{int(new_y)}")
                self.window.update_idletasks()
                self.reset_close_timer()
                return "break"

        def on_border_release(event):
            if self.is_resizing:
                self.is_resizing = False
                self.resize_edge = None
                if self.show_line_numbers: self.update_line_numbers()
                self.reset_close_timer()
                return "break"

        self.window.bind("<Motion>", on_window_motion, add="+")
        self.window.bind("<ButtonPress-1>", on_border_press, add="+")
        self.window.bind("<B1-Motion>", on_border_motion, add="+")
        self.window.bind("<ButtonRelease-1>", on_border_release, add="+")

    def start_move(self, event):
        if self.is_resizing or self.resize_edge is not None: return
        widget_is_title = (event.widget == self.title_label or event.widget == self.title_label.master)
        if not widget_is_title: return
        self.is_dragging = True
        self.drag_start_x, self.drag_start_y = event.x_root, event.y_root
        self.drag_window_start_x, self.drag_window_start_y = self.window.winfo_x(), self.window.winfo_y()

    def stop_move(self, event):
        self.is_dragging = False

    def do_move(self, event):
        if self.is_dragging and not self.is_resizing:
            dx = event.x_root - self.drag_start_x
            dy = event.y_root - self.drag_start_y
            new_x = self.drag_window_start_x + dx
            new_y = self.drag_window_start_y + dy
            self.window.geometry(f"+{new_x}+{new_y}")

    def toggle_pin(self):
        self.is_pinned = not self.is_pinned
        if self.is_pinned:
            self.pin_button.config(text=self.lang_strings['pin_button_text_pinned'], relief=tk.SUNKEN)
            if self.close_timer:
                self.window.after_cancel(self.close_timer)
                self.close_timer = None
        else:
            self.pin_button.config(text=self.lang_strings['pin_button_text_unpinned'], relief=tk.FLAT)
            self.reset_close_timer()

    def toggle_line_numbers(self):
        self.show_line_numbers = not self.show_line_numbers
        self.app.set_line_numbers_enabled(self.show_line_numbers) # Update global state
        if self.show_line_numbers:
            self.line_numbers_button.config(relief=tk.SUNKEN)
            self.show_line_number_area()
        else:
            self.line_numbers_button.config(relief=tk.FLAT)
            self.hide_line_number_area()

    def toggle_syntax_highlight(self):
        self.is_syntax_highlight = not self.is_syntax_highlight
        self.app.set_syntax_highlight_enabled(self.is_syntax_highlight) # Update global state
        if self.is_syntax_highlight:
            self.highlight_button.config(relief=tk.SUNKEN)
            self.apply_syntax_highlight()
        else:
            self.highlight_button.config(relief=tk.FLAT)
            self.remove_syntax_highlight()

    def show_line_number_area(self):
        if not hasattr(self, 'content_text') or not self.window or not self.window.winfo_exists(): return
        text_container = self.content_text.master
        line_numbers_exists = (hasattr(self, 'line_numbers') and self.line_numbers and self.line_numbers.winfo_exists())
        if line_numbers_exists:
            # If it already exists, just ensure layout and update
            if not self.line_numbers.winfo_manager(): # Check if packed
                self.line_numbers.pack_forget()
                self.content_text.pack_forget()
                self.line_numbers.pack(side=tk.LEFT, fill=tk.Y)
                self.content_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            self.update_line_numbers()
            return

        # Create if it doesn't exist
        self.line_numbers = tk.Text(
            text_container, width=4, padx=4, pady=8, takefocus=0, border=0,
            background=self.theme.border_color, foreground=self.theme.fg_color,
            highlightthickness=0, font=self.theme.font
        )
        self.line_numbers.tag_configure("center", justify="right")
        self.line_numbers.bind("<MouseWheel>", lambda e: "break")
        self.line_numbers.bind("<Button-4>", lambda e: "break")
        self.line_numbers.bind("<Button-5>", lambda e: "break")
        self.content_text.pack_forget() # Re-pack to ensure correct order
        self.line_numbers.pack(side=tk.LEFT, fill=tk.Y)
        self.content_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        # Ensure bindings exist
        self.content_text.bind("<<Modified>>", lambda e: self.handle_text_modified(), add='+')
        self.content_text.bind("<Configure>", lambda e: self.update_line_numbers(), add='+')
        self.content_text.bind("<KeyPress>", lambda e: self.content_text.after(1, self.update_line_numbers), add='+')
        self.content_text.bind("<KeyRelease>", lambda e: self.content_text.after(1, self.update_line_numbers), add='+')
        self.content_text.bind("<<YviewChanged>>", lambda e: self.update_line_numbers(), add='+')
        self.update_line_numbers()

    def _on_content_drag_scroll(self, event):
        """Updates line numbers during text selection drag autoscroll."""
        # Check if line numbers are visible and if text is actually selected
        if self.show_line_numbers and self.content_text.tag_ranges("sel"):
            # Check if mouse is near top/bottom edge to guess autoscroll
            widget_height = self.content_text.winfo_height()
            y_pos = event.y # Y position relative to the text widget
            scroll_trigger_margin = 15 # Pixels from edge

            if y_pos < scroll_trigger_margin or y_pos > widget_height - scroll_trigger_margin:
                # Schedule update slightly deferred for robustness
                self.window.after(0, self.update_line_numbers)

    def hide_line_number_area(self):
        if hasattr(self, 'line_numbers') and self.line_numbers and self.line_numbers.winfo_exists():
            self.line_numbers.pack_forget()
            # Re-pack content_text to take full width if needed (scrollbar still exists)
            # self.content_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True) # Might not be needed if scrollbar handles it

    def update_line_numbers(self):
        if not self.show_line_numbers or not hasattr(self, 'line_numbers') or not self.line_numbers.winfo_exists(): return
        try:
            # Ensure the widget is packed before trying to update
            if not self.line_numbers.winfo_manager(): return

            self.line_numbers.config(state='normal') # Ensure writable
            self.line_numbers.delete("1.0", "end")
            contents = self.content_text.get("1.0", "end-1c")
            total_lines = contents.count('\n') + 1 if contents else 1
            line_number_string = "\n".join(str(i) for i in range(1, total_lines + 1))
            self.line_numbers.insert("1.0", line_number_string, "center")
            self.line_numbers.config(state='disabled') # Make read-only
            # Synchronize scrolling
            yview = self.content_text.yview()
            self.line_numbers.yview_moveto(yview[0])
        except tk.TclError:
            pass # Ignore Tcl errors during update, might happen during closing
        except Exception as e:
            print(self.lang_strings['update_lines_error'].format(e=e))


    def handle_text_modified(self):
        # Check if the modification flag is set before updating
        if self.content_text.edit_modified():
            self.update_line_numbers()
            self.content_text.edit_modified(False) # Reset the flag

    def apply_syntax_highlight(self):
        if not hasattr(self, 'content_text') or not self.window or not self.window.winfo_exists(): return
        if self.percolator: return # Already applied

        try:
            self.percolator = idp.Percolator(self.content_text)
            self.color_delegator = idc.ColorDelegator()

            # Use colors directly from the theme manager instance
            base_bg = self.theme.bg_color
            base_fg = self.theme.fg_color
            comment_fg = self.theme.syntax_comment_fg
            keyword_fg = self.theme.syntax_keyword_fg
            builtin_fg = self.theme.syntax_builtin_fg
            string_fg = self.theme.syntax_string_fg
            definition_fg = self.theme.syntax_definition_fg

            # Update tagdefs (make a copy to avoid modifying class defaults)
            custom_tagdefs = self.color_delegator.tagdefs.copy()
            custom_tagdefs['COMMENT'] = {'background': base_bg, 'foreground': comment_fg}
            custom_tagdefs['KEYWORD'] = {'background': base_bg, 'foreground': keyword_fg}
            custom_tagdefs['BUILTIN'] = {'background': base_bg, 'foreground': builtin_fg}
            custom_tagdefs['STRING'] = {'background': base_bg, 'foreground': string_fg}
            custom_tagdefs['DEFINITION'] = {'background': base_bg, 'foreground': definition_fg}
            # Ensure other tags also use the correct background and a reasonable foreground
            for tag in custom_tagdefs:
                if tag not in ['COMMENT', 'KEYWORD', 'BUILTIN', 'STRING', 'DEFINITION', 'NORMAL']:
                    # Apply base background to all other tags
                    custom_tagdefs[tag]['background'] = base_bg
                    # Try to keep original foreground, fallback to base_fg if missing
                    original_fg = self.color_delegator.tagdefs.get(tag, {}).get('foreground')
                    if original_fg:
                        custom_tagdefs[tag]['foreground'] = original_fg
                    else: # Fallback for unconfigured tags
                        custom_tagdefs[tag]['foreground'] = base_fg

            custom_tagdefs['NORMAL'] = {'background': base_bg, 'foreground': base_fg} # Explicitly set NORMAL

            self.color_delegator.tagdefs = custom_tagdefs # Use the customized dict

            self.percolator.insertfilter(self.color_delegator)

            # Force re-colorizing the entire text widget initially
            self.color_delegator.recolorize()

        except Exception as e:
            print(self.lang_strings['apply_highlight_error'].format(e=e))
            self.is_syntax_highlight = False # Reset state on error
            self.app.set_syntax_highlight_enabled(False)
            # Ensure button reflects the state if it exists
            if hasattr(self, 'highlight_button') and self.highlight_button.winfo_exists():
                self.highlight_button.config(relief=tk.FLAT)
            if self.percolator:
                try: self.percolator.close()
                except: pass
            self.percolator = None
            self.color_delegator = None

    def remove_syntax_highlight(self):
        if not self.percolator or not hasattr(self, 'content_text') or not self.content_text.winfo_exists():
            return
        try:
            # Remove the filter first
            if self.color_delegator:
                self.percolator.removefilter(self.color_delegator)
                self.color_delegator = None # Clear reference

            # Close the percolator
            self.percolator.close()
            self.percolator = None # Clear reference

            # Remove all tags applied by the colorizer
            # Get all tags currently defined
            all_tags = self.content_text.tag_names()
            # Identify tags likely added by idlelib (adjust if needed based on idc.ColorDelegator tags)
            highlight_tags = [tag for tag in all_tags if tag in idc.ColorDelegator().tagdefs.keys()]
            # Remove these tags from the entire text range
            for tag in highlight_tags:
                self.content_text.tag_remove(tag, "1.0", "end")

            # Reset the base text color just in case
            self.content_text.config(foreground=self.theme.fg_color)

        except tk.TclError:
            pass # Ignore Tcl errors, e.g., if widget is destroyed
        except Exception as e:
            print(self.lang_strings['remove_highlight_error'].format(e=e))
        finally:
            # Ensure references are cleared even if error occurred mid-way
            self.percolator = None
            self.color_delegator = None

    def on_mousewheel(self, event):
        try:
            scroll_units = 0
            if hasattr(event, 'delta'):  # Windows/macOS
                scroll_units = -3 if event.delta > 0 else 3
                if sys.platform == 'darwin': scroll_units = -event.delta
            elif hasattr(event, 'num'):  # Linux
                scroll_units = -3 if event.num == 4 else 3
            self.content_text.yview_scroll(scroll_units, "units")
            if self.show_line_numbers and hasattr(self, 'line_numbers') and self.line_numbers.winfo_exists():
                self.window.after(0, self.update_line_numbers)
            return "break"
        except Exception as e:
            print(self.lang_strings['mousewheel_error'].format(e=e))
            return None

    def yview_scroll_and_update(self, *args):
        try:
            # Call the original yview method on the Text widget
            self.content_text.yview(*args)
            self.window.after(0, self.update_line_numbers)
        except Exception as e:
            print(self.lang_strings['scroll_update_error'].format(e=e))


    def copy_selected_text(self):
        try:
            if self.content_text.tag_ranges("sel"):
                selected_text = self.content_text.get("sel.first", "sel.last")
                self.app.root.clipboard_clear()
                self.app.root.clipboard_append(selected_text)
        except Exception as e:
            print(self.lang_strings['copy_text_error'].format(e=e))

    def select_all(self):
        try:
            self.content_text.tag_add("sel", "1.0", "end")
            self.content_text.focus_set()
        except Exception as e:
            print(self.lang_strings['select_all_error'].format(e=e))

    def copy_edited_text(self):
        try:
            edited_text = self.content_text.get("1.0", "end-1c")
            self.app.root.clipboard_clear()
            self.app.root.clipboard_append(edited_text)
            current_title = self.title_label.cget('text')
            # Use lang_strings for status message
            copied_status = self.lang_strings['status_copied']
            updated_status = self.lang_strings['status_updated']
            if copied_status not in current_title and updated_status not in current_title:
                self.title_label.config(text=f"{current_title}{copied_status}")
                # Ensure title reverts even if window is destroyed
                def revert_title(original_title=current_title):
                    try:
                        if self.window and self.window.winfo_exists():
                            self.title_label.config(text=original_title)
                    except tk.TclError: pass # Ignore if widget is gone
                self.window.after(1500, revert_title) # Increased visibility time
            self.app.previous_clipboard = edited_text
        except Exception as e:
            print(self.lang_strings['copy_edited_error'].format(e=e))

    def update_content(self, text, title=None):
        try:
            if not self.window or not self.window.winfo_exists(): return # Check if window still exists
            if self.close_timer: self.window.after_cancel(self.close_timer)

            original_title = title # Keep the base title for reverting
            if title:
                total_lines = text.count('\n') + 1
                # Use lang_strings for title format
                if "行" in title or "lines" in title: # Avoid adding line count twice
                    new_title_base = title
                elif total_lines > 5:
                    new_title_base = self.lang_strings['title_copied_text_lines'].format(lines=total_lines)
                else:
                    new_title_base = title # Use original if few lines or already formatted

                original_title = new_title_base # Update original for reverting
                updated_status = self.lang_strings['status_updated']
                self.title_label.config(text=f"{new_title_base}{updated_status}")
                # Ensure title reverts even if window is destroyed
                def revert_title(revert_to_title=original_title):
                    try:
                        if self.window and self.window.winfo_exists():
                            self.title_label.config(text=revert_to_title)
                    except tk.TclError: pass # Ignore if widget is gone
                self.window.after(1500, revert_title) # Increased visibility time


            # Preserve view, update text, reapply state
            current_view = self.content_text.yview()
            self.content_text.config(state='normal') # Ensure editable
            self.content_text.delete("1.0", "end")
            self.content_text.insert("1.0", text)

            # Explicitly trigger modified flag handling for line numbers/highlighting
            self.content_text.edit_modified(True)
            self.handle_text_modified() # Updates line numbers

            # Re-apply highlighting if enabled (Percolator handles incremental updates)
            if self.is_syntax_highlight:
                if self.percolator and self.color_delegator:
                    self.color_delegator.recolorize()
                else:
                    # If percolator wasn't setup (e.g. error before), try again
                    self.apply_syntax_highlight()

            # Restore view position
            self.content_text.yview_moveto(current_view[0])

            self.reset_close_timer()

        except tk.TclError:
            pass # Ignore Tcl errors, e.g. window destroyed during update
        except Exception as e:
            print(self.lang_strings['update_content_error'].format(e=e))


    def reset_close_timer(self):
        if self.is_pinned: return
        if self.close_timer:
            try: self.window.after_cancel(self.close_timer)
            except tk.TclError: pass
            self.close_timer = None
        try:
            if self.window.winfo_exists():
                # Increased auto-close time
                self.close_timer = self.window.after(5000, self.check_auto_close)
        except tk.TclError: pass

    def check_auto_close(self):
        self.close_timer = None
        if self.is_pinned: return
        if not self.window or not self.window.winfo_exists(): return # Exit if window gone

        # Check conditions that should keep the window open
        if self.mouse_pressed_in_window: self.reset_close_timer(); return
        if self.is_dragging: self.reset_close_timer(); return
        if self.is_resizing or self.resize_edge is not None: self.reset_close_timer(); return
        if self.is_mouse_over_popup(): self.reset_close_timer(); return

        # Check focus last, as it's slightly more complex
        try:
            focused_widget = self.window.focus_get()
            # Check if focus is within the popup window tree
            in_popup = False
            widget = focused_widget
            while widget:
                if widget == self.window:
                    in_popup = True
                    break
                # Check if the context menu is active (belongs to the window)
                if isinstance(widget, tk.Menu) and widget.master == self.window:
                    in_popup = True
                    break
                widget = widget.master

            if in_popup:
                # If focus is inside (e.g., Text widget or button), keep open
                self.reset_close_timer()
                return
        except Exception:
            # If focus check fails, rely on other checks (like mouse position)
            pass

        # If none of the above conditions met, close the window
        self.close()


    def is_mouse_over_popup(self):
        try:
            if not self.window or not self.window.winfo_exists(): return False
            mouse_x, mouse_y = pyautogui.position()
            popup_x, popup_y = self.window.winfo_rootx(), self.window.winfo_rooty()
            popup_width, popup_height = self.window.winfo_width(), self.window.winfo_height()
            return (popup_x <= mouse_x < popup_x + popup_width and
                    popup_y <= mouse_y < popup_y + popup_height)
        except Exception:
            return False

    def close(self):
        try:
            if self.close_timer:
                self.window.after_cancel(self.close_timer)
                self.close_timer = None
            if self.percolator:
                try: self.percolator.close()
                except: pass
            if self.window and self.window.winfo_exists():
                self.window.destroy()
            self.app.popup_closed()
        except Exception as e:
            print(self.lang_strings['close_window_error'].format(e=e))
            self.app.popup_closed() # Ensure app knows it's closed

class TextProcessor:
    """
    Handles hotkey actions and text transformations for the clipboard app.
    Determines if the popup text needs transformation (like URL cleaning)
    or if help text should be displayed (if the popup is empty).
    """

    def __init__(self, app):
        """
        Initialize the TextProcessor.

        Args:
            app: The main ClipboardApp instance.
        """
        self.app = app # Store reference to the main app

    # --- Internal Helper Functions for Transformations / Actions ---

    def _get_help_text(self) -> tuple[str, str, str]:
        """
        Retrieves the help content and title.

        Returns:
            A tuple: (help_content, help_title, action_flag)
            action_flag is 'show_help', indicating no clipboard update needed.
        """
        help_content = self.app.lang_strings['help_text_content']
        help_title = self.app.lang_strings['help_text_title']
        # Flag indicates this was specifically the help action
        return help_content, help_title, 'show_help'

    def _clean_url_query(self, text: str) -> tuple[str, str | None, str | None]:
        """
        Internal helper: Finds the first URL and removes its query if present.
        Assumes the check for query presence might have already happened.

        Returns:
            A tuple: (potentially_modified_text, new_title (None), action_flag)
            action_flag is 'do_copy_to_clipboard' if modified, None otherwise.
        """
        try:
            url_match = re.search(r'https?://[^\s<>"]+', text) # Slightly improved regex
            if url_match:
                url_str = url_match.group(0)
                parsed = urlparse(url_str)
                # Double check scheme, netloc, and query for safety
                if parsed.scheme in ('http', 'https') and parsed.netloc and parsed.query:
                    cleaned_url_str = urlunparse(parsed._replace(query='', fragment=''))
                    modified_text = text.replace(url_str, cleaned_url_str, 1)
                    # Return cleaned text, no title change needed, flag to copy
                    return modified_text, None, 'do_copy_to_clipboard'
        except Exception:
            pass # Ignore parsing errors
        # Return original text, no title change, no action flag if failed
        return text, None, None

    # --- Add other specific transformation functions here following the pattern ---
    # Example:
    # def _condense_whitespace(self, text: str) -> tuple[str, str | None, str | None]:
    #     """ Replaces multiple whitespace characters with a single space, trims edges. """
    #     cleaned_text = re.sub(r'\s+', ' ', text).strip()
    #     if cleaned_text != text:
    #         return cleaned_text, None, 'do_copy_to_clipboard'
    #     else:
    #         return text, None, None

    # --- Central Decision Function ---

    def transform_text(self, original_text: str) -> tuple[str, str | None, str | None]:
        """
        Checks conditions and returns the result of ONE applicable transformation
        (or the help text action).

        Returns:
            A tuple: (new_text_content, new_title, action_flag)
            action_flag can be 'show_help', 'do_copy_to_clipboard', or None.
            new_title is only relevant if action_flag is 'show_help'.
        """
        # --- Case 0: Empty or Whitespace Text -> Show Help ---
        if not original_text or not original_text.strip():
            # Condition met: Return the result of the help text function
            return self._get_help_text() # Returns (content, title, 'show_help')

        # --- Case 1: URL with Query Parameters -> Clean URL ---
        try:
            url_match = re.search(r'https?://[^\s<>"]+', original_text)
            if url_match:
                url_str = url_match.group(0)
                parsed = urlparse(url_str)
                # Check if it's a valid web URL *and* has query parameters
                if parsed.scheme in ('http', 'https') and parsed.netloc and parsed.query:
                    # Condition met, call the specific cleaning function
                    return self._clean_url_query(original_text) # Returns (text, None, flag)
        except Exception:
            pass # Ignore parsing errors during check

        # --- Case 2: Condense Whitespace (Example - add elif if needed) ---
        # elif re.search(r'\s{2,}', original_text) or original_text != original_text.strip():
        #     return self._condense_whitespace(original_text) # Define _condense_whitespace if used

        # --- Add other cases (elif conditions calling their specific helpers) here ---


        # --- Default: No transformation applied ---
        # Return original text, no specific title change, no action flag
        return original_text, None, None

    # --- Hotkey Action Handlers ---

    def process_existing_popup_text(self):
        """Gets text from existing popup, determines transformation/help, updates UI & clipboard."""
        if not self.app.popup or not hasattr(self.app.popup, 'window') or not self.app.popup.window.winfo_exists():
            return # Safety check

        try:
            current_text = self.app.popup.content_text.get("1.0", "end-1c")

            # Determine required action and get resulting content/title/flag
            new_text_content, new_title, action_flag = self.transform_text(current_text)

            # Update popup only if content or title actually changes or if showing help
            # (Avoids flicker if no transformation occurred)
            original_title_text = self.app.popup.title_label.cget('text') # Get current title
            should_update_popup = (new_text_content != current_text or
                                   (action_flag == 'show_help' and new_title != original_title_text))

            if should_update_popup:
                # Preserve selection/view before updating
                selection = self.app.popup.content_text.tag_ranges("sel")
                current_view = self.app.popup.content_text.yview()

                # Use new_title only if showing help, otherwise keep existing title
                title_to_set = new_title if action_flag == 'show_help' else None
                self.app.popup.update_content(new_text_content, title=title_to_set)

                # Restore selection/view if possible
                try:
                    if selection:
                        self.app.popup.content_text.tag_add("sel", selection[0], selection[1])
                    self.app.popup.content_text.yview_moveto(current_view[0])
                except tk.TclError: pass # Ignore errors if indices/view invalid

            # Update clipboard *only* if the flag indicates it (e.g., URL cleaned)
            if action_flag == 'do_copy_to_clipboard':
                self.app.root.clipboard_clear()
                self.app.root.clipboard_append(new_text_content)
                self.app.previous_clipboard = new_text_content # Update internal state

        except tk.TclError:
            pass # Ignore errors if text widget is inaccessible during get/update
        except Exception as e:
            print(self.app.lang_strings['process_error'].format(e=e))

    def handle_hotkey_action(self):
        """
        Main entry point called on hotkey press.
        Decides whether to process existing popup or show clipboard/help.
        """
        if self.app.popup and hasattr(self.app.popup, 'window') and self.app.popup.window.winfo_exists():
            # Popup exists: Process its content (which now handles empty/help case internally)
            self.app.root.after(0, self.process_existing_popup_text)
        else:
            # Popup doesn't exist: Show current clipboard or help text in a new popup
            self.app.root.after(0, self.app._show_clipboard_or_help)

class ClipboardApp:
    """剪贴板监控应用的主类"""
    def __init__(self):
        self.previous_clipboard = ""
        self.popup = None
        self.is_running = True
        self.last_update_time = 0
        self.last_file_content = None
        self.last_file_copy_time = 0
        self.max_width = 600
        self._pressed_keys = set()
        self.keyboard_listener = None
        self.mouse_listener = None
        self.tray_icon = None
        self.tray_thread = None

        # --- Language Setup ---
        try:
            # Get default locale (e.g., 'en_US', 'zh_CN')
            lang_code_full, encoding = locale.getlocale()
            if lang_code_full and lang_code_full.lower().startswith('chinese'):
                self.lang_code = 'zh'
            else:
                self.lang_code = 'en' # Default to English
        except Exception:
            self.lang_code = 'en' # Fallback on error
        self.lang_strings = LANGUAGES.get(self.lang_code, LANGUAGES['en'])
        # --- End Language Setup ---

        # --- Global State ---
        self.show_line_numbers_globally = False
        self.is_syntax_highlight_globally = False
        # --- End Global State ---

        self.text_processor = TextProcessor(self)

        self.setup_tray_icon() # Needs lang_strings
        self.root = tk.Tk()
        self.root.withdraw()
        self.theme = ThemeManager(self.lang_strings) # Pass lang_strings
        self.monitor_manager = MonitorManager(self.root, self.lang_strings) # Pass lang_strings
        self.setup_event_listeners()
        self.setup_clipboard_monitor()
        self.root.protocol("WM_DELETE_WINDOW", self.exit_application)
        self.root.mainloop()

    # --- Global State Setters ---
    def set_line_numbers_enabled(self, state: bool):
        self.show_line_numbers_globally = state

    def set_syntax_highlight_enabled(self, state: bool):
        self.is_syntax_highlight_globally = state
    # --- End Global State Setters ---

    def _is_modifier(self, key):
        return key in {
            keyboard.Key.ctrl_l, keyboard.Key.ctrl_r,
            keyboard.Key.cmd_l, keyboard.Key.cmd_r,
            keyboard.Key.alt_l, keyboard.Key.alt_r,
            keyboard.Key.shift_l, keyboard.Key.shift_r,
            keyboard.Key.caps_lock, keyboard.Key.tab
        }

    def _on_key_press(self, key):
        # Add the currently pressed key to the set *before* checking combinations
        self._pressed_keys.add(key)

        is_modifier = self._is_modifier(key)
        hotkey_triggered_show = False # Flag if the hotkey action was triggered

        try:
            # --- Hotkey Detection (Ctrl+Shift+Z) ---
            is_z_related_key = False

            # Check if the event corresponds to 'Z' or its control code '\x1a'
            if hasattr(key, 'char'):
                if key.char == '\x1a':
                    is_z_related_key = True
                elif key.char is not None and key.char.lower() == 'z':
                    is_z_related_key = True
            # Fallback check using KeyCode object
            elif key == keyboard.KeyCode.from_char('z'):
                is_z_related_key = True

            if is_z_related_key:
                # Confirm that BOTH Ctrl and Shift modifiers are held
                ctrl_pressed = any(k in self._pressed_keys for k in [keyboard.Key.ctrl_l, keyboard.Key.ctrl_r, keyboard.Key.cmd_l, keyboard.Key.cmd_r])
                shift_pressed = any(k in self._pressed_keys for k in [keyboard.Key.shift_l, keyboard.Key.shift_r])

                # Trigger ONLY if BOTH modifiers are held
                if ctrl_pressed and shift_pressed:
                    hotkey_triggered_show = True
                    self.text_processor.handle_hotkey_action()
            # --- END: Hotkey Detection ---

        except AttributeError:
            # Ignore errors if key object lacks expected attributes
            pass
        except Exception as e:
            # Log specific key press errors if they occur
            print(self.lang_strings['key_press_error'].format(e=e))


        # --- Check if non-modifier key press outside non-pinned popup should close it ---
        # Close existing non-pinned popup if a non-modifier key is pressed outside it,
        # AND that key press did NOT trigger the hotkey action itself.
        if not hotkey_triggered_show and self.popup and hasattr(self.popup, 'window') and self.popup.window.winfo_exists() and not self.popup.is_pinned and not is_modifier:
            try:
                # Check mouse and focus to determine if the key press was outside the popup
                should_check_focus = not self.popup.is_mouse_over_popup()
                close_popup = False

                if should_check_focus:
                    focused_widget = self.root.focus_get()
                    in_popup = False
                    widget = focused_widget
                    while widget:
                        if widget == self.popup.window:
                            in_popup = True
                            break
                        widget = widget.master
                    if not in_popup:
                        close_popup = True
                # Fallback if focus check failed or wasn't needed but mouse outside
                elif self.popup and hasattr(self.popup, 'window') and self.popup.window.winfo_exists() and not self.popup.is_mouse_over_popup():
                    close_popup = True


                if close_popup:
                    # Schedule close via Tkinter main loop, doesn't block key event
                    self.root.after(0, self.popup.close)

            except Exception:
                # Safer fallback: only close if mouse is definitely outside
                if self.popup and hasattr(self.popup, 'window') and self.popup.window.winfo_exists() and not self.popup.is_mouse_over_popup():
                    self.root.after(0, self.popup.close)
        # --- END: Check popup close ---

    def _show_clipboard_content(self):
        """Gets and shows current clipboard content."""
        try:
            clipboard_content = self.root.clipboard_get()
            mouse_pos = pyautogui.position()
            self.show_popup(clipboard_content, self.lang_strings['clipboard_content_title'], mouse_pos)
        except tk.TclError:
            # Ignore error if clipboard is empty or contains non-text content
            pass
        except Exception as e:
            print(self.lang_strings['clipboard_show_error'].format(e=e))

    def _on_key_release(self, key):
        self._pressed_keys.discard(key)
        # Reset double-tap timer if Ctrl/Cmd is released
        if key in [keyboard.Key.ctrl_l, keyboard.Key.ctrl_r, keyboard.Key.cmd_l, keyboard.Key.cmd_r]:
            # If no other Ctrl/Cmd keys are pressed, reset the timer
            if not any(k in self._pressed_keys for k in [keyboard.Key.ctrl_l, keyboard.Key.ctrl_r, keyboard.Key.cmd_l, keyboard.Key.cmd_r]):
                self.last_ctrl_c_time = 0

    def _on_mouse_click(self, x, y, button, pressed):
        # Check popup validity before potentially accessing its attributes
        if not self.popup or not hasattr(self.popup, 'window') or not self.popup.window.winfo_exists():
            return

        is_over_popup = self.popup.is_mouse_over_popup()

        if not self.popup.is_pinned:
            if pressed:
                if not is_over_popup:
                    # Clicked outside a non-pinned window, close it
                    self.root.after(0, self.popup.close)
            # No special action needed on release regarding the timer reset,
            # as the window interaction itself (press/release inside) resets the timer.
            # If release happens outside after press was outside, it's already closing.


    def setup_event_listeners(self):
        try:
            self.keyboard_listener = keyboard.Listener(on_press=self._on_key_press, on_release=self._on_key_release, suppress=False) # Ensure not suppressed
            self.keyboard_listener.start()
            self.mouse_listener = mouse.Listener(on_click=self._on_mouse_click, suppress=False) # Ensure not suppressed
            self.mouse_listener.start()
        except Exception as e:
            print(self.lang_strings['pynput_error'].format(e=e))

    def setup_clipboard_monitor(self):
        try:
            clipboard_monitor.on_text(self.on_text_change)
            clipboard_monitor.on_files(self.on_files_change)
            clipboard_monitor.on_image(self.on_image_change)
            threading.Thread(target=clipboard_monitor.wait, daemon=True).start()
        except Exception as e:
            print(self.lang_strings['clipboard_monitor_error'].format(e=e))

    def on_text_change(self, text):
        if not self.is_running or not text or not text.strip():
            return

        current_time = time.time()
        # Check against previous content AND time to avoid rapid duplicates from some apps
        if text == self.previous_clipboard and current_time - self.last_update_time < 0.5:
            return

        # Avoid updating if the incoming text is identical to what the popup currently displays
        # (e.g., prevents loop if user copies *from* the popup)
        if self.popup and self.popup.window and self.popup.window.winfo_exists() and hasattr(self.popup, 'content_text'):
            try:
                # Getting text from widget might fail if it's being destroyed
                if text == self.popup.content_text.get("1.0", "end-1c"):
                    return
            except tk.TclError:
                pass # Ignore if widget is gone

        self.previous_clipboard = text
        self.last_update_time = current_time

        # Determine appropriate title based on content
        if self.is_file_path(text):
            title = self.lang_strings['title_file_path'].format(filename=os.path.basename(text))
        else:
            lines = text.split('\n')
            total_lines = len(lines)
            if total_lines > 5: # Show line count for longer text
                title = self.lang_strings['title_copied_text_lines'].format(lines=total_lines)
            else:
                title = self.lang_strings['title_copied_text']

        mouse_pos = pyautogui.position()
        # Schedule UI update on the main Tkinter thread
        self.root.after(0, lambda t=text, ti=title, mp=mouse_pos: self.show_popup(t, ti, mp))

    def on_files_change(self, files):
        if not self.is_running or not files: return
        current_time = time.time()
        # Check against previous content AND time
        files_content = "\n".join(sorted(files))
        if files_content == self.last_file_content and current_time - self.last_file_copy_time < 0.5:
            return
        self.last_file_content = files_content
        self.last_file_copy_time = current_time
        self.last_update_time = current_time
        # Use lang_strings for title
        if len(files) == 1:
            title = self.lang_strings['title_copied_files_single'].format(filename=os.path.basename(files[0]))
        else:
            title = self.lang_strings['title_copied_files_multi'].format(count=len(files))
        content = "\n".join(files)
        mouse_pos = pyautogui.position()
        self.root.after(0, lambda c=content, ti=title, mp=mouse_pos: self.show_popup(c, ti, mp))


    def on_image_change(self):
        if not self.is_running: return
        current_time = time.time()
        # Simple debounce for image detection
        if current_time - self.last_update_time < 0.5:
            # Check if the previous update was also an image (or placeholder)
            if self.previous_clipboard == '[图片]' or self.previous_clipboard == '[Image]':
                return
        try:
            image = ImageGrab.grabclipboard()
            if isinstance(image, Image.Image): # More robust check
                self.last_update_time = current_time
                self.previous_clipboard = '[图片]' # Use consistent placeholder
                width, height = image.size
                # Use lang_strings for title
                title = self.lang_strings['title_copied_image'].format(width=width, height=height)
                mouse_pos = pyautogui.position()
                self.root.after(0, lambda ti=title, mp=mouse_pos: self.show_popup('[图片]', ti, mp)) # Pass placeholder
        except Exception:
            # Ignore errors if clipboard content is not a standard image format PIL understands
            pass


    def is_file_path(self, text):
        try:
            # Handle potential surrounding quotes common in file copies
            text = text.strip().strip('"').strip("'")
            # Basic check: does it look like a path and exist?
            # This is not foolproof but covers common cases.
            # Add more checks if needed (e.g., drive letters on Windows)
            return os.path.exists(text) and (os.path.isfile(text) or os.path.isdir(text))
        except Exception: # Catch potential errors from os.path operations
            return False

    def show_popup(self, text, title, mouse_pos):
        try:
            # Check if the existing popup is still valid
            popup_exists_and_valid = (self.popup and
                                      hasattr(self.popup, 'window') and
                                      self.popup.window.winfo_exists())

            if popup_exists_and_valid:
                # Update existing popup content
                self.popup.update_content(text, title)
            else:
                # Clear any stale reference and create a new popup
                if self.popup: self.popup = None
                self.popup = PopupWindow(
                    self, text, title, mouse_pos,
                    # Pass current global states
                    self.show_line_numbers_globally,
                    self.is_syntax_highlight_globally,
                    self.lang_strings # Pass language strings
                )
        except Exception as e:
            print(self.lang_strings['popup_error'].format(e=e))
            self.popup = None # Ensure popup reference is cleared on error

    def popup_closed(self):
        # Callback from PopupWindow when it closes itself
        self.popup = None

    def setup_tray_icon(self):
        """Sets up and runs the system tray icon in a separate thread."""
        try:
            # 获取正确的资源路径
            if getattr(sys, 'frozen', False):
                # 如果是打包后的程序
                application_path = os.path.dirname(sys.executable)
            else:
                # 如果是开发环境
                application_path = os.path.dirname(__file__)

            image_path = os.path.join(application_path, 'assets', 'copy.png')

            if not os.path.exists(image_path):
                print(self.lang_strings['tray_image_missing'].format(path=image_path))
                self.tray_icon = None
                return
            image = Image.open(image_path)

            def on_exit_clicked(icon, item):
                self.root.after(0, self.exit_application)

            # Use lang_strings for menu item and tooltip
            menu = (item(self.lang_strings['tray_exit'], on_exit_clicked),)
            tooltip = self.lang_strings['tray_tooltip']
            self.tray_icon = pystray.Icon("ClipboardHelper", image, tooltip, menu)

            def run_icon():
                try:
                    # pystray's run() blocks until stop() is called
                    self.tray_icon.run()
                except Exception as thread_e:
                    # Catch errors within the thread if needed
                    # print(f"Error in pystray thread: {thread_e}")
                    pass

            # Start the tray icon thread as a daemon
            self.tray_thread = threading.Thread(target=run_icon, daemon=True)
            self.tray_thread.start()

        except NameError: # Handle missing pystray or PIL
            print(self.lang_strings['tray_load_error'])
            self.tray_icon = None
        except FileNotFoundError: # Handle case where assets/copy.png is missing
            print(self.lang_strings['tray_image_missing'].format(path=image_path))
            self.tray_icon = None
        except Exception as e: # Catch other setup errors
            print(self.lang_strings['tray_setup_error'].format(e=e))
            self.tray_icon = None


    def exit_application(self):
        """Handles the clean shutdown of the application."""
        if not self.is_running: return
        self.is_running = False

        # Stop pynput listeners
        if self.keyboard_listener:
            try: self.keyboard_listener.stop()
            except Exception as e: print(self.lang_strings['stop_keyboard_listener_error'].format(e=e))
        if self.mouse_listener:
            try: self.mouse_listener.stop()
            except Exception as e: print(self.lang_strings['stop_mouse_listener_error'].format(e=e))

        # Stop system tray icon
        if self.tray_icon and hasattr(self.tray_icon, 'stop'): # Check if stop method exists
            try: self.tray_icon.stop()
            except Exception as e: print(self.lang_strings['stop_tray_error'].format(e=e))
            # Wait briefly for the thread to potentially exit cleanly
            # if self.tray_thread and self.tray_thread.is_alive():
            #     self.tray_thread.join(timeout=0.5)

        # Close active popup window safely
        if self.popup and hasattr(self.popup, 'window') and self.popup.window.winfo_exists():
            try:
                # Use the popup's own close method first
                self.popup.close() # This calls popup_closed() which sets self.popup = None
            except Exception as e:
                print(self.lang_strings['close_popup_on_exit_error'].format(e=e))
                # Force destroy if close method fails
                try:
                    if self.popup and self.popup.window: # Check again before destroy
                        self.popup.window.destroy()
                except Exception: pass
            finally:
                self.popup = None # Ensure reference is cleared

        # Schedule the root window destruction
        # Use after(10) to allow other cleanup tasks to potentially finish
        self.root.after(10, self._destroy_root)


    def _destroy_root(self):
        """Safely destroys the Tkinter root window."""
        try:
            if self.root:
                self.root.destroy()
        except tk.TclError as e:
            print(self.lang_strings['destroy_root_tcl_error'].format(e=e))
        except Exception as e:
            print(self.lang_strings['destroy_root_error'].format(e=e))
        finally:
            self.root = None


if __name__ == "__main__":
    # Determine language here *before* creating ClipboardApp instance
    # to print the final message in the correct language.
    app_instance = None
    final_lang_strings = LANGUAGES['en'] # Default
    try:
        lang_code_full, _ = locale.getlocale()
        if lang_code_full and lang_code_full.lower().startswith('chinese'):
            final_lang_strings = LANGUAGES['zh']
    except Exception:
        pass # Keep default English

    try:
        app_instance = ClipboardApp() # App runs its mainloop here
    except Exception as main_e:
        # Use the determined language for the final error message
        print(final_lang_strings['main_error'].format(main_e=main_e))
    finally:
        # Ensure the final exit message is printed regardless of app state
        if app_instance and hasattr(app_instance, 'lang_strings'):
            # Use language from the running app if available
            print(app_instance.lang_strings['exit_message'])
        else:
            # Fallback to initially determined language
            print(final_lang_strings['exit_message'])

# Compile:
# python -m nuitka --standalone --mingw64 --windows-console-mode=disable --enable-plugin=tk-inter --plugin-enable=anti-bloat --nofollow-import-to=numpy,pandas,matplotlib,scipy,PyQt5,PySide2,email,http,ssl,html,xml,test,unittest,tkinter.test,idlelib.idle_test --include-package=pynput,pyautogui,darkdetect,pystray --include-module=idlelib.colorizer,idlelib.percolator --include-data-dir=assets=assets --python-flag=-OO --remove-output --lto=yes --onefile ./main.py

# tips: 结合 Win + V 使用，效果更佳
