import unittest
from CS555_HW5 import *


class TestUS02(unittest.TestCase):

    def testBirthFirst(self):
        """
        Test that no error occurs when birth occurs before death
        :return:
        """
        f = open('./TestFiles/valid.ged', 'r')
        parseFile(f, True)
        self.assertEqual(checkUS02(), "", "Should print no errors.")
        f.close()

    def testEarlyMarriage(self):
        """
        Test that the proper error is printed when both the
        wife and husband are born after the wedding.
        :return:
        """
        f = open('./TestFiles/US02/us02test2_input.ged', 'r')
        parseFile(f, True)
        self.assertEqual(checkUS02(),
                         "Error US02: Birth date of Sarah Alanson (I6000000178401456922) occurs after her marriage date.\nError US02: Birth date of Lloyd Alanson (I6000000178401456922) occurs after his marriage date.\n",
                         "Should print error for husband and wife.")
        f.close()

    def testLateWife(self):
        """
        Test that the proper error is printed when both the
        wife and husband are born after the wedding.
        :return:
        """
        f = open('./TestFiles/US02/us02test3_input.ged', 'r')
        parseFile(f, True)
        self.assertEqual(checkUS02(),
                         "Error US02: Birth date of Jennifer Thomas (I6000000178403254861) occurs after her marriage date.\n",
                         "Should print error for wife only.")
        f.close()

    def testLateHusb(self):
        """
        Test that the proper error is printed when both the
        wife and husband are born after the wedding.
        :return:
        """
        f = open('./TestFiles/US02/us02test4_input.ged', 'r')
        parseFile(f, True)
        self.assertEqual(checkUS02(),
                         "Error US02: Birth date of Elijah Thomas (I6000000178403254861) occurs after his marriage date.\n",
                         "Should print error for husband only.")
        f.close()

    def testDayAfter(self):
        """
        Make sure that the error is caught even if the birth is
        one day after the wedding.
        :return:
        """
        f = open('./TestFiles/US02/us02test5_input.ged', 'r')
        parseFile(f, True)
        self.assertEqual(checkUS02(),
                         "Error US02: Birth date of Elijah Thomas (I6000000178403254861) occurs after his marriage date.\n",
                         "Should print error for husband only.")
        f.close()


class TestUS03(unittest.TestCase):

    def testBirthFirst(self):
        """
        Test that no error occurs when birth occurs before death
        :return:
        """
        f = open('./TestFiles/valid.ged', 'r')
        parseFile(f, True)
        self.assertEqual(checkUS03(), "", "Should print no errors")
        f.close()

    def testDeathFirstInOrderMale(self):
        """
        Test that an error is printed to the screen when death
        occurs before birth and the records are in order (birth->death)
        :return:
        """
        f = open('./TestFiles/US03/us03test2a_input.ged', 'r')
        parseFile(f, True)
        self.assertEqual(checkUS03(),
                         "Error US03: Birth date of Julius Lexus (I6000000178403393861) occurs after his death date.\n",
                         "Should print error with pronoun 'his'.")
        f.close()

    def testDeathFirstWrongOrderMale(self):
        """
        Test that an error is printed to the screen when death
        occurs before birth and the records are not in order (death->birth)
        :return:
        """
        f = open('./TestFiles/US03/us03test2b_input.ged', 'r')
        parseFile(f, True)
        self.assertEqual(checkUS03(),
                         "Error US03: Birth date of Julius Lexus (I6000000178403393861) occurs after his death date.\n",
                         "Should print error with pronoun 'his'.")
        f.close()

    def testDeathFirstInOrderFemale(self):
        """
        Test that an error is printed to the screen when death
        occurs before birth and the records are in order (birth->death)
        :return:
        """
        f = open('./TestFiles/US03/us03test3a_input.ged', 'r')
        parseFile(f, True)
        self.assertEqual(checkUS03(), "Error US03: Birth date of Regan Lexus (I6) occurs after her death date.\n",
                         "Should print error with pronoun 'her'.")
        f.close()

    def testDeathFirstWrongOrderFemale(self):
        """
        Test that an error is printed to the screen when death
        occurs before birth and the records are not in order (death->birth)
        :return:
        """
        f = open('./TestFiles/US03/us03test3b_input.ged', 'r')
        parseFile(f, True)
        self.assertEqual(checkUS03(), "Error US03: Birth date of Regan Lexus (I6) occurs after her death date.\n",
                         "Should print error with pronoun 'her'.")
        f.close()

    def testManyErrors(self):
        """
        Test that an error is printed for each of 3 records with
        death before birth. Also checks all 3 pronoun types
        :return:
        """
        f = open('./TestFiles/US03/us03test4_input.ged', 'r')
        parseFile(f, True)
        self.assertEqual(checkUS03(),
                         "Error US03: Birth date of Jennifer Thomas (I6000000178403254861) occurs after their death date.\nError US03: Birth date of Jacob Alanson (I6000000178403963822) occurs after his death date.\nError US03: Birth date of Sarah Alanson (I6000000178401456922) occurs after her death date.\n",
                         "Should print 3 errors.")
        f.close()

    def testSameYear(self):
        """
        Test that an error is printed for a record that has a birth
        and death in the same year, but death is still earlier
        :return:
        """
        f = open('./TestFiles/US03/us03test5_input.ged', 'r')
        parseFile(f, True)
        self.assertEqual(checkUS03(),
                         "Error US03: Birth date of Julius Lexus (I6000000178403393861) occurs after his death date.\n",
                         "Should print error with pronoun 'his'.")
        f.close()

    def testSameDay(self):
        """
        Test that no error is printed for a record that has a birth
        and death on the same day - this is possible
        :return:
        """
        f = open('./TestFiles/US03/us03test6_input.ged', 'r')
        parseFile(f, True)
        self.assertEqual(checkUS03(), "", "Should not print an error.")
        f.close()

class TestUS04(unittest.TestCase):
    def testMarriageFirst(self):
        '''
        Tests that no errors when marriage is before divorce
        '''
        f = open('./TestFiles/valid.ged', 'r')
        parseFile(f, True)
        self.assertEqual(checkUS04(), "", "Should print no errors")
        f.close()
    def testDivorceFirst(self):
        '''
        Tests that error occurs when divorce is before marriage
        '''
        f = open('./TestFiles/US04/us04test2_input.ged', 'r')
        parseFile(f, True)
        self.assertEqual(checkUS04(), "Error US04: Divorce date of Julius Lexus (I6000000178403393861) and Summer Lexus (I6000000178402244920) is before their marriage.\n", "Should print error")
        f.close()

class TestUS05(unittest.TestCase):
    def testgoodMarriage(self):
        '''
        Tests that no errors when marriage is before death
        '''
        f = open('./TestFiles/valid.ged', 'r')
        parseFile(f, True)
        self.assertEqual(checkUS05(), "", "Should print no errors")
        f.close()
    def testHusbandDeathBeforeMarriage(self):
        '''
        Tests that error occurs when husband death is before marriage
        '''
        f = open('./TestFiles/US05/us05test2_input.ged', 'r')
        parseFile(f, True)
        self.assertEqual(checkUS05(), "Error US05: Marriage date of Elijah Thomas (I6000000178400484002) and Jennifer Thomas (I6000000178403254861) is after one of their death.\n", "Should print no errors")
        f.close()
    def testWifeDeathBeforeMarriage(self):
        '''
        Tests that error occurs when husband death is before marriage
        '''
        f = open('./TestFiles/US05/us05test3_input.ged', 'r')
        parseFile(f, True)
        self.assertEqual(checkUS05(), "Error US05: Marriage date of Julius Lexus (I6000000178403393861) and Summer Lexus (I6000000178402244920) is after one of their death.\n", "Should print no errors")
        f.close()
    def testBothDeathBeforeMarriage(self):
        '''
        Tests that error occurs when both husband and wife are dead before marriage
        '''
        f = open('./TestFiles/US05/us05test4_input.ged', 'r')
        parseFile(f, True)
        self.assertEqual(checkUS05(), "Error US05: Marriage date of Julius Lexus (I6000000178403393861) and Summer Lexus (I6000000178402244920) is after one of their death.\n", "Should print no errors")
        f.close()

class TestUS06(unittest.TestCase):
    def testGoodDivorceDate(self):
        """
        Test that no errors occurs when a valid divorce date is inputted
        :return:
        """
        f = open('./TestFiles/valid.ged', 'r')
        parseFile(f, True)
        self.assertEqual(checkUS06(), "", "Should print no errors")
        f.close()
    def testBadDivorceDate(self):
        """
        Basic test to make sure a "bad" divorce date fails
        :return:
        """
        f = open('./TestFiles/US06/us06test2_input.ged', 'r')
        parseFile(f, True)
        self.assertEqual(checkUS06(),
                         "Error US06: Divorce date of Julius Lexus (I6000000178403393861) and Summer Lexus (I6000000178402244920) is after their deaths.\n",
                         "Should print one error including a divorced couple.")
        f.close()
    def testDeadHusbandLivingWife(self):
        """
        Test to see if a dead husband but living wife will trigger an
        invalid divorce date
        :return:
        """
        f = open('./TestFiles/US06/us06test3_input.ged', 'r')
        parseFile(f, True)
        self.assertEqual(checkUS06(),
                         "",
                         "Should print no errors.")
        f.close()
    def testDeadWifeLivingHusband(self):
        """
        Test to see if a dead wife but living husband will trigger an
        invalid divorce date
        :return:
        """
        f = open('./TestFiles/US06/us06test4_input.ged', 'r')
        parseFile(f, True)
        self.assertEqual(checkUS06(),
                         "",
                         "Should print no errors.")
        f.close()
    def testMultipleBadDivorceDates(self):
        """
        Test to see if a dead wife but living husband will trigger an
        invalid divorce date
        :return:
        """
        f = open('./TestFiles/US06/us06test5_input.ged', 'r')
        parseFile(f, True)
        self.assertEqual(checkUS06(),
                         "Error US06: Divorce date of Julius Lexus (I6000000178403393861) and Summer Lexus (I6000000178402244920) is after their deaths.\nError US06: Divorce date of Lloyd Alanson (I6000000178401748954) and Summer Lexus (I6000000178402244920) is after their deaths.\n",
                         "Should print no errors.")
        f.close()

class TestUS07(unittest.TestCase):
    def testGoodAge(self):
        """
        Test that no errors occurs when the person is under 150 years old
        :return:
        """
        f = open('./TestFiles/valid.ged', 'r')
        parseFile(f, True)
        self.assertEqual(checkUS07(36, "I6000000178401748954"), "", "Should print no errors")
        f.close()

    def testBadAge(self):
        """
        Tests that the proper error is printed when somebody is too old.
        :return:
        """
        f = open('./TestFiles/US07/us07test2_input.ged', 'r')
        parseFile(f, True)
        self.assertEqual(checkUS07(3000, "I6000000178403393861"),
                         "Error US07: Age of Julius Lexus (I6000000178403393861) > 150.\n",
                         "Should print error age too high.")
        f.close()

    def testMaxValidAge(self):
        """
        Tests that no error is thrown when the maximum age is hit
        :return:
        """
        f = open('./TestFiles/US07/us07test3_input.ged', 'r')
        parseFile(f, True)
        self.assertEqual(checkUS07(150, "I6000000178403393861"),
                         "",
                         "Should print no errors.")
        f.close()


class TestUS13(unittest.TestCase):
    def testGoodSiblings(self):
        """
        Test that no error occurs when siblings are born in valid dates
        :return:
        """
        f = open('./TestFiles/valid.ged', 'r')
        parseFile(f, True)
        self.assertEqual(checkUS13(), "", "Should print no errors")
        f.close()

    def testOneWrongSibling(self):
        """
        Tests that the proper error is printed when two siblings are born
        too close together.
        :return:
        """
        f = open('./TestFiles/US13/us13test2_input.ged', 'r')
        parseFile(f, True)
        self.assertEqual(checkUS13(),
                         "Anomaly US13: Birth dates of September Thomas (I6000000178401782906) and August Thomas (I6000000178403634834) are 2 days apart.\n",
                         "Should print error between two siblings.")
        f.close()

    def testOneDayApart(self):
        """
        Tests that no error is printed when two siblings are born
        within one day of each other.
        :return:
        """
        f = open('./TestFiles/US13/us13test3_input.ged', 'r')
        parseFile(f, True)
        self.assertEqual(checkUS13(), "", "Should print no errors.")
        f.close()

    def testOneWrongTriplet(self):
        """
        Tests that the proper error is printed when one sibling is born
        within two days of two others.
        :return:
        """
        f = open('./TestFiles/US13/us13test4_input.ged', 'r')
        parseFile(f, True)
        self.assertEqual(checkUS13(),
                         "Anomaly US13: Birth dates of September Thomas (I6000000178401782906) and April Thomas (I6000000178401304897) are 2 days apart.\n",
                         "Should print two errors.")
        f.close()

    def testTwoWrongSiblings(self):
        """
        Tests that the proper error is printed when three siblings are born
        within one day of each other.
        :return:
        """
        f = open('./TestFiles/US13/us13test5_input.ged', 'r')
        parseFile(f, True)
        self.assertEqual(checkUS13(),
                         "Anomaly US13: Birth dates of August Thomas (I6000000178403634834) and April Thomas (I6000000178401304897) are 32 days apart.\nAnomaly US13: Birth dates of September Thomas (I6000000178401782906) and April Thomas (I6000000178401304897) are 61 days apart.\nAnomaly US13: Birth dates of September Thomas (I6000000178401782906) and August Thomas (I6000000178403634834) are 29 days apart.\n",
                         "Should print one error.")
        f.close()
class TestUS22(unittest.TestCase):
    def testGoodIDs(self):
        """
        Test that no errors occur when all ids are unique for both
        individuals and families
        :return:
        """
        f = open('./TestFiles/valid.ged', 'r')
        parseFile(f, True)
        self.assertEqual(checkUS22("", 0), "", "Should print no errors")
        f.close()
    def testDuplicateIndividualID(self):
        """
        Tests that the proper error is thrown when a duplicate
        individual ID is used.
        :return:
        """
        f = open('./TestFiles/US22/us22test2_input.ged', 'r')
        parseFile(f, True)
        self.assertEqual(checkUS22("I6000000178403862823", 0),
                         "Error US22: Individual ID I6000000178403862823 already used.\n",
                         "Should print one error.")
        f.close()
    def testDuplicateFamilyID(self):
        """
        Tests that the proper error is thrown when a duplicate
        family ID is used.
        :return:
        """
        f = open('./TestFiles/US22/us22test3_input.ged', 'r')
        parseFile(f, True)
        self.assertEqual(checkUS22("F6000000178403660847", 1),
                         "Error US22: Family ID F6000000178403660847 already used.\n",
                         "Should print one error.")
        f.close()
    def testMultipleDuplicateFamilyIDs(self):
        f = open('./TestFiles/US22/us22test4_input.ged', 'r')
        parseFile(f, True)
        test1 = checkUS22("F6000000178403503845", 1)
        test2 = checkUS22("F6000000178401748958", 1)
        self.assertEqual(test1+test2,
                         "Error US22: Family ID F6000000178403503845 already used.\nError US22: Family ID F6000000178401748958 already used.\n",
                         "Should print two errors.")
        f.close()
    def testMultipleDuplicateIndividualIDs(self):
        f = open('./TestFiles/US22/us22test5_input.ged', 'r')
        parseFile(f, True)
        test1 = checkUS22("I6000000178400484002", 0)
        test2 = checkUS22("I6000000178403254861", 0)
        self.assertEqual(test1 + test2,
                         "Error US22: Individual ID I6000000178400484002 already used.\nError US22: Individual ID I6000000178403254861 already used.\n",
                         "Should print two errors.")
        f.close()
if __name__ == "__main__":
    # run all the tests
    unittest.main()