'''
    Authors: Kaitlyn Sharo, Logan Rechler, Mathieu Nagle, Leela Mallela
    Pledge: I pledge my honor that I have abided by the Stevens Honor System.
    Description: CS 555 Homework 03: Pair Programming
'''

from datetime import date
import datetime
from os import error
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
    errors22 = ''
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
            idNum = stripClean(args)
            errors22 += checkUS22(idNum, 0)
            name = ''
            sex = ''
            birth = ''
            death = ''
            famc = ''
            fams = ''

        # start new dictionary entry for each new family id and reset the relevant fields
        if tag == "FAM":
            if fam != '':
                FAMILIES[fam] = Family(fam, marr, husb, wife, chil, div)
            fam = stripClean(args)
            errors22 += checkUS22(fam, 1)
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
            famc = stripClean(args)

        if tag == "FAMS":
            fams = stripClean(args)

        if tag == "WIFE":
            wife = stripClean(args)

        if tag == "HUSB":
            husb = stripClean(args)

        if tag == "CHIL":
            chil.append(stripClean(args))

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
        errors7 = printIndOutput()
        print("\nFamilies")
        printFamOutput()
        print("\nErrors:")
        errors += "\n" + checkUS02() + "\n"
        errors += checkUS03() + "\n"
        errors += checkUS04() + "\n"
        errors += checkUS05() + "\n"
        errors += checkUS06() + "\n"
        errors += errors7 + "\n"
        errors += checkUS08() + "\n"
        errors += checkUS09() + "\n"
        errors += checkUS10() + "\n"
        errors += checkUS11() + "\n"
        errors += checkUS12() + "\n"
        errors += checkUS13() + "\n"
        errors += checkUS14() + "\n"
        errors += checkUS15() + "\n"
        errors += checkUS16() + "\n"
        errors += checkUS17() + "\n"
        errors += checkUS18() + "\n"
        errors += checkUS19() + "\n"
        errors += checkUS20() + "\n"
        errors += checkUS21() + "\n"
        errors += errors22 + "\n"
        errors += checkUS23() + "\n"
        errors += checkUS24() + "\n"
        errors += checkUS25() + "\n"
        errors += checkUS26() + "\n"
        errors += "DECEASED:\n"
        errors += checkUS29() + "\n"
        errors += "LIVING MARRIED:\n"
        errors += checkUS30() + "\n"
        errors += "LIVING SINGLE:\n"
        errors += checkUS31() + "\n"
        errors += "MULTIPLE BIRTHS:\n"
        errors += checkUS32() + "\n"
        errors += "ORPHANS:\n"
        errors += checkUS33() + "\n"
        errors += "LARGE AGE DIFFERENCES:\n"
        errors += checkUS34() + "\n"
        errors += "RECENT BIRTHS:\n"
        errors += checkUS35() + "\n"
        print(errors.replace('\n\n\n', '\n\n'))

def stripClean(x, spaces=True):
    ''' Cleans x by stripping @, / and spaces (optional) '''
    if spaces:
        return x.replace('@', '').replace('/', '').replace(' ', '')
    else:
        return x.replace('@', '').replace('/', '')

def printIndOutput():
    ''' Prints the table with the individuals' information '''
    errors = ""
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
        age = checkUS27(record.birth.year, record.birth.month, record.birth.day, True, 0, 0, 0)
        if record.death != '':
            alive = False
            death = record.death
            age = checkUS27(record.birth.year, record.birth.month, record.birth.day, False, record.death.year, record.death.month, record.death.day)
        errors += checkUS07(age, record.idNum)
        # set child to family id or NA if not applicable
        children = record.famc
        # set spouse to family id or NA if not applicable
        spouses = record.fams
        # add the row to the table
        rowToAdd = [record.idNum, record.name, record.sex, record.birth, age, alive, death, children, spouses]
        indTable.add_row(rowToAdd)
    print(indTable)
    return errors

def formatGroup(group):
    ''' Formats a group of individuals (children or spouses) as
        requested in the assignment: {'child1', 'child2', 'child3'}. '''
    if len(group) == 0:
        toReturn = 'NA'
    else:
        # format spouse record properly
        toReturn = '{'
        for i in group:
            toReturn += "'" + i + "', "
        # remove extra space and comma before ending bracket
        toReturn = toReturn[:len(toReturn)-2] + '}'
    return toReturn

def printFamOutput():
    ''' Prints the table with the families' information '''
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

        children = US28(record.chil)
        # add the row to the table
        rowToAdd = [record.fam, record.marr, div, record.husb, inds[record.husb].name, record.wife, inds[record.wife].name, children]
        famTable.add_row(rowToAdd)
    print(famTable)

def US28(records):
    '''Return the children's ids in order of when they were born'''
    # get the children belonging to that family
    children = 'NA'
    chilAges = {}
    for c in records:
        # ignore that they might be dead and list in order of who was born first
        # calculate age by day
        chilAges[c] = (date.today() - INDIVIDUALS[c].birth).days
    chilList = list(chilAges.keys())
    oldest = sorted(chilList, key = lambda k: chilAges[k], reverse = True)

    # print children in order of who was born first #### US 28
    if len(oldest) > 0:
        children = '{'
        for c in oldest:
            children += "'" + c + "', "
        # remove extra space and comma before ending bracket
        children = children[:len(children)-2] + '}'
    return children

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

def getPronoun(sex):
    ''' Returns the appropriate pronoun based on the individuals' recorded gender. '''
    return 'his' if sex.strip() == 'M' else 'her' if sex.strip() == 'F' else 'their'

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
            pronoun = getPronoun(INDIVIDUALS[FAMILIES[x].wife].sex)
            toReturn += "Error US02: Birth date of " + stripClean(INDIVIDUALS[FAMILIES[x].wife].name, False) + "(" + INDIVIDUALS[FAMILIES[x].wife].idNum +") occurs after " + pronoun + " marriage date.\n"
        if mar < husbBirth:
            pronoun = getPronoun(INDIVIDUALS[FAMILIES[x].husb].sex)
            toReturn += "Error US02: Birth date of " + stripClean(INDIVIDUALS[FAMILIES[x].husb].name, False) + "(" + INDIVIDUALS[FAMILIES[x].husb].idNum +") occurs after " + pronoun + " marriage date.\n"
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
            pronoun = getPronoun(record.sex)
            toReturn += "Error US03: Birth date of " + stripClean(record.name, False) + "(" + record.idNum + ") occurs after " + pronoun + " death date.\n"
    return toReturn

def checkUS04():
    error = ""
    for key in FAMILIES.keys():
        if FAMILIES[key].div == '':
            continue
        else:
            divDate = FAMILIES[key].div
            marrDate = FAMILIES[key].marr
            if (divDate-marrDate).days < 0:
                error += "Error US04: Divorce date of " + stripClean(INDIVIDUALS[FAMILIES[key].husb].name, False) + "(" + stripClean(FAMILIES[key].husb) + ") and " + stripClean(INDIVIDUALS[FAMILIES[key].wife].name, False) + "(" + stripClean(FAMILIES[key].wife) + ") is before their marriage.\n"
    return error

def checkUS05():
    error = ""
    for key in FAMILIES.keys():
        wifeID = FAMILIES[key].wife
        husbandID = FAMILIES[key].husb
        marrDate = FAMILIES[key].marr
        if INDIVIDUALS[husbandID].death != "":
            husbandDeath = INDIVIDUALS[husbandID].death
            if (marrDate-husbandDeath).days >= 0:
                error += "Error US05: Marriage date of " + stripClean(INDIVIDUALS[husbandID].name, False) + "(" + stripClean(husbandID) + ") and " + stripClean(INDIVIDUALS[wifeID].name, False) + "(" + stripClean(wifeID) + ") is after one of their deaths.\n"
                return error
        if INDIVIDUALS[wifeID].death != "":
            wifeDeath = INDIVIDUALS[wifeID].death
            if (marrDate-wifeDeath).days >= 0:
                error += "Error US05: Marriage date of " + stripClean(INDIVIDUALS[husbandID].name, False) + "(" + stripClean(husbandID)+") and " + stripClean(INDIVIDUALS[wifeID].name, False) + "(" + stripClean(wifeID) + ") is after one of their deaths.\n"
                return error
    return error

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
            husbandDeath = INDIVIDUALS[husbandID].death
            if (divDate-wifeDeath).days >= 0 and (divDate-husbandDeath).days >= 0:
                error += "Error US06: Divorce date of " + stripClean(INDIVIDUALS[husbandID].name, False) + "(" + stripClean(husbandID) + ") and " + stripClean(INDIVIDUALS[wifeID].name, False) + "(" + stripClean(wifeID) + ") is after their deaths.\n"
    return error

def checkUS07(age, id):
    error = ""
    if age > 150:
        error += "Error US07: Age of " + stripClean(INDIVIDUALS[id].name, False) + "(" + stripClean(id) + ") > 150.\n"
    return error

def checkUS08():
    error = ""
    for x in FAMILIES:
        i = FAMILIES[x]
        if(i.chil != []):
            for j in i.chil:
                divDate = i.div
                marDate = i.marr
                chilBirth = INDIVIDUALS[j].birth
                pronoun = getPronoun(INDIVIDUALS[j].sex)
                if (divDate != ''):
                    if(chilBirth-divDate).days >= 30*9:
                        error += "Error US08: " + stripClean(INDIVIDUALS[j].name, False) + "(" + stripClean(j) + ") was born more than 9 months after " + pronoun + " parents got divorced.\n"
                if (marDate != ''):
                    if(marDate-chilBirth).days >= 0:
                        error += "Error US08: " + stripClean(INDIVIDUALS[j].name, False) + "(" + stripClean(j) + ") was born before " + pronoun + " parents got married.\n"
                else:
                    error += "Error US08: " + stripClean(INDIVIDUALS[j].name, False) + "(" + stripClean(j) + ") was born before " + pronoun + " parents got married.\n"
    return error

def checkUS09():
    error = ""
    for x in FAMILIES:
        i = FAMILIES[x]
        if(i.chil != []):
            for j in i.chil:
                chilBirth = INDIVIDUALS[j].birth
                mothDeath = INDIVIDUALS[i.wife].death
                fathDeath = INDIVIDUALS[i.husb].death
                pronoun = getPronoun(INDIVIDUALS[j].sex)
                if(mothDeath != ""):
                    if(chilBirth-mothDeath).days >= 1:
                        s = "Error US09: " + stripClean(INDIVIDUALS[j].name, False) + "(" + stripClean(j) + ") was born after the death of " + pronoun + " mother.\n"
                        if s not in error:
                            error += s
                if(fathDeath != ""):
                    if(chilBirth-fathDeath).days >= 30*9:
                        s = "Error US09: " + stripClean(INDIVIDUALS[j].name, False) + "(" + stripClean(j) + ") was born more than 9 months after the death of " + pronoun + " father.\n"
                        if s not in error:
                            error += s
    return error

def checkUS10():
    '''Checks to ensure that both individuals involved in a marriage
       are at least 14 years old.'''
    errors = ""
    for x in FAMILIES:
        f = FAMILIES[x]
        if f.marr == "":
            continue
        else:
            wifeDiff = f.marr - INDIVIDUALS[f.wife].birth
            if wifeDiff.days < 5114 and wifeDiff.days >= 0:
                errors += "Error US10: " + stripClean(INDIVIDUALS[f.wife].name, False) + "(" + stripClean(f.wife) + ") was younger than 14 when she got married.\n"
            husbDiff = f.marr - INDIVIDUALS[f.husb].birth
            if husbDiff.days < 5114 and husbDiff.days >= 0:
                errors += "Error US10: " + stripClean(INDIVIDUALS[f.husb].name, False) + "(" + stripClean(f.husb) + ") was younger than 14 when he got married.\n"
    return errors

def checkUS13():
    '''Checks the dates each sibling was born to make sure they are logical.
        Labeled as an anomaly because of adoptions or step-siblings.'''
    dates = []
    errors = ''
    # go through each family record
    for fam in FAMILIES:
        dates = []
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
                    errors += 'Anomaly US13: Birth dates of ' + stripClean(INDIVIDUALS[children[j]].name, False) + '(' + INDIVIDUALS[children[j]].idNum + ') and ' + stripClean(INDIVIDUALS[children[i]].name, False) + '(' + INDIVIDUALS[children[i]].idNum + ') are ' + str(days) + ' days apart.\n'
    return errors

def checkUS11():
    '''Checks if someone is married to multiple people at the same time.'''
    errors = ""
    for fam in FAMILIES:
        f = FAMILIES[fam]
        wives = f.wife
        hubs = f.husb
        if len(wives) > 1:
            errors += 'Anomaly US11: Family ' + stripClean(f.fam) + ' has multiple wives.\n'
        if len(hubs) > 1:
            errors += 'Anomaly US11: Family ' + stripClean(f.fam) + ' has multiple husbands.\n'

    return errors

def checkUS12():
    """ Checks to make sure that a children's parents are not too old. """
    errors = ""
    for fam in FAMILIES:
        hBirth = INDIVIDUALS[FAMILIES[fam].husb].birth
        wBirth = INDIVIDUALS[FAMILIES[fam].wife].birth
        for c in FAMILIES[fam].chil:
            wAgeDif = INDIVIDUALS[c].birth.year - wBirth.year - ((INDIVIDUALS[c].birth.month, INDIVIDUALS[c].birth.day) < (wBirth.month, wBirth.day))
            if wAgeDif >= 60:
                errors += "Error US12: Mother " + stripClean(INDIVIDUALS[FAMILIES[fam].wife].name, False) + "(" + INDIVIDUALS[FAMILIES[fam].wife].idNum + ") is " + str(wAgeDif) + " years older than " + getPronoun(INDIVIDUALS[FAMILIES[fam].wife].sex) + " child, " + stripClean(INDIVIDUALS[c].name, False) + "(" + INDIVIDUALS[c].idNum + ").\n"
            hAgeDif = INDIVIDUALS[c].birth.year - hBirth.year - ((INDIVIDUALS[c].birth.month, INDIVIDUALS[c].birth.day) < (hBirth.month, hBirth.day))
            if hAgeDif >= 80:
                errors += "Error US12: Father " + stripClean(INDIVIDUALS[FAMILIES[fam].husb].name, False) + "(" + INDIVIDUALS[FAMILIES[fam].husb].idNum + ") is " + str(hAgeDif) + " years older than " + getPronoun(INDIVIDUALS[FAMILIES[fam].husb].sex) + " child, " + stripClean(INDIVIDUALS[c].name, False) + "(" + INDIVIDUALS[c].idNum + ").\n"
    return errors

def checkUS15():
    '''Checks to make sure that there are at most 15 children in a family.'''
    errors = ""
    for fam in FAMILIES:
        f = FAMILIES[fam]
        children = f.chil
        if len(children) > 15:
            errors += 'Anomaly US15: Family ' + stripClean(f.fam) + ' has ' + str(len(children)) + ' children.\n'
    return errors

def checkUS14():
    '''Checks if more than 5 children at once.'''
    errors = ""
    for fam in FAMILIES:
        f = FAMILIES[fam]
        children = f.chil
        if len(children) < 5:
            continue
        else:
            birthdays = []
            for child in children:
                birthdays.append(INDIVIDUALS[child].birth)
            birthsCount = 0
            for r in range(0, len(birthdays)-1):
                if birthdays[r] == birthdays[r+1]:
                    birthsCount += 1
            if birthsCount >= 5:
                errors += 'Anomaly US14: Family ' + stripClean(f.fam) + ' has ' + str(birthsCount) + ' children born on the same day.\n'
    return errors

def checkUS16():
    '''Checks to make sure that all the males in the family has same last names.'''
    errors = ""
    for fam in FAMILIES:
        f = FAMILIES[fam]
        husband = stripClean(INDIVIDUALS[f.husb].name, False).split()
        husb_last = husband[1]
        for c in f.chil:
            ch = stripClean(INDIVIDUALS[c].name, False).split()
            ch_last = ch[1]
            if INDIVIDUALS[c].sex.strip() == 'M':
                if ch_last != husb_last:
                    errors += "Error US16: " + stripClean(INDIVIDUALS[c].name, False) + "is not as same as their father's last name " + stripClean(INDIVIDUALS[FAMILIES[fam].husb].name, False) + ".\n"
    return errors

def checkUS17():
    '''Checks to make sure that parents are not married to their descendants'''
    errors = ""
    for fam in FAMILIES:
        f = FAMILIES[fam]
        husb_id = INDIVIDUALS[f.husb].idNum
        wife_id = INDIVIDUALS[f.wife].idNum
        for c in f.chil:
            ch = INDIVIDUALS[c].idNum
            if ch == husb_id:
                errors += "Error US17: " + stripClean(INDIVIDUALS[f.wife].name, False) + " is married to the descendant " + stripClean(INDIVIDUALS[c].name, False) + ".\n"
            if ch == wife_id:
                errors += "Error US17: " + stripClean(INDIVIDUALS[f.husb].name, False) + " is married to the descendant " + stripClean(INDIVIDUALS[c].name, False) + ".\n"

    return errors

def checkUS18():
    """
    Checks to make sure siblings are not married.
    :return: A string containing error messages.
    """
    errors = ""
    for fam in FAMILIES:
        if INDIVIDUALS[FAMILIES[fam].husb].famc == INDIVIDUALS[FAMILIES[fam].wife].famc and INDIVIDUALS[FAMILIES[fam].husb].famc != '':
            errors += "Error US18: " + stripClean(INDIVIDUALS[FAMILIES[fam].husb].name, False) + "("+INDIVIDUALS[FAMILIES[fam].husb].idNum+") married "+getPronoun(INDIVIDUALS[FAMILIES[fam].husb].sex)+" sibling, " + stripClean(INDIVIDUALS[FAMILIES[fam].wife].name, False) + "("+INDIVIDUALS[FAMILIES[fam].wife].idNum+").\n"
    return errors

def checkUS19():
    '''Checks to make sure first cousins are not married.'''
    errors = ''
    for fam in FAMILIES:
        husb = FAMILIES[fam].husb
        wife = FAMILIES[fam].wife
        if areCousins(husb, wife):
            errors += "Error US19: " + stripClean(INDIVIDUALS[husb].name, False) + "(" + stripClean(husb) + ") married " + getPronoun(INDIVIDUALS[husb].sex) + " cousin, " + stripClean(INDIVIDUALS[wife].name, False) + "(" + stripClean(wife) + ").\n"
    return errors

def checkUS20():
    '''Checks to make sure aunts and uncles do not marry their nieces and nephews.'''
    errors = ''
    for fam in FAMILIES:
        husb = FAMILIES[fam].husb
        wife = FAMILIES[fam].wife
        if isAuntUncle(husb, wife):
            errors += "Error US20: " + stripClean(INDIVIDUALS[husb].name, False) + "(" + stripClean(husb) + ") married " + getPronoun(INDIVIDUALS[husb].sex) + " niece, " + stripClean(INDIVIDUALS[wife].name, False) + "(" + stripClean(wife) + ").\n"
        if isAuntUncle(wife, husb):
            errors += "Error US20: " + stripClean(INDIVIDUALS[wife].name, False) + "(" + stripClean(wife) + ") married " + getPronoun(INDIVIDUALS[wife].sex) + " nephew, " + stripClean(INDIVIDUALS[husb].name, False) + "(" + stripClean(husb) + ").\n"
    return errors

def checkUS21():
    '''Tests if individuals have the correct gender based on role in marriage.'''
    errors = ''
    for fam in FAMILIES:
        husb = FAMILIES[fam].husb
        wife = FAMILIES[fam].wife
        if INDIVIDUALS[husb].sex.strip() == 'F':
            errors += "Error US21: Husband " + stripClean(INDIVIDUALS[husb].name, False) + "(" + stripClean(husb) + ") is assigned the wrong gender for role.\n"
        if INDIVIDUALS[wife].sex.strip() == 'M':
            errors += "Error US21: Wife " + stripClean(INDIVIDUALS[wife].name, False) + "(" + stripClean(wife) + ") is assigned the wrong gender for role.\n"
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

def checkUS23():
    '''Tests if all individuals have a unique name and birthday'''
    errors = ""
    names = []
    birthdays = []
    for ind in INDIVIDUALS:
        names.append(INDIVIDUALS[ind].name)
        birthdays.append(INDIVIDUALS[ind].birth)
    for i in range(0, len(INDIVIDUALS) - 1):
        name1 = names[i]
        for j in range(i + 1, len(INDIVIDUALS)):
            name2 = names[j]
            if name1 == name2:
                if birthdays[i] == birthdays[j]:
                    errors += "Error US23: " + stripClean(name1, False) + "appears in the file multiple times.\n"
    return errors

def checkUS24():
    '''Tests all the names of spouses in all the families and checks if they're similar'''
    errors = ""
    i = 0
    for fam in FAMILIES:
        j = 0
        husb = FAMILIES[fam].husb
        wife = FAMILIES[fam].wife
        mardate = FAMILIES[fam].marr
        for fam1 in FAMILIES:
            if j < i:
                j += 1
                continue
            husb1 = FAMILIES[fam1].husb
            wife1 = FAMILIES[fam1].wife
            mardate1 = FAMILIES[fam1].marr
            j += 1
            if fam != fam1:
                if husb == husb1:
                    if wife == wife1:
                        if mardate == mardate1:
                            errors += "Error US24: " + stripClean(husb, False) + ", " + stripClean(wife, False) + " with marriage date " + str(mardate) + " appears in the multiple families.\n"
            i += 1
    return errors

def checkUS25():
    '''
    Tests all the names of children and their birth dates within a family are unique.
    '''
    errors = ""
    for fam in FAMILIES:
        f = FAMILIES[fam]
        for i in range(0, len(f.chil) - 1):
            chil_name1 = INDIVIDUALS[f.chil[i]].name
            chil_bd1 = INDIVIDUALS[f.chil[i]].birth
            for j in range(i + 1, len(f.chil)):
                chil_name2 = INDIVIDUALS[f.chil[j]].name
                chil_bd2 = INDIVIDUALS[f.chil[j]].birth
                if chil_name1 == chil_name2:
                    if chil_bd1 == chil_bd2:
                        s = "Error US25: " + stripClean(chil_name1, False) +"and "+ str(chil_bd1) + " appears in the file multiple times.\n"
                        if s not in errors:
                            errors += s
                else:
                    errors += ""
    return errors

def checkUS26():
    """
    Makes sure that every family member is in their proper spot in the individuals object and every
    individual is in their proper spot in the families objects.
    :return: a string of errors
    """
    errors = ""
    for f in FAMILIES:
        if FAMILIES[f].husb not in INDIVIDUALS or INDIVIDUALS[FAMILIES[f].husb].fams != FAMILIES[f].fam:
            errors += "Error US26: Husband " + FAMILIES[f].husb + " is not properly in the individuals records.\n"
        if FAMILIES[f].wife not in INDIVIDUALS or INDIVIDUALS[FAMILIES[f].wife].fams != FAMILIES[f].fam:
            errors += "Error US26: Wife " + FAMILIES[f].wife + " is not properly in the individuals records.\n"
        for c in FAMILIES[f].chil:
            if c not in INDIVIDUALS or INDIVIDUALS[c].famc != FAMILIES[f].fam:
                errors += "Error US26: Child " + c + " is not properly in the individuals records.\n"
    for i in INDIVIDUALS:
        if INDIVIDUALS[i].fams != "":
            if INDIVIDUALS[i].fams not in FAMILIES or (FAMILIES[INDIVIDUALS[i].fams].husb != INDIVIDUALS[i].idNum and FAMILIES[INDIVIDUALS[i].fams].wife != INDIVIDUALS[i].idNum):
                errors += "Error US26: Spouse " + stripClean(INDIVIDUALS[i].name, False) + "(" + INDIVIDUALS[i].idNum + ") is not properly in the families records.\n"
        if INDIVIDUALS[i].famc != "":
            if INDIVIDUALS[i].famc not in FAMILIES or INDIVIDUALS[i].idNum not in FAMILIES[INDIVIDUALS[i].famc].chil:
                errors += "Error US26: Child " + stripClean(INDIVIDUALS[i].name, False) + "(" + INDIVIDUALS[i].idNum + ") is not properly in the families records.\n"
    return errors

def checkUS27(year, month, day, alive, dYear, dMonth, dDay):
    today = date.today()
    if alive:
        return today.year - year - ((today.month, today.day) < (month, day))
    else:
        return dYear - year - ((dMonth, dDay) < (month, day))
def checkUS31():
    '''Lists all living individuals over 30 who have never married'''
    unmarr_livin = ''
    for i in INDIVIDUALS:
        indi = INDIVIDUALS[i]
        if indi.death == '':
            age = checkUS27(indi.birth.year, indi.birth.month, indi.birth.day, True, 0, 0, 0)
            if age > 30 and indi.fams == "":
                    unmarr_livin += "US31: " + stripClean(indi.name, False) +  "has never married.\n"

    return unmarr_livin

def checkUS32():
    '''
    Checks and returns if there is any redundancy in the birth dates.
    '''
    birthdays = ""
    for i in INDIVIDUALS:
        bd1 = INDIVIDUALS[i].birth
        for j in INDIVIDUALS:
            if i == j:
                continue
            bd2 = INDIVIDUALS[j].birth
            if bd1 == bd2:
                toAdd = "US32: " + str(INDIVIDUALS[i].birth) +  " is a multiple birth date.\n"
                if toAdd not in birthdays:
                    birthdays += toAdd
    return birthdays

def checkUS29():
    '''List Deceased'''
    deceased = ""
    for ind in INDIVIDUALS:
        if INDIVIDUALS[ind].death == "":
            pass
        else:
            deceased += "US29: " + stripClean(INDIVIDUALS[ind].name, False) + "(" + ind + ") is deceased.\n"
    return deceased

def checkUS30():
    '''List living married'''
    livingMarried = ""
    for ind in INDIVIDUALS:
        if INDIVIDUALS[ind].death == "":
            for fam in FAMILIES:
                if ind == FAMILIES[fam].husb or ind == FAMILIES[fam].wife:
                    if FAMILIES[fam].div == "":
                        livingMarried += "US30: " + stripClean(INDIVIDUALS[ind].name, False) + "(" + ind + ") is married in family " + fam + " and living.\n"
    return livingMarried

def checkUS33():
    '''Lists all orphans'''
    orphans = ''
    for x in INDIVIDUALS:
        # if individual is not dead, calculate their age
        record = INDIVIDUALS[x]
        if record.death == '':
            age = checkUS27(record.birth.year, record.birth.month, record.birth.day, True, 0, 0, 0)
            if age < 18:
                (dad, mom) = getParents(x)
                # if parents' record exists...
                if (dad != ''):
                    # check if dad is dead
                    if INDIVIDUALS[dad].death == '':
                        pass
                    else:
                        if (mom != ''):
                            # check if mom is dead
                            if INDIVIDUALS[mom].death == '':
                                pass
                            else:
                                orphans += "US33: " + stripClean(record.name, False) + "(" + x + ") is an orphan.\n"
    return orphans
def checkUS34():
    couples = ""
    for f in FAMILIES:
        husb = INDIVIDUALS[FAMILIES[f].husb]
        wife = INDIVIDUALS[FAMILIES[f].wife]
        hAge = 0
        wAge = 0
        if husb.death == "":
            hAge = checkUS27(husb.birth.year, husb.birth.month, husb.birth.day, False, 0,0,0)
        else:
            hAge = checkUS27(husb.birth.year, husb.birth.month, husb.birth.day, True, husb.death.year, husb.death.month, husb.death.day)
        if wife.death == "":
            wAge = checkUS27(wife.birth.year, wife.birth.month, wife.birth.day, wife.death == "", 0, 0, 0)
        else:
            wAge = checkUS27(wife.birth.year, wife.birth.month, wife.birth.day, True, wife.death.year, wife.death.month, wife.death.day)
        if hAge > 2*wAge:
            couples += "US34: Husband "+stripClean(husb.name, False) + "(" + str(husb.idNum)+"), age "+ str(hAge) +" is more than twice as old as his wife "+stripClean(wife.name, False) + "(" + str(wife.idNum)+"), age "+ str(wAge) +".\n"
        if wAge > 2*hAge:
            couples += "US34: Wife "+stripClean(wife.name, False) + "(" + str(wife.idNum)+"), age "+ str(wAge) +" is more than twice as old as her husband "+stripClean(husb.name, False) + "(" + str(husb.idNum)+"), age "+ str(hAge) +".\n"
    return couples
def checkUS35():
    newborns = ""
    curr = datetime.datetime.now()
    curr = date(curr.year, curr.month, curr.day)
    for i in INDIVIDUALS:
        birth = date(INDIVIDUALS[i].birth.year, INDIVIDUALS[i].birth.month, INDIVIDUALS[i].birth.day)
        dif = (curr-birth).days
        if dif <= 30:
            newborns += "US35: "+stripClean(INDIVIDUALS[i].name, False) + "("+str(INDIVIDUALS[i].idNum)+") is less than 30 days old.\n"
    return newborns
def areCousins(p1, p2):
    '''Checks if p1 and p2 are cousins. Returns true if they are, false otherwise.'''
    (dad1, mom1) = getParents(p1)
    (dad2, mom2) = getParents(p2)
    if dad1 == '' or dad2 == '':
        # not enough information to tell! parents don't exist in our database
        return False
    if areSiblings(dad1, dad2) or areSiblings(mom1, mom2) or areSiblings(dad1, mom2) or areSiblings(dad2, mom1):
        return True
    return False

def areSiblings(p1, p2):
    ''' returns true if p1 and p2 are siblings, false otherwise'''
    if INDIVIDUALS[p1].famc == '' or INDIVIDUALS[p2].famc == '':
        return False
    if INDIVIDUALS[p1].famc == INDIVIDUALS[p2].famc:
        return True
    return False

def isAuntUncle(p1, p2):
    '''Checks if p1 is p2's aunt or uncle. Returns true if so, false otherwise.'''
    (dad, mom) = getParents(p2)
    if dad != '' and mom != '':
        if areSiblings(dad, p1) or areSiblings(mom, p1):
            return True
    return False

def getParents(p):
    '''Returns the parent ids of individual p as a tuple, empty if no parents are recorded.'''
    for fam in FAMILIES:
        if p in FAMILIES[fam].chil:
            return(FAMILIES[fam].husb, FAMILIES[fam].wife)
    return ('', '')

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
