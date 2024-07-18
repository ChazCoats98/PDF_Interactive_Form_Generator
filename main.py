import sys
from PyQt5.QtWidgets import QApplication
from views import Main

def main():
    app = QApplication(sys.argv)
    
    dashboard = Main()
    dashboard.show()
    
    sys.exit(app.exec_())
    
if __name__ == "__main__":
    main()