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
from module import Module, Weapon, ModuleLibrary, WeaponLibrary
from util import XmlRetrieval, DataRetrieval

class Fitting:
    def __init__(self, name, character, ds_name):
        self.dropsuit_library = DropsuitLibrary()
        self.character_library = CharacterLibrary()
        self.weapon_library = WeaponLibrary()
        self.module_library = ModuleLibrary()
        self.name = name
        self.character = character
        self.ds_name = ds_name
        self.dropsuit = self.dropsuit_library.get(ds_name)

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

    def change_character(self, character_obj):
        """ This method will change the stored character to whichever character
            object has the given name then changes the character for the 
            Dropsuit ojbect. """
        self.character = character_obj
        self.dropsuit.change_character(self.character)

    def show_stats(self):
        """ Displays fitting status with all calculations, modules, and skills
        active. """

        def get_mod_names(slot):
            name_list = []
            for module in slot:
                name_list.append(module.name)
            return name_list

        # Display dropsuit stats.
        print 'Character Name:                    %s' % self.character.name
        print 'CPU:                            %s/%s' % (self.current_cpu, self.get_max_cpu())
        print 'PG:                             %s/%s' % (self.current_pg, self.get_max_pg())
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
        #module = Module(self.character.leveled_skill_effects, mod_name)
        module = self.module_library.get(mod_name)
        slot_type = module.properties['slot_type']
        used_slots = len(getattr(self, slot_type))
        max_slots = self.dropsuit.stats[slot_type]
        if used_slots < max_slots:
            if True: #cpu/pg reqs go here.
                self._update_cpu(module)
                self._update_pg(module)
                getattr(self, module.properties['slot_type']).append(module)
                self._update_module_bonus() # Must be called after the module has been added to the list

    def remove_module(self, mod_name):
        """ Finds a module that needs to be deleted and removes it if it has 
        been fitted. """
        for m in self.heavy_weapon:
            if m.name in mod_name:
                self.heavy_weapon.remove(m)
                self._free_cpu(m)
                self._free_pg(m)
                self._update_module_bonus()
                break
        for m in self.light_weapon:
            if m.name in mod_name:
                self.light_weapon.remove(m)
                self._free_cpu(m)
                self._free_pg(m)
                self._update_module_bonus()
                break
        for m in self.sidearm:
            if m.name in mod_name:
                self.sidearm.remove(m)
                self._free_cpu(m)
                self._free_pg(m)
                self._update_module_bonus()
                break
        for m in self.grenade:
            if m.name in mod_name:
                self.grenade.remove(m)
                self._free_cpu(m)
                self._free_pg(m)
                self._update_module_bonus()
                break
        for m in self.equipment:
            if m.name in mod_name:
                self.equipment.remove(m)
                self._free_cpu(m)
                self._free_pg(m)
                self._update_module_bonus()
                break
        for m in self.hi_slot:
            if m.name in mod_name:
                self.hi_slot.remove(m)
                self._free_cpu(m)
                self._free_pg(m)
                self._update_module_bonus()
                break
        for m in self.low_slot:
            if m.name in mod_name:
                self.low_slot.remove(m)
                self._free_cpu(m)
                self._free_pg(m)
                self._update_module_bonus()
                break

    def add_weapon(self, weapon_name):
        """ Adds a weapon. THIS MUST bE CALLED AFTER MODULES HAVE BEEN ADDED. """
        weapon = self.weapon_library.get(weapon_name)
        slot_type = weapon.get('slot_type')
        used_slots = len(getattr(self, slot_type))
        max_slots = self.dropsuit.stats[slot_type]
        if used_slots < max_slots:
            if True: #cpu/pg reqs go here.
                self._update_cpu(weapon)
                self._update_pg(weapon)
                getattr(self, weapon.get('slot_type')).append(weapon)

    def get_max_cpu(self):
        """ Returns the maximum cpu. Takes dropsuit, skills, and cpu enhancing
        modules into account. This method will update self.max_cpu as well as
        return the value of self.max_cpu. """
        self.max_cpu = self.dropsuit.stats['cpu']
        for module in self.hi_slot + self.low_slot:
            if 'cpu_bonus' in module.properties:
                self.max_cpu = self.max_cpu * (1 + module.properties['cpu_bonus'])
        return self.max_cpu

    def get_max_pg(self):
        """ Returns the maximum pg. Takes dropsuit, skills, and pg enhancing
        modules into account. This method will update self.max_pg as well as
        return the value of self.max_pg. """
        self.max_pg = self.dropsuit.stats['pg']
        for module in self.hi_slot + self.low_slot:
            if 'pg_bonus' in module.properties:
                self.max_pg += module.properties('pg_bonus')
        return self.max_pg

    def get_cpu_over(self):
        """ If the dropsuit is using more CPU then it has available, return the
        percentage that it's over as a string. Otherwise return ''. """
        if self.current_cpu > self.max_cpu:
            perc =( (self.current_cpu-self.max_cpu) / self.max_cpu) * 100
            return '%s%% over' % round(perc, 1)
        else:
            return None

    def get_pg_over(self):
        """ If the dropsuit is using more PG then it has available, return the
        percentage that it's over as a string. Otherwise return ''. """
        if self.current_pg > self.max_pg:
            perc =( (self.current_pg-self.max_pg) / self.max_pg) * 100
            return '%s%% over' % round(perc, 1)
        else:
            return None

    def get_primary_weapon_name(self):
        """ Returns the module name of the Heavy or Light weapon. """
        if self.heavy_weapon:
            return self.heavy_weapon[0].name
        elif self.light_weapon:
            return self.light_weapon[0].name
        return None

    def get_primary_stats(self, stat):
        if self.heavy_weapon:
            return round(self.heavy_weapon[0].stats[stat], 1)
        elif self.light_weapon:
            return round(self.light_weapon[0].stats[stat], 1)
        return None

    def get_primary_dps(self):
        if self.heavy_weapon:
            return round(self.heavy_weapon[0].stats['damage'] * (self.heavy_weapon[0].stats['rate_of_fire']/60), 1)
        elif self.light_weapon:
            return round(self.light_weapon[0].stats['damage'] * (self.light_weapon[0].stats['rate_of_fire']/60), 1)
        return None

    def get_primary_dpm(self):
        if self.heavy_weapon:
            return round(self.heavy_weapon[0].stats['damage'] * self.heavy_weapon[0].stats['clip_size'], 2)
        elif self.light_weapon:
            return round(self.light_weapon[0].stats['damage'] * self.light_weapon[0].stats['clip_size'], 2)
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

    def get_movement_speed(self):
        return round(self._get_multiplicative_stacking_stat('movement_speed'), 2)

    def get_sprint_speed(self):
        return round(self._get_multiplicative_stacking_stat('sprint_speed'), 2)

    def get_sprint_duration(self):
        return round(self._get_multiplicative_stacking_stat('sprint_duration'), 2)

    def get_stamina_recovery(self):
        """ Returns the amount of time it takes to fully recover stamina. """
        stam = self._get_multiplicative_stacking_stat('stamina')
        recov = self._get_multiplicative_stacking_stat('stamina_recovery_rate')
        return round(stam/recov, 2)

    def get_scan_profile(self):
        return round(self._get_multiplicative_stacking_stat('scan_profile'), 2)

    def get_scan_precision(self):
        return round(self._get_multiplicative_stacking_stat('scan_precision'), 2)

    def get_scan_radius(self):
        return round(self._get_multiplicative_stacking_stat('scan_radius'), 2)

    def get_all_modules(self):
        """ """
        module_list = []

        for mod in self.heavy_weapon:
            module_list.append(('H', mod.name, mod.properties['cpu'], mod.properties['pg']))
        for mod in range( len(self.heavy_weapon), int(self.dropsuit.stats['heavy_weapon']) ):
            module_list.append(('H', 'None', '0', '0'))
        for mod in self.light_weapon:
            module_list.append(('L', mod.name, mod.properties['cpu'], mod.properties['pg']))
        for mod in range( len(self.light_weapon), int(self.dropsuit.stats['light_weapon']) ):
            module_list.append(('L', 'None', '0', '0'))
        for mod in self.sidearm:
            module_list.append(('S', mod.name, mod.properties['cpu'], mod.properties['pg']))
        for mod in range( len(self.sidearm), int(self.dropsuit.stats['sidearm']) ):
            module_list.append(('S', 'None', '0', '0'))
        for mod in self.grenade:
            module_list.append(('G', mod.name, mod.properties['cpu'], mod.properties['pg']))
        for mod in range( len(self.grenade), int(self.dropsuit.stats['grenade']) ):
            module_list.append(('G', 'None', '0', '0'))
        for mod in self.equipment:
            module_list.append(('E', mod.name, mod.properties['cpu'], mod.properties['pg']))
        for mod in range( len(self.equipment), int(self.dropsuit.stats['equipment']) ):
            module_list.append(('E', 'None', '0', '0'))
        for mod in self.hi_slot:
            module_list.append(('--', mod.name, mod.properties['cpu'], mod.properties['pg']))
        for mod in range( len(self.hi_slot), int(self.dropsuit.stats['hi_slot']) ):
            module_list.append(('--', 'None', '0', '0'))
        for mod in self.low_slot:
            module_list.append(('-', mod.name, mod.properties['cpu'], mod.properties['pg']))
        for mod in range( len(self.low_slot), int(self.dropsuit.stats['low_slot']) ):
            module_list.append(('-', 'None', '0', '0'))

        return module_list

    def get_overview_abilities(self):
        """ Returns a list of general stats and abilities that a user should
        know about this fit.  Returned list contains tuples consisting of name 
        and statlist pairs. """
        overview = []

        stats = []
        stats.append( ('CPU:', '%s/%s' % (self.current_cpu, self.max_cpu)) )
        if self.get_cpu_over():
            stats.append( ('Over:', self.get_cpu_over()) )
        else:
            stats.append( ('', '') )
        stats.append( ('PG:', '%s/%s' % (self.current_pg, self.max_pg)) )
        if self.get_pg_over():
            stats.append( ('Over:', self.get_pg_over()))
        else:
            stats.append( ('', '') )
        overview.append( ('Resources', stats) )

        for weapon in self.heavy_weapon + self.light_weapon + self.sidearm:
            overview.append( (weapon.name, weapon.get_information()) )
            break

        stats = []
        stats.append( ('Shield Hp:', self.get_shield_hp()) )
        stats.append( ('Recharge:', self.get_shield_recharge()) )
        stats.append( ('Armor Hp:', self.get_armor_hp()) )
        stats.append( ('Repair:', self.get_armor_repair_rate()) )
        overview.append( ('Defenses', stats))

        stats = []
        stats.append( ('Scan Profile:', self.get_scan_profile()) )
        stats.append( ('Scan Precision:', self.get_scan_precision()) )
        overview.append( ('Sensors', stats) )

        stats = []
        stats.append( ('Speed:', self.get_movement_speed()) )
        stats.append( ('Sprint:', self.get_sprint_speed()) )
        overview.append( ('Mobility', stats) )

        return overview

    def get_offensive_abilities(self):
        """ Returns a list of offensive abilities this fit possesses for the 
        GUI. Returned list contains tuples consisting of name and statlist 
        pairs. """
        abilities = []
        for weapon in self.heavy_weapon + self.light_weapon + self.sidearm + self.grenade:
            abilities.append( (weapon.name, weapon.get_information()) )
        if not abilities:
            pass
        return abilities

    def get_defensive_abilities(self):
        """ Returns a list of defensive abilities this fit possesses for the 
        GUI. """
        defenses = []

        stats = []
        time_to_recharge = round((self.get_shield_hp()/self.get_shield_recharge())+self.get_shield_depleted_recharge_delay(), 1)
        stats.append( ('Shield Hp:', self.get_shield_hp()) )
        stats.append( ('Recharge:', self.get_shield_recharge()) )
        stats.append( ('Delay:', self.get_shield_recharge_delay()) )
        stats.append( ('Depleted:', self.get_shield_depleted_recharge_delay()) )
        stats.append( ('Full Recharge:', time_to_recharge))
        defenses.append( ('Shields', stats) )

        stats = []
        stats.append( ('Armor Hp:', self.get_armor_hp()) )
        if self.get_armor_repair_rate():
            time_to_repair = round(self.get_armor_hp()/self.get_armor_repair_rate(), 1)
            stats.append( ('Repair:', self.get_armor_repair_rate()) )
            stats.append( ('Full Repair:', time_to_repair))
        defenses.append( ('Armor:', stats) )

        stats = []
        stats.append( ('Speed:', self.get_movement_speed()) )
        stats.append( ('Sprint:', self.get_sprint_speed()) )
        stats.append( ('Duration:', self.get_sprint_duration()) )
        stats.append( ('Recovery:', self.get_stamina_recovery()) )
        defenses.append( ('Mobility', stats) )

        stats = []
        stats.append( ('Scan Profile:', self.get_scan_profile()) )
        defenses.append( ('Stealth', stats) )

        return defenses

    def get_systems_abilities(self):
        """ Returns a list of systems/equipment abilities this fit possesses for
        the GUI. """
        systems = []

        stats = []
        stats.append( ('Precision:', self.get_scan_precision()) )
        stats.append( ('Radius:', self.get_scan_radius()) )
        systems.append( ('Sensors', stats) )

        for mod in self.equipment:
            systems.append(mod.get_information())

        return systems

    def _get_all_modules(self):
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
        for i in range( len(self.low_slot), int(self.dropsuit.stats['low_slot']) ):
            module_list.append(get_output('-','None','0','0'))

        return tuple(module_list)

    def _update_cpu(self, module):
        """ Called by add_module or add_weapon methods.  This will update the
        fittings current_cpu and max_cpu when a module has been added. 
        ONLY  FOR ADDING CPU. """
        self.current_cpu += module.properties['cpu']
        if 'cpu_bonus' in module.properties:
            self.max_cpu += self.max_cpu * module.properties['cpu_bonus']

    def _update_pg(self, module):
        """ Called by add_module or add_weapon methods.  This will update the
        fittings current_pg and max_pg when a module has been added. 
        ONLY FOR ADDING PG"""
        self.current_pg += module.properties['pg']
        if 'pg_bonus' in module.properties:
            self.max_pg += module.properties['pg_bonus']

    def _free_cpu(self, module):
        """ Called by remove_module. This will free CPU resources from the
        fitting when a module has been removed. """
        self.current_cpu -= module.properties['cpu']
        self.current_cpu = round(self.current_cpu, 3)
        if 'cpu_bonus' in module.properties:
            # For the love of god, please note that this equation is far 
            # different than the others. Especially the equal sign!!!!!
            self.max_cpu = self.max_cpu / (1 + module.properties['cpu_bonus'])

    def _free_pg(self, module):
        """ Called by remove_module. This will free CPU resources from the
        fitting when a module has been removed. """
        self.current_pg -= module.properties['pg']
        self.current_pg = round(self.current_pg, 3)
        if 'pg_bonus' in module.properties:
            self.max_pg -= module.properties['pg_bonus']

    def _update_module_bonus(self):
        """ This will update weapons with any modules that give a bonus to them.
        This is intended to be a hotfix. """
        for w in self.heavy_weapon + self.light_weapon + self.sidearm:
            w.__init__(self.char.skill_effect, w.name, self.hi_slot)

    def _get_additive_stat(self, stat):
        output = self.dropsuit.stats[stat]
        for m in self.hi_slot + self.low_slot:
            try:
                output = output + m.get(stat)
            except TypeError:
                # If mod doesn't have the proper stat, None is returned.
                pass
        return output

    def _get_multiplicative_stat(self, stat):
        output = self.dropsuit.stats[stat]
        for m in self.hi_slot + self.low_slot:
            try:
                output = output + (output * m.get(stat))
            except TypeError:
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


class Dropsuit2:
    def __init__(self, char, ds_name):
        self.stats = {}
        self.skill_effects = char.leveled_skill_effects
        self.ds_name = ds_name

        dropsuit_data = XmlRetrieval('dropsuit.xml')
        self.parent, properties, effecting_skills = dropsuit_data.get_target(ds_name)
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

class Dropsuit:
    def __init__(self, name, category, properties, effecting_skills, prerequisites, character):
        self.name = name
        self.category = category
        self.stats = properties #TODO: Rename to something more descriptive
        self.effecting_skills = effecting_skills
        self.prerequisites = prerequisites

        self.character = character

    def change_character(self, character):
        """ Changes the character object and calls _apply_skills to change the
            values stored in stats. """
        self.character = character
        self._apply_skills()

    def _apply_skills(self):
        """ Modifies the values stored in stats with the characters skills. """
        print self.character.get_leveled_skill_effect('Shield Control')
        for property, skill_name_list in self.effecting_skills.iteritems():
            for skill_name in skill_name_list:
                self.stats[property] = self.stats[property] * (1+self.character.get_leveled_skill_effect(skill_name))


class FittingLibrary:
    def __init__(self):
        self.fitting_data = DataRetrieval('fittings.dat')
        # If no fitting.dat file exists then create  a default fitting and
        # save it.
        if not self.fitting_data.data:
            self._create_default_fitting()

        self.fitting_list = self.fitting_data.data

    def get_fitting(self, fitting_name):
        """ Returns a the specified fitting instance. """
        return self.fitting_list[fitting_name]

    def get_fitting_list(self):
        """ Returns a list of the names of all fitting names as a tuple. """
        return tuple(self.fitting_list.keys())

    def save_fitting(self, fitting):
        """ """
        self.fitting_data.save_data(fitting)

    def delete_fitting(self, fitting):
        self.fitting_data.delete_data(fitting)

    def _create_default_fitting(self):
        """ Called when no fitting data has been found. This method will
        create a 'My Fitting' fit and save it for future used. """
        cl = CharacterLibrary()
        my_fitting = Fitting('My Fitting', cl.get_character('No Skills'), 'Assault Type-I')
        self.save_fitting(my_fitting)


class DropsuitLibrary:
    def __init__(self):
        self.dropsuit_dict = {}
        self.dropsuit_data = XmlRetrieval('dropsuit.xml')

        self._get_all_dropsuits()

    def get(self, name):
        """ Returns a dropsuit object when given the name of the dropsuit. """
        return self.dropsuit_dict[name]

    def get_all_names(self):
        """ Returns dropsuit names as a tuple. """
        return tuple(self.dropsuit_dict.keys())

    def _get_all_dropsuits(self):
        # Dropsuits require a character. Created a CharacterLibrary object and
        # give each dropsuit a 'No Skills' character.
        character_library = CharacterLibrary()
        for name, category, properties, effecting_skills, prerequisites in self.dropsuit_data.get_all():
            self.dropsuit_dict[name] = Dropsuit(name, category, properties, effecting_skills, prerequisites, character_library.get_character('No Skills'))


if __name__ == '__main__':
    fitting_library = FittingLibrary()
    character_library = CharacterLibrary()
    dropsuit_library = DropsuitLibrary()

    print 'SHOW ALL DROPSUITS: ', dropsuit_library.get_all_names()
    test_ds = dropsuit_library.get('Assault Type-II')
    print 'Test dropsuit: ', test_ds.name
    test_fit = Fitting('Test Fitting', test_ds, 'Assault Type-I')
    print '\n\n\nSTATS WITH NO SKILLS\n', test_fit.show_stats()
    test_fit.change_character('Max Skills')
    print '\n\n\nSTATS WITH MAX SKILLS\n', test_fit.show_stats()
    test_fit.add_module('Enhanced CPU Upgrade')
    print '\n\n\nSTATS WITH MAX SKILLS AND CPU UPGRADE (.25)\n', test_fit.show_stats()
    test_fit.remove_module('Enhanced CPU Upgrade')
    print '\n\n\nREMOVED MODULE\n', test_fit.show_stats()
    test_fit.add_weapon('Assault Rifle')
    print '\n\n\nADD ASSAULT RIFLE\n', test_fit.show_stats()