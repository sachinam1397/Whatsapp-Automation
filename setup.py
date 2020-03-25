from interface import main_window
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
import sys, os

def main():
	# Start main GUI
	app = QApplication(sys.argv)
	app.setStyleSheet(open('Elements/style.qss', "r").read())
	# app.setAttribute(Qt.AA_EnableHighDpiScaling)

	screen = app.primaryScreen()
	rect = screen.availableGeometry()
	available_width = rect.width()
	available_height = rect.height()

	wizard = main_window(
		available_width, 
		available_height
	)
	wizard.show()
	sys.exit(app.exec_())
	
if __name__ == '__main__':
	main()
