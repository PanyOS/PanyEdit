import sys
import os
from PyQt5.QtGui import QColor, QPainter, QTextFormat
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTextEdit,
                             QToolBar, QLineEdit, QPushButton, QStatusBar,
                             QAction, QColorDialog, QHBoxLayout, QWidget, 
                             QScrollArea, QTabWidget, QFileDialog, QPlainTextEdit)

# 1.顶层窗体;2.标签页;
# 文本内:1.行数;2.文本高亮
# 文本搜索
# 文本滚轮

class LineNumberArea(QWidget):

    def __init__(self, editor):
        super().__init__(editor)
        self.myeditor = editor

    def sizeHint(self):
        return Qsize(self.editor.lineNumberAreaWidth(), 0)

    def paintEvent(self, event):
        self.myeditor.lineNumberAreaPaintEvent(event)

class CodeEditor(QPlainTextEdit):
    def __init__(self):
        super().__init__()
        self.lineNumberArea = LineNumberArea(self)

        self.blockCountChanged.connect(self.updateLineNumberAreaWidth)
        self.updateRequest.connect(self.updateLineNumberArea)
        self.cursorPositionChanged.connect(self.highlightCurrentLine)

        self.updateLineNumberAreaWidth(0)


    def lineNumberAreaWidth(self):
        digits = 1
        count = max(1, self.blockCount())
        while count >= 10:
            count /= 10
            digits += 1
        space = 3 + self.fontMetrics().width('9') * digits
        return space


    def updateLineNumberAreaWidth(self, _):
        self.setViewportMargins(self.lineNumberAreaWidth(), 0, 0, 0)


    def updateLineNumberArea(self, rect, dy):

        if dy:
            self.lineNumberArea.scroll(0, dy)
        else:
            self.lineNumberArea.update(0, rect.y(), self.lineNumberArea.width(),
                       rect.height())

        if rect.contains(self.viewport().rect()):
            self.updateLineNumberAreaWidth(0)


    def resizeEvent(self, event):
        super().resizeEvent(event)

        cr = self.contentsRect();
        self.lineNumberArea.setGeometry(QRect(cr.left(), cr.top(),
                    self.lineNumberAreaWidth(), cr.height()))


    def lineNumberAreaPaintEvent(self, event):
        mypainter = QPainter(self.lineNumberArea)
        mypainter.fillRect(event.rect(), Qt.white)

        block = self.firstVisibleBlock()
        blockNumber = block.blockNumber()
        top = self.blockBoundingGeometry(block).translated(self.contentOffset()).top()
        bottom = top + self.blockBoundingRect(block).height()

        # Just to make sure I use the right font
        height = self.fontMetrics().height()
        while block.isValid() and (top <= event.rect().bottom()):
            if block.isVisible() and (bottom >= event.rect().top()):
                number = str(blockNumber + 1)
                mypainter.setPen(Qt.blue)
                mypainter.drawText(0, int(top), self.lineNumberArea.width(), height,
                 Qt.AlignRight, number)

            block = block.next()
            top = bottom
            bottom = top + self.blockBoundingRect(block).height()
            blockNumber += 1


    def highlightCurrentLine(self):
        extraSelections = []

        if not self.isReadOnly():
            selection = QTextEdit.ExtraSelection()

            lineColor = QColor(Qt.blue).lighter(195)

            selection.format.setBackground(lineColor)
            selection.format.setProperty(QTextFormat.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extraSelections.append(selection)
        self.setExtraSelections(extraSelections)

class CodePad(QMainWindow):
    def __init__(self):
        super().__init__()
        self.message = ""
        self.resize(300,400)
        self.setWindowTitle("CodePad")
        self.setMenuBar()
        self.setTabBar()
        self.setStatus()

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

    def setStatus(self):
        # 设置状态栏
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)
        self.statusbar.showMessage(self.message)

    def setMessage(self):
        # 设置状态栏信息
        cursor = self.textedit.textCursor()
        row = cursor.blockNumber()
        col = cursor.columnNumber()
        self.message = "{}行,{}列".format(row+1, col+1)
        self.statusbar.showMessage(self.message)

    def addTab(self, filename):
        # 添加标签页
        scroll = QScrollArea(self)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setWidgetResizable(True)
        self.textedit = CodeEditor()
        self.textedit.setLineWrapMode(CodeEditor.NoWrap)
        cursor = self.textedit.textCursor()
        self.textedit.ensureCursorVisible()
        self.textedit.setTextCursor(cursor)
        self.textedit.cursorPositionChanged.connect(self.setMessage)
        scroll.setWidget(self.textedit)
        self.tabs.addTab(scroll, filename)
        return scroll

    def slot_openFile(self):
        # 打开文件
        fileName_choose, filetype = QFileDialog.getOpenFileName(self,
                                                                "Open File",  
                                                                os.getcwd(), 
                                                                "All Files (*);;Text Files (*.txt)")
        with open(fileName_choose, "r", encoding='utf-8') as file_read:
            read_text = file_read.read()
            tab = self.addTab(fileName_choose)
            tab.widget().setPlainText(read_text)

    def setTabBar(self):
        # 设置标签栏
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
    

app = QApplication(sys.argv)
codepad = CodePad()
sys.exit(app.exec_())