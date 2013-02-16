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

from char import Character, CharacterLibrary
from module import Module, Weapon
from util import XmlRetrieval, DataRetrieval

class Fitting:
	def __init__(self, character, ds_name):
		self.char = character
		#self.dropsuit = Dropsuit(self.char.skill_effect, ds_type, ds_name)
		self.dropsuit = Dropsuit(self.char, ds_name)

		self.heavy_weapon = []
		self.light_weapon = []
		self.sidearm = []
		self.grenade = []
		self.equipment = []
		self.hi_slot = []
		self.low_slot = []
		self.current_cpu = 0
		self.current_pg = 0
		self.max_cpu = self.dropsuit.stats['cpu']
		self.max_pg = self.dropsuit.stats['pg']
		self.shield_hp = self.dropsuit.stats['shield_hp']
		self.armor_hp = self.dropsuit.stats['armor_hp']
		self.armor_repair_rate = self.dropsuit.stats['armor_repair_rate']
		self.movement_speed = self.dropsuit.stats['movement_speed']
		self.sprint_speed = self.dropsuit.stats['sprint_speed']
		self.shield_recharge = self.dropsuit.stats['shield_recharge']
		self.shield_recharge_delay = self.dropsuit.stats['shield_recharge_delay']
		self.shield_depleted_recharge_delay = self.dropsuit.stats['shield_depleted_recharge_delay']
		self.scan_profile = self.dropsuit.stats['scan_profile']

	def show_stats(self):
		""" Displays fitting status with all calculations, modules, and skills
		active. """

		def get_mod_names(slot):
			name_list = []
			for module in slot:
				name_list.append(module.name)
			return name_list

		def get_bonus(bonus):
			""" Find all bonus' to cpu or pg and return them. """
			output = 0
			for m in self.low_slot:
				if bonus in m.stats:
					output += m.stats[bonus]
			return output

		# Display dropsuit stats.
		print 'CPU:                            %s/%s' % (self.current_cpu, self.max_cpu)
		print 'PG:                             %s/%s' % (self.current_pg, self.max_pg)
		print 'Heavy Weapon:                      %s' % get_mod_names(self.heavy_weapon)
		print 'Light Weapon:                      %s' % get_mod_names(self.light_weapon)
		print 'Sidearm:                           %s' % get_mod_names(self.sidearm)
		print 'Grenade:                           %s' % get_mod_names(self.grenade)
		print 'Equipment:                         %s' % get_mod_names(self.equipment)
		print 'Hi Slot:                           %s' % get_mod_names(self.hi_slot)
		print 'Low Slot:                          %s' % get_mod_names(self.low_slot)
		print 'Shield HP:                         %s' % self.get_shield_hp()
		print 'Shield Recharge:                   %s' % self.get_shield_recharge()
		print 'Shield Recharge Delay:             %s' % self.get_shield_recharge_delay()
		print 'Shield Depleted Recharge Delay:    %s' % self.get_shield_depleted_recharge_delay()
		print 'Armor HP:                          %s' % self.get_armor_hp()
		print 'Armor Repair Rate:                 %s' % self.get_armor_repair_rate()
		print 'Movement Speed:                    %s' % self._get_multiplicative_stat('movement_speed')
		print 'Sprint Speed:                      %s' % self._get_multiplicative_stacking_stat('sprint_speed')
		print 'Scan Profile:                      %s' % self._get_multiplicative_stacking_stat('scan_profile')
		print 'Stamina:                           %s' % self._get_multiplicative_stacking_stat('stamina')

	def show_module_stats(self):
		""" Displays module stats with and without calculations. """
		p = Character('p')
		for mod in self.light_weapon:
			print '\nPlain'
			plain = Weapon(p.skill_effect,mod.name)
			plain.show_stats()
			print '\nWith Character Stats'
			mod.show_stats()
			print '======================================================'
		for mod in self.sidearm:
			print '\nPlain'
			plain = Weapon(p.skill_effect,mod.name)
			plain.show_stats()
			print '\nWith Character Stats'
			mod.show_stats()
			print '======================================================'
		for mod in self.hi_slot:
			print '\nPlain'
			plain = Module(p.skill_effect,mod.name)
			plain.show_stats()
			print '\nWith Character Stats'
			mod.show_stats()
			print '======================================================'
		for mod in self.low_slot:
			print '\nPlain'
			plain = Module(p.skill_effect,mod.name)
			plain.show_stats()
			print '\nWith Character Stats'
			mod.show_stats()
			print '======================================================'
		for mod in self.grenade:
			print '\nPlain'
			plain = Weapon(p.skill_effect,mod.name)
			plain.show_stats()
			print '\nWith Character Stats'
			mod.show_stats()
			print '======================================================'
		for mod in self.equipment:
			print '\nPlain'
			plain = Module(p.skill_effect,mod.name)
			plain.show_stats()
			print '\nWith Character Stats'
			mod.show_stats()
			print '======================================================'


	def add_module(self, mod_name):
		""" Adds a module if there is enough CPU, PG, and slots available. """
		module = Module(self.char.skill_effect, mod_name)
		slot_type = module.stats['slot_type']
		used_slots = len(getattr(self, slot_type))
		max_slots = self.dropsuit.stats[slot_type]
		if used_slots < max_slots:
			if True: #cpu/pg reqs go here.
				self._update_cpu(module)
				self._update_pg(module)
				getattr(self, module.stats['slot_type']).append(module)

	def remove_module(self, mod_name):
		""" Finds a module that needs to be deleted and removes it if it has 
		been fitted. """
			
		for m in self.heavy_weapon:
			if m.name in mod_name:
				self.heavy_weapon.remove(m)
				self._free_cpu(m)
				self._free_pg(m)
				break
		for m in self.light_weapon:
			if m.name in mod_name:
				self.light_weapon.remove(m)
				self._free_cpu(m)
				self._free_pg(m)
				break
		for m in self.sidearm:
			if m.name in mod_name:
				self.sidearm.remove(m)
				self._free_cpu(m)
				self._free_pg(m)
				break
		for m in self.grenade:
			if m.name in mod_name:
				self.grenade.remove(m)
				self._free_cpu(m)
				self._free_pg(m)
				break
		for m in self.equipment:
			if m.name in mod_name:
				self.equipment.remove(m)
				self._free_cpu(m)
				self._free_pg(m)
				break
		for m in self.hi_slot:
			if m.name in mod_name:
				self.hi_slot.remove(m)
				self._free_cpu(m)
				self._free_pg(m)
				break
		for m in self.low_slot:
			if m.name in mod_name:
				self.low_slot.remove(m)
				self._free_cpu(m)
				self._free_pg(m)
				break

	def add_weapon(self, weapon_name):
		""" Adds a weapon. THIS MUST bE CALLED AFTER MODULES HAVE BEEN ADDED. """
		weapon = Weapon(self.char.skill_effect, weapon_name, self.hi_slot)
		slot_type = weapon.stats['slot_type']
		used_slots = len(getattr(self, slot_type))
		max_slots = self.dropsuit.stats[slot_type]
		if used_slots < max_slots:
			if True: #cpu/pg reqs go here.
				self._update_cpu(weapon)
				self._update_pg(weapon)
				getattr(self, weapon.stats['slot_type']).append(weapon)

	def get_cpu_over(self):
		""" If the dropsuit is using more CPU then it has available, return the
		percentage that it's over as a string. Otherwise return ''. """
		if self.current_cpu > self.max_cpu:
			perc =( (self.current_cpu-self.max_cpu) / self.max_cpu) * 100
			return '%s%%' % round(perc, 1)
		else:
			return None

	def get_pg_over(self):
		""" If the dropsuit is using more PG then it has available, return the
		percentage that it's over as a string. Otherwise return ''. """
		if self.current_pg > self.max_cpu:
			perc =( (self.current_pg-self.max_pg) / self.max_pg) * 100
			return '%s%%' % round(perc, 1)
		else:
			return None

	def get_shield_hp(self):
		return round(self._get_additive_stat('shield_hp'), 2)

	def get_shield_recharge(self):
		return round(self._get_multiplicative_stacking_stat('shield_recharge'), 2)

	def get_shield_recharge_delay(self):
		return round(self._get_multiplicative_stacking_stat('shield_recharge_delay'), 2)

	def get_shield_depleted_recharge_delay(self):
		return round(self._get_multiplicative_stacking_stat('shield_depleted_recharge_delay'), 2)

	def get_armor_hp(self):
		return round(self._get_additive_stat('armor_hp'), 2)

	def get_armor_repair_rate(self):
		return round(self._get_additive_stat('armor_repair_rate'), 2)

	def get_all_modules(self):
		""" Returns a tuple of modules and weapons for the GUI. """
		def get_output(icon, name, cpu, pg):
			return '{:3.3} {:<30.30} {:>5.5} {:>5.5}'.format(icon, name, cpu, pg)

		module_list = []
		for mod in self.heavy_weapon:
			module_list.append(get_output('H',mod.name, mod.stats['cpu'], mod.stats['pg']))
		for i in range( len(self.heavy_weapon), int(self.dropsuit.stats['heavy_weapon']) ):
			module_list.append(get_output('H','None','0','0'))
		for mod in self.light_weapon:
			module_list.append(get_output('L',mod.name, mod.stats['cpu'], mod.stats['pg']))
		for i in range( len(self.light_weapon), int(self.dropsuit.stats['light_weapon']) ):
			module_list.append(get_output('L','None','0','0'))
		for mod in self.sidearm:
			module_list.append(get_output('S',mod.name, mod.stats['cpu'], mod.stats['pg']))
		for i in range( len(self.sidearm), int(self.dropsuit.stats['sidearm']) ):
			module_list.append(get_output('S','None','0','0'))
		for mod in self.grenade:
			module_list.append(get_output('G',mod.name, mod.stats['cpu'], mod.stats['pg']))
		for i in range( len(self.grenade), int(self.dropsuit.stats['grenade']) ):
			module_list.append(get_output('G','None','0','0'))
		for mod in self.equipment:
			module_list.append(get_output('E',mod.name, mod.stats['cpu'], mod.stats['pg']))
		for i in range( len(self.equipment), int(self.dropsuit.stats['equipment']) ):
			module_list.append(get_output('E','None','0','0'))
		for mod in self.hi_slot:
			module_list.append(get_output('--',mod.name, mod.stats['cpu'], mod.stats['pg']))
		for i in range( len(self.hi_slot), int(self.dropsuit.stats['hi_slot']) ):
			module_list.append(get_output('--','None','0','0'))
		for mod in self.low_slot:
			module_list.append(get_output('-',mod.name, mod.stats['cpu'], mod.stats['pg']))
		for i in range( len(self.low_slot), int(self.dropsuit.stats['hi_slot']) ):
			module_list.append(get_output('-','None','0','0'))

		return tuple(module_list)

	def _update_cpu(self, module):
		""" Called by add_module or add_weapon methods.  This will update the
		fittings current_cpu and max_cpu when a module has been added. 
		ONLY  FOR ADDING CPU. """
		self.current_cpu += module.stats['cpu']
		if 'cpu_bonus' in module.stats:
			self.max_cpu += self.max_cpu * module.stats['cpu_bonus']

	def _update_pg(self, module):
		""" Called by add_module or add_weapon methods.  This will update the
		fittings current_pg and max_pg when a module has been added. 
		ONLY FOR ADDING PG"""
		self.current_pg += module.stats['pg']
		if 'pg_bonus' in module.stats:
			self.max_pg += module.stats['pg_bonus']

	def _free_cpu(self, module):
		""" Called by remove_module. This will free CPU resources from the
		fitting when a module has been removed. """
		self.current_cpu -= module.stats['cpu']
		self.current_cpu = round(self.current_cpu, 3)
		if 'cpu_bonus' in module.stats:
			# For the love of god, please note that this equation is far 
			# different than the others. Especially the equal sign!!!!!
			self.max_cpu = self.max_cpu / (1 + module.stats['cpu_bonus'])

	def _free_pg(self, module):
		""" Called by remove_module. This will free CPU resources from the
		fitting when a module has been removed. """
		self.current_pg -= module.stats['pg']
		self.current_pg = round(self.current_pg, 3)
		if 'pg_bonus' in module.stats:
			self.max_pg -= module.stats['pg_bonus']

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
	def __init__(self, char, ds_name):
		self.stats = {}
		self.skill_effects = char.skill_effect
		self.ds_name = ds_name

		dropsuit_data = XmlRetrieval('dropsuit.xml')
		properties, effecting_skills = dropsuit_data.get_target(ds_name)
		self._add_stats(properties, effecting_skills)

	def show_stats(self):
		for key in self.stats:
			print key, self.stats[key]

	def _add_stats(self, properties, effecting_skills):
		""" Adds the properties and effecting skills to the Dropsuit.stats
		dictionary. """
		def skill_modifiers(attrib):
			""" Finds all skills in attrib.values and applies the appropriate
			modifier.  If no modifier found, 1 is returned for no change.  Each
			modifier found will multiply itself onto the output. """
			skill_list = attrib
			output = 1
			for skill in skill_list:
				if skill in self.skill_effects:
					output *= (1 + self.skill_effects[skill])
			return output

		# Apply stats. Add skill modifiers when applicable.
		for key in properties:
			if key in effecting_skills:
				stat = properties[key] * skill_modifiers(effecting_skills[key])
			else:
				stat = properties[key]
			self.stats[key] = round(stat, 3)


class DropsuitLibrary:
	def __init__(self):
		dropsuit_data = XmlRetrieval('dropsuit.xml')

		self.names = dropsuit_data.get_list()		

	def get_names(self):
		""" Returns dropsuit names as a tuple. """
		return tuple(self.names)


if __name__ == '__main__':
	charlib = CharacterLibrary()

	"""reimus = Character('Reimus Klinsman')
	reimus.set_skill('Dropsuit Command', 1)
	reimus.set_skill('Profile Dampening', 0)
	reimus.set_skill('Nanocircuitry', 1)
	reimus.set_skill('Circuitry', 4)
	reimus.set_skill('Combat Engineering', 2)
	reimus.set_skill('Vigor', 0)
	reimus.set_skill('Endurance', 0)
	reimus.set_skill('Shield Boost Systems', 3)
	reimus.set_skill('Shield Enhancements', 4)
	reimus.set_skill('Light Weapon Sharpshooter', 4)
	reimus.set_skill('Weaponry', 5)
	reimus.set_skill('Assault Rifle Proficiency', 2)

	richard = Character('Richard C Mongler')
	richard.set_skill('Dropsuit Command', 1)
	richard.set_skill('Endurance', 4)
	richard.set_skill('Vigor', 3)
	richard.set_skill('Profile Dampening', 3)
	richard.set_skill('Field Mechanics', 1)

	plain = Character('No Skills')

	charlib.save_character(reimus)
	charlib.save_character(richard)
	charlib.save_character(plain)"""

	plain_fit = Fitting(charlib.get_character('No Skills'), 'Assault Type-I')

	reimus_fit = Fitting(charlib.get_character('Reimus Klinsman'),'Assault Type-I')
	reimus_fit.add_module('Complex Shield Extender')
	reimus_fit.add_module('Complex Shield Extender')
	reimus_fit.add_module('Militia CPU Upgrade')
	reimus_fit.add_module('Militia CPU Upgrade')
	reimus_fit.add_module('Militia PG Upgrade')
	reimus_fit.add_module('Militia Nanite Injector')
	reimus_fit.add_module('Militia CPU Upgrade')
	reimus_fit.add_weapon('Assault Rifle')
	reimus_fit.add_weapon('Submachine Gun')
	reimus_fit.add_weapon('AV Grenade')

	reimus_fit.show_module_stats()

	print 'Plain Character Fitting'
	plain_fit.show_stats()
	print '====================================================='
	print 'Richard Fitting'
	reimus_fit.show_stats()

	dsl = DropsuitLibrary()
	print dsl.get_names()