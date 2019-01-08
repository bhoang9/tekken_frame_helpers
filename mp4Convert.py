#Runs through movelist mp4 files and converts them into gifs through an automated browser
#using selenium

import os
import urllib.request
import logging
import sys
from datetime import datetime
from selenium.webdriver.remote.remote_connection import LOGGER
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

LOGGER.setLevel(logging.WARNING)
print(datetime.now())

ogDir = os.getcwd()
srcDir = ogDir + "/" + sys.argv[1] + "_gif_raw" #source of raw mp4 files
#targetDir = ogDir + "/" + character + "_gif_complete" #destination of completed gifs
targetDir = "/home/bhoang8/Pictures/" + sys.argv[1] + "_complete"
ogList = os.listdir(srcDir)
fileList = ogList[:]
fileList.sort()

if os.path.isdir(targetDir) is False:
	os.mkdir(targetDir)

ffprofile = webdriver.FirefoxProfile('/home/bhoang8/Videos/ff_profile_ex')
browser = webdriver.Firefox(ffprofile)
browser.implicitly_wait(30)
browser.get("https://ezgif.com/video-to-gif")

for index,vidFile in enumerate(fileList):
	if(vidFile == "geckodriver.log" or (vidFile.endswith('.mp4') is False)):
		print("invalid file, moving on...")
		continue

	os.chdir(srcDir)

	#specify which video to turn into gif
	browser.find_element_by_id("new-image").send_keys(os.getcwd()+"/" + vidFile)
	browser.find_element_by_name("upload").click()

	#resize video to be 320XAUTO
	wait = WebDriverWait(browser, 15)
	select_fr = Select(browser.find_element_by_id("size"))
	select_fr.select_by_index(7)

	browser.find_element_by_name("video-to-gif").click()
	browser.find_element_by_class_name("m-btn-optimize").click()

	#set lossy compression to 200
	browser.find_element_by_id("lossy").send_keys("200")
	browser.find_element_by_name("optimize").click()

	#get resulting gif
	optimized_gif = browser.find_element_by_xpath("//img[@alt='[optimize output image]']")
	src = optimized_gif.get_attribute("src")
	nFileName = vidFile.split(".")[0]

	os.chdir(targetDir)
	urllib.request.urlretrieve(src, nFileName+".gif")
	print(nFileName + " gif created")

	browser.find_element_by_class_name("video").click()


print("complete")
print(datetime.now())
browser.quit()
