import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTextEdit,
                             QToolBar, QLineEdit, QPushButton, 
                             QAction, QColorDialog, QHBoxLayout, QWidget, QTabWidget)

# 1.顶层窗体;2.标签页;
# 文本内:1.行数;2.文本高亮
# 文本搜索

class CodePad(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(300,400)
        self.setWindowTitle("CodePad")
        self.setMenuBar()

        self.tabs = QTabWidget()
        self.tab1 = QTextEdit(self)
        self.tabs.addTab(self.tab1,"New")

        # self.textEdit = QTextEdit(self)
        self.setCentralWidget(self.tabs)

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

    # 设置菜单栏:File......
    def setMenuBar(self):
        self.menubar = self.menuBar()
        # 设置File菜单
        self.fileMenu = self.menubar.addMenu('File')
        newFile = QAction('New File', self)
        newFile.setShortcut('Ctrl+N')
        self.fileMenu.addAction(newFile)
        self.statusBar()

app = QApplication(sys.argv)
codepad = CodePad()
sys.exit(app.exec_())