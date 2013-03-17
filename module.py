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
    def __init__(self, name, category, properties, effecting_skills, prerequisites):
        self.name = name
        self.category = category
        self.properties = properties
        self.effecting_skills = effecting_skills
        self.prerequisites = prerequisites

    def get(self, prop_name):
        if prop_name in self.properties:
            return self.properties[prop_name]
        else:
            return None

    def show_stats(self):
        print self.name
        for key in self.stats:
            print '{:<20} {:<15}'.format(key, self.stats[key])

    def get_information(self):
        """ Returns a list of stats needed for output. """
        return (self.name, self.get_bestest_stats())

    def get_bestest_stats(self):
        """ Returns the most valuable stats depending on what item this is. """
        output = []
        if self.category == 'nanite_injector':
            output.append( ('Revive Armor:', self.get('armor_repaired_on_revive')) )
        elif self.category == 'repair_tool':
            output.append( ('Dropsuit:', self.get('repair_rate_on_dropsuit')) )
            output.append( ('Vehicle:', self.get('repair_rate_on_vehicle')) )
            output.append( ('Range:', self.get('max_repair_distance')) )
            output.append( ('Targets:', self.get('max_targets', 0)) )
        elif self.category == 'nanohive':
            output.append( ('Resupply:', self.get('max_nanite_clusters')) )
            output.append( ('Rate:', self.get('ammo_resupply_rate')) )
            output.append( ('Max Active:', self.get('max_active', 0)) )
            output.append( ('Max Carried:', self.get('max_carried', 0)) )
            output.append( ('Range', self.get('effective_range')) )
        elif self.category == 'drop_uplink':
            output.append( ('Max Spawns:', self.get('max_spawns_per_unit', 0)) )
            output.append( ('Spawn Time:', self.get('spawn_time_modifier')) )
            output.append( ('Max Active:', self.get('max_active', 0)) )
            output.append( ('Max Carried:', self.get('max_carried', 0)) )
        elif self.category == 'remote_explosives':
            if 'Remote' in self.name:
                detonated_by = 'Trigger:'
            else:
                detonated_by = 'Vehicle:'
            output.append( ('Radius:', self.get('blast_radius')) )
            output.append( ('Detonated:', detonated_by) )
            output.append( ('Max Active:', self.get('max_active', 0)) )
            output.append( ('Max Carried:', self.get('max_carried', 0)) )
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
    def __init__(self, name, category, properties, effecting_skills, prerequisites):
        self.name = name
        self.category = category
        self.properties = properties
        self.effecting_skills = effecting_skills
        self.prerequisites = prerequisites

    def get(self, prop_name):
        if prop_name in self.properties:
            return self.properties[prop_name]
        else:
            return None

    def get_information(self):
        """ Returns a list of stats needed for output. """
        return self.get_bestest_stats()

    def get_bestest_stats(self):
        """ Returns the most valuable stats depending on what item this is. """
        output = []
        if self.category == 'assault_rifles':
            output.append( ('Damage:', self.get('damage')) )
            output.append( ('Rof:', self.get('rate_of_fire')) )
            output.append( ('Optimal:', self.get('optimal_range_high')) )
            output.append( ('Max Range:', self.get('max_range')) )
            output.append( ('Magazine:', self.get('clip_size')) )
            output.append( ('Max Ammo:', self.get('max_ammo')) )
        elif self.category == 'forge_guns':
            rof = round(60/self.get('charge-up_time'), 1)
            output.append( ('Damage:', self.get('direct_damage')) )
            output.append( ('Rof:', rof) )
            output.append( ('Magazine:', self.get('clip_size')) )
            output.append( ('Charge Time:', self.get('charge-up_time')) )
            output.append( ('Spash Damage:', self.get('splash_damage')) )
            output.append( ('Blast Radius:', self.get('blast_radius')) )
        elif self.category == 'heavy_machine_guns':
            dps = round(self.get('damage')*(self.get('rate_of_fire')/60), 1)
            tto = round(100/self.get('heat_build-up_per_second'), 1)
            output.append( ('Damage:', self.get('damage')) )
            output.append( ('Rof:', self.get('rate_of_fire')) )
            output.append( ('Dps:', dps) )
            output.append( ('Time to Overheat:', tto) )
            output.append( ('Optimal:', self.get('optimal_range_high')) )
            output.append( ('Max Range:', self.get('max_range')) )
        elif self.category == 'submachine_guns':
            output.append( ('Damage:', self.get('damage')) )
            output.append( ('Rof:', self.get('rate_of_fire')) )
            output.append( ('Optimal:', self.get('optimal_range_high')) )
            output.append( ('Max Range:', self.get('max_range')) )
            output.append( ('Magazine:', self.get('clip_size')) )
            output.append( ('Max Ammo:', self.get('max_ammo')) )
        elif self.category == 'shotguns':
            output.append( ('Damage:', self.get('damage')) )
            output.append( ('Rof:', self.get('rate_of_fire')) )
            output.append( ('Optimal:', self.get('optimal_range_high')) )
            output.append( ('Max Range:', self.get('max_range')) )
            output.append( ('Shots:', self.get('clip_size')) )
            output.append( ('Reload Time:', self.get('reload_time')) )
        elif self.category == 'laser_rifles':
            output.append( ('Damage:', self.get('damage')) )
            output.append( ('Rof:', self.get('rate_of_fire')) )
            output.append( ('Optimal Low:', self.get('optimal_range_low')) )
            output.append( ('Optimal High:', self.get('optimal_range_high')) )
            output.append( ('Max Range:', self.get('max_range')) )
        elif self.category == 'sniper_rifles':
            output.append( ('Damage:', self.get('damage')) )
            output.append( ('Rof:', self.get('rate_of_fire')) )
            output.append( ('Magazine:', self.get('clip_size')) )
            output.append( ('Max Ammo:', self.get('max_ammo')) )
        elif self.category == 'grenades':
            if 'Locus' in self.name:
                output.append( ('Damage:', self.get('splash_damage')) )
                output.append( ('Radius:', self.get('blast_radius')) )
            elif 'AV' in self.name:
                output.append( ('Damage:', self.get('splash_damage')) )
                output.append( ('Targets:', 'Vehicles') )
            elif 'Flux' in self.name:
                pass
        return output

    def add_module_bonus(self, module_list):
        """ Searching module_list for any modules which effect this 
        weapons slot type (found in the modules 'enhances' cell. If so, it will 
        add the bonuses for that module. 
        CURRENTLY ONLY WORKS FOR DAMAGE!!! """
        slot_type = self.properties['slot_type']
        for m in module_list:
            try:
                if slot_type == m.properties('enhances'):
                    self.properties['damage'] = self.properties['damage'] * (1 + m.properties['damage'])
            except KeyError:
                # Module does not have a key 'enhances' in its stats dictionary.
                pass


class ModuleLibrary:
    def __init__(self):
        self.module_dict = {}
        self.module_data = XmlRetrieval('module.xml')

        self._get_all_modules()

    def get(self, name):
        """ Returns the object with the same name. """
        return self.module_dict[name]

    def get_names(self):
        """ Returns module names as a tuple. """
        return tuple(self.module_dict.keys())

    def get_parents(self):
        return self.module_data.get_parents()

    def get_children(self, parent):
        return self.module_data.get_children(parent)

    def _get_all_modules(self):
        for name, category, properties, effecting_skills, prerequisites in self.module_data.get_all():
            self.module_dict[name] = Module(name, category, properties, effecting_skills, prerequisites)
            

class WeaponLibrary:
    def __init__(self):
        self.weapon_dict = {}
        self.weapon_data = XmlRetrieval('weapon.xml')

        self._get_all_weapons()

    def get(self, name):
        """ Returns the object with the same name. """
        return self.weapon_dict[name]

    def get_names(self):
        """ Returns module names as a tuple. """
        return tuple(self.names)

    def get_parents(self):
        return self.weapon_data.get_parents()

    def get_children(self, parent):
        return self.weapon_data.get_children(parent)

    def _get_all_weapons(self):
        for name, category, properties, effecting_skills, prerequisites in self.weapon_data.get_all():
            self.weapon_dict[name] = Weapon(name, category, properties, effecting_skills, prerequisites)


if __name__ == '__main__':
    modlib = ModuleLibrary()
    wealib = WeaponLibrary()
    print modlib.module_dict['Nanohive'].prerequisites
    print wealib.weapon_dict['Duvolle Assault Rifle'].name