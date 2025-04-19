# Clipboard Helper 📋✨

**轻量级但功能强大的 Windows 剪贴板增强工具。**

> *注：此README将在后续版本中进一步完善*

Clipboard Helper 实时监控您的剪贴板，即时提供复制内容（文本、文件路径、图片）的交互式预览。您可以在弹出的窗口中直接编辑文本、切换语法高亮、通过行号管理长片段等等——所有这些都在一个流畅、可自动隐藏的弹窗中完成。

[![截图](img.png)](img.png)
*<p align="center">弹出窗口显示已复制文本，包含语法高亮和行号。</p>*

*[此处添加更多相关截图，例如：显示文件路径、图片信息、浅色模式、右键菜单]*

## ✨ 主要功能

-   🔄 **实时监控**：即时预览复制的**文本**、**文件/文件夹路径**和**图片**。
-   🖱️ **智能弹窗**：在光标附近显示；无活动几秒后自动消失（除非被钉选）。
-   📝 **原地编辑**：直接在弹出窗口中修改复制的文本。
-   💾 **即时保存**：使用 `Ctrl+Enter` 将编辑后的文本保存回剪贴板。
-   🎨 **语法高亮**：为代码片段切换语法高亮（基于 `idlelib` 的类 Python 高亮）。
-   🔢 **行号显示**：切换行号以方便阅读长文本或代码。
-   🧹 **内容清除**：使用 `Ctrl+Shift+X` 快速清空弹窗内容和系统剪贴板。
-   ↩️ **特定撤销**：使用 `Ctrl+Z` 撤销最后一次清除操作（此撤销在清除后进行任何编辑则失效）。
-   🪄 **URL 清理**：当弹窗打开时，通过 `Ctrl+Shift+Z` 可自动清理 URL 中的跟踪参数（如 `?utm_source=...`）。
-   📌 **窗口钉选**：将弹窗固定在屏幕上，防止自动关闭。
-   🖼️ **图片信息**：显示已复制图片的尺寸。
-   📂 **文件路径处理**：为单个或多个复制的文件/文件夹显示清晰的标题。
-   🌓 **主题感知**：自动适应 Windows 亮色/暗色模式，提供原生观感。
-   ↔️ **可调大小与拖动**：轻松调整窗口大小（通过底部/右侧边缘）和移动窗口位置。
-   ⌨️ **快捷键支持**：多种键盘快捷键，提升效率。
-   🖱️ **右键菜单**：快速访问常用操作（复制选中、全选等）。
-   🖥️ **多显示器感知**：在多显示器环境下智能定位弹窗。
-   💼 **系统托盘图标**：在系统托盘中安静运行，提供退出选项。
-   🌍 **多语言支持**：根据系统区域设置自动支持英文和中文（简体）。
-   🚫 **单实例运行**：防止程序重复运行。
-   ⚙️ **字体支持**：为获得最佳显示效果优化设计，推荐使用 "Maple Mono" 字体（已包含）。

## 🚀 使用方法

### 基本流程

1.  运行 `Clipboard-Helper.exe`。程序将最小化到系统托盘。
2.  复制任何内容（文本、文件、图片）到剪贴板。
3.  弹出窗口将在您的鼠标光标附近出现，显示内容。
4.  与弹窗交互或将鼠标移开。如果未钉选，窗口将在无交互（鼠标悬停、获得焦点、拖动、调整大小）约 5 秒后自动关闭。

### 窗口控件 (标题栏按钮)

-   💾 **保存:** 将弹窗中当前（可能已编辑）的文本复制回系统剪贴板。
-   🎨 **高亮:** 切换语法高亮的开关状态。
-   🔢 **行号:** 切换行号显示的开关状态。
-   📌 / 📍 **钉选/取消钉选:** 切换窗口的钉选状态。钉选后的窗口 (📍) 不会自动关闭。
-   ❌ **关闭:** 立刻关闭弹窗。

### 键盘快捷键

-   **`Ctrl + Shift + Z`**:
-   **弹窗已打开:** 处理文本（当前功能为清理 URL 查询参数，如 `?utm_source=...`）。
-   **弹窗已关闭:** 在弹窗中显示当前剪贴板内容。如果剪贴板为空，则显示帮助信息。
-   **`Ctrl + Enter`** (在文本编辑区内): 将编辑后的文本保存回系统剪贴板 (同 💾 按钮)。
-   **`Ctrl + Shift + X`** (在文本编辑区内): 清空弹窗中的文本*和*系统剪贴板。
-   **`Ctrl + Z`** (在文本编辑区内): **撤销**上一次 `Ctrl+Shift+X` 的清除操作，*前提是*清除后没有进行其他编辑。不影响标准的文本编辑撤销/重做。

### 右键菜单

在弹窗的任何位置（包括标题栏）右击可访问：

-   **复制选中:** 仅复制弹窗内高亮选中的文本。
-   **更新剪贴板:** 将弹窗内全部文本保存到剪贴板 (同 💾 按钮 / `Ctrl+Enter`)。
-   **全选:** 选中弹窗内所有文本。
-   **关闭窗口:** 关闭弹窗 (同 ❌ 按钮)。

### 使用技巧

-   结合 Windows 剪贴板历史记录 (`Win + V`) 以获得更佳体验。
-   安装推荐字体 (`/assets/fonts/MapleMonoNormalNL-NF-CN-Regular.ttf`) 以获得最佳视觉效果。双击字体文件并选择"安装"。

## 🛠️ 安装方法

### 方式一：预编译版本 (推荐)

1.  前往 [**Releases**](https://github.com/foxerine/clipboard-helper/releases) 页面。
2.  下载最新的 `.exe` 文件 (例如 `clipboard-helper.exe`)。
3.  (可选但推荐) 安装字体：进入解压后的 `assets/fonts` 文件夹，双击 `MapleMonoNormalNL-NF-CN-Regular.ttf`，然后点击"安装"。
4.  运行 `clipboard-helper.exe`。

### 方式二：从源码运行

```bash
# 1. 克隆仓库
git clone https://github.com/foxerine/clipboard-helper.git
cd clipboard-helper

# 2. 安装所需的 Python 包
pip install -r requirements.txt

# 3. 安装推荐字体 (对 UI 统一性很重要)
#    在文件浏览器中找到 'assets/fonts' 文件夹。
#    双击 'MapleMonoNormalNL-NF-CN-Regular.ttf' 并选择 '安装'。

# 4. 运行程序
python main.py
```

### 方式三：从源码编译 (高级)

确保已安装 Python、pip 及 requirements.txt 中列出的依赖。安装 Nuitka (`pip install nuitka`)。然后运行编译命令（如果需要，请调整路径）：

```bash
# 如果需要，请确保已安装 Mingw64 并为 Nuitka 配置好
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

(注意：Nuitka 编译可能比较复杂。详情请参阅 Nuitka 文档。)

## 🔧 系统要求

- **操作系统**: 主要在 Windows 11 上测试。可能兼容 Windows 10，但未充分保证。未在 macOS/Linux 上测试。
- **Python**: Python 3.7+ (如果从源码运行)。
- **权限**: 可能需要键盘/鼠标监听器 (pynput) 的必要权限，具体取决于系统配置。
- **依赖项** (如果从源码运行): pyautogui, pynput, darkdetect, clipboard-monitor, Pillow, pystray, psutil。还使用了 Tkinter (通常随 Python 一起安装) 和 idlelib。

## 🤝 贡献

欢迎提交问题报告 (Issue) 或功能建议！也欢迎代码贡献：

1. Fork 本项目
2. 创建您的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交您的更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建一个 Pull Request

## 📄 许可

本项目采用 [MIT 许可](LICENSE) 开源。详情请见 LICENSE 文件。

## 🙏 致谢

- 感谢本项目中使用的所有优秀开源库的开发者。
- 感谢所有提供反馈和建议的用户。
