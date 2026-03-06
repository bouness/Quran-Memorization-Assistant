import os
import sys

def resource_path(relative_path):
    """Get path relative to the executable or script."""
    if getattr(sys, "frozen", False):
        base_path = os.path.dirname(sys.executable)
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)

ASSESTS_DIR = resource_path("assets")
DATA_DIR = resource_path(f"{ASSESTS_DIR}/data")
LANG_DIR = resource_path(f"{ASSESTS_DIR}/lang")
PNG_ICON = resource_path(f"{ASSESTS_DIR}/icon.png")
CHAPTERS_INFO = resource_path(f"{DATA_DIR}/chapters.json")

# Fallback: bundled "audio" folder
BUNDLED_AUDIO_PATH = resource_path(f"{ASSESTS_DIR}/audio")

# RECITER = {
#     "name": "Fares Abaad",
#     "dir": "Fares_Abaad"
# }

RECITER = {
    "name": "Yassin Al-Jazaery",
    "dir": "Yassin_Al-Jazaery"
}

RECITERS = [
    {"name": "Fares Abaad (Hafs)",         "dir": "Fares_Abaad"},
    {"name": "Yassin Al-Jazaery (Warsh)",     "dir": "Yassin_Al-Jazaery"},
    # {"name": "Husary (Hafs)",              "dir": "Husary"},
    # {"name": "Mishary Alafasy (Hafs)",      "dir": "Mishary_Alafasy"},
    # {"name": "Maher Al Muaiqly (Hafs)",     "dir": "Maher_Al-Muaiqly"},
    # {"name": "Ibrahim Al-Dosary (Warsh)",     "dir": "Ibrahim_Al-Dosary"},
    # {"name": "Yasser Al-Dussary (Hafs)",     "dir": "Yasser_Ad-Dussary"},
    # {"name": "Saad Al-Ghamadi (Hafs)",       "dir": "Saad_Al-Ghamadi"},
]

UI_LANGUAGES = {
    'en': {'name': 'English', 'rtl': False},
    'ar': {'name': 'العربية', 'rtl': True}
}

TEXT_TRANSLATIONS = {
    'ar': {'path': f'{DATA_DIR}/quran.json', 'name': 'العربية'},
    'en': {'path': f'{DATA_DIR}/editions/en.json', 'name': 'English'},
    'es': {'path': f'{DATA_DIR}/editions/es.json', 'name': 'Español'},
    'fr': {'path': f'{DATA_DIR}/editions/fr.json', 'name': 'Français'},
    'ru': {'path': f'{DATA_DIR}/editions/ru.json', 'name': 'Русский'},
    'bn': {'path': f'{DATA_DIR}/editions/bn.json', 'name': 'বাংলা'},
    'sv': {'path': f'{DATA_DIR}/editions/sv.json', 'name': 'Svenska'},
    'tr': {'path': f'{DATA_DIR}/editions/tr.json', 'name': 'Türkçe'},
    'ur': {'path': f'{DATA_DIR}/editions/ur.json', 'name': 'اردو'},
    'zh': {'path': f'{DATA_DIR}/editions/zh.json', 'name': '中文'},
    'Transliteration': {
            'path': f'{DATA_DIR}/editions/transliteration.json', 
            'name': 'Transliteration'
        },
}

BASE_STYLES = """
    QMainWindow {
        background-color: %(bg_color)s;
    }
    QMenuBar {
        background-color: %(menubar_bg)s;
        color: %(text_color)s;
        border-bottom: 1px solid %(border_color)s;
        padding: 2px 4px;
        font-size: 13px;
    }
    QMenuBar::item {
        background: transparent;
        color: %(text_color)s;
        padding: 4px 10px;
        border-radius: 4px;
    }
    QMenuBar::item:selected {
        background: %(accent_color)s;
        color: %(accent_text)s;
    }
    QMenu {
        background-color: %(group_bg)s;
        color: %(text_color)s;
        border: 1px solid %(border_color)s;
        border-radius: 6px;
        padding: 4px 0;
    }
    QMenu::item {
        padding: 6px 28px 6px 18px;
    }
    QMenu::item:selected {
        background-color: %(accent_color)s;
        color: %(accent_text)s;
        border-radius: 4px;
    }
    QMenu::separator {
        height: 1px;
        background: %(border_color)s;
        margin: 4px 8px;
    }
    QGroupBox {
        border: 1px solid %(border_color)s;
        border-radius: 10px;
        margin-top: 14px;
        padding-top: 14px;
        background-color: %(group_bg)s;
        font-weight: 600;
    }
    QGroupBox::title {
        subcontrol-origin: margin;
        left: 14px;
        padding: 0 6px;
        color: %(accent_color)s;
        font-size: 13px;
        font-weight: 700;
    }
    QPushButton {
        background-color: %(button_bg)s;
        color: %(button_text)s;
        padding: 10px 28px;
        border-radius: 6px;
        min-width: 110px;
        font-size: 13px;
        font-weight: 600;
        border: none;
    }
    QPushButton:hover {
        background-color: %(button_hover)s;
    }
    QPushButton:pressed {
        background-color: %(button_pressed)s;
    }
    QPushButton:disabled {
        background-color: %(border_color)s;
        color: %(muted_text)s;
    }
    QTextEdit, QLineEdit {
        background-color: %(input_bg)s;
        color: %(text_color)s;
        border: 1px solid %(border_color)s;
        border-radius: 6px;
        padding: 4px 8px;
        font-size: 13px;
        selection-background-color: %(accent_color)s;
    }
    QTextEdit:focus, QLineEdit:focus {
        border: 1.5px solid %(accent_color)s;
    }
    QComboBox {
        background-color: %(input_bg)s;
        color: %(text_color)s;
        border: 1px solid %(border_color)s;
        border-radius: 6px;
        padding: 4px 8px;
        font-size: 13px;
        min-width: 140px;
    }
    QComboBox:focus {
        border: 1.5px solid %(accent_color)s;
    }
    QComboBox::drop-down {
        border: none;
        width: 22px;
    }
    QComboBox QAbstractItemView {
        background-color: %(group_bg)s;
        color: %(text_color)s;
        border: 1px solid %(border_color)s;
        border-radius: 6px;
        padding: 2px;
        selection-background-color: %(accent_color)s;
        selection-color: %(accent_text)s;
    }
    QLabel {
        color: %(text_color)s;
        font-size: 13px;
    }
    QDialog {
        background-color: %(group_bg)s;
        color: %(text_color)s;
    }
    QScrollBar:vertical {
        background: %(input_bg)s;
        width: 8px;
        border-radius: 4px;
    }
    QScrollBar::handle:vertical {
        background: %(border_color)s;
        border-radius: 4px;
        min-height: 20px;
    }
    QScrollBar::handle:vertical:hover {
        background: %(accent_color)s;
    }
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
        height: 0;
    }
"""

COLOR_SCHEME = {
    'dark': {
        'bg_color':      '#1a1a2e',
        'menubar_bg':    '#16213e',
        'group_bg':      '#1e2a45',
        'text_color':    '#e2e8f0',
        'muted_text':    '#718096',
        'border_color':  '#2d3748',
        'accent_color':  '#2dd4bf',
        'accent_text':   '#0f2027',
        'button_bg':     '#2dd4bf',
        'button_text':   '#0f2027',
        'button_hover':  '#14b8a6',
        'button_pressed':'#0d9488',
        'input_bg':      '#152033',
        'play_btn_bg':   '#2dd4bf',
        'play_btn_hover':'#14b8a6',
        'stop_btn_bg':   '#ef4444',
        'stop_btn_hover':'#dc2626',
    },
    'light': {
        'bg_color':      '#f0fafa',
        'menubar_bg':    '#ffffff',
        'group_bg':      '#ffffff',
        'text_color':    '#1a202c',
        'muted_text':    '#a0aec0',
        'border_color':  '#ccf0ec',
        'accent_color':  '#0d9488',
        'accent_text':   '#ffffff',
        'button_bg':     '#0d9488',
        'button_text':   '#ffffff',
        'button_hover':  '#0f766e',
        'button_pressed':'#115e59',
        'input_bg':      '#f7fffe',
        'play_btn_bg':   '#0d9488',
        'play_btn_hover':'#0f766e',
        'stop_btn_bg':   '#ef4444',
        'stop_btn_hover':'#dc2626',
    }
}

SUBTITLE_STYLE = """
    QTextEdit {
        background: %(input_bg)s;
        border: 2px solid %(accent_color)s;
        border-radius: 10px;
        min-height: 130px;
        color: %(text_color)s;
        padding: 12px;
        line-height: 1.6;
    }
"""

PLAY_BUTTON_STYLE = """
    QPushButton#playButton {
        background-color: %(play_btn_bg)s;
        color: #ffffff;
        padding: 12px 40px;
        border-radius: 8px;
        min-width: 160px;
        font-size: 15px;
        font-weight: 700;
    }
    QPushButton#playButton:hover {
        background-color: %(play_btn_hover)s;
    }
"""

STOP_BUTTON_STYLE = """
    QPushButton#playButton {
        background-color: %(stop_btn_bg)s;
        color: #ffffff;
        padding: 12px 40px;
        border-radius: 8px;
        min-width: 160px;
        font-size: 15px;
        font-weight: 700;
    }
    QPushButton#playButton:hover {
        background-color: %(stop_btn_hover)s;
    }
"""

SMALL_BUTTON_STYLE = """
    QPushButton {
        min-width: 32px;
        max-width: 32px;
        min-height: 32px;
        max-height: 32px;
        font-size: 16px;
        font-weight: 700;
        padding: 0;
        border-radius: 6px;
    }
"""

# Legacy alias kept for compatibility
BUTTON_STYLE = SMALL_BUTTON_STYLE
SUBTITLE_LABEL_STYLE = SUBTITLE_STYLE   # unused legacy alias

UI_STRINGS = {
    "menu": {
        "file": "File",
        "help": "Help",
        "about": "About",
        "theme": "Theme",
        "language": "Language"
    },
    "label": {
        "language": "Language:",
        "chapter": "Chapter:",
        "reciter": "Reciter:"
    },
    "button": {"play": "▶  Start Playback", "stop": "■  Stop Playback"},
    "group": {"settings": "Settings"},
    "theme": {
        "dark": "🌙  Dark Mode",
        "light": "☀️  Light Mode"
    }
}
