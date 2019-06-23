#Scraping TOOLASSISTED website for tekken frame data
#Use functions defined in "tekken_frame_sql_helpers"

from selenium import webdriver
from bs4 import BeautifulSoup
import tekken_frame_sql_helpers as sql_helpers
import requests
import itertools
import re
import os
import json
import sqlite3

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
        #create database for character moves
        char_name = character.split('/')
        char_db_name = (char_name[1] + '_frame_data.db')
        con = sqlite3.connect(char_db_name)
        cursor = con.cursor()

        #create the table for the movelist and character name
        cursor.execute(sql_helpers.create_moveList_table())
        cursor.execute(sql_helpers.create_name_table())

        sql_helpers.insert_name(cursor, char_name[1])
        con.commit()

        browser = webdriver.Firefox()
        browser.implicitly_wait(30)
        browser.get("https://toolassisted.github.io/T7/MOVELIST/" + character)
        page_content = BeautifulSoup(browser.page_source, 'html.parser')
 
        moveList = []
        movesData = []

        #get entire character's movelist
        moves = page_content.find_all('tr')

        #individual moves + their properties
        for index,move in enumerate(moves):
            nArr = []
            move_nums = move.find_all('td', class_="NUMTD")
            move_props = move.find_all('td',class_="MOVETD")

            for num_data,prop_data in zip(move_nums,move_props):
                nArr = []
                num_data_arr = num_data.find_all('div')
                prop_data_arr = prop_data.find_all('div')
                nArr = get_move_data(num_data_arr, prop_data_arr)
                nArr.append(index) #index of the move

                #append to table that contains all moves
                sql_helpers.insert_move(cursor, nArr)
                con.commit()


        con.close()
        browser.quit()

def get_move_data(num_data_array, prop_data_array):

    nArr = []

    #command
    nArr.append(prop_data_array[1].text.replace("][",",")
    .replace("[","").replace("]","")) 
    #hit_height
    nArr.append(prop_data_array[4].text.replace("][",",")
    .replace("[","").replace("]","")) 
    #start_frame
    nArr.append(num_data_array[1].text.replace("[ START ", "")
    .replace("F ]","")) 
    #block_frame
    nArr.append(num_data_array[2].text.replace("[ BLK ", "")
    .replace("]","")) 
    #hit_frame
    nArr.append(num_data_array[3].text.replace("[ HIT ", "")
    .replace("]","")) 
    #damage
    nArr.append(num_data_array[4].text.replace("[","").replace("DMG", "")
    .replace("]","")) 

    return nArr

main()

