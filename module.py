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
import xml.etree.ElementTree as ET
import math

from char import Character


class Module:
	def __init__(self, skills, mod_name):
		self.stats = {}
		self.name = mod_name
		self.skills = skills

		properties, effecting_skills = self._get_xml(self._get_file_loc('module.xml'))
		self._add_stats(properties,effecting_skills)

	def show_stats(self):
		print self.name
		for key in self.stats:
			print '{:<20} {:<15}'.format(key, self.stats[key])

	def get(self, stat):
		if stat in self.stats:
			return self.stats[stat]
		else:
			return None

	def _add_stats(self, properties, effecting_skills):
		""" Uses the properties list and effecting_skills list to populate
		the stats dictionary with all appropriate values. 
		THIS ALSO HANDLES SKILL BONUSES! """

		def _get_skill_modifier(skill_list):
			output = 0
			for name in skill_list:
				try:
					output = output + self.skills[name]
				except KeyError:
					# Skill is not in self.skills
					pass
			return output

		for key in properties:
			if key in effecting_skills.keys():
				# Skills effect this property. Get and apply the skill modifier.
				skill_list = effecting_skills[key]
				mod = _get_skill_modifier(skill_list)
				self.stats[key] = math.floor(properties[key] * (1 + mod))
			else:
				self.stats[key] = properties[key]

	def _get_file_loc(self, file_name):
		""" Will return the path to the desired file depending on whether this
		is an executable or in development. """
		if getattr(sys, 'frozen', None):
			basedir = sys._MEIPASS
		else:
			basedir = os.path.dirname('data/')
		return os.path.join(basedir, file_name)

	def _get_xml(self,src):
		def is_number(s):
			""" Checks if a string is a number. """
			try:
				float(s)
				return True
			except ValueError:
				return False

		xml_tree = ET.parse(src)
		# Finds the desired target in xml file
		for child in xml_tree.getroot():
			if child.attrib['name'] == self.name:
				target = child
				break
		# Create a dictionary of the targets properties and effecting skills.
		properties = {}
		effecting_skills = {}
		for prop in target:
			# Get any xml attributes and save them to a dict for later use.
			if 'effected_by' in prop.attrib.keys():
				effecting_skills[prop.tag] = prop.attrib.values()
			# Get the properties and convert them to a float if needed.
			if is_number(prop.text):
				properties[prop.tag] = round(float(prop.text), 3)
			else:
				properties[prop.tag] = prop.text

		# Returns the properties list and effecting_skills list as a tuple
		return (properties, effecting_skills)


class Weapon(Module):
	""" Req dropsuit and fitting to test properly. """
	def __init__(self, skills, weapon_name, module_list=[]):
		self.stats = {}
		self.name = weapon_name
		self.skills = skills
		self.module_list = module_list

		properties, effecting_skills = self._get_xml(self._get_file_loc('weapon.xml'))
		self._add_stats(properties,effecting_skills)
		self._add_module_bonus()

	def _add_module_bonus(self):
		""" Searching self.module_list for any modules which effect this 
		weapons slot type (found in the modules 'enhances' cell. If so, it will 
		add the bonuses for that module. 
		CURRENTLY ONLY WORKS FOR DAMAGE!!! """
		slot_type = self.stats['slot_type']
		for m in self.module_list:
			try:
				if slot_type == m.stats['enhances']:
					self.stats['damage'] = self.stats['damage'] * (1 + m.stats['damage'])
			except KeyError:
				# Module does not have a key 'enhances' in its stats dictionary.
				pass


class ModuleLibrary:
	def __init__(self):
		self.names = []

		self._get_xml(self._get_file_loc('module.xml'))

	def get_names(self):
		""" Returns module names as a tuple. """
		return tuple(self.names)

	def _get_file_loc(self, file_name):
		""" Will return the path to the desired file depending on whether this
		is an executable or in development. """
		if getattr(sys, 'frozen', None):
			basedir = sys._MEIPASS
		else:
			basedir = os.path.dirname('data/')
		return os.path.join(basedir, file_name)

	def _get_xml(self, src):
		""" Finds all the names of every module in the xml file. """
		xml_tree = ET.parse(src)

		for child in xml_tree.getroot():
			self.names.append(child.get('name'))
			

class WeaponLibrary(ModuleLibrary):
	def __init__(self):
		self.names = []

		self._get_xml(self._get_file_loc('weapon.xml'))


if __name__ == '__main__':
	r = Character()
	r.set_skill('Shield Enhancements',5)
	r.set_skill('Armor Upgrades',5)

	extender = Module(r.skill_effect, 'Complex Shield Extender')
	plate = Module(r.skill_effect, 'Complex Armor Plates')

	extender.show_stats()
	print '\n\n\n'
	plate.show_stats()

	modlib = ModuleLibrary()
	wealib = WeaponLibrary()
	print modlib.get_names()
	print wealib.get_names()