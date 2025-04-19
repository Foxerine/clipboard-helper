# Clipboard Helper 📋✨

**Lightweight yet powerful clipboard enhancement utility for Windows.**

> *Note: This readme is still under construction. *

Clipboard Helper monitors your clipboard in real-time, providing an instant, interactive preview of copied content (text, file paths, images). Edit text on the fly, toggle syntax highlighting, manage long snippets with line numbers, and much more – all within a sleek, auto-hiding popup window.

[![Screenshot](img.png)](img.png)
*<p align="center">Popup showing copied text with syntax highlighting and line numbers.</p>*

*[Add more relevant screenshots here, e.g., showing file paths, image info, light mode, context menu]*

## ✨ Key Features

-   🔄 **Real-time Monitoring:** Instantly previews copied **text**, **file/folder paths**, and **images**.
-   🖱️ **Intelligent Popup:** Appears near your cursor; automatically disappears after a few seconds of inactivity.
-   📝 **In-place Editing:** Modify copied text directly within the popup window.
-   💾 **Instant Save:** Use `Ctrl+Enter` to save edited text back to the clipboard.
-   🎨 **Syntax Highlighting:** Toggle syntax highlighting for code snippets (Python-like highlighting via `idlelib`).
-   🔢 **Line Numbers:** Toggle line numbers for better readability of long text or code.
-   🧹 **Content Clearing:** Quickly clear popup content and the system clipboard with `Ctrl+Shift+X`.
-   ↩️ **Specific Undo:** Undo the clear action with `Ctrl+Z` (invalidated by subsequent edits).
-   🪄 **URL Cleaning:** Automatically cleans tracking parameters from URLs via `Ctrl+Shift+Z` when the popup is open.
-   📌 **Window Pinning:** Keep the popup window visible indefinitely.
-   🖼️ **Image Info:** Displays dimensions for copied images.
-   📂 **File Path Handling:** Shows clear titles for single or multiple copied files/folders.
-   🌓 **Theme Aware:** Automatically adapts to Windows Light/Dark mode for a native look and feel.
-   ↔️ **Resizable & Draggable:** Easily resize (from bottom/right edges) and move the popup window.
-   ⌨️ **Comprehensive Hotkeys:** Efficient workflow with multiple keyboard shortcuts.
-   🖱️ **Context Menu:** Quick access to common actions like copy selection, select all, etc.
-   🖥️ **Multi-Monitor Aware:** Positions the popup intelligently on the correct monitor.
-   💼 **System Tray Icon:** Runs discreetly in the system tray with an exit option.
-   🌍 **Multi-Lingual:** Supports English and Chinese (简体中文) based on system locale.
-   🚫 **Single Instance:** Prevents multiple copies of the application from running.
-   ⚙️ **Custom Font Support:** Designed for optimal display with the "Maple Mono" font (included).

## 🚀 Usage Guide

### Basic Workflow

1.  Run `Clipboard-Helper.exe`. It will minimize to the system tray.
2.  Copy anything (text, files, image) to your clipboard.
3.  The popup window will appear near your mouse cursor, showing the content.
4.  Interact with the popup or move your mouse away. If unpinned, it will auto-close after ~5 seconds of inactivity (no mouse hover, focus, dragging, or resizing).

### Window Controls (Title Bar Buttons)

-   💾 **Save:** Copies the current (potentially edited) text from the popup back to the system clipboard.
-   🎨 **Highlight:** Toggles syntax highlighting on/off.
-   🔢 **Line Numbers:** Toggles the line number display on/off.
-   📌 / 📍 **Pin/Unpin:** Toggles the pinned state. Pinned windows (📍) do not auto-close.
-   ❌ **Close:** Immediately closes the popup window.

### Keyboard Shortcuts

-   **`Ctrl + Shift + Z`**:
    -   **Popup Open:** Processes text (currently cleans URL query parameters like `?utm_source=...`).
    -   **Popup Closed:** Shows the current clipboard content in the popup. If the clipboard is empty, shows the help text.
-   **`Ctrl + Enter`** (Inside Text Area): Saves the edited text back to the system clipboard (same as 💾 button).
-   **`Ctrl + Shift + X`** (Inside Text Area): Clears the text in the popup *and* the system clipboard.
-   **`Ctrl + Z`** (Inside Text Area): **Undoes** the last `Ctrl+Shift+X` clear action *only if* no other edits were made after clearing. Does not interfere with standard text editing undo/redo otherwise.

### Context Menu (Right-Click)

Right-click anywhere within the popup window (including the title bar) to access:

-   **Copy Selected:** Copies only the highlighted text within the popup.
-   **Update Clipboard:** Saves the entire current text to the clipboard (same as 💾 button / `Ctrl+Enter`).
-   **Select All:** Selects all text in the popup.
-   **Close Window:** Closes the popup (same as ❌ button).

### Tips

-   Combine with Windows Clipboard History (`Win + V`) for an even better workflow.
-   Install the recommended font (`/assets/fonts/MapleMonoNormalNL-NF-CN-Regular.ttf`) for the intended visual appearance. Double-click the file and choose "Install".

## 🛠️ Installation

### Option 1: Pre-compiled Version (Recommended)

1.  Go to the [**Releases**](https://github.com/foxerine/clipboard-helper/releases) page.
2.  Download the latest `.exe` file (e.g., `clipboard-helper.exe`).
3.  (Optional but Recommended) Install the font: Navigate to the extracted `assets/fonts` folder, double-click `MapleMonoNormalNL-NF-CN-Regular.ttf`, and click "Install".
4.  Run `Clipboard-Helper.exe`.

### Option 2: From Source Code

```bash
# 1. Clone the repository
git clone https://github.com/foxerine/clipboard-helper.git
cd clipboard-helper

# 2. Install required Python packages
pip install -r requirements.txt

# 3. Install the recommended font (Important for UI consistency)
#    Navigate to the 'assets/fonts' folder in your file explorer.
#    Double-click 'MapleMonoNormalNL-NF-CN-Regular.ttf' and choose 'Install'.

# 4. Run the application
python main.py
```

### Option 3: Compile from Source (Advanced)

Ensure you have Python, pip, and the required dependencies (requirements.txt) installed. Install Nuitka (`pip install nuitka`). Then run the compile command (adjust paths if needed):

```bash
# Ensure Mingw64 is installed and configured for Nuitka if needed
python -m nuitka --standalone --mingw64 --windows-console-mode=disable ^
    --enable-plugin=tk-inter --plugin-enable=anti-bloat ^
    --nofollow-import-to=numpy,pandas,matplotlib,scipy,PyQt5,PySide2,email,http,ssl,html,xml,test,unittest,tkinter.test,idlelib.idle_test ^
    --include-package=pynput,pyautogui,darkdetect,pystray ^
    --include-module=idlelib.colorizer,idlelib.percolator ^
    --include-data-dir=assets=assets ^
    --output-dir=dist ^
    --python-flag=-OO --remove-output --lto=yes --onefile ./main.py ^
    --output-filename=Clipboard-Helper.exe
```

(Note: Nuitka compilation can be complex. Refer to Nuitka documentation for details.)

## 🔧 System Requirements

- **Operating System**: Primarily tested on Windows 11. May work on Windows 10, but not guaranteed. Untested on macOS/Linux.
- **Python**: Python 3.7+ (if running from source).
- **Permissions**: May require necessary permissions for keyboard/mouse listeners (pynput) depending on system configuration.
- **Dependencies** (if running from source): pyautogui, pynput, darkdetect, clipboard-monitor, Pillow, pystray, psutil. Tkinter (usually included with Python) and idlelib are also used.

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check issues page.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

Distributed under the MIT License. See LICENSE file for more information.

## 🙏 Acknowledgements

- The developers of all the fantastic open-source libraries used in this project.
- Users providing feedback and suggestions.
