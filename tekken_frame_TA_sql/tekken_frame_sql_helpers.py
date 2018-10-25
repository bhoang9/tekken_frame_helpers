import sqlite3

def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
        return None

#create table with movelist
def create_moveList_table():
	moveList_sql = """
	CREATE TABLE if not exists moves (
        id integer PRIMARY KEY,
	movelist_id integer,
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
	INSERT INTO moves (movelist_id, command, hit_height, start_frame, block_frame, hit_frame, damage)
	VALUES (?,?,?,?,?,?,?)"""

	cursor.execute(move_insert_sql, (move_array[6],move_array[0],move_array[1],move_array[2],
		move_array[3], move_array[4], move_array[5]))

#insert name into name table
def insert_name(cursor, name):
	name_insert_sql = """
	INSERT INTO name (name) VALUES (?) """

	cursor.execute(name_insert_sql, (name,))

#update move id
def update_move_id(cursor, old_id, incr_amt):
        new_id = old_id + incr_amt
        print(new_id)
        update_move_id_sql = """
        UPDATE moves SET movelist_id = ? WHERE id = ? """

        cursor.execute(update_move_id_sql, (new_id, old_id))
