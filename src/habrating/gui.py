import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import uic

from . import logger

def run_gui ():
    """
    Run habrating in GUI mode
        :return: exit code
    """
    app = QApplication (sys.argv)
    window = MainWindow ()
    window.show ()
    return app.exec_ ()
    
class MainWindow (QMainWindow):
    def __init__ (self):
        super (MainWindow, self).__init__ ()
        
        uic.loadUi ("mainwindow.ui", self)
        
        self.setWindowTitle ("Habrating")
        self.resize (800, 600)
        self.statusbar.showMessage ("Ready")
        
        self.predict_button.clicked.connect (self.on_predict_clicked)
        
    def get_int_from_field (self, field):
        text = field.text ()
        if len (text):
            return int (text)
        return 0
        
    def predict_url (self, url):
        """
        Predict rating by URL to article
            :param url: self-descriptive
            :return: estimate rating
        """
        # TODO: insert actual model here
        return hash (url) % 350
    
    def predict_direct (self, data):
        """
        Predict rating by directly fed article
            :param data: dict in default format (with 'title', 'body', etc. fields)
            :return: estimate rating
        """
        # TODO: insert actual model here
        # By the way, what's the accuracy of this method?
        return hash (data['title'] + data['body']) % 350
        
    def on_predict_clicked (self):
        try:
            url = self.url_field.text ()
            self.statusbar.showMessage ("I'm thinking, wait a minute...")
            score = 0
            if url:
                logger.info (f"predicting by url {url}")
                score = self.predict_url (url)
            else:
                logger.info (f"predicting by direct feed")
                data = {}
                data['title'] = self.title_field.text ()
                data['body'] = self.text_field.toPlainText ()
                data['views'] = self.get_int_from_field (self.views_edit)
                data['comments'] = self.get_int_from_field (self.comments_edit)
                data['bookmarks'] = self.get_int_from_field (self.bmarks_edit)
                data['author rating'] = self.get_int_from_field (self.arating_edit)
                data['author karma'] = self.get_int_from_field (self.akarma_edit)
                data['author followers'] = self.get_int_from_field (self.asubs_edit)
                score = self.predict_direct (data)
            self.result_field.setText (f"You will get {score} point(s)")
            self.statusbar.showMessage ("Done!")
        except ValueError:
            self.statusbar.showMessage ("Wrong input! Only integers are allowed in additional fields")
            