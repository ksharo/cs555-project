'''
    Authors: Kaitlyn Sharo, Logan Rechler, Mathieu Nagle
    Pledge: I pledge my honor that I have abided by the Stevens Honor System.
    Description: CS 555 Project 03: Teamwork Begins
'''

from datetime import date
# pip install -U prettytable
from prettytable import PrettyTable

VALID_TAGS = ["INDI", "NAME", "SEX", "BIRT", "DEAT", "FAMC", "FAMS", "FAM", "MARR", "HUSB", "WIFE", "CHIL", "DIV", "DATE", "HEAD", "TRLR", "NOTE"]

MONTHS = {
    "JAN": '01',
    "FEB": '02',
    "MAR": '03',
    "APR": '04',
    "MAY": '05',
    "JUN": '06',
    "JUL": '07',
    "AUG": '08',
    "SEP": '09',
    "OCT": '10',
    "NOV": '11',
    "DEC": '12'
    }

INDIVIDUALS = {} # dictionary of an individual's id matching with their data

def parseFile(file):
    '''Parses a GEDCOM file based on the specifications given in the
        homework description'''
    INDIVIDUALS = {}
    name = ''
    sex = ''
    birth = ''
    death = ''
    idNum = ''
    famc = ''
    fams = ''
    fam = ''
    marr = ''
    husb = ''
    wife = ''
    chil = ''
    div = ''
    nextBirth = False
    nextDeath = False
    nextMarr = False
    nextDiv = False
    for line in file:
         # separate the line into a list of all words with spaces in between
        sections = line.split(" ")
        # strip each element in the list to remove newline characters
        for x in range(len(sections)):
            sections[x] = sections[x].strip()
        # get the tag of the output
        tag = ""
        args = ""
        if "INDI" in sections or "FAM" in sections:
            # get the tag and arguments
            args = sections[1]
            tag = sections[2]
        else:
            tag = sections[1]
            for x in sections[2:]:
                args += x + " "
        
        # start new dictionary entry for each new indi num and reset
        if tag == "INDI":
            if idNum != '':
                INDIVIDUALS[idNum] = Record(idNum, name, sex, birth, death, famc, fams, fam, marr, husb, wife, chil, div)
            idNum = args.replace('@', '')
            name = ''
            sex = ''
            birth = ''
            death = ''

        # set record fields for each tag
        if tag == "NAME":
            name = args

        if tag == "SEX":
            sex = args

        if tag == "BIRT":
            nextBirth = True

        if tag == "DEAT":
            nextDeath = True

        if tag == "MARR":
            nextMarr = True

        if tag == "DIV":
            nextDiv = True

        if tag == "DATE" and nextBirth:
            birth = returnDate(args)
            nextBirth = False

        if tag == "DATE" and nextDeath:
            death = returnDate(args)
            nextDeath = False

        if tag == "DATE" and nextMarr:
            marr = returnDate(args)
            nextMarr = False

        if tag == "DATE" and nextDiv:
            div = returnDate(args)
            nextDiv = False

    # make sure the last record in the file is included
    if idNum != '':
        INDIVIDUALS[idNum] = Record(idNum, name, sex, birth, death, famc, fams, fam, marr, husb, wife, chil, div)
    # print all records in table format
    printIndOutput(INDIVIDUALS)


def printIndOutput(records):
    indTable = PrettyTable()
    indHeader = ['ID', 'Name', 'Gender', 'Birthday', 'Age', 'Alive', 'Death', 'Child', 'Spouse']
    indTable.field_names = indHeader
    for x in sorted (records.keys()):
        record = records[x]
        alive = True
        death = 'NA'
        today = date.today()
        age = today.year - record.birth.year - ((today.month, today.day) < (record.birth.month, record.birth.day))
        if record.death != '':
            alive = False
            death = record.death
            age = record.death.year - record.birth.year - ((record.death.month, record.death.day) < (record.birth.month, record.birth.day))
        rowToAdd = [record.idNum, record.name, record.sex, record.birth, age, alive, death, '-', '-']
        indTable.add_row(rowToAdd)
    print(indTable)
    

def returnDate(args):
    ''' creates a python date object out of the date information
        found in the ged file for easier comparison'''
    dateInfo = args.split(" ")
    year = dateInfo[2]
    day = dateInfo[0]
    if len(day) == 1:
        day = '0' + day
    month = MONTHS[dateInfo[1]]
    fullDate = year + '-' + month + '-' + day
    return date.fromisoformat(fullDate)

class Record:
    ''' A record contains the id number of the individual with name 'name', their
        sex, birth date, death date, famc, fams, fam, marriage date, husband,
        wife, children, and divorce date, for whatever is applicable'''
    def __init__(self, idNum, name, sex, birth, death, famc, fams, fam, marr, husb, wife, chil, div):
        self.idNum = idNum
        self.name = name
        self.sex = sex
        self.birth = birth
        self.death = death
        self.famc = famc
        self.fams = fams
        self.fam = fam
        self.marr = marr
        self.husb = husb
        self.wife = wife
        self.chil = chil
        self.div = div
    

if __name__ == "__main__":
    fileName = input("What is the name of your file? (Make sure it is in your current directory)\n")
    file = open(fileName, "r")
    parseFile(file)
