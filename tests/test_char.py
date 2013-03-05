#!/usr/bin/env python
# Unittests for the char module


import sys
import unittest

from dft.char import Character, InvalidSkillException


class TestCharacter(unittest.TestCase):
    """ Tests for the Character Class """

    def test_instantiation(self):
        """Test we can instiantiate the Character class"""
        my_char = Character(None)
        # This simple test just checks that my_char is an object
        # and the instantiation didn't error
        self.assertTrue(my_char)

    def test_character_name(self):
        """Test we can instiantiate the Character class with a name"""
        my_char = Character('Bob')
        self.assertEqual('Bob', my_char.name)


class TestCharacterSkills(unittest.TestCase):
    """ Tests for Skills in the Character Class """

    def setUp(self):
        """Set up environment and attributes used in all tests
           in this test case"""
        self.test_char = Character('test character')

    def test_character_set_skill_level(self):
        """ Test setting a skill level """
        skill_name = 'Dropsuit Command'
        skill_level = 1

        self.test_char.set_skill(skill_name, skill_level)

        self.assertEqual(self.test_char.skill_level[skill_name], skill_level)

    def test_character_set_invalid_skill(self):
        """ Test setting an invalid skill.
            Should raise an InvalidSkillException"""
        skill_name = 'I dont exist'
        skill_level = 1

        with self.assertRaises(InvalidSkillException):
            self.test_char.set_skill(skill_name, skill_level)




if __name__=='__main__':
    unittest.main()