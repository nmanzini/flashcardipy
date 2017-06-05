import sqlite3

def create_database(name):
    """
    generates an empty sqlite3 database that stores words and their meaning

    :param name: name of the final file
    :type name: string
    :return: generates an empty in the folder
    :rtype: name.db
    """
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
    add a row to a database with word, definition and example
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
    a small tool to manually input words in the database
    :param name: file name of the database
    :type name: string
    :return: add words one by one
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
    """

    :param name: name of the database file
    :type name: string ending in .db
    :param filename: txt file with a lsit of words and definition divided by a tab
    :type filename:
    :return: add the file to the database
    :rtype: none
    """
    text_file = open(filename, "r")
    for line in text_file.read().splitlines():
        elements = line.split('\t', maxsplit=1)
        add_word(name, elements[0], elements[1])
    text_file.close()



while True:
    print()
    print(" input 1 if you want to generate a new database")
    print(" input 2 if you want to add a word manually to a new file")
    print(" input 3 if you want to import a text file to an existing database")
    print(" input 4 if you want to create a new database and import a txt in it")
    print(" input 9 to close")

    decision = input("input a number: ")

    if decision == "1":
        name = input("decide a name for the database you want to create, do not ad .db: ") + ".db"
        create_database(name)
    elif decision == "2":
        name = input("decide a name for the database you want to work on, do not ad .db: ") + ".db: "
        add_words_manually(name)
    elif decision == "3":
        name = input("decide a name for the database you want to work on, do not ad .db: ") + ".db: "
        filename = input("decide a name for the text file you want to import, do not ad .txt: ")+".txt"
        add_words_txt(name, filename)
    elif decision == "4":
        name = input("decide a name for the database you want to work on, do not ad .db: ") + ".db"
        filename = input("decide a name for the text file you want to import, do not ad .txt: ") + ".txt"
        create_database(name)
        add_words_txt(name, filename)
    elif decision == "9":
        break
    else:
        print("input not valid")
    print()
print("closing")