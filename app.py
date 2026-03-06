import sys
import os
import json
import platform
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QMessageBox, QComboBox, QTextEdit,
    QGroupBox, QGridLayout, QMenuBar, QDialog, QMenu, QDialogButtonBox,
    QProgressBar, QFrame, QFileDialog
)
from PySide6.QtCore import (
    QUrl, QTranslator, Qt, QObject, Signal, QTimer, QSettings, QSize
)
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtGui import QFont, QIcon, QAction, QIntValidator, QDesktopServices

from configs import (
    BASE_STYLES, COLOR_SCHEME, SUBTITLE_STYLE, UI_STRINGS,
    SMALL_BUTTON_STYLE, PLAY_BUTTON_STYLE, STOP_BUTTON_STYLE,
    RECITER, RECITERS, UI_LANGUAGES, TEXT_TRANSLATIONS, 
    BUNDLED_AUDIO_PATH, CHAPTERS_INFO, LANG_DIR, PNG_ICON
)

def get_user_config_dir():
    """Get the appropriate user configuration directory based on OS."""
    app_name = "QMA"  # Replace with your application name
    if platform.system() == "Windows":
        return os.path.join(os.environ["APPDATA"], app_name)
    elif platform.system() == "Darwin":  # macOS
        return os.path.join(
            os.path.expanduser("~/Library/Application Support"), app_name
        )
    else:  # Linux and other Unix-like systems
        return os.path.join(os.path.expanduser("~/.config"), app_name)

def get_default_audio_path():
    """Return an OS-appropriate writable default directory for audio files."""
    system = platform.system()
    if system == "Windows":
        base = os.environ.get("USERPROFILE", os.path.expanduser("~"))
        return os.path.join(base, "Music", "Quran")
    elif system == "Darwin":  # macOS
        return os.path.join(os.path.expanduser("~"), "Music", "Quran")
    else:  # Linux / other
        # Respect XDG_MUSIC_DIR if set
        xdg_music = os.environ.get("XDG_MUSIC_DIR",
                                   os.path.join(os.path.expanduser("~"), "Music"))
        return os.path.join(xdg_music, "Quran")


QSettings.setDefaultFormat(QSettings.IniFormat)


class HelpDialog(QDialog):
    def __init__(self, parent=None, is_dark_mode=False, lang_code='en'):
        super().__init__(parent)
        self.is_dark_mode = is_dark_mode
        self.lang_code = lang_code
        self.ui_strings = parent.ui_strings if parent else UIStrings(UI_STRINGS)

        self.setWindowTitle(self.ui_strings.get('help.title', 'Help'))
        self.setMinimumSize(QSize(500, 400))

        self.about_label = QLabel()
        self.about_label.setWordWrap(True)
        self.instructions_label = QLabel()
        self.instructions_label.setWordWrap(True)
        self.audio_help_label = QLabel()
        self.audio_help_label.setWordWrap(True)
        self.audio_help_label.setOpenExternalLinks(True)
        self.audio_help_label.linkActivated.connect(self.open_link)

        layout = QVBoxLayout()
        layout.setSpacing(12)
        layout.addWidget(self.about_label)
        layout.addWidget(self.instructions_label)
        layout.addWidget(self.audio_help_label)

        btn_box = QDialogButtonBox(QDialogButtonBox.Ok)
        btn_box.accepted.connect(self.accept)
        layout.addStretch()
        layout.addWidget(btn_box)

        self.setLayout(layout)
        self.update_texts()
        self.apply_styles()
        self.set_rtl_layout()

    def update_texts(self):
        self.setWindowTitle(self.ui_strings.get('help.title', 'Help'))
        self.about_label.setText(self.ui_strings.get('help.about', ''))
        self.instructions_label.setText(self.ui_strings.get('help.instructions', ''))
        self.audio_help_label.setText(self.ui_strings.get('help.audio_files', ''))

    def set_rtl_layout(self):
        if self.lang_code == 'ar':
            self.setLayoutDirection(Qt.RightToLeft)

    def open_link(self, url):
        QDesktopServices.openUrl(QUrl(url))

    def apply_styles(self):
        scheme = COLOR_SCHEME['dark' if self.is_dark_mode else 'light']
        self.setStyleSheet(BASE_STYLES % scheme)


class SettingsManager:
    def __init__(self):
        USER_CONFIG_DIR = get_user_config_dir()
        self.settings = QSettings(f"{USER_CONFIG_DIR}/settings.ini", QSettings.IniFormat)

    @property
    def language(self):
        return self.settings.value("ui/language", "en")

    @language.setter
    def language(self, value):
        self.settings.setValue("ui/language", value)

    @property
    def dark_mode(self):
        return self.settings.value("ui/dark_mode", False, type=bool)

    @dark_mode.setter
    def dark_mode(self, value):
        self.settings.setValue("ui/dark_mode", value)

    @property
    def chapter(self):
        return self.settings.value("playback/chapter", "1")

    @chapter.setter
    def chapter(self, value):
        self.settings.setValue("playback/chapter", str(value))

    @property
    def start_verse(self):
        return self.settings.value("playback/start_verse", "1")

    @start_verse.setter
    def start_verse(self, value):
        self.settings.setValue("playback/start_verse", str(value))

    @property
    def end_verse(self):
        return self.settings.value("playback/end_verse", "1")

    @end_verse.setter
    def end_verse(self, value):
        self.settings.setValue("playback/end_verse", str(value))

    @property
    def repeat(self):
        return self.settings.value("playback/repeat", "1")

    @repeat.setter
    def repeat(self, value):
        self.settings.setValue("playback/repeat", str(value))

    @property
    def font_size(self):
        return self.settings.value("ui/font_size", 22, type=int)

    @font_size.setter
    def font_size(self, value):
        self.settings.setValue("ui/font_size", value)

    @property
    def geometry(self):
        return self.settings.value("window/geometry")

    @geometry.setter
    def geometry(self, value):
        self.settings.setValue("window/geometry", value)

    @property
    def reciter_dir(self):
        return self.settings.value("playback/reciter_dir", RECITER["dir"])

    @reciter_dir.setter
    def reciter_dir(self, value):
        self.settings.setValue("playback/reciter_dir", value)

    @property
    def audio_path(self):
        return self.settings.value("playback/audio_path", "")

    @audio_path.setter
    def audio_path(self, value):
        self.settings.setValue("playback/audio_path", value)


class TranslationManager:
    def __init__(self, app):
        self.app = app
        self.translator = QTranslator()
        self.rtl_languages = {'ar', 'he', 'fa'}
        self.current_lang = 'en'
        self.current_direction = Qt.LeftToRight

    def load_translation(self, lang_code):
        if self.translator.load(f":/translations/{lang_code}.qm"):
            self.app.removeTranslator(self.translator)
            self.app.installTranslator(self.translator)
            self.current_lang = lang_code
            self.current_direction = Qt.RightToLeft if lang_code in self.rtl_languages else Qt.LeftToRight
            return True
        return False


class UIStrings:
    def __init__(self, source):
        try:
            if isinstance(source, str):
                with open(source, 'r', encoding='utf-8') as f:
                    self.strings = json.load(f)
            elif isinstance(source, dict):
                self.strings = source
            else:
                raise ValueError("Invalid source type")
        except Exception as e:
            print(f"Error loading UI strings: {e}")
            self.strings = {}

    def get(self, key, default=""):
        keys = key.split('.')
        value = self.strings
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default


class QuranTextManager:
    def __init__(self, language_file):
        self.translations = {}
        try:
            with open(language_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                for item in data.get("verses", []):
                    key = (item["chapter"], item["verse"])
                    self.translations[key] = item["text"]
        except Exception as e:
            print(f"Error loading {language_file}: {e}")

    def get_text(self, chapter, verse):
        return self.translations.get((chapter, verse), "[No text available]")


class QuranAudioPlayer(QObject):
    playback_finished = Signal()
    verse_progress = Signal(int, int)   # current_index, total

    def __init__(self, base_dir=".", reciter_dir="", chapter=1,
                 start_verse=1, end_verse=1, repeat=1, subtitle_callback=None):
        super().__init__()
        self.base_dir = base_dir
        self.reciter_dir = reciter_dir
        self.chapter = chapter
        self.start_verse = start_verse
        self.end_verse = end_verse
        self.repeat = repeat
        self.current_index = 0
        self.current_repetition = 0
        self.playlist = self._build_playlist()
        self.subtitle_callback = subtitle_callback
        self.is_playing = False

        self.player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.player.setAudioOutput(self.audio_output)
        self.player.mediaStatusChanged.connect(self._handle_media_status)

    def _build_playlist(self):
        playlist = []
        # Support reciter subdirectory if set
        audio_dir = os.path.join(self.base_dir, self.reciter_dir) if self.reciter_dir else self.base_dir
        for verse in range(self.start_verse, self.end_verse + 1):
            chapter_str = f"{self.chapter:03d}"
            verse_str = f"{verse:03d}"
            filename = f"{chapter_str}{verse_str}.mp3"
            filepath = os.path.join(audio_dir, filename)
            if not os.path.isfile(filepath):
                print(f"Warning: File not found: {filepath}")
            playlist.append((filepath, self.chapter, verse))
        return playlist

    def _handle_media_status(self, status):
        if status == QMediaPlayer.MediaStatus.EndOfMedia:
            self.current_index += 1
            if self.current_index >= len(self.playlist):
                self.current_repetition += 1
                if self.current_repetition < self.repeat:
                    self.current_index = 0
                    QTimer.singleShot(50, self._play_current)
                else:
                    self.stop()
                    self.playback_finished.emit()
            else:
                self._play_current()

    def _play_current(self):
        filepath, chap, verse = self.playlist[self.current_index]
        if self.subtitle_callback:
            self.subtitle_callback(chap, verse)
        self.verse_progress.emit(self.current_index + 1, len(self.playlist))
        url = QUrl.fromLocalFile(filepath)
        # print(f"Playing: {filepath} (Rep {self.current_repetition + 1}/{self.repeat})")
        self.player.setSource(url)
        self.player.play()

    def start(self):
        if not self.is_playing and self.playlist:
            self.is_playing = True
            self.current_index = 0
            self.current_repetition = 0
            self._play_current()

    def stop(self):
        self.player.stop()
        self.is_playing = False


def safe_update(widget, text):
    if widget is None:
        return
    if isinstance(widget, (QLabel, QPushButton)):
        widget.setText(text)
    elif isinstance(widget, QGroupBox):
        widget.setTitle(text)
    elif isinstance(widget, QMenu):
        widget.setTitle(text)


class ChapterManager:
    def __init__(self, chapters_file):
        self.chapters = []
        self.chapter_map = {}  # Map by ID
        self.load_chapters(chapters_file)
    
    def load_chapters(self, chapters_file):
        try:
            with open(chapters_file, 'r', encoding='utf-8') as f:
                self.chapters = json.load(f)
                # Create lookup maps
                for chapter in self.chapters:
                    self.chapter_map[chapter['id']] = chapter
        except Exception as e:
            print(f"Error loading chapters: {e}")
            self.chapters = []
    
    def get_chapter_by_id(self, chapter_id):
        return self.chapter_map.get(int(chapter_id), None)
    
    def get_chapter_info_text(self, chapter_id, lang_code='en'):
        chapter = self.get_chapter_by_id(chapter_id)
        if not chapter:
            return ""
        
        if lang_code == 'ar':
            return f"{chapter['name']} ({chapter['total_verses']} آيات)"
        else:
            return f"{chapter['transliteration']} - {chapter['translation']} ({chapter['total_verses']} verses)"
    
    def get_chapter_names_for_completer(self, lang_code='en'):
        """Return list of chapter names for autocomplete"""
        if lang_code == 'ar':
            return [f"{c['id']}: {c['name']}" for c in self.chapters]
        else:
            return [f"{c['id']}: {c['transliteration']} - {c['translation']}" for c in self.chapters]
    
    def get_total_verses(self, chapter_id):
        chapter = self.get_chapter_by_id(chapter_id)
        return chapter['total_verses'] if chapter else 0
    

class MainWindow(QMainWindow):
    def __init__(self, app):
        super().__init__()
        self.setWindowTitle("Quran Memorization Assistant")
        self.setMinimumSize(1000, 720)
        self.setWindowIcon(QIcon(PNG_ICON))

        # Add chapter manager
        self.chapter_manager = None
        self.load_chapters()

        # Core states
        self.is_playing = False
        self.is_dark_mode = False
        self.subtitle_font_size = 22
        self.current_lang = 'en'
        self.text_manager = None
        self.audio_player = None

        # Managers
        self.settings = SettingsManager()
        self.translation_manager = TranslationManager(app)
        self.ui_strings = UIStrings(UI_STRINGS)

        self.ui_languages = UI_LANGUAGES
        self.quran_translations = TEXT_TRANSLATIONS
        self.lang_actions = []

        self._create_menu()
        self._setup_ui()
        self._setup_fonts()
        self._load_settings()
        self._apply_styles()
        self.load_ui_language(self.settings.language)

    def load_chapters(self):
        """Load chapters from chapters.json file"""
        if os.path.exists(CHAPTERS_INFO):
            self.chapter_manager = ChapterManager(CHAPTERS_INFO)
        else:
            print("Warning: chapters.json not found")
            self.chapter_manager = None

    # ------------------------------------------------------------------ fonts
    def _setup_fonts(self):
        self.arabic_font = QFont('Traditional Arabic', self.subtitle_font_size)
        self.subtitle_label.setFont(self.arabic_font)
        self._update_font_size()

    def _update_font_size(self):
        self.arabic_font.setPointSize(self.subtitle_font_size)
        self.subtitle_label.setFont(self.arabic_font)
        self.subtitle_label.document().setDefaultFont(self.arabic_font)

    def increase_font(self):
        self.subtitle_font_size = min(40, self.subtitle_font_size + 2)
        self._update_font_size()

    def decrease_font(self):
        self.subtitle_font_size = max(14, self.subtitle_font_size - 2)
        self._update_font_size()

    # ------------------------------------------------------------------ menu
    def _create_menu(self):
        menu_bar = QMenuBar(self)
        self.file_menu = QMenu("", self)
        self.lang_menu = QMenu("", self)
        self.help_menu = QMenu("", self)
        self.theme_menu = QMenu("", self)

        self.dark_mode_action = QAction("", self)
        self.dark_mode_action.setCheckable(True)
        self.dark_mode_action.triggered.connect(self.toggle_theme)
        self.theme_menu.addAction(self.dark_mode_action)

        self.help_action = QAction("", self)
        self.help_action.triggered.connect(self.show_help)
        self.help_menu.addAction(self.help_action)

        for lang_code in ['en', 'ar']:
            action = QAction("", self)
            action.lang_code = lang_code
            action.triggered.connect(lambda _, code=lang_code: self.load_ui_language(code))
            self.lang_menu.addAction(action)
            self.lang_actions.append(action)

        self.file_menu.addMenu(self.help_menu)
        self.file_menu.addMenu(self.theme_menu)
        self.file_menu.addMenu(self.lang_menu)
        menu_bar.addMenu(self.file_menu)
        self.setMenuBar(menu_bar)

    def show_help(self):
        dialog = HelpDialog(
            parent=self,
            is_dark_mode=self.is_dark_mode,
            lang_code=self.current_lang
        )
        dialog.exec()

    def toggle_theme(self):
        self.is_dark_mode = not self.is_dark_mode
        self.settings.dark_mode = self.is_dark_mode
        self._apply_styles()
        self._update_theme_action_text()

    def _update_theme_action_text(self):
        key = 'theme.light' if self.is_dark_mode else 'theme.dark'
        default = '☀️  Light Mode' if self.is_dark_mode else '🌙  Dark Mode'
        self.dark_mode_action.setText(self.ui_strings.get(key, default))

    # ------------------------------------------------------------------ UI
    def _setup_ui(self):
        central_widget = QWidget()
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(24, 20, 24, 20)
        main_layout.setSpacing(18)

        # ---- Settings group ----
        self.settings_group = QGroupBox()
        grid_layout = QGridLayout(self.settings_group)
        grid_layout.setVerticalSpacing(14)
        grid_layout.setHorizontalSpacing(18)
        grid_layout.setContentsMargins(10, 10, 10, 10)

        INPUT_H = 30

        # Row 0: Reciter
        self.reciter_label = QLabel()
        self.reciter_combo = QComboBox()
        self.reciter_combo.setMinimumHeight(INPUT_H)
        for r in RECITERS:
            self.reciter_combo.addItem(r["name"], userData=r["dir"])
        grid_layout.addWidget(self.reciter_label, 0, 0)
        grid_layout.addWidget(self.reciter_combo, 0, 1, 1, 3)

        # Row 1: Text language
        self.lang_label = QLabel()
        self.lang_combo = QComboBox()
        self.lang_combo.setMinimumHeight(INPUT_H)
        grid_layout.addWidget(self.lang_label, 1, 0)
        grid_layout.addWidget(self.lang_combo, 1, 1, 1, 3)

        # Divider
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        grid_layout.addWidget(line, 2, 0, 1, 4)

        # Row 3: Audio directory
        self.audio_dir_label = QLabel()
        self.audio_dir_edit = QLineEdit()
        self.audio_dir_edit.setMinimumHeight(INPUT_H)
        self.audio_dir_edit.setReadOnly(True)
        self.audio_dir_edit.setPlaceholderText(get_default_audio_path())
        self.audio_dir_edit.setToolTip("Folder containing reciter sub-folders with MP3 files")
        self.browse_btn = QPushButton("📂")
        self.browse_btn.setFixedSize(INPUT_H, INPUT_H)
        self.browse_btn.setToolTip("Browse for audio directory")
        self.browse_btn.clicked.connect(self._browse_audio_dir)
        self.clear_audio_dir_btn = QPushButton("✕")
        self.clear_audio_dir_btn.setFixedSize(INPUT_H, INPUT_H)
        self.clear_audio_dir_btn.setToolTip("Reset to default")
        self.clear_audio_dir_btn.clicked.connect(self._clear_audio_dir)
        audio_dir_row = QHBoxLayout()
        audio_dir_row.setSpacing(6)
        audio_dir_row.addWidget(self.audio_dir_edit)
        audio_dir_row.addWidget(self.browse_btn)
        audio_dir_row.addWidget(self.clear_audio_dir_btn)
        grid_layout.addWidget(self.audio_dir_label, 3, 0)
        grid_layout.addLayout(audio_dir_row, 3, 1, 1, 3)

        # Second divider
        line2 = QFrame()
        line2.setFrameShape(QFrame.HLine)
        line2.setFrameShadow(QFrame.Sunken)
        grid_layout.addWidget(line2, 4, 0, 1, 4)

        # Row 5: Chapter - REPLACED WITH DROPDOWN
        self.chapter_label = QLabel()
        self.chapter_combo = QComboBox()
        self.chapter_combo.setMinimumHeight(INPUT_H)
        self.chapter_combo.setMinimumWidth(250)  # Wider to show full chapter names
        self.chapter_combo.currentIndexChanged.connect(self.on_chapter_changed)
        grid_layout.addWidget(self.chapter_label, 5, 0)
        grid_layout.addWidget(self.chapter_combo, 5, 1, 1, 3)

        # Row 6: Start verse
        self.start_label = QLabel()
        self.start_edit = QLineEdit()
        self.start_edit.setMinimumHeight(INPUT_H)
        self.start_edit.setPlaceholderText("From")
        self.start_edit.setMaximumWidth(90)
        grid_layout.addWidget(self.start_label, 6, 0)
        grid_layout.addWidget(self.start_edit, 6, 1)

        # Row 7: End verse
        self.end_label = QLabel()
        self.end_edit = QLineEdit()
        self.end_edit.setMinimumHeight(INPUT_H)
        self.end_edit.setPlaceholderText("To")
        self.end_edit.setMaximumWidth(90)
        grid_layout.addWidget(self.end_label, 7, 0)
        grid_layout.addWidget(self.end_edit, 7, 1)

        # Row 8: Repeat
        self.repeat_label = QLabel()
        self.repeat_edit = QLineEdit()
        self.repeat_edit.setMinimumHeight(INPUT_H)
        self.repeat_edit.setPlaceholderText("1")
        self.repeat_edit.setMaximumWidth(90)
        grid_layout.addWidget(self.repeat_label, 8, 0)
        grid_layout.addWidget(self.repeat_edit, 8, 1)

        main_layout.addWidget(self.settings_group)

        # ---- Subtitle / verse display group ----
        self.subtitle_group = QGroupBox()
        subtitle_layout = QVBoxLayout(self.subtitle_group)
        subtitle_layout.setSpacing(8)
        subtitle_layout.setContentsMargins(10, 10, 10, 10)

        # Verse index + font controls on same row
        top_row = QHBoxLayout()
        self.subtitle_index = QLabel()
        self.subtitle_index.setStyleSheet("font-weight: 700; font-size: 14px;")
        top_row.addWidget(self.subtitle_index)
        top_row.addStretch()

        self.font_size_label = QLabel()
        self.decrease_font_btn = QPushButton("−")
        self.decrease_font_btn.setObjectName("smallBtn")
        self.decrease_font_btn.setFixedSize(32, 32)
        self.decrease_font_btn.clicked.connect(self.decrease_font)
        self.increase_font_btn = QPushButton("+")
        self.increase_font_btn.setObjectName("smallBtn")
        self.increase_font_btn.setFixedSize(32, 32)
        self.increase_font_btn.clicked.connect(self.increase_font)
        top_row.addWidget(self.font_size_label)
        top_row.addWidget(self.decrease_font_btn)
        top_row.addWidget(self.increase_font_btn)
        subtitle_layout.addLayout(top_row)

        self.subtitle_label = QTextEdit()
        self.subtitle_label.setReadOnly(True)
        self.subtitle_label.setMinimumHeight(130)
        subtitle_layout.addWidget(self.subtitle_label)

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setFormat("%v / %m verses")
        self.progress_bar.setMinimumHeight(24)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border-radius: 6px;
                background: rgba(128,128,128,0.15);
                text-align: center;
                font-size: 12px;
                font-weight: 600;
            }
            QProgressBar::chunk {
                border-radius: 6px;
                background: #2dd4bf;
            }
        """)
        subtitle_layout.addWidget(self.progress_bar)

        main_layout.addWidget(self.subtitle_group)

        # ---- Play button ----
        self.play_button = QPushButton()
        self.play_button.setObjectName("playButton")
        self.play_button.setMinimumWidth(180)
        self.play_button.setMinimumHeight(48)
        main_layout.addWidget(self.play_button, 0, Qt.AlignCenter)

        self.setCentralWidget(central_widget)
        self.play_button.clicked.connect(self._start_playback)
    
    def populate_chapter_combo(self):
        """Populate the chapter dropdown with data from chapters.json"""
        if not self.chapter_manager or not self.chapter_manager.chapters:
            return
        
        self.chapter_combo.blockSignals(True)
        self.chapter_combo.clear()
        
        for chapter in self.chapter_manager.chapters:
            # Create display text based on current language
            if self.current_lang == 'ar':
                display_text = f"{chapter['id']:03d} - {chapter['name']} ({chapter['total_verses']} آيات)"
            else:
                display_text = f"{chapter['id']:03d} - {chapter['transliteration']} - {chapter['translation']} ({chapter['total_verses']} verses)"
            
            # Store the full chapter data as user data
            self.chapter_combo.addItem(display_text, userData=chapter)
        
        self.chapter_combo.blockSignals(False)
        
        # Restore previously selected chapter
        saved_chapter = self.settings.chapter
        try:
            saved_id = int(saved_chapter)
            for i in range(self.chapter_combo.count()):
                chapter_data = self.chapter_combo.itemData(i)
                if chapter_data and chapter_data['id'] == saved_id:
                    self.chapter_combo.setCurrentIndex(i)
                    break
        except ValueError:
            # If saved chapter is not a valid number, default to first chapter
            self.chapter_combo.setCurrentIndex(0)

    def on_chapter_changed(self, index):
        """Handle chapter selection change"""
        if index < 0 or not self.chapter_manager:
            return
        
        chapter_data = self.chapter_combo.itemData(index)
        if chapter_data:
            # Update settings
            self.settings.chapter = str(chapter_data['id'])
            
            # Update verse range hints
            total_verses = chapter_data['total_verses']
            self.start_edit.setPlaceholderText(f"1-{total_verses}")
            self.end_edit.setPlaceholderText(f"1-{total_verses}")
            
            # Optional: Auto-set end verse to total verses if current value is out of range
            try:
                current_end = int(self.end_edit.text()) if self.end_edit.text() else 1
                if current_end > total_verses:
                    self.end_edit.setText(str(total_verses))
            except ValueError:
                pass

    # ------------------------------------------------------------------ audio dir
    def _get_subdirs(self, path):
        """Return sorted list of immediate subdirectory names under path."""
        try:
            return sorted(
                d for d in os.listdir(path)
                if os.path.isdir(os.path.join(path, d)) and not d.startswith('.')
            )
        except OSError:
            return []

    def _refresh_reciter_combo(self, audio_root):
        """
        Repopulate the reciter combo with subdirectories found under audio_root.
        Falls back to the built-in RECITERS list when no subdirs are found.
        Tries to preserve the previously selected reciter name.
        """
        prev_name = self.reciter_combo.currentText()
        prev_data = self.reciter_combo.currentData()

        self.reciter_combo.blockSignals(True)
        self.reciter_combo.clear()

        subdirs = self._get_subdirs(audio_root) if audio_root and os.path.isdir(audio_root) else []

        if subdirs:
            for d in subdirs:
                self.reciter_combo.addItem(d, userData=d)
        else:
            # No subdirs found — fall back to the static RECITERS list
            for r in RECITERS:
                self.reciter_combo.addItem(r["name"], userData=r["dir"])

        self.reciter_combo.blockSignals(False)

        # Restore previous selection by name, then by data, then default to index 0
        restored = False
        for i in range(self.reciter_combo.count()):
            if self.reciter_combo.itemText(i) == prev_name or \
               self.reciter_combo.itemData(i) == prev_data:
                self.reciter_combo.setCurrentIndex(i)
                restored = True
                break
        if not restored:
            self.reciter_combo.setCurrentIndex(0)

    def _browse_audio_dir(self):
        start = self.audio_dir_edit.text() or get_default_audio_path()
        chosen = QFileDialog.getExistingDirectory(
            self,
            self.ui_strings.get('dialog.choose_audio_dir', 'Select Audio Directory'),
            start,
            QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks
        )
        if chosen:
            self.audio_dir_edit.setText(chosen)
            self.settings.audio_path = chosen
            self._refresh_reciter_combo(chosen)

    def _clear_audio_dir(self):
        self.audio_dir_edit.clear()
        self.settings.audio_path = ""
        self._refresh_reciter_combo("")

    def _resolve_audio_path(self):
        """Return the active audio root: custom path > default user dir > bundled dir."""
        custom = self.audio_dir_edit.text().strip()
        if custom and os.path.isdir(custom):
            return custom
        default = get_default_audio_path()
        if os.path.isdir(default):
            return default
        return BUNDLED_AUDIO_PATH

    # ------------------------------------------------------------------ settings
    def _load_settings(self):
        self.current_lang = self.settings.language
        self.load_ui_language(self.current_lang)
        self.is_dark_mode = self.settings.dark_mode

        self.subtitle_font_size = self.settings.font_size
        
        # Don't set chapter text anymore - it's handled by populate_chapter_combo
        self.start_edit.setText(self.settings.start_verse)
        self.end_edit.setText(self.settings.end_verse)
        self.repeat_edit.setText(self.settings.repeat)

        saved_audio = self.settings.audio_path
        if saved_audio:
            self.audio_dir_edit.setText(saved_audio)

        # Refresh reciter list from disk, then restore saved reciter selection
        self._refresh_reciter_combo(saved_audio or "")
        saved_reciter = self.settings.reciter_dir
        for i in range(self.reciter_combo.count()):
            if self.reciter_combo.itemData(i) == saved_reciter or \
            self.reciter_combo.itemText(i) == saved_reciter:
                self.reciter_combo.setCurrentIndex(i)
                break

        if self.settings.geometry:
            self.restoreGeometry(self.settings.geometry)

    # ------------------------------------------------------------------ styles
    def _apply_styles(self):
        scheme = COLOR_SCHEME['dark' if self.is_dark_mode else 'light']
        self.setStyleSheet(BASE_STYLES % scheme)
        self.subtitle_label.setStyleSheet(SUBTITLE_STYLE % scheme)
        if self.is_playing:
            self.play_button.setStyleSheet(STOP_BUTTON_STYLE % scheme)
        else:
            self.play_button.setStyleSheet(PLAY_BUTTON_STYLE % scheme)
        # Re-apply font after stylesheet (CSS can reset QFont on QTextEdit)
        if hasattr(self, 'arabic_font'):
            self._update_font_size()
        # Keep progress bar text visible regardless of theme
        self.progress_bar.setStyleSheet(f"""
            QProgressBar {{
                border-radius: 6px;
                background: rgba(128,128,128,0.15);
                text-align: center;
                font-size: 12px;
                font-weight: 600;
                color: {scheme['text_color']};
            }}
            QProgressBar::chunk {{
                border-radius: 6px;
                background: {scheme['accent_color']};
            }}
        """)

    # ------------------------------------------------------------------ i18n
    def _retranslate_ui(self):
        btn_text = self.ui_strings.get('button.stop', '■  Stop Playback') if self.is_playing \
                   else self.ui_strings.get('button.play', '▶  Start Playback')
        safe_update(self.play_button, btn_text)
        self._update_theme_action_text()
        self.help_action.setText(self.ui_strings.get('menu.about', 'About'))
        self.setWindowTitle(self.ui_strings.get('window.title', 'Quran Memorization Assistant'))
        self.file_menu.setTitle(self.ui_strings.get('menu.file', 'File'))
        self.lang_menu.setTitle(self.ui_strings.get('menu.language', 'Language'))

        for action in self.lang_actions:
            display_name = self.ui_strings.get(
                f"languages.{action.lang_code}",
                self.ui_languages[action.lang_code]['name']
            )
            action.setText(display_name)

        self.lang_combo.clear()
        for lang_code, info in self.quran_translations.items():
            self.lang_combo.addItem(info['name'], userData=lang_code)

        safe_update(self.help_menu,      self.ui_strings.get('menu.help', 'Help'))
        safe_update(self.theme_menu,     self.ui_strings.get('menu.theme', 'Theme'))
        safe_update(self.increase_font_btn, self.ui_strings.get('button.font_increase', '+'))
        safe_update(self.decrease_font_btn, self.ui_strings.get('button.font_decrease', '−'))
        safe_update(self.settings_group, self.ui_strings.get('group.settings', 'Settings'))
        safe_update(self.subtitle_group, self.ui_strings.get('group.subtitle', 'Current Verse'))
        safe_update(self.lang_label,      self.ui_strings.get('label.language', 'Language:'))
        safe_update(self.reciter_label,   self.ui_strings.get('label.reciter', 'Reciter:'))
        safe_update(self.audio_dir_label, self.ui_strings.get('label.audio_dir', 'Audio Dir:'))
        safe_update(self.chapter_label,   self.ui_strings.get('label.chapter', 'Chapter:'))
        safe_update(self.start_label,    self.ui_strings.get('label.start_verse', 'Start Verse:'))
        safe_update(self.end_label,      self.ui_strings.get('label.end_verse', 'End Verse:'))
        safe_update(self.repeat_label,   self.ui_strings.get('label.repetitions', 'Repetitions:'))
        safe_update(self.font_size_label, self.ui_strings.get('label.font_size', 'Font Size:'))

    def _update_rtl_layout(self, lang_code):
        is_rtl = self.ui_languages.get(lang_code, {}).get('rtl', False)
        direction = Qt.RightToLeft if is_rtl else Qt.LeftToRight
        self.setLayoutDirection(direction)
        alignment = Qt.AlignRight if is_rtl else Qt.AlignLeft
        for widget in [self.subtitle_label, self.lang_label, self.reciter_label,
                       self.audio_dir_label, self.chapter_label, self.start_label,
                       self.end_label, self.repeat_label]:
            if isinstance(widget, QLabel):
                widget.setAlignment(alignment | Qt.AlignVCenter)
        for edit in [self.start_edit, self.end_edit, self.repeat_edit]:
            edit.setValidator(QIntValidator(1, 999, self))
        self.lang_combo.setLayoutDirection(direction)

    def load_ui_language(self, lang_code):
        self.current_lang = lang_code
        self.settings.language = lang_code
        try:
            try:
                self.ui_strings = UIStrings(f'{LANG_DIR}/{lang_code}.json')
            except Exception:
                self.ui_strings = UIStrings(UI_STRINGS)
            self._retranslate_ui()
            self._update_rtl_layout(lang_code)
            
            # Repopulate chapter dropdown for new language
            self.populate_chapter_combo()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load translations: {e}")

    # ------------------------------------------------------------------ playback
    def _stop_playback(self):
        if self.audio_player:
            self.audio_player.stop()
            self.audio_player = None
        self.is_playing = False
        self.progress_bar.setValue(0)
        self.subtitle_index.clear()
        self.subtitle_label.clear()
        self._update_play_button()
        self._apply_styles()

    def _update_play_button(self):
        btn_text = self.ui_strings.get('button.stop', '■  Stop Playback') if self.is_playing \
                   else self.ui_strings.get('button.play', '▶  Start Playback')
        self.play_button.setText(btn_text)

    def _start_playback(self):
        if self.is_playing:
            self._stop_playback()
            return

        try:
            # Get chapter from dropdown
            chapter_data = self.chapter_combo.currentData()
            if not chapter_data:
                QMessageBox.warning(
                    self,
                    self.ui_strings.get('error.input', 'Input Error'),
                    self.ui_strings.get('error.no_chapter', 'Please select a chapter')
                )
                return
            
            chapter = chapter_data['id']
            start_verse = int(self.start_edit.text() or "1")
            end_verse = int(self.end_edit.text() or str(chapter_data['total_verses']))
            repeat = int(self.repeat_edit.text() or "1")

            if repeat < 1:
                raise ValueError("Repeat count must be at least 1")
            
            # Validate verse range against chapter total verses
            total_verses = chapter_data['total_verses']
            if start_verse < 1 or end_verse > total_verses or start_verse > end_verse:
                QMessageBox.warning(
                    self,
                    self.ui_strings.get('error.input', 'Input Error'),
                    self.ui_strings.get('error.verse_range', 
                                    f'Please enter valid verse range (1-{total_verses})')
                )
                return

            lang_code = self.lang_combo.currentData() or 'ar'
            text_path = self.quran_translations.get(lang_code, {}).get('path')
            if not text_path or not os.path.exists(text_path):
                QMessageBox.warning(
                    self,
                    self.ui_strings.get('error.file', 'File Error'),
                    self.ui_strings.get('error.translation_file', 'Translation file not found')
                )
                return

            self.text_manager = QuranTextManager(text_path)

            reciter_dir = self.reciter_combo.currentData() or RECITER["dir"]
            self.settings.reciter_dir = reciter_dir

            self.audio_player = QuranAudioPlayer(
                base_dir=self._resolve_audio_path(),
                reciter_dir=reciter_dir,
                chapter=chapter,
                start_verse=start_verse,
                end_verse=end_verse,
                repeat=repeat,
                subtitle_callback=self.update_subtitle
            )
            self.audio_player.playback_finished.connect(self._stop_playback)
            self.audio_player.verse_progress.connect(self._update_progress)
            total = end_verse - start_verse + 1
            self.progress_bar.setRange(0, total)
            self.audio_player.start()
            self.is_playing = True
            self._update_play_button()
            self._apply_styles()

        except ValueError:
            QMessageBox.warning(
                self,
                self.ui_strings.get('error.input', 'Input Error'),
                self.ui_strings.get('error.numeric', 'Please enter valid numeric values')
            )
        except Exception as e:
            self.is_playing = False
            self._update_play_button()
            self._apply_styles()
            QMessageBox.critical(
                self,
                self.ui_strings.get('error.general', 'Error'),
                f"{self.ui_strings.get('error.unknown', 'An error occurred')}: {e}"
            )

    def _update_progress(self, current, total):
        self.progress_bar.setRange(0, total)
        self.progress_bar.setValue(current)

    def update_subtitle(self, chapter, verse):
        if not self.audio_player or not self.audio_player.is_playing:
            self._stop_playback()
            return
        if self.text_manager:
            text = self.text_manager.get_text(chapter, verse)
            current = self.audio_player.current_repetition
            repeats = self.audio_player.repeat
            self.subtitle_label.setText(text)
            self.subtitle_index.setText(f"(Repeat {current + 1}/{repeats}) .:|:. [{chapter}:{verse}]")
        else:
            self._stop_playback()

    def closeEvent(self, event):
        self.settings.geometry    = self.saveGeometry()
        self.settings.dark_mode   = self.is_dark_mode
        self.settings.font_size   = self.subtitle_font_size
        self.settings.language    = self.current_lang
        
        # Save chapter ID from dropdown
        chapter_data = self.chapter_combo.currentData()
        if chapter_data:
            self.settings.chapter = str(chapter_data['id'])
        
        self.settings.start_verse = self.start_edit.text()
        self.settings.end_verse   = self.end_edit.text()
        self.settings.repeat      = self.repeat_edit.text()
        self.settings.audio_path  = self.audio_dir_edit.text().strip()
        super().closeEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow(app)
    window.show()
    sys.exit(app.exec())
