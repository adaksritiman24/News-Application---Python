#This is a simple news App created using PyQt5
import os
from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5.QtCore import QLine, QSize,Qt
from PyQt5.QtWidgets import QApplication, QComboBox, QGridLayout, QHBoxLayout, QLabel, QLineEdit,  QWidget, QPushButton, QWidget
QGridLayout, QLine
import sys
import requests

from DisplayArea import DisplayArea

BASE_DIR = os.getcwd()+"\\resources\\"
print(BASE_DIR)
#This widgets has control over the whole application
#Contains side bar for Toggle options and searchbar
class Main(QWidget):
    def __init__(self):
        super().__init__()
        self.title = "News At Glance - by @SritimanAdak";
        self.setWindowTitle(self.title)
        self.setWindowIcon(QtGui.QIcon(BASE_DIR+'world-news.png'))
        self.setFixedSize(QSize(1290, 900))
        self.setStyleSheet("background-color: rgb(61, 56, 52)")
        self.setWindowOpacity(0.93)
        self.countryMap = {"India":"in","USA":"us","Russia":"ru","UK":"gb", "France":"fr","China":"ch"}
        self.searchWidgetStyle = """
            background: none;
            background-color: rgba(0,0,0,180);
            border-radius: 10px;
            border : none;
        """
        self.searchLabelStyle = """
            font-size:20px;
            color: white;
            font-weight:bold;
            border: none;
        """
        self.searchBarStyle = """
            QLineEdit{
            margin:0px;
            font-size:18px;
            font-family:Arial;
            border: 2px solid red;
            color: white;
            border-radius: 5px;
            }
        """
        self.createUI()

    #this method is used for creating the whole layout and add widgets
    def createUI(self):
        self.layout = QHBoxLayout(self)

        self.layout.addWidget(self.createMenuOptions())

        #display area is used to show the news fetched from API
        self.displayArea = DisplayArea()
        
        self.layout.addWidget(self.displayArea)#add displayarea to layout

        #business is the initial feed ->This Is shown when the program is run. 
        self.fetchNews("business")

    def createMenuOptions(self): #creating the side munubar for toggle
        self.menu = QWidget()
        customizedStyle = """
            QWidget{
                background-color: qlineargradient(spread:pad, x1:0.00497512, y1:0.023, x2:0, y2:1,
                 stop:0.41791 rgba(40, 0, 13, 255), 
                 stop:0.885572 rgba(20, 0, 111, 255), 
                 stop:1 rgba(40, 0, 13, 255));
                border-radius:4px
            }
            QPushButton{
                color: white;
                background-color: rgba(0,0,0,0);
                margin-bottom:10px;
                padding:8px;
                font-size:20px;
                border:none;
                border: 1px solid rgba(0,0,0,0);
                border-radius: 7px;
                text-align:left;
            }
            QPushButton:hover{
                background-color: black;
                border: 1px solid white;
            }
            QPushButton::pressed{
                background-color: black;
                border: 1px solid white;
            }
            QPushButton:focus{
                background-color: black;
                border: 1px solid white;
            }
        """
        self.menu.setStyleSheet(customizedStyle)
        self.menu.setFixedWidth(300)

        self.menuLayout = QGridLayout()#Layout for adding buttons and Searchbar
        self.menu.setLayout(self.menuLayout)

        self.addMainIcon()
        self.addUtilityButtons()
        self.addSearchWidgetForCountry()
        self.addSearchWidget()
        self.showMoreBtn()
        return self.menu

    def addMainIcon(self): #main icon for the application
        pixmap = QtGui.QPixmap(BASE_DIR+"fake-news.png").scaledToWidth(150)
        labelIcon = QLabel("")
        labelIcon.setPixmap(pixmap)
        labelIcon.setAlignment(Qt.AlignCenter)
        labelIcon.setStyleSheet("background:none;")
        self.menuLayout.addWidget(labelIcon)

        pass
    def addSearchWidget(self): #for adding search reelated items -> search label, search field, search button
        searchWidget = QWidget() #this widget will pack all the other three widgets mentioned
        searchWidget.setStyleSheet(self.searchWidgetStyle)
        #grid layout for searchwidget
        searchLayout = QGridLayout(searchWidget)

        searchLabel = QLabel("Search News") #label
        searchLabel.setStyleSheet(self.searchLabelStyle)
        searchLabel.setFixedHeight(40)

        #search field
        self.searchBar = QLineEdit()
        self.searchBar.setStyleSheet(self.searchBarStyle)
        self.searchBar.setPlaceholderText("Search Term")
        self.searchBar.setFixedHeight(50)

        #search button -> Go
        searchbutton = QPushButton(QtGui.QIcon(BASE_DIR+"search.png"),"")
        searchbutton.setIconSize(QSize(35,35))
        searchbutton.clicked.connect(self.searchHandler)
        searchbutton.setStyleSheet(
            """
            QPushButton{
            background-color: rgba(0,200,0,180);
            margin:0px;
            }
            QPushButton:hover{
                background-color: rgba(0,200,0,250);
            }
            """
        )
        searchbutton.setFixedHeight(50)

        #adding the widgets to layout
        searchLayout.addWidget(searchLabel)
        searchLayout.addWidget(self.searchBar,1, 0)  
        searchLayout.addWidget(searchbutton ,1, 1)

        searchLayout.setAlignment(Qt.AlignTop)

        #adding the main search widget to the main sidemenu layout
        self.menuLayout.addWidget(searchWidget)  

    def addSearchWidgetForCountry(self): #for adding search reelated items for country wise search -> search label, search field, search button
        searchWidget = QWidget() #this widget will pack all the other three widgets mentioned
        searchWidget.setStyleSheet(self.searchWidgetStyle)
        #grid layout for searchwidget
        searchLayout = QGridLayout(searchWidget)

        searchLabel = QLabel("Search By Country") #label
        searchLabel.setStyleSheet(self.searchLabelStyle)
        searchLabel.setFixedHeight(40)
        #search field
        self.searchCountryBar = QComboBox()
        self.searchCountryBar.setEditable(False)
        self.searchCountryBar.addItem("India")
        self.searchCountryBar.addItem("USA")
        self.searchCountryBar.addItem("China")
        self.searchCountryBar.addItem("Russia")
        self.searchCountryBar.addItem("UK")
        self.searchCountryBar.addItem("France")

        self.searchCountryBar.setStyleSheet("""
            QComboBox{
                color:white;
                background-color:rgba(0,0,0,0);
                font-size:25px;
                border:2px solid pink;
                border-radius:6px;
            }
            QComboBox QListView {
                background-color: black;
                color: white;
                border:2px solid white;
            }
        """
        )
        self.searchCountryBar.setPlaceholderText("Country")
        self.searchCountryBar.setFixedHeight(50)

        #search button -> Go
        searchbutton = QPushButton(QtGui.QIcon(BASE_DIR+"search.png"),"")
        searchbutton.setIconSize(QSize(35,35))
        searchbutton.clicked.connect(self.searchByCountry)
        searchbutton.setStyleSheet(
            """
            QPushButton{
            background-color: rgba(0,0,200,180);
            margin:0px;
            }
            QPushButton:hover{
                background-color: rgba(0,0,200,250);
            }
            """
        )
        searchbutton.setFixedHeight(50)

        #adding the widgets to layout
        searchLayout.addWidget(searchLabel)
        searchLayout.addWidget(self.searchCountryBar,1, 0)  
        searchLayout.addWidget(searchbutton ,1, 1)

        searchLayout.setAlignment(Qt.AlignTop)

        #adding the main search widget to the main sidemenu layout
        self.menuLayout.addWidget(searchWidget) 

    def showMoreBtn(self):
        showMore = QPushButton("Show More")
        showMore.setStyleSheet(
            """
            QPushButton{
                background-color: none;
                color:white;
                border:none;
                text-align:center;
            }
            QPushButton:hover{
                color:yellow;
                border:none;
            }
            QPushButton::pressed{
                color:yellow;
            }
            """
        )
        showMore.clicked.connect(self.showNext)
        self.menuLayout.addWidget(showMore)

    def searchByCountry(self):#this function handles searches made through the search field
        searchedCountry = self.countryMap[self.searchCountryBar.currentText()]
        self.fetchNews(type=None, search=True, searchedCountry = searchedCountry)

    def searchHandler(self):#this function handles searches made through the search field
        #internally calls news API
        searchTerm = self.searchBar.text()
        self.fetchNews(type=None, search=True, searchTerm=searchTerm)
        

    def addUtilityButtons(self): #set of buttons used to toggle various category of news

        #for business news
        self.businessBtn = QPushButton(QtGui.QIcon(BASE_DIR+"analytics.png")," Business")
        self.businessBtn.clicked.connect(lambda: self.fetchNews("business"))
        
        #for sports news
        self.sportsBtn = QPushButton(QtGui.QIcon(BASE_DIR+"sports.png")," Sports")
        self.sportsBtn.clicked.connect(lambda: self.fetchNews("sports"))

        #for Politics news
        self.politicsBtn = QPushButton(QtGui.QIcon(BASE_DIR+"capitol.png")," Politics")
        self.politicsBtn.clicked.connect(lambda: self.fetchNews("politics"))

        #for tech news
        self.techBtn = QPushButton(QtGui.QIcon(BASE_DIR+"project-management.png")," Technology")
        self.techBtn.clicked.connect(lambda: self.fetchNews("technology"))

        #for science news
        self.scienceBtn = QPushButton(QtGui.QIcon(BASE_DIR+"science.png")," Science")
        self.scienceBtn.clicked.connect(lambda: self.fetchNews("science"))

        #for entertainment news
        self.eBtn = QPushButton(QtGui.QIcon(BASE_DIR+"popcorn.png")," Entertainment")
        self.eBtn.clicked.connect(lambda: self.fetchNews("entertainment"))

        #for health news
        self.healthBtn = QPushButton(QtGui.QIcon(BASE_DIR+"healthcare.png")," Health")
        self.healthBtn.clicked.connect(lambda: self.fetchNews("health"))


        #adding buttons to the main menu layout
        self.menuLayout.addWidget(self.businessBtn)
        self.menuLayout.addWidget(self.sportsBtn)
        self.menuLayout.addWidget(self.politicsBtn)
        self.menuLayout.addWidget(self.techBtn)
        self.menuLayout.addWidget(self.scienceBtn)
        self.menuLayout.addWidget(self.eBtn)
        self.menuLayout.addWidget(self.healthBtn)
    

        self.menuLayout.setAlignment(QtCore.Qt.AlignTop)

    def fetchNews(self, type, search=False, searchTerm=None, searchedCountry=None):#Fetches news from API, formats data and displays data to News Feed
        api_key = "5bac3ffc864645989537205ecda7c4e5"
        self.page = 1
        if search: # if method is called via search 
            if searchTerm:
                self.URL= f"https://newsapi.org/v2/everything?language=en&q={searchTerm}&sortBy=popularity&apiKey={api_key}&page="
            else:
                self.URL= f"https://newsapi.org/v2/top-headlines?country={searchedCountry}&sortBy=popularity&apiKey={api_key}&page="    
        else: #if method is called via toggle buttons
            self.URL = f"https://newsapi.org/v2/top-headlines?language=en&category={type}&sortBy=popularity&apiKey={api_key}&page="
        self.startFetching(self.URL+str(self.page))    


    def startFetching(self,URL, showNextPage=False):        
        filtered = []
        try: 
            print("Fetching....")
            self.setWindowTitle(self.title+"           Please Wait, fetching news....")
            data = requests.get(URL, timeout=15).json()
            for news in data['articles']:
                filtered.append(
                    {
                        "source" : news["source"]['name'],
                        "author": news["author"],
                        "title": news["title"],
                        "description": news["description"],
                        "img": news['urlToImage'],
                        "url": news["url"],
                        "published": news["publishedAt"].split("T"),
                        "content": news["content"],
                    }
                )

            if showNextPage:
                self.displayArea.showNews(filtered, keepPrevious=True)
            else:
                self.displayArea.showNews(filtered, keepPrevious=False)    
            self.setWindowTitle(self.title)

        except Exception as err:
            print("Coudn't Connect !", err)
            #display error in Display Area
            self.displayArea.showError("Connection Failed!")
            self.page = 0
            return None
    
    def showNext(self):    
        self.page+=1
        self.startFetching(self.URL+str(self.page), showNextPage=True)


if __name__ == "__main__":
    #start application
    app = QApplication(sys.argv)

    window = Main()
    window.show()
    sys.exit(app.exec_())         