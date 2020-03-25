from selenium import webdriver
import time
from random import randint
from excel import open_file

def get_scanner():
	try:
		driver = webdriver.Chrome("chromedriver.exe")
	except Exception as error:
		print("[ DRIVER ] NOT FOUND")
	try:
		driver.get("https://web.whatsapp.com")
	except:
		print("[ INTERNET CONNECTIVITY ]")
	while(True):
		try:
			element = driver.find_element_by_class_name('_3RWII')
			break
		except:
			pass
	return driver


def get_user(driver,number,msg,file_location=None):
	accept="image/*,video/mp4,video/3gpp,video/quicktime"
	accept_document="*"
	try:
		driver.get("https://web.whatsapp.com/send?phone={}".format(number))
	except Exception as error:
		print("[ PAGE NOT FOUND ]")
	while(True):
		try:
			msg_box = driver.find_element_by_class_name('_13mgZ')
			break
		except:
			pass
	if(file_location == None):
		pass
	else:
		extention = file_location.split('.')
		extention = extention[len(extention) - 1]
		attachments = driver.find_element_by_xpath('//div[@title = "Attach"]')
		attachments.click()
		if(extention == 'jpg' or extention == 'png' or extention == 'gif'):
			image_box = driver.find_element_by_xpath('//input[@accept = "{}"]'.format(accept))
			image_box.send_keys(file_location)
			while(True):
				try:
					send_button = driver.find_element_by_xpath('//span[@data-icon = "send-light"]')
					break
				except:
					pass
			send_button.click()
		elif(extention == '.txt' or extention == '.pdf' or extention == '.docx'):
			document = driver.find_element_by_xpath('//input[@accept = "{}"]'.format(accept_document))
			document.send_keys(file_location)
			while(True):
				try:
					send_button = driver.find_element_by_xpath('//span[@data-icon = "send-light"]')
					break
				except:
					pass
			send_button.click()
		else:
			print("WRONG INPUT FILE ! ")
	time.sleep(5)
	msg_box.send_keys(msg)
	time.sleep(5)
	button = driver.find_element_by_class_name('_3M-N-')
	button.click()


def main(excel_location,sheet_index,start,end,msg):
	dictionary,name_dictionary = open_file(excel_location,sheet_index,start,end,msg)

	return dictionary,name_dictionary

def get_driver():
	driver = get_scanner()
	return driver

def page2_main(driver,time_out,dictionary,name_dictionary,file_location):
	if(dictionary == None):
		print("[ EXCEL READ ERROR ]")
	else:
		for key,value in dictionary.items():
			get_user(driver,key,value,file_location)
			if(time_out < 10 and time_out != 0):
				time_out = 10
			elif(time_out >= 10):
				pass
			else:
				time_out = randint(7,13)
			time.sleep(int(time_out))
		print("[ ALL MESSAGES SENT SUCCESSFULLY ]")
