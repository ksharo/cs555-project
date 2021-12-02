import unittest
from CS555_HW5 import *


class TestExtraMethods(unittest.TestCase):
    def testPronounHe(self):
        self.assertEqual(getPronoun('M'), 'his', 'Should return his for sex M.')

    def testPronounShe(self):
        self.assertEqual(getPronoun('F'), 'her', 'Should return her for sex F.')

    def testPronounTheir(self):
        self.assertEqual(getPronoun(''), 'their', 'Should return their for sex "".')

    def testGroupPrint(self):
        self.assertEqual(formatGroup(['1', '2', '3']), "{'1', '2', '3'}", 'Should return a properly formatted group.')


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
                         "Error US02: Birth date of Sarah Alanson (I6000000178401456922) occurs after her marriage date.\nError US02: Birth date of Lloyd Alanson (I6000000178401748954) occurs after his marriage date.\n",
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
                         "Error US02: Birth date of Elijah Thomas (I6000000178400484002) occurs after his marriage date.\n",
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
                         "Error US02: Birth date of Elijah Thomas (I6000000178400484002) occurs after his marriage date.\n",
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


class TestUS08(unittest.TestCase):
    def testValidInput(self):
        ''' Test that no errors occurs with valid input. '''
        f = open('./TestFiles/valid.ged', 'r')
        parseFile(f, True)
        self.assertEqual(checkUS08(), "", "Should print no errors")
        f.close()

    def testEarlyDivorce(self):
        ''' Test that an error is printed when a child is born more than
            9 months after his/her parents' divorce. '''
        f = open('./TestFiles/US08/us08test2_input.ged', 'r')
        parseFile(f, True)
        self.assertEqual(checkUS08(),
                         "Error US08: Elijah Thomas (I6000000178400484002) was born more than 9 months after his parents got divorced.\n",
                         "Should print a divorce error")
        f.close()

    def testLateMarriage(self):
        ''' Test that an error is printed when a child is born before his/her parents' marriage. '''
        f = open('./TestFiles/US08/us08test3_input.ged', 'r')
        parseFile(f, True)
        self.assertEqual(checkUS08(),
                         "Error US08: September Thomas (I6000000178401782906) was born before her parents got married.\n",
                         "Should print a marriage error")
        f.close()

    def testMultErrDiv(self):
        ''' Test that an error is printed when three siblings have errors with divorce '''
        f = open('./TestFiles/US08/us08test4_input.ged', 'r')
        parseFile(f, True)
        self.assertEqual(checkUS08(),
                         "Error US08: April Thomas (I6000000178401304897) was born more than 9 months after her parents got divorced.\nError US08: August Thomas (I6000000178403634834) was born more than 9 months after his parents got divorced.\nError US08: September Thomas (I6000000178401782906) was born more than 9 months after her parents got divorced.\n",
                         "Should print two divorce errors")
        f.close()

    def testMultErrMarr(self):
        ''' Test that an error is printed when two children have errors with marriage'''
        f = open('./TestFiles/US08/us08test5_input.ged', 'r')
        parseFile(f, True)
        self.assertEqual(checkUS08(),
                         "Error US08: August Thomas (I6000000178403634834) was born before his parents got married.\nError US08: Jacob Alanson (I6000000178403963822) was born before his parents got married.\n",
                         "Should print two marriage errors")
        f.close()

    def testMultErrMix(self):
        ''' Test that an error is printed when many errors of each type occur '''
        f = open('./TestFiles/US08/us08test6_input.ged', 'r')
        parseFile(f, True)
        self.assertEqual(checkUS08(),
                         "Error US08: August Thomas (I6000000178403634834) was born before his parents got married.\nError US08: September Thomas (I6000000178401782906) was born more than 9 months after her parents got divorced.\nError US08: Elijah Thomas (I6000000178400484002) was born before his parents got married.\n",
                         "Should print multiple errors")
        f.close()
class TestUS09(unittest.TestCase):
    def testValidInput(self):
        ''' Test that no errors occurs with valid input. '''
        f = open('./TestFiles/valid.ged', 'r')
        parseFile(f, True)
        self.assertEqual(checkUS09(), "", "Should print no errors")
        f.close()

    def testBirthAfterMothersDeath(self):
        ''' Tests that an error is printed when a child is born after their mother's death '''
        f = open('./TestFiles/US09/us09test2_input.ged', 'r')
        parseFile(f, True)
        self.assertEqual(checkUS09(),
                         "Error US09: Elijah Thomas (I6000000178400484002) was born after the death of his mother.\n",
                         "Should print a birth after mother's death error")
        f.close()

    def testBirth9MonthsAfterFathersDeath(self):
        ''' Test that an error is printed when a child is born
        more than 9 months after their father's death. '''
        f = open('./TestFiles/US09/us09test3_input.ged', 'r')
        parseFile(f, True)
        self.assertEqual(checkUS09(),
                         "Error US09: Elijah Thomas (I6000000178400484002) was born more than 9 months after the death of his father.\n",
                         "Should print a birth after father's death error")
        f.close()

    def testMultErrFather(self):
        ''' Test that an error is printed when three siblings have errors with father's death '''
        f = open('./TestFiles/US09/us09test4_input.ged', 'r')
        parseFile(f, True)
        self.assertEqual(checkUS09(),
                         "Error US09: April Thomas (I6000000178401304897) was born more than 9 months after the death of her father.\nError US09: August Thomas (I6000000178403634834) was born more than 9 months after the death of his father.\nError US09: September Thomas (I6000000178401782906) was born more than 9 months after the death of her father.\n",
                         "Should print 3 birth after father's death errors")
        f.close()

    def testMultErrMother(self):
        ''' Test that an error is printed when three children have errors with mother's death'''
        f = open('./TestFiles/US09/us09test5_input.ged', 'r')
        parseFile(f, True)
        self.assertEqual(checkUS09(),
                         "Error US09: April Thomas (I6000000178401304897) was born after the death of her mother.\nError US09: August Thomas (I6000000178403634834) was born after the death of his mother.\nError US09: September Thomas (I6000000178401782906) was born after the death of her mother.\n",
                         "Should print three birth after mother's death errors")
        f.close()
# class TestUS11(unittest.TestCase):
#     def testNoBigamy(self):
#         f = open('./TestFiles/valid.ged', 'r')
#         parseFile(f, True)
#         self.assertEqual(checkUS11(), "", "Should print no errors")
#         f.close()
#
#     def testBigamy(self):
#         f = open('./TestFiles/US11/us11test2_input.ged', 'r')
#         parseFile(f, True)
#         self.assertEqual(checkUS11(),
#                          "Anomaly US11: Family F600000017840325486 has multiple wives.\n")
#         f.close()

class TestUS12(unittest.TestCase):
    def testGoodAges(self):
        f = open('./TestFiles/valid.ged', 'r')
        parseFile(f, True)
        self.assertEqual(checkUS12(), "", "Should print no errors")
        f.close()

    def testBadMotherAge(self):
        f = open('./TestFiles/US12/us12test2_input.ged', 'r')
        parseFile(f, True)
        self.assertEqual(checkUS12(),
                         "Error US12: Mother Sarah Alanson (I6000000178401456922) is 1000 years older than her child, Billy Alanson (I6000000178403660843).\n")
        f.close()
    def testBadFatherAge(self):
        f = open('./TestFiles/US12/us12test3_input.ged', 'r')
        parseFile(f, True)
        self.assertEqual(checkUS12(),
                         "Error US12: Father Julius Lexus (I6000000178403393861) is 973 years older than his child, Winter Thomas (I6000000178403503840).\n")
        f.close()
    def testBadBothAge(self):
        self.maxDiff = None
        f = open('./TestFiles/US12/us12test4_input.ged', 'r')
        parseFile(f, True)
        self.assertEqual(checkUS12(),
                         "Error US12: Mother Winter Thomas (I6000000178403503840) is 995 years older than her child, Elijah Thomas (I6000000178400484002).\nError US12: Father Ned Thomas (I6000000178403862823) is 995 years older than his child, Elijah Thomas (I6000000178400484002).\n")
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
class TestUS14(unittest.TestCase):
    def testGoodInput(self):
        f = open('./TestFiles/valid.ged', 'r')
        parseFile(f, True)
        self.assertEqual(checkUS14(), "", "Should print no errors")
        f.close()

    def testMoreThan5Births(self):
        f = open('./TestFiles/US14/us14test2_input.ged', 'r')
        parseFile(f, True)
        self.assertEqual(checkUS14(),
                         "Anomaly US14: Family F6000000178403254865 has 7 children born on the same day.\n")
        f.close()

class TestUS16(unittest.TestCase):
    def testMaleNames(self):
        f = open('./TestFiles/US16/us16test2_input.ged', 'r')
        parseFile(f, True)
        self.assertEqual(checkUS16(),
                         "Error US16: August Thomas is not as same as their father's last name Elijah John .\nError US16: Elijah John is not as same as their father's last name Ned Thomas .\n")
        f.close()

class TestUS17(unittest.TestCase):
    def testMarriageDescendants(self):
        f = open('./TestFiles/US17/us17test2_input.ged', 'r')
        parseFile(f, True)
        self.assertEqual(checkUS17(),
                         "Error US17: Jennifer Thomas  is married to the descendant Elijah Thomas .\n")
        f.close()

class TestUS18(unittest.TestCase):
    def testGoodMarriages(self):
        f = open('./TestFiles/valid.ged', 'r')
        parseFile(f, True)
        self.assertEqual(checkUS22("", 0), "", "Should print no errors")
        f.close()

    def testBadMarriage(self):
        f = open('./TestFiles/US18/us18test2_input.ged', 'r')
        parseFile(f, True)
        self.assertEqual(checkUS18(),
                         "Error US18: August Thomas (I3634834) married his sibling, April Thomas (I3254861).\n")
        f.close()

class TestUS19(unittest.TestCase):
    def testGoodInput(self):
        f = open('./TestFiles/valid.ged', 'r')
        parseFile(f, True)
        self.assertEqual(checkUS19(), "", "Should print no errors")
        f.close()
    def testCousinMarriage(self):
        f = open('./TestFiles/US19/us19test2_input.ged', 'r')
        parseFile(f, True)
        self.assertEqual(checkUS19(), "Error US19: Ron Swanson (I0576) married his cousin, Diane Someone (I0618).\n", "Should print error with Ron first.")
        f.close()

class TestUS20(unittest.TestCase):
    def testGoodInput(self):
        f = open('./TestFiles/valid.ged', 'r')
        parseFile(f, True)
        self.assertEqual(checkUS20(), "", "Should print no errors")
        f.close()
    def testOneBadMarriage(self):
        f = open('./TestFiles/US20/us20test2_input.ged', 'r')
        parseFile(f, True)
        self.assertEqual(checkUS20(), "Error US20: Ann Perkins (I0572) married her nephew, Chris Traeger (I0617).\n", "Should print one error.")
        f.close()
    def testManyBadMarriages(self):
        f = open('./TestFiles/US20/us20test3_input.ged', 'r')
        parseFile(f, True)
        self.assertEqual(checkUS20(), "Error US20: Ann Perkins (I0572) married her nephew, Chris Traeger (I0617).\nError US20: Diane Someone (I0618) married her nephew, Ron Swanson (I0576).\nError US20: Fairway Frank (I0574) married her nephew, Champion Dwyer (I0600).\n", "Should print three errors.")
        f.close()

class TestUS21(unittest.TestCase):
    def testGoodInput(self):
        f = open('./TestFiles/valid.ged', 'r')
        parseFile(f, True)
        self.assertEqual(checkUS21(), "", "Should print no errors")
        f.close()
    def testWrongGenderHusb(self):
        f = open('./TestFiles/US21/us21test2_input.ged', 'r')
        parseFile(f, True)
        self.assertEqual(checkUS21(), "Error US21: Husband Elijah Thomas (I6000000178400484002) is assigned the wrong gender for role.\n", "Should print one error.")
        f.close()
    def testWrongGenderWife(self):
        f = open('./TestFiles/US21/us21test3_input.ged', 'r')
        parseFile(f, True)
        self.assertEqual(checkUS21(), "Error US21: Wife Jennifer Thomas (I6000000178403254861) is assigned the wrong gender for role.\n", "Should print one error.")
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
        self.assertEqual(test1 + test2,
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

class TestUS23(unittest.TestCase):
    def testGoodInput(self):
        f = open('./TestFiles/valid.ged', 'r')
        parseFile(f, True)
        self.assertEqual(checkUS23(), "", "Should print no errors")
        f.close()
    def testSameName(self):
        f = open('./TestFiles/US23/us23test2_input.ged', 'r')
        parseFile(f, True)
        self.assertEqual(checkUS23(), "", "Should print no errors")
        f.close()
    def testBirthday(self):
        f = open('./TestFiles/US23/us23test3_input.ged', 'r')
        parseFile(f, True)
        self.assertEqual(checkUS23(), "", "Should print no errors")
        f.close()     
    def testError(self):
        f = open('./TestFiles/US23/us23test4_input.ged', 'r')
        parseFile(f, True)
        self.assertEqual(checkUS23(), "Error US23: Elijah Thomas appears in the file multiple times.\n", "Should print one error.")
        f.close()

class TestUS24(unittest.TestCase):
    def testSimilarHusbName(self):
        f = open('./TestFiles/US24/us24test3_input.ged', 'r')
        parseFile(f, True)
        self.assertEqual(checkUS24(), "", "Should print no errors")
        f.close()
    def testSimilarWifeName(self):
        f = open('./TestFiles/US24/us24test3_input.ged', 'r')
        parseFile(f, True)
        self.assertEqual(checkUS24(), "", "Should print no errors")
        f.close()
    def testError(self):
        f = open('./TestFiles/US24/us24test2_input.ged', 'r')
        parseFile(f, True)
        self.assertEqual(checkUS24(), "Error US24: I02319, I0417 with marriage date 2014-12-12 appears in the multiple families.\n")
        f.close()

class TestUS25(unittest.TestCase):
    def testSimilarName(self):
        f = open('./TestFiles/US25/us25test3_input.ged', 'r')
        parseFile(f, True)
        self.assertEqual(checkUS25(), "", "Should print no errors")
        f.close()
    def testSimilarBirthDate(self):
        f = open('./TestFiles/US25/us25test3_input.ged', 'r')
        parseFile(f, True)
        self.assertEqual(checkUS25(), "", "Should print no errors")
        f.close()
    def testError(self):
        f = open('./TestFiles/US25/us25test2_input.ged', 'r')
        parseFile(f, True)
        self.assertEqual(checkUS25(), "Error US25: April Thomas and 2021-01-17 appears in the file multiple times.\n")
        f.close()
class TestUS26(unittest.TestCase):
    def testGoodInput(self):
        f = open('./TestFiles/US26/us26test1_input.ged', 'r')
        parseFile(f, True)
        self.assertEqual(checkUS26(), "", "Should print no errors")
        f.close()

    def testInFamNotIndi(self):
        f = open('./TestFiles/US26/us26test2_input.ged', 'r')
        parseFile(f, True)
        self.assertEqual(checkUS26(), "Error US26: Child I0576 is not properly in the individuals records.\nError US26: Husband I0576 is not properly in the individuals records.\n", "Should print 2 errors")
        f.close()

    def testInIndiNotFam(self):
        f = open('./TestFiles/US26/us26test3_input.ged', 'r')
        parseFile(f, True)
        self.assertEqual(checkUS26(), "Error US26: Husband I02319 is not properly in the individuals records.\nError US26: Spouse Ron Swanson (I0576) is not properly in the families records.\nError US26: Child Ron Swanson (I0576) is not properly in the families records.\n", "Should print 3 errors")
        f.close()

class TestUS27(unittest.TestCase):
    def testAlivePerson(self):
        self.assertEqual(checkUS27(2000,2,17,True,0,0,0), 21)

    def testDeadPerson(self):
        self.assertEqual(checkUS27(1905,1,1,False,1986,7,4), 81)

class TestUS28(unittest.TestCase):
    ''' Test printing children in order of age '''
    def testOneChild(self):
        '''Make sure that one child still prints properly '''
        f = open('./TestFiles/valid.ged', 'r')
        parseFile(f, True)
        self.assertEqual(US28(['I6000000178403660843']), "{'I6000000178403660843'}", 'Should print one child ID')
        f.close()
    def testNoChildren(self):
        ''' Test that no children still prints properly '''
        self.assertEqual(US28([]), "NA", 'Should print "NA"')
    def testMultipleChildren(self):
        ''' Test that children print in order of birth date '''
        f = open('./TestFiles/US26/us26test3_input.ged', 'r')
        parseFile(f, True)
        self.assertEqual(US28(['I0600', 'I0617', 'I0618']), "{'I0617', 'I0618', 'I0600'}", 'Should print 3 children in order of birth')
        f.close()

class TestUS31(unittest.TestCase):
    ''' Test orphan printing '''
    def testNoSingles(self):
        '''Test that no singles are found.'''
        f = open('./TestFiles/US31/us31test2_input.ged', 'r')
        parseFile(f, True)
        self.assertEqual(checkUS31(), '', 'Should print nothing as there were no singles.')
        f.close()
    def testSingles(self):
        '''Test that there are singles found.'''
        f = open('./TestFiles/US31/us31test3_input.ged', 'r')
        parseFile(f, True)
        self.assertEqual(checkUS31(), 'US31: September Thomas has never married.\n', 'Should print singles.')
        f.close()

class TestUS32(unittest.TestCase):
    ''' Test orphan printing '''
    def testNoMulBirth(self):
        '''Test that no singles are found.'''
        f = open('./TestFiles/US32/us32test2_input.ged', 'r')
        parseFile(f, True)
        self.assertEqual(checkUS32(), '', 'Should print nothing as there were no multiple births.')
        f.close()
    def testMulBirth(self):
        '''Test that there are singles found.'''
        f = open('./TestFiles/US32/us32test3_input.ged', 'r')
        parseFile(f, True)
        self.assertEqual(checkUS32(), 'US32: 2021-01-17 is a multiple birth date.\n', 'should print multiple birth dates.')
        f.close()

class TestUS30(unittest.TestCase):
    ''' Test living married listing '''
    def testNoLivingMarried(self):
        '''Tests when there are no living married'''
        f = open('./TestFiles/US30/US30test1_input.ged', 'r')
        parseFile(f, True)
        self.assertEqual(checkUS30(), '', 'Should print no living married.')
        f.close()

    def testOneLivingMarried(self):
        '''Tests one living married'''
        f = open('./TestFiles/US30/US30test2_input.ged', 'r')
        parseFile(f, True)
        self.assertEqual(checkUS30(), 'US30: Elijah Thomas (I6000000178400484002) is married in family F6000000178403254865 and living.\n', 'Should print one living married.')
        f.close()

    def testMultipleLivingMarried(self):
        '''Tests multiple deceased'''
        f = open('./TestFiles/valid.ged', 'r')
        parseFile(f, True)
        self.assertEqual(checkUS30(), 'US30: Elijah Thomas (I6000000178400484002) is married in family F6000000178403254865 and living.\nUS30: Jennifer Thomas (I6000000178403254861) is married in family F6000000178403254865 and living.\nUS30: Winter Thomas (I6000000178403503840) is married in family F6000000178403503845 and living.\nUS30: Ned Thomas (I6000000178403862823) is married in family F6000000178403503845 and living.\nUS30: Lloyd Alanson (I6000000178401748954) is married in family F6000000178401748958 and living.\nUS30: Lloyd Alanson (I6000000178401748954) is married in family F6000000178403660847 and living.\n', 'Should print six living married.')
        f.close()

class TestUS33(unittest.TestCase):
    ''' Test orphan printing '''
    def testNoOrphans(self):
        '''Test that no false orphans are found.'''
        f = open('./TestFiles/valid.ged', 'r')
        parseFile(f, True)
        self.assertEqual(checkUS33(), '', 'Should print no orphans.')
        f.close()
    
    def testOneOrphan(self):
        '''Test that one orphan is printed.'''
        f = open('./TestFiles/US33/US33test3_input.ged', 'r')
        parseFile(f, True)
        self.assertEqual(checkUS33(), 'US33: Baby Perkins (I0700) is an orphan.\n', 'Should print one orphan.')
        f.close()

    def testMultipleOrphans(self):
        '''Test that multiple orphans can be found.'''
        f = open('./TestFiles/US33/US33test2_input.ged', 'r')
        parseFile(f, True)
        self.assertEqual(checkUS33(), 'US33: April Thomas (I6000000178401304897) is an orphan.\nUS33: August Thomas (I6000000178403634834) is an orphan.\nUS33: September Thomas (I6000000178401782906) is an orphan.\n', 'Should print multiple orphan names.')
        f.close()

class testUS34(unittest.TestCase):
    def testNoLargeDifs(self):
        f = open('./TestFiles/valid.ged', 'r')
        parseFile(f, True)
        self.assertEqual(checkUS33(), '', 'Should print no orphans.')
        f.close()
    def testLargeDifs(self):
        f = open('./TestFiles/US34/US34test2_input.ged', 'r')
        parseFile(f, True)
        self.assertEqual(checkUS34(), "US34: Husband Ben Wyatt (I02319), age 121 is more than twice as old as his wife Leslie Knope (I0417), age 19.\n")
        f.close()
    def testExactlyDouble(self):
        f = open('./TestFiles/US34/US34test3_input.ged', 'r')
        parseFile(f, True)
        self.assertEqual(checkUS34(), "")
        f.close()

class testUS35(unittest.TestCase):
    def testNoRecentBirths(self):
        f = open('./TestFiles/valid.ged', 'r')
        parseFile(f, True)
        self.assertEqual(checkUS33(), '', 'Should print no orphans.')
        f.close()
    def testRecentBirths(self):
        f = open('./TestFiles/US35/US35test2_input.ged', 'r')
        parseFile(f, True)
        self.assertEqual(checkUS35(), "US35: Leslie Knope (I0417) is less than 30 days old.\n")
        f.close()

if __name__ == "__main__":
    # run all the tests
    unittest.main()