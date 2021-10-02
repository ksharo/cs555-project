import unittest
from CS555_HW5 import *

class TestUS02(unittest.TestCase):

    def testBirthFirst(self):
        ''' Test that no error occurs when birth occurs before death '''
        file = open('./TestFiles/valid.ged', 'r')
        parseFile(file, True)
        self.assertEqual(checkUS02(), "", "Should print no errors.")
        file.close()

    def testEarlyMarriage(self):
        ''' Test that the proper error is printed when both the
            wife and husband are born after the wedding. '''
        file = open('./TestFiles/US02/us02test2_input.ged', 'r')
        parseFile(file, True)
        self.assertEqual(checkUS02(), "Error US02: Birth date of Sarah Alanson (I6000000178401456922) occurs after her marriage date.\nError US02: Birth date of Lloyd Alanson (I6000000178401456922) occurs after his marriage date.\n", "Should print error for husband and wife.")
        file.close()

    def testLateWife(self):
        ''' Test that the proper error is printed when both the
            wife and husband are born after the wedding. '''
        file = open('./TestFiles/US02/us02test3_input.ged', 'r')
        parseFile(file, True)
        self.assertEqual(checkUS02(), "Error US02: Birth date of Jennifer Thomas (I6000000178403254861) occurs after her marriage date.\n", "Should print error for wife only.")
        file.close()

    def testLateHusb(self):
        ''' Test that the proper error is printed when both the
            wife and husband are born after the wedding. '''
        file = open('./TestFiles/US02/us02test4_input.ged', 'r')
        parseFile(file, True)
        self.assertEqual(checkUS02(), "Error US02: Birth date of Elijah Thomas (I6000000178403254861) occurs after his marriage date.\n", "Should print error for husband only.")
        file.close()

    def testDayAfter(self):
        ''' Make sure that the error is caught even if the birth is
            one day after the wedding. '''
        file = open('./TestFiles/US02/us02test5_input.ged', 'r')
        parseFile(file, True)
        self.assertEqual(checkUS02(), "Error US02: Birth date of Elijah Thomas (I6000000178403254861) occurs after his marriage date.\n", "Should print error for husband only.")
        file.close()

class TestUS03(unittest.TestCase):

    def testBirthFirst(self):
        ''' Test that no error occurs when birth occurs before death '''
        file = open('./TestFiles/valid.ged', 'r')
        parseFile(file, True)
        self.assertEqual(checkUS03(), "", "Should print no errors")
        file.close()

    def testDeathFirstInOrderMale(self):
        ''' Test that an error is printed to the screen when death
            occurs before birth and the records are in order (birth->death)'''
        file = open('./TestFiles/US03/us03test2a_input.ged', 'r')
        parseFile(file, True)
        self.assertEqual(checkUS03(), "Error US03: Birth date of Julius Lexus (I6000000178403393861) occurs after his death date.\n", "Should print error with pronoun 'his'.")
        file.close()

    def testDeathFirstWrongOrderMale(self):
        ''' Test that an error is printed to the screen when death
            occurs before birth and the records are not in order (death->birth)'''
        file = open('./TestFiles/US03/us03test2b_input.ged', 'r')
        parseFile(file, True)
        self.assertEqual(checkUS03(), "Error US03: Birth date of Julius Lexus (I6000000178403393861) occurs after his death date.\n", "Should print error with pronoun 'his'.")
        file.close()

    def testDeathFirstInOrderFemale(self):
        ''' Test that an error is printed to the screen when death
            occurs before birth and the records are in order (birth->death)'''
        file = open('./TestFiles/US03/us03test3a_input.ged', 'r')
        parseFile(file, True)
        self.assertEqual(checkUS03(), "Error US03: Birth date of Regan Lexus (I6) occurs after her death date.\n", "Should print error with pronoun 'her'.")
        file.close()


    def testDeathFirstWrongOrderFemale(self):
        ''' Test that an error is printed to the screen when death
            occurs before birth and the records are not in order (death->birth)'''
        file = open('./TestFiles/US03/us03test3b_input.ged', 'r')
        parseFile(file, True)
        self.assertEqual(checkUS03(), "Error US03: Birth date of Regan Lexus (I6) occurs after her death date.\n", "Should print error with pronoun 'her'.")
        file.close()

    def testManyErrors(self):
        ''' Test that an error is printed for each of 3 records with
            death before birth. Also checks all 3 pronoun types'''
        file = open('./TestFiles/US03/us03test4_input.ged', 'r')
        parseFile(file, True)
        self.assertEqual(checkUS03(), "Error US03: Birth date of Jennifer Thomas (I6000000178403254861) occurs after their death date.\nError US03: Birth date of Jacob Alanson (I6000000178403963822) occurs after his death date.\nError US03: Birth date of Sarah Alanson (I6000000178401456922) occurs after her death date.\n", "Should print 3 errors.")
        file.close()
        
    def testSameYear(self):
        ''' Test that an error is printed for a record that has a birth
            and death in the same year, but death is still earlier'''
        file = open('./TestFiles/US03/us03test5_input.ged', 'r')
        parseFile(file, True)
        self.assertEqual(checkUS03(), "Error US03: Birth date of Julius Lexus (I6000000178403393861) occurs after his death date.\n", "Should print error with pronoun 'his'.")
        file.close()

    def testSameDay(self):
        ''' Test that no error is printed for a record that has a birth
            and death on the same day - this is possible'''
        file = open('./TestFiles/US03/us03test6_input.ged', 'r')
        parseFile(file, True)
        self.assertEqual(checkUS03(), "", "Should not print an error.")
        file.close()

class TestUS13(unittest.TestCase):
        def testGoodSiblings(self):
            ''' Test that no error occurs when siblings are born in valid dates '''
            file = open('./TestFiles/valid.ged', 'r')
            parseFile(file, True)
            self.assertEqual(checkUS13(), "", "Should print no errors")
            file.close()

        def testOneWrongSibling(self):
            ''' Tests that the proper error is printed when two siblings are born
                too close together. '''
            file = open('./TestFiles/US13/us13test2_input.ged', 'r')
            parseFile(file, True)
            self.assertEqual(checkUS13(), "Anomaly US13: Birth dates of September Thomas (I6000000178401782906) and August Thomas (I6000000178403634834) are 2 days apart.\n", "Should print error between two siblings.")
            file.close()

        def testOneDayApart(self):
            ''' Tests that no error is printed when two siblings are born
                within one day of each other. '''
            file = open('./TestFiles/US13/us13test3_input.ged', 'r')
            parseFile(file, True)
            self.assertEqual(checkUS13(), "", "Should print no errors.")
            file.close()

        def testOneWrongTriplet(self):
            ''' Tests that the proper error is printed when one sibling is born
                within two days of two others. '''
            file = open('./TestFiles/US13/us13test4_input.ged', 'r')
            parseFile(file, True)
            self.assertEqual(checkUS13(), "Anomaly US13: Birth dates of September Thomas (I6000000178401782906) and April Thomas (I6000000178401304897) are 2 days apart.\n", "Should print two errors.")
            file.close()

        def testTwoWrongSiblings(self):
            ''' Tests that the proper error is printed when three siblings are born
                within one day of each other. '''
            file = open('./TestFiles/US13/us13test5_input.ged', 'r')
            parseFile(file, True)
            self.assertEqual(checkUS13(), "Anomaly US13: Birth dates of August Thomas (I6000000178403634834) and April Thomas (I6000000178401304897) are 32 days apart.\nAnomaly US13: Birth dates of September Thomas (I6000000178401782906) and April Thomas (I6000000178401304897) are 61 days apart.\nAnomaly US13: Birth dates of September Thomas (I6000000178401782906) and August Thomas (I6000000178403634834) are 29 days apart.\n", "Should print one error.")
            file.close()
            
if __name__ == "__main__":
    # run all the tests
    unittest.main()
