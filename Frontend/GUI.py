from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QFrame, QSizePolicy, QTextEdit, QStackedWidget, QWidget, QLineEdit, QGridLayout, QVBoxLayout, QHBoxLayout, QPushButton
from PyQt5.QtCore import Qt, QSize, QTimer
from PyQt5.QtGui import QFont, QMovie, QTextCharFormat, QColor, QPixmap, QTextBlockFormat, QIcon, QPainter
from dotenv import dotenv_values
import sys
import os

env_vars = dotenv_values(".env")
Assistantname = env_vars.get("Assistantname")

current_dir = os.path.dirname(os.path.abspath(__file__))
old_chat_message = "" 
TempDirPath = os.path.join(current_dir, "Files")
GraphicsDirPath = os.path.join(current_dir, "Graphics/Graphics")

def AnswerModifier(Answer):
    lines = Answer.split("\n")
    non_empty_lines = [line for line in lines if line.strip()]
    modified_answer = "\n".join(non_empty_lines)
    return modified_answer


def QueryModifier(Query):
    new_query = Query.lower().strip()
    query_words = new_query.split()
    question_words = [
        "how", "what", "who", "where", "when", "why",
        "which", "whose", "whom", "can you", "what's",
        "where's", "how's"
    ]

    if any(word in new_query for word in question_words):
        if query_words[-1][-1] in ['.', '?', '!']:
            new_query = new_query[:-1] + "?"
        else:
            new_query += "?"
    else:
        if query_words[-1][-1] in ['.', '?', '!']:
            new_query = new_query[:-1] + "."
        else:
            new_query += "."

    return new_query.capitalize()


def SetMicrophoneStatus(Command):
    with open(rf"{TempDirPath}\Mic.data", "w", encoding="utf-8") as file:
        file.write(Command)


def GetMicrophoneStatus():
    with open(rf"{TempDirPath}\Mic.data", "r", encoding="utf-8") as file:
        Status = file.read()
    return Status


def SetAssistantStatus(Status):
    with open(rf"{TempDirPath}\Status.data", "w", encoding="utf-8") as file:
        file.write(Status)


def GetAssistantStatus():
    with open(rf"{TempDirPath}\Status.data", "r", encoding="utf-8") as file:
        Status = file.read()
    return Status

def MicButtonInitialized():
    SetMicrophoneStatus("False")


def MicButtonClosed():
    SetMicrophoneStatus("True")


def GraphicsDirectoryPath(Filename):
    Path = rf"{GraphicsDirPath}\{Filename}"
    return Path


def TempDirectoryPath(Filename):
    Path = rf"{TempDirPath}\{Filename}"
    return Path


def ShowTextToScreen(Text):
    with open(rf"{TempDirPath}\Responses.data", "w", encoding="utf-8") as file:
        file.write(Text)

class ChatSection(QWidget):

    def __init__(self):
        super(ChatSection, self).__init__()

        layout = QVBoxLayout(self)

        self.chat_text_edit = QTextEdit()
        self.chat_text_edit.setReadOnly(True)

        # ✅ BORDER REMOVE
        self.chat_text_edit.setFrameShape(QFrame.NoFrame)
        self.chat_text_edit.setStyleSheet("""
    QTextEdit {
        background-color: black;
        color: white;
        border: none;
        outline: none;
    }
     """)

        layout.addWidget(self.chat_text_edit)

        self.setStyleSheet("background:black;")

        # Background
        self.setStyleSheet("background-color: black;")

        layout.setSizeConstraint(QVBoxLayout.SetDefaultConstraint)
        layout.setStretch(1, 1)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Text color formatting
        text_color = QColor(Qt.blue)
        self.text_color_format = QTextCharFormat()
        self.text_color_format.setForeground(text_color)

       # GIF Section
        self.gif_label = QLabel()
        self.gif_label.setStyleSheet("border: none;")

        movie = QMovie(GraphicsDirectoryPath("Nova.gif"))
        max_gif_size_w = 480
        max_gif_size_h = 270
        movie.setScaledSize(QSize(max_gif_size_w, max_gif_size_h))

        self.gif_label.setAlignment(Qt.AlignRight | Qt.AlignBottom)
        self.gif_label.setMovie(movie)
        movie.start()

        layout.addWidget(self.gif_label)

        # Extra Text Label
        self.label = QLabel("")
        self.label.setStyleSheet(
           "color: white; "
           "font-size:16px; "
           "margin-right:190px; "
           "border:none; "
           "margin-top: -10px;"
        )
        self.label.setAlignment(Qt.AlignRight)

        layout.addWidget(self.label)

        layout.addStretch(1)
        layout.setSpacing(-10)

        # Font Size
        font = QFont()
        font.setPointSize(13)
        self.chat_text_edit.setFont(font)

        # Timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.loadMessages)
        self.timer.timeout.connect(self.SpeechRecognition)
        self.timer.start(100)

         # Event filter
        self.chat_text_edit.viewport().installEventFilter(self)

         # Scrollbar Styling
        self.setStyleSheet("""
        QScrollBar:vertical {
            border: none;
            background: black;
            width: 10px;
            margin: 0px;
        }

        QScrollBar::handle:vertical {
            background: white;
            min-height: 20px;
            border-radius: 0px;
        }

        QScrollBar::add-line:vertical {
            background: black;
            subcontrol-position: bottom;
            subcontrol-origin: margin;
            height: 10px;
        }

        QScrollBar::sub-line:vertical {
            background: black;
            subcontrol-position: top;
            subcontrol-origin: margin;
            height: 10px;
        }

        QScrollBar::up-arrow:vertical,
        QScrollBar::down-arrow:vertical {
            background: none;
        }

        QScrollBar::add-page:vertical,
        QScrollBar::sub-page:vertical {
            background: none;
        }
    """)
        
          # TIMER
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.loadMessages)
        self.timer.timeout.connect(self.SpeechRecognition)
        self.timer.start(10)

    def loadMessages(self):

        global old_chat_message

        try:
            with open(
                TempDirectoryPath("Responses.data"),
                "r",
                encoding="utf-8"
            ) as file:

                messages = file.read()

            if messages != old_chat_message:

               self.chat_text_edit.clear()
               self.chat_text_edit.append(messages)

               old_chat_message = messages
               
        except:
              pass
        
    def SpeechRecognition(self):
        try:
            with open(
                TempDirectoryPath("Status.data"),
                "r",
                encoding="utf-8"
            ) as file:
                self.label.setText(file.read())
        except:
            pass


    # ✅ INSIDE CLASS
    def addMessage(self, message, color):

        cursor = self.chat_text_edit.textCursor()

        fmt = QTextCharFormat()
        fmt.setForeground(QColor(color))

        cursor.setCharFormat(fmt)
        cursor.insertText(message + "\n")

        self.chat_text_edit.setTextCursor(cursor)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(-10, 40, 40, 100)
        layout.setSpacing(-100)

        self.chat_text_edit = QTextEdit()
        self.chat_text_edit.setReadOnly(True)
        self.chat_text_edit.setTextInteractionFlags(Qt.NoTextInteraction)
        self.chat_text_edit.setFrameStyle(QFrame.NoFrame)

        layout.addWidget(self.chat_text_edit)

def toggle_icon(self, event=None):

   if self.toggled:
      self.load_icon(GraphicsDirectoryPath("Mic_on.png"), 40, 40)
      MicButtonInitialized()
   else:
         self.load_icon(GraphicsDirectoryPath("Mic_off.png"), 40, 40)
         MicButtonClosed()

         self.toggled = not self.toggled

def load_icon(self, path, width=40, height=40):
    pixmap = QPixmap(path)
    new_pixmap = pixmap.scaled(width, height)
    self.icon_label.setPixmap(new_pixmap)

class InitialScreen(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        desktop = QApplication.desktop()
        screen_width = desktop.screenGeometry().width()
        screen_height = desktop.screenGeometry().height()

        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignCenter)

        # =========================
        # NOVA GIF
        # =========================
        self.gif_label = QLabel()
        self.gif_label.setAlignment(Qt.AlignCenter)

        movie = QMovie(GraphicsDirectoryPath("Nova.gif"))

        # ✅ NO STRETCH
        self.gif_label.setFixedSize(550, 550)
        self.gif_label.setMovie(movie)

        movie.start()

        # =========================
        # STATUS TEXT (MIC KE UPAR)
        # =========================
        self.label = QLabel("Available")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("""
            color:white;
            font-size:18px;
        """)

        # =========================
        # MIC ICON
        # =========================
        self.icon_label = QLabel()
        self.icon_label.setAlignment(Qt.AlignCenter)

        self.toggled = False
        self.load_icon(GraphicsDirectoryPath("Mic_off.png"))

        self.icon_label.mousePressEvent = self.toggle_icon

        # =========================
        # LAYOUT ORDER ⭐ IMPORTANT
        # =========================
        main_layout.addStretch()

        main_layout.addWidget(self.gif_label)
        main_layout.addSpacing(20)

        # ✅ TEXT ABOVE MIC
        main_layout.addWidget(self.label)

        main_layout.addSpacing(10)
        main_layout.addWidget(self.icon_label)

        main_layout.addStretch()

        self.setLayout(main_layout)
        self.setStyleSheet("background:black;")
        self.setFixedSize(screen_width, screen_height)

        # =========================
        # STATUS UPDATE TIMER
        # =========================
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.SpeechRecogText)
        self.timer.start(200)

    # =========================
    # LOAD MIC ICON
    # =========================
    def load_icon(self, path):

        pixmap = QPixmap(path)

        self.icon_label.setPixmap(
            pixmap.scaled(
                70,
                70,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
        )

    # =========================
    # MIC TOGGLE
    # =========================
    def toggle_icon(self, event=None):

        if self.toggled:
            self.load_icon(GraphicsDirectoryPath("Mic_off.png"))
            MicButtonClosed()
        else:
            self.load_icon(GraphicsDirectoryPath("Mic_on.png"))
            MicButtonInitialized()

        self.toggled = not self.toggled

    # =========================
    # STATUS TEXT UPDATE
    # =========================
    def SpeechRecogText(self):
        try:
            with open(
                TempDirectoryPath("Status.data"),
                "r",
                encoding="utf-8"
            ) as file:
                self.label.setText(file.read())
        except:
            pass

class MessageScreen(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        desktop = QApplication.desktop()
        screen_width = desktop.screenGeometry().width()
        screen_height = desktop.screenGeometry().height()

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 380, 0, 0)

        # spacer
        spacer = QLabel("")
        layout.addWidget(spacer)

        # CHAT SECTION
        self.chat_section = ChatSection()
        layout.addWidget(self.chat_section)

        self.setLayout(layout)
        self.setStyleSheet("background-color:black;")

        self.setFixedHeight(screen_height)
        self.setFixedWidth(screen_width)

class CustomTopBar(QWidget):

    def __init__(self, parent, stacked_widget):
        super().__init__(parent)

        self.parent = parent
        self.stacked_widget = stacked_widget
        self.current_screen = None

        self.initUI()

    def initUI(self):

        self.setFixedHeight(50)

        layout = QHBoxLayout(self)
        layout.setAlignment(Qt.AlignRight)
        layout.setContentsMargins(10, 0, 10, 0)

        # ===== Home Button =====
        home_button = QPushButton()
        home_icon = QIcon(GraphicsDirectoryPath("Home.png"))
        home_button.setIcon(home_icon)
        home_button.setText(" Home")
        home_button.setStyleSheet(
          "height:40px; line-height:40px; background-color:white; color:black;"
        )
        layout.addWidget(home_button)

        # ===== Chat Button =====
        message_button = QPushButton()
        message_icon = QIcon(GraphicsDirectoryPath("Chats.png"))
        message_button.setIcon(message_icon)
        message_button.setText(" Chat")
        message_button.setStyleSheet(
          "height:40px; line-height:40px; background-color:white; color:black;"
        )
        layout.addWidget(message_button)

        # ===== Minimize Button =====
        self.minimize_button = QPushButton()
        self.minimize_icon = QIcon(GraphicsDirectoryPath("Minimize2.png"))
        self.minimize_button.setIcon(self.minimize_icon)
        self.minimize_button.setStyleSheet("background-color:white")
        self.minimize_button.clicked.connect(self.minimizeWindow)
        layout.addWidget(self.minimize_button)


        # ===== Maximize Button =====
        self.maximize_button = QPushButton()
        self.maximize_icon = QIcon(GraphicsDirectoryPath("Maximize.png"))
        self.restore_icon = QIcon(GraphicsDirectoryPath("Minimize.png"))

        self.maximize_button.setIcon(self.maximize_icon)
        self.maximize_button.setStyleSheet("background-color:white")
        self.maximize_button.clicked.connect(self.maximizeWindow)
        layout.addWidget(self.maximize_button)

        # ===== Close Button =====
        close_button = QPushButton()
        close_icon = QIcon(GraphicsDirectoryPath("Close.png"))
        close_button.setIcon(close_icon)
        close_button.setStyleSheet("background-color:white")
        close_button.clicked.connect(self.closeWindow)


        # ===== Line Separator =====
        line_frame = QFrame()
        line_frame.setFixedHeight(1)
        line_frame.setFrameShape(QFrame.HLine)
        line_frame.setFrameShadow(QFrame.Sunken)
        line_frame.setStyleSheet("border-color: black;")


        # ===== Title Label =====
        title_label = QLabel(f"{str(Assistantname).capitalize()} AI")
        title_label.setStyleSheet(
          "color: black; font-size: 18px; background-color:white"
        )


        # ===== Screen Switching =====
        home_button.clicked.connect(
             lambda: self.stacked_widget.setCurrentIndex(0)
        )

        message_button.clicked.connect(
                lambda: self.stacked_widget.setCurrentIndex(1)
        )
    
        # ===== Add Widgets to Layout =====
        layout.addWidget(title_label)
        layout.addStretch(1)
        layout.addWidget(home_button)
        layout.addWidget(message_button)
        layout.addStretch(1)
        layout.addWidget(self.minimize_button)
        layout.addWidget(self.maximize_button)
        layout.addWidget(close_button)
        self.setLayout(layout)
        self.draggable = True
        self.offset = None

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), Qt.white)
        super().paintEvent(event)

    def minimizeWindow(self):
        self.parent.showMinimized()
    def maximizeWindow(self):

        if self.parent.isMaximized():
           self.parent.showNormal()
           self.maximize_button.setIcon(self.maximize_icon)
        else:
           self.parent.showMaximized()
           self.maximize_button.setIcon(self.restore_icon)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and self.draggable:
           self.offset = event.pos()

    def mouseMoveEvent(self, event):
         if self.offset is not None and self.draggable:
            self.parent().move(event.globalPos() - self.offset)

    def mouseReleaseEvent(self, event):
        self.offset = None

    def closeWindow(self):
        self.parent.close()

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.initUI()


    def initUI(self):

        desktop = QApplication.desktop()
        screen_width = desktop.screenGeometry().width()
        screen_height = desktop.screenGeometry().height()

        # ===== Stacked Widget =====
        self.stacked_widget = QStackedWidget(self)

        self.initial_screen = InitialScreen()
        self.message_screen = MessageScreen()

        self.stacked_widget.addWidget(self.initial_screen)
        self.stacked_widget.addWidget(self.message_screen)

        # ===== Main Layout =====
        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # ===== Top Bar =====
        self.top_bar = CustomTopBar(self, self.stacked_widget)

        main_layout.addWidget(self.top_bar)
        main_layout.addWidget(self.stacked_widget)

        self.setCentralWidget(main_widget)

        # ===== Window Settings =====
        self.setGeometry(0, 0, screen_width, screen_height)
        self.setStyleSheet("background-color: black;")

        self.show()

def GraphicalUserInterface():

    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
