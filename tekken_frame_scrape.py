#Reads from rbnorway and outputs JSON files for all characters and creates new folders for them as well

from bs4 import BeautifulSoup
import requests
import json
import os


def main():

    characters = ["akuma","alisa", "asuka", "bob", "bryan", "claudio", "devil-jin",
                "dragunov", "eddy","eliza","feng","gigas","heihachi",
                "hwoarang","jack7","jin","josie","katarina","kazuya",
                "king","kuma","lars","lei","law","lee","leo","lili",
                "lucky-chloe","master-raven","miguel","nina","noctis",
                "paul","shaheen","steve","xiaoyu","yoshimitsu"]

    for character in characters:

        url = "http://rbnorway.org/" + character  + "-t7-frames/"
        page_response = requests.get(url, timeout=5)

        page_content = BeautifulSoup(page_response.content, "html.parser")

        #move list in text form and in dictionary form
        moveList = []
        moveListJSON = []

        #get all moves from html
        moves = page_content.find_all('tr')

        #get <td> within <tr> element
        for move in moves:
            move_props = extract_td_element(move)
            moveList.append(move_props)

        #take string array and move to dictionary for JSON 
        for move in moveList:
            move_dict = get_move_properties(move)
            moveListJSON.append(move_dict)

        try:
            os.mkdir(character + "_frame")
        except FileExistsError:
            print("already exists")

        file = open((character + "_frame_data"), "w")
        output = {"moves": moveListJSON}
        json.dump(output, file)
        file.close()

def extract_td_element(move):
    single_move_properties = []
    move_properties = move.find_all('td')

    for data in move_properties:
        single_move_properties.append(data.text)

    return single_move_properties

def get_move_properties(move):
        move_dict = {
            "command": move[0],
            "hit_height": move[1],
            "damage": move[2],
            "start_frame": move[3],
            "block_frame": move[4],
            "hit_frame": move[5],
            "CH_frame": move[6],
            "notes": move[7]
            }   
        return move_dict

main()
