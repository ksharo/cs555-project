'''
    Author: Kaitlyn Sharo
    Pledge: I pledge my honor that I have abided by the Stevens Honor System.
    Description: CS 555 Project 02: GEDCOM reader
'''

VALID_TAGS = ["INDI", "NAME", "SEX", "BIRT", "DEAT", "FAMC", "FAMS", "FAM", "MARR", "HUSB", "WIFE", "CHIL", "DIV", "DATE", "HEAD", "TRLR", "NOTE"]

def parseFile(file):
    '''Parses a GEDCOM file based on the specifications given in the
        homework description'''
    for line in file:
        end = "" if "\n" in line else "\n"
        print("-->", line, end=end)
        printOutput(line)

def printOutput(line):
    output = "<--"
    # separate the line into a list of all words with spaces in between
    sections = line.split(" ")
    # error catching to avoid indexing errors
    if len(sections) < 2:
        print("<-- INVALID GED FORMAT:", line)
    # strip each element in the list to remove newline characters
    for x in range(len(sections)):
        sections[x] = sections[x].strip()
    # add the line number to the output
    output += " " + sections[0] + "|"
    # get the tag of the output
    tag = ""
    args = ""
    validity = "N"
    if "INDI" in sections or "FAM" in sections:
        # get the tag and arguments
        args = sections[1]
        tag = sections[2]
    else:
        tag = sections[1]
        for x in sections[2:]:
            args += x + " "
    if tag in VALID_TAGS:
        # check for 2 NAME and 1 DATE
        if (tag == "NAME" and sections[0] == "2") or (tag == "DATE" and sections[0] == "1"):
            validity = "N"
        else:
            validity = "Y"
    # add the tag, validity, and arguments to the output
    output += tag + "|" + validity + "|" + args
    # print the output
    print(output)
    

if __name__ == "__main__":
    fileName = input("What is the name of your file? (Make sure it is in your current directory)\n")
    file = open(fileName, "r")
    parseFile(file)
