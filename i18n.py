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
        'status_cleared': ' - Cleared!',
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

Hotkey: Ctrl+Shift+X
- When editing in text block, clear content and system clipboard.
 
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
        'status_cleared': ' - 已清空!',
        'help_text_content': """按钮功能:
💾 保存内容到系统剪贴板
🎨 切换语法高亮
🔢 切换显示行号
📍 固定窗口 (保持打开) 
❌ 关闭窗口

快捷键: Ctrl+Shift+Z
 - 如果窗口已开启: 对文本框中的文字进行快速处理 (如去掉所有的URL参数)。 
 - 如果窗口未开启: 显示剪贴板内容； 如果剪贴板为空: 显示这个帮助信息。 
 
快捷键: Ctrl+Shift+X
 - 当在文本框内编辑时，清空内容和系统剪贴板。

快捷键: Ctrl+Enter
 - 当在文本框内编辑时，立即保存内容到系统剪贴板

作者: 砂糖橘(Foxerine at GitHub)""",
    }
}
# --- End Language Strings ---
