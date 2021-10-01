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
FAMILIES = {} # dictionary of a family id matching with their data

def parseFile(file):
    '''Parses a GEDCOM file based on the specifications given in the
        homework description'''
    # reset the dictionaries
    INDIVIDUALS = {}
    FAMILIES = {}
    # individuals fields
    name = ''
    sex = ''
    birth = ''
    death = ''
    idNum = ''
    famc = []
    fams = []
    # family fields
    fam = ''
    marr = ''
    husb = ''
    wife = ''
    chil = []
    div = ''
    # keep track of what the date in the next line is for
    nextBirth = False
    nextDeath = False
    nextMarr = False
    nextDiv = False

    # iterate through every line in the file
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
        
        # start new dictionary entry for each new individual id and reset the relevant fields
        if tag == "INDI":
            if idNum != '':
                INDIVIDUALS[idNum] = Record(idNum, name, sex, birth, death, famc, fams)
            idNum = args.replace('@', '')
            name = ''
            sex = ''
            birth = ''
            death = ''
            famc = []
            fams = []

        # start new dictionary entry for each new family id and reset the relevant fields
        if tag == "FAM":
            if fam != '':
                FAMILIES[fam] = Family(fam, marr, husb, wife, chil, div)
            fam = args.replace('@', '')
            marr = ''
            husb = ''
            wife = ''
            chil = []
            div = ''
            

        # set record fields for each tag
        if tag == "NAME":
            name = args

        if tag == "SEX":
            sex = args

        if tag == "FAMC":
            famc.append(args.replace('@', '').replace(' ', ''))

        if tag == "FAMS":
            fams.append(args.replace('@', '').replace(' ', ''))

        if tag == "WIFE":
            wife = args.replace('@', '').replace(' ', '')

        if tag == "HUSB":
            husb = args.replace('@', '').replace(' ', '')

        if tag == "CHIL":
            chil.append(args.replace('@', '').replace(' ', ''))
            
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

    # make sure the last individual record in the file is included
    if idNum != '':
        INDIVIDUALS[idNum] = Record(idNum, name, sex, birth, death, famc, fams)

    # make sure the last family record in the file is included
    if fam != '':
        FAMILIES[fam] = Family(fam, marr, husb, wife, chil, div)

    # print all records in table format
    print("Individuals")
    printIndOutput(INDIVIDUALS)
    print("Families")
    printFamOutput(FAMILIES, INDIVIDUALS)


def printIndOutput(records):
    indTable = PrettyTable()
    indHeader = ['ID', 'Name', 'Gender', 'Birthday', 'Age', 'Alive', 'Death', 'Child', 'Spouse']
    indTable.field_names = indHeader
    for x in sorted (records.keys()):
        # get the individual record
        record = records[x]
        # calculate age and set death date or NA
        alive = True
        death = 'NA'
        today = date.today()
        age = today.year - record.birth.year - ((today.month, today.day) < (record.birth.month, record.birth.day))
        if record.death != '':
            alive = False
            death = record.death
            age = record.death.year - record.birth.year - ((record.death.month, record.death.day) < (record.birth.month, record.birth.day))
        # set child to family id or NA if not applicable
        children = record.famc
        if len(children) == 0:
            child = 'NA'
        else:
            # format child record properly
            child = '{'
            for c in children:
                child += "'" + c + "', "
            # remove extra space and comma before ending bracket
            child = child[:len(child)-2] + '}'
        # set spouse to family id or NA if not applicable
        spouses = record.fams
        if len(spouses) == 0:
            spouse = 'NA'
        else:
            # format child record properly
            spouse = '{'
            for s in spouses:
                spouse += "'" + s + "', "
            # remove extra space and comma before ending bracket
            spouse = spouse[:len(spouse)-2] + '}'
        # add the row to the table
        rowToAdd = [record.idNum, record.name, record.sex, record.birth, age, alive, death, child, spouse]
        indTable.add_row(rowToAdd)
    print(indTable)

def printFamOutput(families, inds):
    famTable = PrettyTable()
    famHeader = ['ID', 'Married', 'Divorced', 'Husband ID', 'Husband Name', 'Wife ID', 'Wife Name', 'Children']
    famTable.field_names = famHeader
    for x in sorted (families.keys()):
        # get the individual record
        record = families[x]

        # check if there has been a divorce
        div = record.div
        if div == '':
            div = 'NA'

        # get the children belonging to that family
        children = 'NA'
        if len(record.chil) > 0:
            children = '{'
            for c in record.chil:
                children += "'" + c + "', "
            # remove extra space and comma before ending bracket
            children = children[:len(children)-2] + '}'
        
        # add the row to the table
        rowToAdd = [record.fam, record.marr, div, record.husb, inds[record.husb].name, record.wife, inds[record.wife].name, children]
        famTable.add_row(rowToAdd)
    print(famTable)

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
        sex, birth date, death date, famc, and fams, for whatever is applicable'''
    def __init__(self, idNum, name, sex, birth, death, famc, fams):
        self.idNum = idNum
        self.name = name
        self.sex = sex
        self.birth = birth
        self.death = death
        self.famc = famc
        self.fams = fams

class Family:
    ''' A family contains all relevant information about the family, including the family ID,
        marriage date, husband, wife, children, and divorce date, for whatever is applicable '''
    def __init__(self, fam, marr, husb, wife, chil, div):
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
