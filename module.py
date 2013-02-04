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

from char import Character

class Module:
	def __init__(self, skills, mod_name):
		self.attributes = []
		self.mod_name = None

		self._get_xml(skills, mod_name)

	def show_stats(self):
		print self.mod_name
		for attr in self.attributes:
			print '{:<20} {:<15}'.format(attr, getattr(self,attr))

	def get(self, stat):
		if hasattr(self, stat):
			return getattr(self, stat)
		else:
			return None

	def _get_xml(self, skills, mod_name):
		""" Extracts basic module values from an xml file using mod_name as 
		search parameters. """
		def _apply_stats(skills, item):
			skill_name = item.get('effected_by')
			try:
				mod = skills[skill_name]
			except KeyError: # Skill_name isn't in skills dictionary.
				mod = 0
			return float(item.text) * (1+mod)

		xml_tree = ET.parse('data/module.xml')
		xml_root = xml_tree.getroot()
		for mod in xml_root:
			if mod.attrib['mod_name'] == mod_name:
				break

		self.mod_name = mod.attrib['mod_name']

		for item in mod:
			try:
				if item.attrib:
					value = _apply_stats(skills, item)
				else:
					value = float(item.text)
			except ValueError: #Catches int(text) errors.
				value = item.text
			setattr(self, item.tag, value)
			self.attributes.append(item.tag)

if __name__ == '__main__':
	r = Character()
	r.set_skill('Shield Enhancements',5)
	r.set_skill('Armor Upgrades',5)

	extender = Module(r.skill_effect, 'Complex Shield Extender')
	plate = Module(r.skill_effect, 'Complex Armor Plates')

	extender.show_stats()
	print '\n\n\n'
	plate.show_stats()