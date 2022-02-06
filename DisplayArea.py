from PyQt5.QtCore import QLine, QSize, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QGridLayout,QLabel, QScrollArea, QWidget, QPushButton,QWidget, QApplication
QGridLayout, QLine
import os
from FullNews import FullNews
from LoadingScreen import LoaderScreen

BASE_DIR = os.getcwd()+"\\resources\\"
class DisplayArea(QScrollArea):
    def __init__(self):
        super().__init__()

        self.newsCursor = 0
        self.styler = """
            QWidget{
            background-color: rgba(0,0,17,160);
            border-radius: 5px;
            }
            QScrollArea{
            border-radius: 5px;
            }
        """
        self.setStyleSheet(self.styler)
        self.gridWidget = QWidget()
        
        self.grid = QGridLayout(self.gridWidget)
  
        self.setWidgetResizable(True)
        self.setWidget(self.gridWidget) 
    
    def removeAll(self):
        for i in reversed(range(self.grid.count())):
            self.grid.itemAt(i).widget().setParent(None)
        self.verticalScrollBar().setSliderPosition(0)    
        
    def showNews(self, news, keepPrevious=False):
        self.news = news
        if not keepPrevious:
            self.newsCursor = 0
            self.removeAll()

        cols = 2
        for i,article in enumerate(self.news):
            self.grid.addWidget(self.newsTemplate(article), self.newsCursor, i%cols)

            if i%cols == cols - 1:
                self.newsCursor+=1


    def showError(self, message):
        self.removeAll()
        error = QLabel(f"<img src = '{BASE_DIR}error.png' alt='NF'width=100 height = 100 /><br/><center>Error: {message}</center>")

        error.setStyleSheet("""
            color:rgb(255, 100, 100);
            background-color: none;
            font-size:30px;
        """)
        error.setAlignment(Qt.AlignCenter)
        self.grid.addWidget(error)

    def newsTemplate(self, article):
    
        newsPoster = QWidget()
        vbox = QGridLayout(newsPoster)
        # vbox.setAlignment(Qt.AlignTop)
        newsPoster.setStyleSheet(
            f"""
            margin: 4px;
            background-color: qlineargradient(spread:reflect, x1:0.870826, y1:0.04,
                            x2:0.865672, y2:0.528,
                            stop:0 rgba(69, 0, 70, 233), 
                            stop:1 rgba(120, 15, 78, 255));
            border-radius: 8px;
            border: 1px solid rgba(100,100,100,144);
            """
        )   
        newsPoster.setFixedHeight(600)
        newsPoster.setFixedWidth(440)  

        #title-adding
        titleLabel = QLabel()
        titleLabel.setStyleSheet("""
            color: white;
            font-size:32px;
            font-weight:bold;
            background: none;
            padding-top:0px;
            font-family: Trebuchet MS;
            border:none;
        """)
        titleLabel.setText(article["title"])
        titleLabel.setAlignment(Qt.AlignLeft)
        titleLabel.setWordWrap(True)
        vbox.addWidget(titleLabel)

        #title-adding
        dateLabel = QLabel(article['published'][0]+", "+article["published"][1][:-4])
        dateLabel.setStyleSheet("""
            color: white;
            font-size:18px;
            font-style:italic;
            background: none;
            padding-top:0px;
            font-family: Arial;
            border:none;
        """)
        dateLabel.setFixedHeight(38)
        dateLabel.setAlignment(Qt.AlignLeft)
        dateLabel.setWordWrap(True)
        vbox.addWidget(dateLabel)

        #description-adding
        descLabel = QLabel()
        descLabel.setStyleSheet("""
            color: pink;
            font-size:22px;
            background: none;
            padding-top:0px;
            font-family: Yu Gothic UI;
            border: none;
        """)
        descLabel.setText(article["description"])
        descLabel.setAlignment(Qt.AlignLeft)
        descLabel.setWordWrap(True)
        vbox.addWidget(descLabel)

        read_full = QPushButton("Read News")
        read_full.setStyleSheet(
            """
            QPushButton{
            background:none;
            border: 2px solid pink;
            border-radius:10px;
            font-family: Franklin Gothic Medium;
            font-size:17px;
            font-weight: bold;
            color: rgb(200, 200, 190);
            }
            QPushButton:hover{
                background-color:rgb(230, 100, 180);
                color: white;
            }
            QPushButton:pressed{
                background-color:rgb(230, 100, 180);
                color: white;
            }
            """
        )
        read_full.setFixedHeight(57)
        read_full.clicked.connect(lambda: self.showFullNews(article["img"],article['title'], article["description"], article["url"]))
        vbox.addWidget(read_full)
        
        return newsPoster

    def showFullNews(self, image, title, content, url):
        loader = LoaderScreen()
        loader.showLoading()
        QApplication.processEvents()
        current_news = {
            "image" : image,
            "title": title,
            "content":content,
            "url":url,
        }
        try:
            fullNewsWidget = FullNews(current_news)

            self.removeAll()
            

            self.backButton = QPushButton("Back")
            self.backButton.setIcon(QIcon(BASE_DIR+"back.png"))
            self.backButton.setIconSize(QSize(40, 40))
            self.backButton.setStyleSheet("""
                color: white;
                background-color: blue;
                font-size: 22px;
                font-family: Arial;
            """)
            self.backButton.setFixedWidth(100)
            self.backButton.clicked.connect(self.backToPage)

            self.grid.addWidget(self.backButton,0,0,1,1)
            self.grid.addWidget(fullNewsWidget,1,0,2,2)
        except Exception as exp:
            print("Connection Error!")
        loader.stopLoading()    
            

    def backToPage(self):
        self.showNews(self.news)


