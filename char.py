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
		self.skills = Skills()
		self.skill_level = {} # Used for module reqs
		self.skill_effect = {} # Used for modifying modules

	def show_skills(self):
		print self.skill_level

	def set_skill(self, skill, level):
		self.skill_level[skill] = level
		self.skill_effect[skill] = level * self.skills.skill_effect[skill]

	def get_all_skills(self):
		""" Returns a dictionary of all known skills and the characters skill
		levels. """
		output = {}
		# Gets all known skills and if Character has a level for them, apply it.
		for s in self.skills.get_names():
			if s in self.skill_level:
				output[s] = self.skill_level[s]
			else:
				output[s] = 0
		return output


class CharacterLibrary:
	def __init__(self):
		self.character_data = DataRetrieval('characters.dat')

		self.character_list = self.character_data.data
		#self._load_characters('characters.dat')

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


class Skills:
	def __init__(self):
		# Dict of skills and their effects on stats {Skill_Name: Effect}
		self.skill_effect = {}
		
		# THIS STILL USES THE OLDER VERSION TO RETRIEVE XML.... ITS TOO
		# DIFFERENT TO USE THE OTHER SHIT. FUCK. IL FIX IT LATER
		self._get_xml(self._get_file_loc('skills.xml'))

	def show_skills(self):
		print self.skill_effect

	def get_names(self):
		""" Returns a tuple of skill names. """
		return tuple(self.skill_effect.keys())

	def _get_file_loc(self, file_name):
		""" Will return the path to the desired file depending on whether this
		is an executable or in development. """
		if getattr(sys, 'frozen', None):
			basedir = sys._MEIPASS + '/data/'
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


if __name__ == '__main__':
	pass
	#char1 = Character('Char1')
	#char1.set_skill('Shield Control',2)
	#char1.set_skill('Field Mechanics',4)
	#char2 = Character('Char2')
	#char2.set_skill('Weaponry',5)
	#char2.set_skill('Dropsuit Command',4)
	#char3 = Character('Char3')
	#char3.set_skill('Weaponry',5)
	#char3.set_skill('Dropsuit Command',4)

	char_lib = CharacterLibrary()	
	#char_lib.save_character(char3)
	print char_lib.get_character_list()
	char = char_lib.get_character('Reimus Klinsman')
	print char.get_all_skills()

	#sk = Skills()
	#print sk.skill_effect