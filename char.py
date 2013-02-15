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

class Character:
	def __init__(self, name):
		self.name = name
		self.skills = Skills()
		self.skill_level = {} # Used for module reqs
		self.skill_effect = {} # Used for modifying modules

	def show_skills(self):
		print self.skill_level

	def set_skill(self, skill, level):
		self.skill_level[skill] = level
		self.skill_effect[skill] = level * self.skills.skill_effect[skill]


class CharacterLibrary:
	def __init__(self):
		self.character_list = {}

		self._load_characters('characters.dat')

	def get_character(self, char_name):
		""" Returns a the specified character instance. """
		for char in self.character_list:
			if char_name == char.name:
				#print char_name
				pass

	def get_character_list(self):
		""" Returns a list of the names of all characters. """
		return self.character_list.keys()

	def save_character(self, character):
		""" Will save all the character classes. """
		self.character_list[character.name] = character

		char_file = open(self._get_file_loc('characters.dat'), 'wb')
		pickle.dump(self.character_list, char_file)
		char_file.close()

	def _load_characters(self, src_file):
		""" Loads all characters from file and passes them into the
		character_list """
		try:
			char_file = open(self._get_file_loc('characters.dat'), 'rb')
			self.character_list = character = pickle.load(char_file)
		except IOError:
			print 'No character file found.'

	def _get_file_loc(self, file_name):
		""" Will return the path to the desired file depending on whether this
		is an executable or in development. """
		if getattr(sys, 'frozen', None):
			basedir = sys._MEIPASS
		else:
			basedir = os.path.dirname('data/')
		return os.path.join(basedir, file_name)


class Skills:
	def __init__(self):
		# Dict of skills and their effects on stats {Skill_Name: Effect}
		self.skill_effect = {}
		self._get_xml(self._get_file_loc('skills.xml'))

	def show_skills(self):
		for s in self.skill_list:
			print '%s: %s' % (s, self.skill_effect[s])
		print self.skill_modifies

	def get_modifier_name(self, modifies):
		return self.skill_modifies[modifies]

	def _get_file_loc(self, file_name):
		""" Will return the path to the desired file depending on whether this
		is an executable or in development. """
		if getattr(sys, 'frozen', None):
			basedir = sys._MEIPASS
		else:
			basedir = os.path.dirname('data/')
		return os.path.join(basedir, file_name)

	def _get_xml(self, src):
		""" Extracts skill information from an xml file. """
		xml_tree = ET.parse(src)
		xml_root = xml_tree.getroot()

		for skill in xml_root.findall('skill'):
			name = skill.get('name')
			effect = round(float(skill.find('effect').text), 3)
			self.skill_effect[name] = effect


class SkillsLibrary:
	def __init__(self):
		self.name = []

		self._get_xml('data/skills.xml')


	def _get_xml(self, src):
		""" Finds all the names of every Skill in the xml file. """
		xml_tree = ET.parse(src)

		for child in xml_tree.getroot():
			self.name.append(child.get('name'))

if __name__ == '__main__':
	char1 = Character('Char1')
	char1.set_skill('Shield Control',2)
	char1.set_skill('Field Mechanics',4)
	char2 = Character('Char2')
	char2.set_skill('Weaponry',5)
	char2.set_skill('Dropsuit Command',4)

	char_lib = CharacterLibrary()
	char_lib.save_character(char1)
	char_lib.save_character(char2)
	print char_lib.get_character_list()