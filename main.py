import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTextEdit,
                             QToolBar, QLineEdit, QPushButton, 
                             QAction, QColorDialog, QHBoxLayout, QWidget, 
                             QScrollArea, QTabWidget)

# 1.顶层窗体;2.标签页;
# 文本内:1.行数;2.文本高亮
# 文本搜索
# 文本滚轮

class CodePad(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(300,400)
        self.setWindowTitle("CodePad")
        self.setMenuBar()
        self.setTabBar()

        # widget = QWidget(self)
        # vb = QHBoxLayout(widget)
        # vb.setContentsMargins(0, 0, 0, 0)
        # self.findText = QLineEdit(self)
        # self.findText.setText('self')
        # findBtn = QPushButton('高亮', self)
        # vb.addWidget(self.findText)
        # vb.addWidget(findBtn)
        # tb = QToolBar(self)
        # tb.addWidget(widget)
        # self.addToolBar(tb)
        self.show()

    def setMenuBar(self):
        # 设置菜单栏:File......
        self.menubar = self.menuBar()
        self.fileMenu = self.menubar.addMenu('File')
        newFile = QAction('New File', self)
        newFile.setShortcut('Ctrl+N')
        self.fileMenu.addAction(newFile)
        self.statusBar()

    def setTabBar(self):
        # 设置标签栏
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        scroll = QScrollArea(self)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        scroll.setWidgetResizable(True)
        textedit = QTextEdit(self)
        textedit.setLineWrapMode(QTextEdit.NoWrap)
        cursor = textedit.textCursor()
        textedit.ensureCursorVisible()
        textedit.setTextCursor(cursor)
        scroll.setWidget(textedit)
        self.tabs.addTab(scroll, "New")

app = QApplication(sys.argv)
codepad = CodePad()
sys.exit(app.exec_())