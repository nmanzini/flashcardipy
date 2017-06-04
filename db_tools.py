import sqlite3
import time


name = 'test01.db'

def create_database(name):
    '''
    generates an empty sqlite3 database that stores words and their meaning

    :param name: name of the final file
    :type name: string
    :return: generates an empty in the folder
    :rtype: name.db
    '''
    conn = sqlite3.connect(name)
    c = conn.cursor()

    variables = []
    variables.append("word TEXT")           # the actual word
    variables.append("definition TEXT")     # definition of the word
    variables.append("example TEXT")        # example of usage
    variables.append("history BLOB")        # binary list of 01 to mark historical progress right 1 or wrong0
    variables.append("time BLOB")           # binary list of unix time at the past mark
    variables.append("seen INT")            # times seen
    variables.append("right INT")           # times marked right
    variables.append("wrong INT")           # times marked wrong
    variables.append("streak INT")          # streak of rights (+1,+2,+3) wrong( -1,-2,-3)
    variables.append("reported INT")        # reported by the user (1 = reported)


    print(', '.join(variables))
    c.execute("CREATE TABLE IF NOT EXISTS words("+','.join(variables)+")")

    c.close
    conn.close()

def add_word(name,word,definition,example = ""):
    """
    takes a database name and add a row to a database with word, definition and example
    :param name: name of the database
    :type name: string
    :param word:
    :type word: string
    :param definition:
    :type definition: string
    :param example:
    :type example: string
    :return: nothing, edits the database
    :rtype: None
    """
    conn = sqlite3.connect(name)
    c = conn.cursor()

    columns = "(word , definition , example , history, time , seen, right , wrong , streak , reported )"
    marks = "(?,?,?,?,?,?,?,?,?,?)"
    variables = (word, definition, example, None, None, 0, 0, 0, 0, 0)

    c.execute("INSERT INTO words "+columns+" VALUES "+marks, variables)
    print(word+" added.")
    conn.commit()
    c.close()
    conn.close()

def add_words_manually(name):
    """

    :param name: file name of the database
    :type name: string
    :return:
    :rtype:
    """
    print('Starting manual input, now you can input words in the database , input X to exit)')
    print()

    conn = sqlite3.connect(name)
    c = conn.cursor()

    while True:
        word = input('input a new word (input X to close)')
        if word == "X":
            print('closing the manual input')

            c.close()
            conn.close()

            return
        definition = input('input ' + word + ' meaning here:')
        example = input('input an example using ' + word + ':')
        add_word(name,word, definition, example)
        conn.commit()
        print()


def add_words_txt(name, filename):
    text_file = open(filename, "r")
    for line in text_file.read().splitlines():
        elements = line.split('\t', maxsplit=1)
        add_word(name, elements[0], elements[1])
    text_file.close()


filename = "grelist.txt"

add_words_txt(name, filename)
