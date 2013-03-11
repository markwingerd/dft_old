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

import sys
import os
import xml.etree.ElementTree as ET
import math

from char import Character
from util import XmlRetrieval


class Module:
    def __init__(self, skills, mod_name, filename_or_stream='module.xml'):
        """
        skills - A dictionary of skill, value pairs
                 e.g. {'Nanocircuitry': 0.05}
        module - The name of the module
                 e.g. "Militia Nanite Injector"
        filename_or_stream - If a string this represents an xml file containing
                             The module data.
                             If a StringIO object then the object will contain
                             the XML data and read directly
        """
        self.stats = {}
        self.name = mod_name
        self.skills = skills

        module_data = XmlRetrieval(filename_or_stream)
        # Properties include: slot_type, cpu, pg
        # Effecting_skills are the names of skills (list) which will adjust the
        # value of the Property, in a dictionary in the format
        # {'property':['skill', 'skill']}
        properties, effecting_skills = module_data.get_target(mod_name)
        self._add_stats(properties, effecting_skills)

    def show_stats(self):
        print self.name
        keys = self.stats.keys()
        keys.sort()
        for key in keys:
            print '{:<20} {:<15}'.format(key, self.stats[key]).strip()

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
                # Skills effect this property.
                # Get and apply the skill modifier.
                skill_list = effecting_skills[key]
                mod = _get_skill_modifier(skill_list)
                self.stats[key] = math.floor(properties[key] * (1 + mod))
            else:
                self.stats[key] = properties[key]


class Weapon(Module):
    """ Req dropsuit and fitting to test properly. """
    def __init__(self, skills, weapon_name, filename_or_stream='weapon.xml',
                 module_list=[]):
        self.stats = {}
        self.name = weapon_name
        self.skills = skills
        self.module_list = module_list

        weapon_data = XmlRetrieval(filename_or_stream)
        properties, effecting_skills = weapon_data.get_target(weapon_name)
        self._add_stats(properties, effecting_skills)
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
                    self.stats['damage'] = self.stats['damage'] \
                        * (1 + m.stats['damage'])
            except KeyError:
                # Module does not have a key 'enhances'
                # in its stats dictionary.
                pass


class ModuleLibrary(object):
    def __init__(self, filename_or_stream='module.xml'):
        self.module_data = XmlRetrieval(filename_or_stream)

        self.names = self.module_data.get_list()

    def get_names(self):
        """ Returns module names as a tuple. """
        return tuple(self.names)

    def get_parents(self):
        return self.module_data.get_parents()

    def get_children(self, parent):
        return self.module_data.get_children(parent)


class WeaponLibrary(ModuleLibrary):
    def __init__(self, filename_or_stream='module.xml'):
        super(WeaponLibrary, self).__init__(filename_or_stream)


if __name__ == '__main__':
    modlib = ModuleLibrary()
    print modlib.get_parents()
    print modlib.get_children('shields')
