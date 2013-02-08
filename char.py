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

import xml.etree.ElementTree as ET

class Character:
	def __init__(self):
		self.skills = Skills()
		self.skill_level = {} # Used for module reqs
		self.skill_effect = {} # Used for modifying modules

	def show_skills(self):
		print self.skill_level

	def set_skill(self, skill, level):
		self.skill_level[skill] = level
		self.skill_effect[skill] = level * self.skills.skill_effect[skill]



class Skills:
	def __init__(self):
		# Dict of skills and their effects on stats {Skill_Name: Effect}
		self.skill_effect = {}
		self._get_skill_info()

	def show_skills(self):
		for s in self.skill_list:
			print '%s: %s' % (s, self.skill_effect[s])
		print self.skill_modifies

	def get_modifier_name(self, modifies):
		return self.skill_modifies[modifies]


	def _get_skill_info(self):
		""" Extracts skill information from an xml file. """
		xml_tree = ET.parse('data/skills.xml')
		xml_root = xml_tree.getroot()

		for skill in xml_root.findall('skill'):
			name = skill.get('name')
			effect = float(skill.find('effect').text)
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
	char = Character()
	#char.skill_info.show_skills()
	char.set_skill('Shield Control',2)
	char.set_skill('Field Mechanics',4)
	print char.skill_effect

	skillslib = SkillsLibrary()
	print skillslib.name