import sqlite3

#create table with movelist
def create_moveList_table():
	moveList_sql = """
	CREATE TABLE if not exists moves (
	id integer,
	command text,
	hit_height text,
	start_frame text,
	block_frame text,
	hit_frame text,
	damage text) """

	return moveList_sql

#table containing character name
def create_name_table():
	name_sql = """
	CREATE TABLE if not exists name (
	name text) """

	return name_sql

#insert move into moveList table
def insert_move(cursor, move_array):
	move_insert_sql = """
	INSERT INTO moves (id, command, hit_height, start_frame, block_frame, hit_frame, damage)
	VALUES (?,?,?,?,?,?,?)"""

	cursor.execute(move_insert_sql, (move_array[6],move_array[0],move_array[1],move_array[2],
		move_array[3], move_array[4], move_array[5]))

#insert name into name table
def insert_name(cursor, name):
	name_insert_sql = """
	INSERT INTO name (name) VALUES (?) """

	cursor.execute(name_insert_sql, (name,))