#!/usr/bin/env python
# Unittests for the char module

import sys
import unittest
# Mock module required "pip install mock"
from mock import patch

try:
    from char import (
        Character,
        CharacterLibrary,
        InvalidSkillException,
        InvalidCharacterException
        )
except ImportError:
    print "Please place the 'dft' directory on the PYTHONPATH"
    sys.exit(1)


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
            If the skill doesn't exist then we would expect
            an InvalidSkillException raised"""
        skill_name = 'I dont exist'
        skill_level = 1

        with self.assertRaises(InvalidSkillException):
            self.test_char.set_skill(skill_name, skill_level)

    def test_character_get_skill_level(self):
        """ Get the skill level for a skill """
        skill_name = 'Dropsuit Command'
        skill_level = 1

        # first we set the skill
        self.test_char.set_skill(skill_name, skill_level)

        # then we make our call to get_skill_level to test it
        self.assertEqual(self.test_char.get_skill_level(skill_name), skill_level)

    def test_character_get_unknown_skill_level(self):
        """ Get the skill level for an unknown skill
            It is possible to request a skill thats not
            saved against the character and it should return 0"""
        skill_name = 'I dont exist'
        skill_level = 0

        # Any skill that doesn't exist on this character
        # should return 0
        self.assertEqual(self.test_char.get_skill_level(skill_name), skill_level)

    @patch("char.Skills.get_names")
    def test_get_all_skills(self, get_names):
        """ Test the get_all_skills method of Character
            For this test we will overwrite the list of skills
            with a mock object so that we can test all skills
            are returned. Otherwise as soon as we add a new skill
            to the data this test would break... incorrectly"""
        # this is our fake return from any call to get_names
        get_names.return_value = ['test skill 1',
                                  'test skill 2',
                                  'test skill 3']
        # Set up the expected skill values
        self.test_char.skill_level['test skill 1']=1
        self.test_char.skill_level['test skill 2']=2
        self.test_char.skill_level['test skill 3']=3

        # The is the result we expect to get back
        expected_skills = {'test skill 1': 1,
                           'test skill 2': 2,
                           'test skill 3': 3}

        self.assertEqual(self.test_char.get_all_skills(),
                         expected_skills)

    @patch("char.Skills.get_names")
    def test_get_all_skills_default(self, get_names):
        """ Test the get_all_skills method of Character
            and give the default of 0 if the skill doesn't exist
            on that character.
            For this test we will overwrite the list of skills
            with a mock object so that we can test all skills
            are returned. Otherwise as soon as we add a new skill
            to the data this test would break... incorrectly"""
        # this is our fake return from any call to get_names
        get_names.return_value = ['test skill 1',
                                  'test skill 2',
                                  'test skill 3']
        # We don't set up any default values

        # The is the result we expect to get back
        expected_skills = {'test skill 1': 0,
                           'test skill 2': 0,
                           'test skill 3': 0}

        self.assertEqual(self.test_char.get_all_skills(),
                         expected_skills)


class TestCharacterLibrary(unittest.TestCase):
    """ Tests for the CharacterLibrary Class """

    def test_instantiation(self):
        """Instantiation of the class"""
        # Just tests that it doesn't raise any Exceptions
        char_library = CharacterLibrary()

class TestCharacterLibraryGet(unittest.TestCase):
    """ Tests for the CharacterLibrary Classes Get method """

    def setUp(self):
        """Create our Character and CharacterLibrary test data"""
        self.char_library = CharacterLibrary()
        # overwrite the data in the library to something
        # we can test
        self.char_name = 'Bob'
        self.test_char = Character(self.char_name)
        self.char_library.character_list = {self.test_char.name: self.test_char}

    def test_get_character(self):
        """Get a character out of the library"""
        # now get the character from the library and assert that it
        # is our character
        returned_char = self.char_library.get_character(self.char_name)
        self.assertEqual(self.test_char, returned_char)

    def test_get_character_not_exist(self):
        """Try to get a character from the library that doesn't exist"""
        # We try to get a character by name that doesn't exist in the library
        # This should raise an InvalidCharacterException
        with self.assertRaises(InvalidCharacterException):
            returned_char = self.char_library.get_character("i dont exist")


class TestCharacterLibraryGetList(unittest.TestCase):
    """ Tests for the CharacterLibrary Classes Get_character_list method """

    def setUp(self):
        """Create our Character and CharacterLibrary test data"""
        self.char_library = CharacterLibrary()
        # overwrite the data in the library to something
        # we can test
        self.char_names = ['Bob', 'Fish', 'Wibble']
        self.char_library.character_list = {}

        # Loop creating all the chars in the char_names list
        for char_name in self.char_names:
            test_char = Character(char_name)
            self.char_library.character_list[test_char.name] = test_char

    def test_get_character_list(self):
        """Get the character list from the library"""
        # Check that we get all of the characters we are expecting
        char_list = self.char_library.get_character_list()
        # Returns a tuple not a list
        self.assertEqual(tuple(self.char_names), char_list)


if __name__=='__main__':
    unittest.main()