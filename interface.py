from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPalette, QColor, QPixmap
from PyQt5.QtCore import *
from ui_widgets import *
from whatsapp import main, get_driver, page2_main
from threading import Thread


class ThreadWithReturnValue(Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs={}, Verbose=None):
        Thread.__init__(self, group, target, name, args, kwargs)
        self._return = None
    def run(self):
        print(type(self._target))
        if self._target is not None:
            self._return = self._target(*self._args,
                                                **self._kwargs)
    def join(self, *args):
        Thread.join(self, *args)
        return self._return
        

class main_window(QWizard):
	def __init__(
			self, 
			available_width, 
			available_height, 
			parent=None
		):
		super(main_window, self).__init__(parent)
		self.setWindowIcon(QIcon('Elements/logo.png'))
		self.setWindowTitle("Whatsapp Automate")
		self.setFixedSize(available_width/2, available_height/2)
		self.box_width = available_width/2
		self.box_height = available_height/2
	
		self.page1 = wizard_page(1)
		self.addPage(self.page1)
		self.page2 = wizard_page(2)
		self.addPage(self.page2)
		self.page3 = wizard_page(3)
		self.addPage(self.page3)

		self.currentIdChanged.connect(self.page_changed_handler)

	def page_changed_handler(self, page):
		if page == -1:
			print('Cancelled')
		elif page == 0:
			pass
		elif page == 1:
			if(self.field("StartingPoint") == ''):
				StartingPoint = 2
			else:
				StartingPoint = self.field("StartingPoint")
			if(self.field("EndingPoint") == ''):
				EndingPoint = 0
			else:
				EndingPoint = self.field("EndingPoint")
			print(self.field("Message"))
			if(self.field("Message") == ''):
				msg = None
			else:
				msg = self.field("Message")

			self.dictionary,self.name_dictionary = main(
				self.field("Path"),
				int(self.field("SheetIndex")),
				int(StartingPoint),
				int(EndingPoint),
				msg
				)
			if(len(self.name_dictionary) > 0):
				for key,value in self.dictionary.items():
					if(key in self.name_dictionary):
						self.dictionary[key] = self.name_dictionary[key] + " " + self.dictionary[key]

			
			self.driver = get_driver()

			self.page2.layout().itemAt(0).widget().layout().itemAt(0).widget().setText('Pass')

		elif page == 2:
			table = self.page3.layout().itemAt(0).widget().layout().itemAt(1).widget()
			if(self.field("DocPath") == ''):
				path = None
			else:
				path = self.field("DocPath")
			time_out = int(self.field("Timeout"))
			start_thread(self.driver,time_out,self.dictionary,self.name_dictionary,path)
			# page2_main(self.driver,time_out,self.dictionary,self.name_dictionary,path)


def start_thread(driver,time_out,dictionary,name_dictionary,path):
	start_msg = Thread(
		target = page2_main,
		args = (driver,time_out,dictionary,name_dictionary,path,)
		)
	start_msg.start()