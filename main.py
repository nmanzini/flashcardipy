import sqlite3, random, os
import time

name = 'test01.db'
filename = "grelist.txt"
conn = sqlite3.connect(name)
c = conn.cursor()

'''word, definition, example, history, time, seen, right, wrong, streak, reported'''

class Word(object):
    def __init__(self, row_id):
        """
        Initialize a Word object with all that stuff
        :param row_id: integer value of the row
        :type row_id: integer
        """
        c.execute('SELECT * FROM words WHERE rowid = ' + str(row_id))
        word_data = c.fetchone()

        self.row_id = row_id
        self.word = word_data[0]
        self.definition = word_data[1]
        self.example = word_data[2]
        self.history = word_data[3]
        self.time_h = word_data[4]
        self.seen = word_data[5]
        self.right = word_data[6]
        self.wrong = word_data[7]
        self.streak = word_data[8]
        self.reported = word_data[9]

    def show(self):
        """
        shows the previously selected word and react to the input

        :return:
        :rtype:
        """

        # TODO: polish the console gui by adding an introduction at the beginning
        # TODO: polish the visualization of words, showing history  and last time seen.

        positive = ("yes", "y", "Y", "Yes", "YES", "1", " ")
        negative = ("no", "n", "N", "No", "NO", "0", "")
        exit_answers = ("exit", "e")
        report = ("report", "r")



        print()
        print("       " + self.word.upper())
        print()
        print()

        answer = input('do you remember this word?')
        print()

        if answer in positive:
            print("DEFINITION:")
            print(self.definition)
            print()
            print()
            print("good!")
            input('press enter when done')
            self.opened_edit()
            self.positive_edit()
            self.streak_edit(1)

        elif answer in negative:
            print("DEFINITION:")
            print(self.definition)
            print()
            print()
            print("you will remember next time")
            input('press enter when done')
            self.opened_edit()
            self.negative_edit()
            self.streak_edit(0)

        elif answer in exit_answers:
            print("Ok, see you soon!")
            return True

        elif answer in report:
            print("sorry the word was incorrect")
            self.report_edit()

        else:
            print("invalid input")

        self.update()
        os.system('cls')
        return

    def opened_edit(self):
        """
        react to the opening of the file, increments seen and add a time slot
        :return:
        :rtype:
        """
        if self.time_h:
            self.time_h += " , " + str(int(time.time()))
        else:
            self.time_h = str((int(time.time())))
        self.seen += 1

    # TODO: merge opened(self,input) with positive and negative, the input shal be 1 or 0 for right or wrong

    def positive_edit(self):
        """
        react to the positive answer updating histoy and the right counter
        :return:
        :rtype:
        """
        if self.history:
            self.history += 1
        else:
            self.history = 1
        self.right +=1

    def negative_edit(self):
        """
        React to a negative answer updating history and wrong
        :return:
        :rtype:
        """
        if self.history:
            self.history += 0
        else:
            self.history = 0
        self.wrong += 1

    def report_edit(self):
        self.reported = 1

    def streak_edit(self, value):
        """
        update the streak, positive means the user is on a positive streak for the word and vice versa
        :param value: integer (1 or 0)
        :type value: int
        """
        if value == 1:
            if self.streak >= 0:
                self.streak += 1
            else:
                self.streak = 1
        if value == 0:
            if self.streak >= 0:
                self.streak = -1
            else:
                self.streak += -1

    def update(self):
        variables = ['history', 'time', 'seen', 'right', 'wrong', 'streak', 'reported']

        marks = ["?"]*len(variables)

        values = [self.history, self.time_h, self.seen, self.right, self.wrong, self.streak, self.reported]

        output_list = [a+" = "+b for a, b in zip(variables, marks)]
        output_line = " , ".join(output_list)
        c.execute('UPDATE words SET '+ output_line+' WHERE rowid = '+str(self.row_id),values)
        conn.commit()


def chooser():
    case = random.random()
    if case < 0.1:
        c.execute('SELECT rowid FROM words WHERE reported = 0  ORDER BY RANDOM() LIMIT 1;')
    elif case < 0.2:
        c.execute('SELECT rowid FROM words WHERE reported = 0 and streak < 0 ORDER BY RANDOM() LIMIT 1;')
    else:
        c.execute('SELECT rowid FROM words WHERE reported = 0 and streak > 0 ORDER BY RANDOM() LIMIT 1;')
    row_id = c.fetchone()
    if not row_id:
        c.execute('SELECT rowid FROM words WHERE reported = 0 ORDER BY RANDOM() LIMIT 1;')
        row_id = c.fetchone()
    return row_id[0]


while True:
    test_word = Word(chooser())
    result = test_word.show()
    if result:
        break

c.close()
conn.close()
