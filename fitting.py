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
from module import Module, Weapon

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

		# Update dropsuit cpu/pg and current cpu/pg if there are cpu/pg upgrades.
		cpu_bonus = self.dropsuit.stats['cpu'] * get_bonus('cpu_bonus')
		pg_bonus = get_bonus('pg_bonus')
		self.dropsuit.stats['cpu'] += cpu_bonus
		self.dropsuit.stats['pg'] += pg_bonus
		self.current_cpu += cpu_bonus
		self.current_pg += pg_bonus

		# Display dropsuit stats.
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
		print 'Scan Profile:                      %s' % self._get_multiplicative_stacking_stat('scan_profile')
		print 'Stamina:                           %s' % self._get_multiplicative_stacking_stat('stamina')

	def show_module_stats(self):
		""" Displays module stats with and without calculations. """
		p = Character()
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
			if True: #self.current_cpu >= module.cpu and self.current_pg >= module.pg:
				self.current_cpu = self.current_cpu - module.stats['cpu']
				self.current_pg = self.current_pg - module.stats['pg']
				getattr(self, module.stats['slot_type']).append(module)

	def add_weapon(self, weapon_name):
		""" Adds a weapon. THIS MUST bE CALLED AFTER MODULES HAVE BEEN ADDED. """
		weapon = Weapon(self.char.skill_effect, weapon_name, self.hi_slot)
		slot_type = weapon.stats['slot_type']
		used_slots = len(getattr(self, slot_type))
		max_slots = self.dropsuit.stats[slot_type]
		if used_slots < max_slots:
			if True: #cpu/pg reqs go here.
				self.current_cpu = self.current_cpu - weapon.stats['cpu']
				self.current_pg = self.current_pg - weapon.stats['pg']
				getattr(self, weapon.stats['slot_type']).append(weapon)

	def get_cpu_over(self):
		""" If the dropsuit is using more CPU then it has available, return the
		percentage that it's over. Otherwise return None. """
		if self.current_cpu < 0:
			perc =(abs(self.current_cpu) / self.dropsuit.stats['cpu']) * 100
			return round(perc, 1)
		else:
			return None

	def get_pg_over(self):
		""" If the dropsuit is using more PG then it has available, return the
		percentage that it's over. Otherwise return None. """
		if self.current_pg < 0:
			perc =(abs(self.current_pg) / self.dropsuit.stats['pg']) * 100
			return round(perc, 1)
		else:
			return None

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

		self._get_xml('data/dropsuit.xml')


	def show_stats(self):
		for key in self.stats:
			print key, self.stats[key]

	def _get_xml(self, src):
		""" Extracts the dropsuit Values from an xml file using self.ds_type
		and self.ds_name as search parameters. """

		def is_number(s):
			try:
				float(s)
				return True
			except ValueError:
				return False

		def skill_modifiers(attrib):
			""" Finds all skills in attrib.values and applies the appropriate
			modifier.  If no modifier found, 1 is returned for no change.  Each
			modifier found will multiply itself onto the output. """
			skill_list = attrib.values()
			output = 1
			for skill in skill_list:
				if skill in self.skill_effects:
					output *= (1 + self.skill_effects[skill])
			return output

		xml_tree = ET.parse(src)
		# Finds the desired target in xml file
		for child in xml_tree.getroot():
			if child.attrib['name'] == self.ds_name:
				target = child
				break

		# Apply stats. Add skill modifiers when applicable.
		for prop in target:
			if is_number(prop.text):
				self.stats[prop.tag] = float(prop.text) * skill_modifiers(prop.attrib)
			else:
				self.stats[prop.tag] = prop.text


class DropsuitLibrary:
	def __init__(self):
		self.names = []

		self._get_xml('data/dropsuit.xml')

	def get_names(self):
		""" Returns dropsuit names as a tuple. """
		return tuple(self.names)

	def _get_xml(self, src):
		""" Finds all the names of every dropsuit in the xml file. """
		xml_tree = ET.parse(src)

		for child in xml_tree.getroot():
			self.names.append(child.get('name'))


if __name__ == '__main__':
	plain = Character()
	plain_fit = Fitting(plain,'Assault Type-I')

	reimus = Character()
	reimus.set_skill('Dropsuit Command', 1)
	reimus.set_skill('Profile Dampening', 0)
	reimus.set_skill('Circuitry', 3)
	reimus.set_skill('Combat Engineering', 2)
	reimus.set_skill('Vigor', 2)
	reimus.set_skill('Endurance', 2)
	reimus.set_skill('Shield Boost Systems', 5)
	reimus.set_skill('Shield Enhancements', 4)
	reimus.set_skill('Light Weapon Sharpshooter', 3)
	reimus.set_skill('Weaponry', 5)
	reimus.set_skill('Assault Rifle Proficiency', 2)

	reimus_fit = Fitting(reimus,'Assault Type-I')
	reimus_fit.add_module('Complex Shield Extender')
	reimus_fit.add_module('Complex Shield Extender')
	reimus_fit.add_module('Militia CPU Upgrade')
	reimus_fit.add_module('Militia PG Upgrade')
	reimus_fit.add_module('Militia Nanite Injector')
	reimus_fit.add_weapon('Assault Rifle')
	reimus_fit.add_weapon('Submachine Gun')
	reimus_fit.add_weapon('AV Grenade')

	#richard = Character()
	#richard_fit = Fitting(richard,'God','Type-I')
	#richard_fit.add_module('Complex Light Damage Modifier')
	#richard_fit.add_module('Complex Light Damage Modifier')
	#richard_fit.add_weapon('Duvolle Assault Rifle')

	#richard_fit.show_module_stats()
	reimus_fit.show_module_stats()

	print 'Plain Character Fitting'
	plain_fit.show_stats()
	print '====================================================='
	print 'Richard Fitting'
	reimus_fit.show_stats()

	dsl = DropsuitLibrary()
	print dsl.get_names()

	print reimus_fit.get_cpu_over()