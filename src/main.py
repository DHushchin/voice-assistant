from gui import ListenerGUI
from timefhuman import timefhuman
import datetime

def main():
    print(timefhuman('3 days later', now=datetime.datetime.now().date()))
    # gui = ListenerGUI()
    # gui.run()

if __name__ == '__main__':
    main()
