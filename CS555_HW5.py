'''
    Authors: Kaitlyn Sharo, Logan Rechler, Mathieu Nagle
    Pledge: I pledge my honor that I have abided by the Stevens Honor System.
    Description: CS 555 Homework 03: Pair Programming
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

INDIVIDUALS = {}  # dictionary of an individual's id matching with their data
FAMILIES = {}  # dictionary of a family id matching with their data

def parseFile(file, test=False):
    '''Parses a GEDCOM file based on the specifications given in the
        homework description. if test==True, don't print'''
    errors = ""
    # reset the dictionaries
    INDIVIDUALS.clear()
    FAMILIES.clear()
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
            errors += checkUS22(idNum, 0)
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
            errors += checkUS22(fam, 1)
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
    if not test:
        print("Individuals")
        printIndOutput()
        print("Families")
        printFamOutput()
        print("\nErrors:")
        errors += "\n" + checkUS02() + "\n"
        errors += checkUS03() + "\n"
        errors += checkUS06() + "\n"
        errors += checkUS13() + "\n"
        print(errors)


def printIndOutput():
    records = INDIVIDUALS
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

def printFamOutput():
    families = FAMILIES
    inds = INDIVIDUALS
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

#### USER STORIES ####

def checkUS02():
    '''Checks the dictionary of records (initialized in parsefile) to find errors
        where the individual has been recorded as having been married before being born'''
    toReturn = ''
    for x in FAMILIES:
        mar = FAMILIES[x].marr
        wifeBirth = INDIVIDUALS[FAMILIES[x].wife].birth
        husbBirth= INDIVIDUALS[FAMILIES[x].husb].birth
        if mar < wifeBirth:
            pronoun = 'his' if INDIVIDUALS[FAMILIES[x].wife].sex.strip() == 'M' else 'her' if INDIVIDUALS[FAMILIES[x].wife].sex.strip() == 'F' else 'their'
            toReturn += "Error US02: Birth date of " + INDIVIDUALS[FAMILIES[x].wife].name.replace('/', '') + "(" + INDIVIDUALS[FAMILIES[x].wife].idNum +") occurs after " + pronoun + " marriage date.\n"
        if mar < husbBirth:
            pronoun = 'his' if INDIVIDUALS[FAMILIES[x].husb].sex.strip() == 'M' else 'her' if INDIVIDUALS[FAMILIES[x].husb].sex.strip() == 'F' else 'their'
            toReturn += "Error US02: Birth date of " + INDIVIDUALS[FAMILIES[x].husb].name.replace('/', '') + "(" + INDIVIDUALS[FAMILIES[x].wife].idNum +") occurs after " + pronoun + " marriage date.\n"
    return toReturn

def checkUS03():
    '''Checks the dictionary of records (initialized in parsefile) to find errors
        where the individual has been recorded as having died before being born'''
    toReturn = ''
    for x in INDIVIDUALS:
        record = INDIVIDUALS[x]
        # if information is missing or the individual has not died, continue, no error.
        if record.death == '' or record.birth == '':
            continue
        if record.death < record.birth:
            # choose proper pronoun
            pronoun = 'his' if record.sex.strip() == 'M' else 'her' if record.sex.strip() == 'F' else 'their'
            toReturn += "Error US03: Birth date of " + record.name.replace('/', '') + "(" + record.idNum + ") occurs after " + pronoun + " death date.\n"
    return toReturn

def checkUS06():
    error = ""
    for key in FAMILIES.keys():
        if FAMILIES[key].div == "":
            continue
        else:
            divDate = FAMILIES[key].div
            wifeID = FAMILIES[key].wife
            husbandID = FAMILIES[key].husb
            if INDIVIDUALS[husbandID].death == "":
                continue
            if INDIVIDUALS[wifeID].death == "":
                continue
            wifeDeath = INDIVIDUALS[wifeID].death
            print("Wife: "+str(wifeDeath))
            husbandDeath = INDIVIDUALS[husbandID].death
            print("Husband: "+str(husbandDeath)+" "+str(INDIVIDUALS[husbandID].name))
            print("DIV:"+str(divDate))
            if (divDate-wifeDeath).days >= 0 and (divDate-husbandDeath).days >= 0:
                error += "Error US06: Divorce date of "+INDIVIDUALS[husbandID].name.replace('/', '')+"("+husbandID.replace('@', '')+") and "+INDIVIDUALS[wifeID].name.replace('/', '')+"("+wifeID.replace("@", '')+") is after their deaths.\n"
    return error



def checkUS13():
    '''Checks the dates each sibling was born to make sure they are logical.
        Labeled as an anomaly because of adoptions or step-siblings.'''
    dates = []
    errors = ''
    # go through each family record
    for fam in FAMILIES:
        f = FAMILIES[fam]
        children = f.chil
        # if there are not two children to compare, skip the rest
        if len(children) < 2:
            continue
        # get the birth dates for each child
        for c in children:
            dates.append(INDIVIDUALS[c].birth)
        # compare each birth date with every other birth date
        for i in range(len(dates)-1):
            for j in range(i+1, len(dates)):
                days = abs((dates[j] - dates[i])).days
                # check if the birth dates are in the valid range
                if days < 2 or days > 240:
                    continue
                else:
                    errors += 'Anomaly US13: Birth dates of ' + INDIVIDUALS[children[j]].name.replace('/', '') + '(' + INDIVIDUALS[children[j]].idNum + ') and ' + INDIVIDUALS[children[i]].name.replace('/', '') + '(' + INDIVIDUALS[children[i]].idNum + ') are ' + str(days) + ' days apart.\n'
    return errors

def checkUS22(args, tag):
    '''Check to ensure that no family or individual id is used more than once.'''
    errors = ""
    if tag:
        if args in FAMILIES.keys():
            errors += "Error US22: Family ID " + args + " already used.\n"
    else:
        if args in INDIVIDUALS.keys():
            errors += "Error US22: Individual ID " + args + " already used.\n"
    return errors

### CLASSES ###

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