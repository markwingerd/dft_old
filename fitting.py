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
from module import Module

class Fitting:
	def __init__(self, character, ds_type, ds_name):
		self.char = character
		self.dropsuit = Dropsuit(self.char.skill_effect, ds_type, ds_name)

		self.heavy_weapon = []
		self.light_weapon = []
		self.sidearm = []
		self.grenade = []
		self.equipment = []
		self.hi_slot = []
		self.low_slot = []
		self.current_cpu = self.dropsuit.stats['cpu']
		self.current_pg = self.dropsuit.stats['pg']
		self.shield_hp = self.dropsuit.stats['shield_hp']
		self.armor_hp = self.dropsuit.stats['armor_hp']
		self.armor_repair_rate = self.dropsuit.stats['armor_repair_rate']
		self.movement_speed = self.dropsuit.stats['movement_speed']
		self.sprint_speed = self.dropsuit.stats['sprint_speed']
		self.shield_recharge = self.dropsuit.stats['shield_recharge']
		self.shield_recharge_delay = self.dropsuit.stats['shield_recharge_delay']
		self.shield_depleted_recharge_delay = self.dropsuit.stats['shield_depleted_recharge_delay']

	def show_stats(self):
		""" Displays fitting status with all calculations, modules, and skills
		active. """

		def get_mod_names(slot):
			name_list = []
			for module in slot:
				name_list.append(module.mod_name)
			return name_list

		print 'CPU:                            %s/%s' % (self.current_cpu, self.dropsuit.stats['cpu'])
		print 'PG:                             %s/%s' % (self.current_pg, self.dropsuit.stats['pg'])
		print 'Heavy Weapon:                      %s' % get_mod_names(self.heavy_weapon)
		print 'Light Weapon:                      %s' % get_mod_names(self.light_weapon)
		print 'Sidearm:                           %s' % get_mod_names(self.sidearm)
		print 'Grenade:                           %s' % get_mod_names(self.grenade)
		print 'Equipment:                         %s' % get_mod_names(self.equipment)
		print 'Hi Slot:                           %s' % get_mod_names(self.hi_slot)
		print 'Low Slot:                          %s' % get_mod_names(self.low_slot)
		print 'Shield HP:                         %s' % self._get_additive_stat('shield_hp')
		print 'Armor HP:                          %s' % self._get_additive_stat('armor_hp')
		print 'Armor Repair Rate:                 %s' % self._get_additive_stat('armor_repair_rate')
		print 'Movement Speed:                    %s' % self._get_multiplicative_stat('movement_speed')
		print 'Sprint Speed:                      %s' % self._get_multiplicative_stacking_stat('sprint_speed')
		print 'Shield Recharge:                   %s' % self._get_multiplicative_stacking_stat('shield_recharge')
		print 'Shield Recharge Delay:             %s' % self._get_multiplicative_stacking_stat('shield_recharge_delay')
		print 'Shield Depleted Recharge Delay:    %s' % self._get_multiplicative_stacking_stat('shield_depleted_recharge_delay')

	def show_module_stats(self):
		""" Displays module stats with and without calculations. """
		p = Character()
		for mod in self.light_weapon:
			print '\nPlain'
			plain = Module(p.skill_effect,mod.mod_name)
			plain.show_stats()
			print '\nWith Character Stats'
			mod.show_stats()
			print '======================================================'
		for mod in self.hi_slot:
			print '\nPlain'
			plain = Module(p.skill_effect,mod.mod_name)
			plain.show_stats()
			print '\nWith Character Stats'
			mod.show_stats()
			print '======================================================'
		for mod in self.low_slot:
			print '\nPlain'
			plain = Module(p.skill_effect,mod.mod_name)
			plain.show_stats()
			print '\nWith Character Stats'
			mod.show_stats()
			print '======================================================'


	def add_module(self, mod_name):
		""" Adds a module if there is enough CPU, PG, and slots available. """
		module = Module(self.char.skill_effect, mod_name)
		used_slots = len(getattr(self, module.slot_type))
		slot_type = module.slot_type
		max_slots = self.dropsuit.stats[slot_type]
		if used_slots < max_slots:
			if True: #self.current_cpu >= module.cpu and self.current_pg >= module.pg:
				self.current_cpu = self.current_cpu - module.cpu
				self.current_pg = self.current_pg - module.pg
				getattr(self, module.slot_type).append(module)

	def add_weapon(self, weapon_name):
		""" Adds a weapon if there are enough slots available.  Takes current
		modules into account (damage mods). """
		weapon = Module(self.char.skill_effect, mod_name, effecting_modules=None)

	def _get_additive_stat(self, stat):
		output = self.dropsuit.stats[stat]
		for m in self.hi_slot:
			try:
				output = output + m.get(stat)
			except TypeError:
				# If mod doesn't have the proper stat, None is returned.
				pass
		for m in self.low_slot:
			try:
				output = output + m.get(stat)
			except:
				# If mod doesn't have the proper stat, None is returned.
				pass
		return output

	def _get_multiplicative_stat(self, stat):
		output = self.dropsuit.stats[stat]
		for m in self.hi_slot:
			try:
				output = output + (output * m.get(stat))
			except TypeError:
				# If mod doesn't have the proper stat, None is returned.
				pass
		for m in self.low_slot:
			try:
				output = output + (output * m.get(stat))
			except:
				# If mod doesn't have the proper stat, None is returned.
				pass
		return output

	def _get_multiplicative_stacking_stat(self, stat):
		ds_stat = self.dropsuit.stats[stat]
		modifier_list = []
		for m in self.hi_slot:
			if m.get(stat):
				modifier_list.append(m.get(stat))
		for m in self.low_slot:
			if m.get(stat):
				modifier_list.append(m.get(stat))
		return self._stacking_penalty(ds_stat, modifier_list)

	def _stacking_penalty(self, ds_stat, modifier_list):
		penalty = (1, 0.87, 0.57, 0.28, 0.105, 0.03)
		output = ds_stat
		for m, p in zip(modifier_list, penalty):
			output = output + output*m*p
		return output


class Dropsuit:
	def __init__(self, char_skills, type, ds_name):
		self.stats = {}
		self._get_xml(char_skills, type, ds_name)

	def show_stats(self):
		for key in self.stats:
			print key, self.stats[key]

	def _get_xml(self, char_skills, type, ds_name):
		"""Extracts dropsuit values from an xml and applies skill modifiers."""
		def _get_stat(name, ds, cs=char_skills):
			stat = float(ds.find(name).text)
			mod = 0
			try:
				modifier = ds.find(name).get('effected_by')
				for m in ds.find(name).attrib.values():
					mod = mod + char_skills[m]
			except KeyError:
				mod = 0
			return stat * ( 1 + mod )

		xml_tree = ET.parse('data/dropsuit.xml')
		xml_root = xml_tree.getroot()
		for ds in xml_root:
			if ds.attrib['type'] == type and ds.attrib['ds_name'] == ds_name:
				break
		self.stats['cpu'] = _get_stat('cpu', ds)
		self.stats['pg'] = _get_stat('pg', ds)
		self.stats['heavy_weapon'] = _get_stat('heavy_weapon', ds)
		self.stats['light_weapon'] = _get_stat('light_weapon', ds)
		self.stats['sidearm'] = _get_stat('sidearm', ds)
		self.stats['grenade'] = _get_stat('grenade', ds)
		self.stats['equipment'] = _get_stat('equipment', ds)
		self.stats['hi_slot'] = _get_stat('hi_slot', ds)
		self.stats['low_slot'] = _get_stat('low_slot', ds)
		self.stats['shield_hp'] = _get_stat('shield_hp', ds)
		self.stats['armor_hp'] = _get_stat('armor_hp', ds)
		self.stats['shield_recharge'] = _get_stat('shield_recharge', ds)
		self.stats['shield_recharge_delay'] = _get_stat('shield_recharge_delay', ds)
		self.stats['shield_depleted_recharge_delay'] = _get_stat('shield_depleted_recharge_delay', ds)
		self.stats['armor_repair_rate'] = _get_stat('armor_repair_rate', ds)
		self.stats['movement_speed'] = _get_stat('movement_speed', ds)
		self.stats['sprint_speed'] = _get_stat('sprint_speed', ds)
		self.stats['sprint_duration'] = _get_stat('sprint_duration', ds)
		self.stats['stamina'] = _get_stat('stamina', ds)
		self.stats['stamina_recovery_rate'] = _get_stat('stamina_recovery_rate', ds)
		self.stats['scan_profile'] = _get_stat('scan_profile', ds)
		self.stats['scan_precision'] = _get_stat('scan_precision', ds)
		self.stats['scan_radius'] = _get_stat('scan_radius', ds)
		self.stats['melee_damage'] = _get_stat('melee_damage', ds)
		self.stats['meta_level'] = _get_stat('meta_level', ds)


if __name__ == '__main__':
	richard = Character()
	plain = Character()
	plain_fit = Fitting(plain,'God','Type-I')
	richard.set_skill('Light Weapon Upgrades',2)
	richard.set_skill('Assault Rifle Proficiency',2)
	#richard.set_skill('Endurance',2)
	#richard.set_skill('Vigor',4)
	#richard.set_skill('Circuitry',5)
	#richard.set_skill('Combat Engineering',5)
	#richard.set_skill('Shield Enhancements',5)
	#richard.set_skill('Shield Boost Systems',5)
	#richard.set_skill('Armor Repair Systems',5)
	#richard.set_skill('Armor Upgrades',5)
	#richard.set_skill('Field Mechanics',2)

	fitting = Fitting(richard,'God','Type-I')
	fitting.add_module('Duvolle Assault Rifle')
	#fitting.add_module('Complex Armor Repairer')
	#fitting.add_module('Complex Shield Extender')
	#fitting.add_module('Complex Shield Extender')
	#fitting.add_module('Complex Armor Plates')
	#fitting.add_module('Complex Armor Plates')
	#fitting.add_module('Complex Shield Recharger')
	#fitting.add_module('Complex Shield Regulator')
	fitting.add_module('Complex Light Damage Modifier')
	fitting.add_module('Complex Light Damage Modifier')

	fitting.show_module_stats()

	print 'Plain Character Fitting'
	plain_fit.show_stats()
	print '====================================================='
	print 'Richard Fitting'
	fitting.show_stats()