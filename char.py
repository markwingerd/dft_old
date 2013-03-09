#!/usr/bin/env python
# connectionmon.py - Views your network connections.
# Copyright (C) 2013 Mark Wingerd <markwingerd@yahoo.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import sys, os
import pickle
import xml.etree.ElementTree as ET
from util import DataRetrieval

class Character:
    def __init__(self, name):
        self.name = name
        self.skill_dict = SkillLibrary().skill_dict
        self.leveled_skill_effects = {} # Used for modifying modules
        self.skillpoints_used = 0

    def set_skill(self, skill, level):
        self.skill_dict[skill].set_level(level)
        self.leveled_skill_effects[skill] = level * self.skill_dict[skill].effect
        # Recalculate how much skillpoints have been used on skills.
        self.skillpoints_used = 0
        for skill in self.skill_dict.values():
            self.skillpoints_used += skill.get_sp_used()
        print self.skillpoints_used

    def get_skill_level(self, skill_name):
        """ Returns the skill level. If none found in the self.skill_level dict
        then return 0 as the level. """
        if skill_name in self.skill_dict:
            return self.skill_dict[skill_name].level
        else:
            return 0

    def get_all_skills(self):
        """ Returns a dictionary of all known skills and the characters skill
        levels. """
        output = {}
        # Gets all known skills and if Character has a level for them, apply it.
        for skill_name, skill in self.skill_dict.iteritems():
            output[skill_name] = skill.level
        return output


class CharacterLibrary:
    def __init__(self):
        self.character_data = DataRetrieval('characters.dat')
        # If no characters.dat file exists then create default characters and
        # save them.
        if not self.character_data.data:
            self._create_default_characters()

        self.character_list = self.character_data.data

    def get_character(self, char_name):
        """ Returns a the specified character instance. """
        return self.character_list[char_name]

    def get_character_list(self):
        """ Returns a list of the names of all characters as a tuple. """
        return tuple(self.character_list.keys())

    def save_character(self, character):
        """ """
        self.character_data.save_data(character)

    def delete_character(self, character):
        self.character_data.delete_data(character)

    def _create_default_characters(self):
        """ Called when no character data has been found. This method will
        create a 'No Skills' character and a 'Max Skills' character.  Both
        default characters will be saved for future used. """
        no_skills = Character('No Skills')
        max_skills = Character('Max Skills')
        # Set all known skills to Lv5 for max_skills
        for skill_name in max_skills.skill_dict:
            max_skills.set_skill(skill_name, 5)

        # Save characters.
        self.save_character(no_skills)
        self.save_character(max_skills)


class Skill:
    def __init__(self, name, skill_category, effect, multiplier, prerequisites):
        self.name = name
        self.skill_category = skill_category
        self.effect = round(float(effect), 2)
        self.multiplier = int(multiplier)
        self.prerequisites = prerequisites
        self.level = 0

    def set_level(self, level):
        if 0 <= level <= 5:
            self.level = level

    def get_sp_used(self):
        """ Converts a skills multiplier into SP based on the level. """
        if self.level == 1:
            return 6220 * self.multiplier
        if self.level == 2:
            return 24870 * self.multiplier
        if self.level == 3:
            return 68400 * self.multiplier
        if self.level == 4:
            return 155460 * self.multiplier
        if self.level == 5:
            return 3109920 * self.multiplier
        else:
            return 0


class SkillLibrary:
    def __init__(self):
        self.skill_dict = {}
        self.file_name = self._get_file_loc('skills.xml')
        
        self._build_skills()

    def get_all_skill_categories(self):
        """ Returns a list of all parents in the xml file. """
        skill_categories = []

        for skill in self.skill_dict.values():
            if skill.skill_category not in skill_categories:
                skill_categories.append(skill.skill_category)

        return skill_categories

    def get_skill_by_category(self, category):
        """ Returns all the children of a given parent. """
        skills_by_category = []

        for skill in self.skill_dict.values():
            if category == skill.skill_category:
                skills_by_category.append(skill.name)

        return skills_by_category

    def _build_skills(self):
        """ Get a list of all data needed for every skill found in the
        skills.xml file and instantiates a skill class to hold the data. That
        object will be added to a dictionary of skills. """
        skill_data_list = self._get_xml()
        for name, skill_category, effect, multiplier, prereq in skill_data_list:
            self.skill_dict[name] = Skill(name, skill_category, effect, multiplier, prereq)

    def _get_file_loc(self, file_name):
        """ Will return the path to the desired file depending on whether this
        is an executable or in development. """
        if getattr(sys, 'frozen', None):
            basedir = sys._MEIPASS + '/data/'
        else:
            basedir = os.path.dirname('data/')
        return os.path.join(basedir, file_name)

    def _get_xml(self):
        """ Extracts skill information from an xml file. And returns that data
        as a list of tuples. """
        skill_data = []
         # THIS STILL USES THE OLDER VERSION TO RETRIEVE XML.... ITS TOO
        # DIFFERENT TO USE THE OTHER SHIT. FUCK. IL FIX IT LATER
        xml_tree = ET.parse(self.file_name)
        xml_root = xml_tree.getroot()

        for skill in xml_root.findall('.//skill'):
            name = skill.get('name')
            skill_category = xml_tree.find('.//*[@name="%s"]/..' % name).tag
            effect = round(float(skill.find('effect').text), 3)
            multiplier = int(skill.find('multiplier').text)
            prerequisites = []
            for prereq in skill.findall('./prerequisites/prerequisite'):
                prerequisites.append( (prereq.attrib['skill'], int(prereq.text)) )
            skill_data.append( (name, skill_category, effect, multiplier, prerequisites) )

        return skill_data


if __name__ == '__main__':
    char_lib = CharacterLibrary()
    print 'CHARACTER LIST: ', char_lib.get_character_list()
    char = char_lib.get_character('No Skills')
    print 'SHOW ALL SKILLS: ', char.get_all_skills()
    s = SkillLibrary()
    print 'SHOW PARENTS: ', s.get_all_skill_categories()
    print 'SHOW CHILDREN OF HWU: ', s.get_skill_by_category('handheld_weapon_upgrades')
    #print 'SHOW ALL MILTIPLIERS: ', s.skill_multiplier
    #sk = Skills()
    #print sk.skill_effect