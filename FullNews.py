from os import read
import webbrowser
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import  QFrame, QLabel, QPushButton, QVBoxLayout
import requests

class FullNews(QFrame):

    def __init__(self, news):
        super().__init__()
        self.maxWidth = 888
        self.news = news
        self.styles = """
            background-color: rgb(200,200,200);
            border : none;
        """
        self.setStyleSheet(self.styles)
        self.setWindowOpacity(1)
        self.createUI()
        
    def createUI(self):
 
        self.vbox = QVBoxLayout(self)
        self.vbox.setAlignment(Qt.AlignTop)

        self.showTitle()
        self.showImage()
        self.showContent()
        self.readFull()

    def showImage(self):   
        # img_URL = "https://cdn.cnn.com/cnnnext/dam/assets/211110193311-elon-musk-file-071321-restricted-super-tease.jpg"
        img_URL = self.news["image"]
        image = QImage()
        image.loadFromData(requests.get(img_URL).content)

        thumbnailImg = QPixmap(image).scaledToWidth(self.maxWidth)
        imageLabel = QLabel()
        imageLabel.setStyleSheet("""
            border:none;
        """)
        imageLabel.setPixmap(thumbnailImg)
        self.vbox.addWidget(imageLabel)   

    def showTitle(self):
        title = QLabel(self.news["title"])
        title.setStyleSheet(
            """
            border:none;
            font-size: 45px;
            color: black;
            font-weight: bold;
            font-family : Trebuchet MS;
            """
        )
        title.setMaximumWidth(self.maxWidth)
        title.setWordWrap(True)
        self.vbox.addWidget(title)

    def showContent(self):
        content = QLabel(self.news["content"])  
        content.setStyleSheet(
            """
            border:none;
            font-size: 32px;
            color: black;
            font-family : Calibri;
            """
        )  
        content.setMaximumWidth(self.maxWidth)
        content.setWordWrap(True)
        self.vbox.addWidget(content)
        
    def readFull(self):
        button = QPushButton("Read Full Article")
        button.clicked.connect(self.readFullNews)
        button.setFixedWidth(self.maxWidth//3)
        button.setStyleSheet(
            """
            QPushButton{
            border:none;
            font-size: 30px;
            color: white;
            background-color: black;
            font-family :  Trebuchet MS;
            border-radius: 8px;
            padding: 6px;
            }
            QPushButton:hover{
            color: yellow;  
            }
            """
        )    
        self.vbox.addWidget(button)


    def readFullNews(self):
        print(f"Redirecting to > {self.news['url']} ...")   
        webbrowser.open(self.news["url"],new = 2)    





