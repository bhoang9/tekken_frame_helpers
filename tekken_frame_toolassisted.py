#To extract frame data from toolassisted website

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import requests
import itertools
import re
import os
import json


def main():

    charArr = [ "#32/AKUMA", "#19/ALISA", "#12/ASUKA", "#31/BOB",
            "#07/BRYAN","#22/CHLOE", "#20/CLAUDIO", "#13/DEVIL JIN",
            "#16/DRAGUNOV","#35/EDDY","#36/ELIZA","#14/FENG","#25/GIGAS"
            "#08/HEIHACHI", "#04/HWOARANG", "#11/JACK-7", "#06/JIN",
            "#24/JOSIE", "#21/KATARINA", "#26/KAZUMI", "#09/KAZUYA",
            "#02/KING", "#33/KUMA", "#18/LARS", "#01/LAW", "#30/LEE",
            "#17/LEO", "#15/LILI", "#37/MIGUEL", "#28/NINA", "#34/PANDA",
            "#00/PAUL", "#29/RAVEN", "#23/SHAHEEN", "#10/STEVE", "#05/XIAOYU",
            "#03/YOSHI"]

    for character in charArr:
        browser = webdriver.Firefox()
        browser.implicitly_wait(30)
        browser.get("https://toolassisted.github.io/T7/MOVELIST/" + character)
        page_content = BeautifulSoup(browser.page_source, 'html.parser')
 
        moveList = []
        movesData = []

        #all moves
        moves = page_content.find_all('tr')

        #individual moves + their properties
        for move in moves:
            nArr = []
            move_nums = move.find_all('td', class_="NUMTD")
            move_props = move.find_all('td',class_="MOVETD")

            for num_data,prop_data in zip(move_nums,move_props):
                nArr = []
                nDater = num_data.find_all('div')
                nDater2 = prop_data.find_all('div')
                nArr.append(nDater2[1].text.replace("][",",")
                .replace("[","").replace("]","")) #command
                nArr.append(nDater2[4].text.replace("][",",")
                .replace("[","").replace("]","")) #hit_height
                nArr.append(nDater[1].text.replace("[ START ", "")
                .replace("F]","")) #start_frame
                nArr.append(nDater[2].text.replace("[ BLK ", "")
                .replace("]","")) #block_frame
                nArr.append(nDater[3].text.replace("[ HIT ", "")
                .replace("]","")) #hit_frame
                nArr.append(nDater[4].text.replace("[","").replace("DMG", "")
                .replace("]","")) #damage
                moveList.append(nArr)


        for move in moveList:
            movesData.append(move_to_JSON(move))


        browser.quit()
        character_name_string = character.split("/")[1]
        char_frame_JSON = open((character_name_string + "_frame_data"), 'w')
        output = {"name": character_name_string, "moves": movesData}
        json.dump(output, char_frame_JSON)
        char_frame_JSON.close()


def move_to_JSON(move_data):
    move_dict = {
            "command": move_data[0],
            "hit_height": move_data[1],
            "start_frame":move_data[2],
            "block_frame":move_data[3],
            "hit_frame":move_data[4],
            "damage":move_data[5]
            }
    return move_dict


main()

