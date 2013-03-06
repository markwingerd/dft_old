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
from util import XmlRetrieval


class Module:
	def __init__(self, skills, mod_name):
		self.stats = {}
		self.name = mod_name
		self.skills = skills

		module_data = XmlRetrieval('module.xml')
		self.parent, properties, effecting_skills = module_data.get_target(mod_name)
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

	def get_stat(self, stat_name, precision=1):
		return round(self.stats[stat_name], precision)

	def get_information(self):
		""" Returns a list of stats needed for output. """
		return (self.name, self.get_bestest_stats())

	def get_bestest_stats(self):
		""" Returns the most valuable stats depending on what item this is. """
		output = []
		if self.parent == 'nanite_injector':
			output.append( ('Revive Armor:', self.get_stat('armor_repaired_on_revive')) )
		elif self.parent == 'repair_tool':
			output.append( ('Dropsuit:', self.get_stat('repair_rate_on_dropsuit')) )
			output.append( ('Vehicle:', self.get_stat('repair_rate_on_vehicle')) )
			output.append( ('Range:', self.get_stat('max_repair_distance')) )
			output.append( ('Targets:', self.get_stat('max_targets', 0)) )
		elif self.parent == 'nanohive':
			output.append( ('Resupply:', self.get_stat('max_nanite_clusters')) )
			output.append( ('Rate:', self.get_stat('ammo_resupply_rate')) )
			output.append( ('Max Active:', self.get_stat('max_active', 0)) )
			output.append( ('Max Carried:', self.get_stat('max_carried', 0)) )
			output.append( ('Range', self.get_stat('effective_range')) )
		elif self.parent == 'drop_uplink':
			output.append( ('Max Spawns:', self.get_stat('max_spawns_per_unit', 0)) )
			output.append( ('Spawn Time:', self.get_stat('spawn_time_modifier')) )
			output.append( ('Max Active:', self.get_stat('max_active', 0)) )
			output.append( ('Max Carried:', self.get_stat('max_carried', 0)) )
		elif self.parent == 'remote_explosives':
			if 'Remote' in self.name:
				detonated_by = 'Trigger:'
			else:
				detonated_by = 'Vehicle:'
			output.append( ('Radius:', self.get_stat('blast_radius')) )
			output.append( ('Detonated:', detonated_by) )
			output.append( ('Max Active:', self.get_stat('max_active', 0)) )
			output.append( ('Max Carried:', self.get_stat('max_carried', 0)) )
		return output

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
				self.stats[key] = round(properties[key] * (1 + mod), 3)
			else:
				self.stats[key] = properties[key]


class Weapon(Module):
	""" Req dropsuit and fitting to test properly. """
	def __init__(self, skills, weapon_name, module_list=[]):
		self.stats = {}
		self.name = weapon_name
		self.skills = skills
		self.module_list = module_list

		weapon_data = XmlRetrieval('weapon.xml')
		self.parent, properties, effecting_skills = weapon_data.get_target(weapon_name)
		self._add_stats(properties,effecting_skills)
		self._add_module_bonus()

	def get_stat(self, stat_name, precision=1):
		return round(self.stats[stat_name], precision)

	def get_information(self):
		""" Returns a list of stats needed for output. """
		return self.get_bestest_stats()

	def get_bestest_stats(self):
		""" Returns the most valuable stats depending on what item this is. """
		output = []
		if self.parent == 'assault_rifles':
			output.append( ('Damage:', self.get_stat('damage')) )
			output.append( ('Rof:', self.get_stat('rate_of_fire')) )
			output.append( ('Optimal:', self.get_stat('optimal_range_high')) )
			output.append( ('Max Range:', self.get_stat('max_range')) )
			output.append( ('Magazine:', self.get_stat('clip_size')) )
			output.append( ('Max Ammo:', self.get_stat('max_ammo')) )
		elif self.parent == 'forge_guns':
			rof = round(60/self.get_stat('charge-up_time'), 1)
			output.append( ('Damage:', self.get_stat('direct_damage')) )
			output.append( ('Rof:', rof) )
			output.append( ('Magazine:', self.get_stat('clip_size')) )
			output.append( ('Charge Time:', self.get_stat('charge-up_time')) )
			output.append( ('Spash Damage:', self.get_stat('splash_damage')) )
			output.append( ('Blast Radius:', self.get_stat('blast_radius')) )
		elif self.parent == 'heavy_machine_guns':
			dps = round(self.get_stat('damage')*(self.get_stat('rate_of_fire')/60), 1)
			tto = round(100/self.get_stat('heat_build-up_per_second'), 1)
			output.append( ('Damage:', self.get_stat('damage')) )
			output.append( ('Rof:', self.get_stat('rate_of_fire')) )
			output.append( ('Dps:', dps) )
			output.append( ('Time to Overheat:', tto) )
			output.append( ('Optimal:', self.get_stat('optimal_range_high')) )
			output.append( ('Max Range:', self.get_stat('max_range')) )
		elif self.parent == 'submachine_guns':
			output.append( ('Damage:', self.get_stat('damage')) )
			output.append( ('Rof:', self.get_stat('rate_of_fire')) )
			output.append( ('Optimal:', self.get_stat('optimal_range_high')) )
			output.append( ('Max Range:', self.get_stat('max_range')) )
			output.append( ('Magazine:', self.get_stat('clip_size')) )
			output.append( ('Max Ammo:', self.get_stat('max_ammo')) )
		elif self.parent == 'shotguns':
			output.append( ('Damage:', self.get_stat('damage')) )
			output.append( ('Rof:', self.get_stat('rate_of_fire')) )
			output.append( ('Optimal:', self.get_stat('optimal_range_high')) )
			output.append( ('Max Range:', self.get_stat('max_range')) )
			output.append( ('Shots:', self.get_stat('clip_size')) )
			output.append( ('Reload Time:', self.get_stat('reload_time')) )
		elif self.parent == 'laser_rifles':
			output.append( ('Damage:', self.get_stat('damage')) )
			output.append( ('Rof:', self.get_stat('rate_of_fire')) )
			output.append( ('Optimal Low:', self.get_stat('optimal_range_low')) )
			output.append( ('Optimal High:', self.get_stat('optimal_range_high')) )
			output.append( ('Max Range:', self.get_stat('max_range')) )
		elif self.parent == 'sniper_rifles':
			output.append( ('Damage:', self.get_stat('damage')) )
			output.append( ('Rof:', self.get_stat('rate_of_fire')) )
			output.append( ('Magazine:', self.get_stat('clip_size')) )
			output.append( ('Max Ammo:', self.get_stat('max_ammo')) )
		elif self.parent == 'grenades':
			if 'Locus' in self.name:
				output.append( ('Damage:', self.get_stat('splash_damage')) )
				output.append( ('Radius:', self.get_stat('blast_radius')) )
			elif 'AV' in self.name:
				output.append( ('Damage:', self.get_stat('splash_damage')) )
				output.append( ('Targets:', 'Vehicles') )
			elif 'Flux' in self.name:
				pass
		return output

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
		self.module_data = XmlRetrieval('module.xml')

		self.names = self.module_data.get_list()

	def get_names(self):
		""" Returns module names as a tuple. """
		return tuple(self.names)

	def get_parents(self):
		return self.module_data.get_parents()

	def get_children(self, parent):
		return self.module_data.get_children(parent)
			

class WeaponLibrary(ModuleLibrary):
	def __init__(self):
		self.weapon_data = XmlRetrieval('weapon.xml')

		self.names = self.weapon_data.get_list()

	def get_parents(self):
		return self.weapon_data.get_parents()

	def get_children(self, parent):
		return self.weapon_data.get_children(parent)


if __name__ == '__main__':
	modlib = ModuleLibrary()
	print modlib.get_parents()
	print modlib.get_children('shields')