import sys
from PyQt5.QtWidgets import QApplication
from modules.ui import UpbitTradingUI
from modules.trader import UpbitTrader

def main():
    app = QApplication(sys.argv)
    
    # trader 객체 생성
    trader = UpbitTrader()
    
    # UI 생성 시 trader 객체 전달
    ex = UpbitTradingUI(trader)
    ex.show()
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main() 