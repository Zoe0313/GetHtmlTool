#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
import threading
from urllib import request
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication,QMainWindow
from gethtml_ui import Ui_Dialog

class GetHtmlDialog(QMainWindow,Ui_Dialog):
    htmlGet = QtCore.pyqtSignal(str)

    def __init__(self, *args, **kwargs):
        super(GetHtmlDialog, self).__init__(*args,**kwargs)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.on_click_get)

        self.headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}
        # 同步更新内容
        self.htmlGet.connect(lambda s: self.textBrowser.setPlainText(s))

        clipboard = QApplication.clipboard()
        url = clipboard.text()
        print('clipboard url: '+url)
        if url:
            self.lineEdit.setText(url)

    def get_html(self, url):
        if (not 'http' in url) or (not 'https' in url):
            url = 'http://' + url
        try:
            req = request.Request(url,headers=self.headers)
            res = request.urlopen(req)
            html = res.read().decode('utf-8')
            # 同步到主线程
            self.htmlGet.emit(html)
        except Exception as e:
            self.htmlGet.emit(e.message)
        finally:
            self.pushButton.setEnabled(True)

    def on_click_get(self):
        url = self.lineEdit.text()
        if not url:
            self.textBrowser.append("url不能为空")
            return

        self.pushButton.setEnabled(False)
        t = threading.Thread(target=GetHtmlDialog.get_html,
                             args=(self, url),
                             name='thread')
        t.start()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    dialog = GetHtmlDialog()
    dialog.show()
    sys.exit(app.exec_())
