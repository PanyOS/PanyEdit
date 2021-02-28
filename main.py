import sys
import os
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTextEdit,
                             QToolBar, QLineEdit, QPushButton, 
                             QAction, QColorDialog, QHBoxLayout, QWidget, 
                             QScrollArea, QTabWidget, QFileDialog, QPlainTextEdit)

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
        # 设置创建动作
        newFile = QAction('New File', self)
        newFile.setShortcut('Ctrl+N')
        # 设置打开动作
        openFile = QAction('Open File', self)
        openFile.setShortcut('Ctrl+O')
        openFile.triggered.connect(self.slot_openFile)

        self.fileMenu.addAction(newFile)
        self.fileMenu.addAction(openFile)
        self.statusBar()

    def slot_openFile(self):
        # 打开文件
        fileName_choose, filetype = QFileDialog.getOpenFileName(self,
                                                                "Open File",  
                                                                os.getcwd(), 
                                                                "All Files (*);;Text Files (*.txt)")
        with open(fileName_choose, "r") as file_read:
            read_text = file_read.read()
            tab = self.addTab(fileName_choose)
            tab.widget().setPlainText(read_text)

    def addTab(self, filename):
        # 添加标签页
        scroll = QScrollArea(self)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        scroll.setWidgetResizable(True)
        textedit = QPlainTextEdit(self)
        textedit.setLineWrapMode(QPlainTextEdit.NoWrap)
        cursor = textedit.textCursor()
        textedit.ensureCursorVisible()
        textedit.setTextCursor(cursor)
        scroll.setWidget(textedit)
        self.tabs.addTab(scroll, filename)
        return scroll

    def setTabBar(self):
        # 设置标签栏
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
    

app = QApplication(sys.argv)
codepad = CodePad()
sys.exit(app.exec_())