#!/usr/bin/env python
#coding:utf-8

# Unittests for the module module

import sys
import unittest
from mock import patch
from module import Module, Weapon
from char import Skills
from cStringIO import StringIO

MODULE_XML = """
<data>
    <nanite_injector>
        <module name="Militia Nanite Injector">
            <slot_type>equipment</slot_type>
            <cpu effected_by="Nanocircuitry">20</cpu>
            <pg>4</pg>
            <armor_repaired_on_revive>0.30</armor_repaired_on_revive>
        </module>
    </nanite_injector>
    <repair_tool>
        <module name="Militia Repair Tool">
            <slot_type>equipment</slot_type>
            <cpu>15</cpu>
            <pg>7</pg>
            <repair_rate_on_dropsuit>25</repair_rate_on_dropsuit>
            <repair_rate_on_vehicle>75</repair_rate_on_vehicle>
            <max_repair_distance>15</max_repair_distance>
            <max_targets>1</max_targets>
        </module>
    </repair_tool>
    <weapons_upgrades>
        <module name="Basic Light Damage Modifier">
            <slot_type>hi_slot</slot_type>
            <cpu>23</cpu>
            <pg>3</pg>
            <enhances>light_weapon</enhances>
            <damage>0.03</damage>
        </module>
    </weapons_upgrades>
</data>
"""


class TestModule(unittest.TestCase):
    """Tests for the Module class in the Module module.. hoho"""

    def test_instantiation(self):
        """
        The instantiation of the class will load the data
        """
        test_data = StringIO(MODULE_XML)
        test_skills = {'Nanocircuitry': -0.05}
        test_module = Module(test_skills, "Militia Nanite Injector", test_data)

    def test_skill_modifier(self):
        """
        The Nanocircuitry modifier of -0.05 should reduce the cpu
        from 20 to 19
        """
        test_data = StringIO(MODULE_XML)
        test_skills = {'Nanocircuitry': -0.05}
        test_module = Module(test_skills, "Militia Nanite Injector", test_data)
        self.assertEqual(19, test_module.get('cpu'))

    def test_skill_modifier_no_matching_skill(self):
        """
        The instantiate the Module but the skills passed in do not
        contain the skill referenced in the module.
        When this happens
        """
        test_data = StringIO(MODULE_XML)
        test_skills = {}
        test_module = Module(test_skills, "Militia Nanite Injector", test_data)
        self.assertEqual(20, test_module.get('cpu'))

    def test_show_stats(self):
        """
        Outputs the stats of a module
        """
        test_data = StringIO(MODULE_XML)
        test_skills = {}
        test_module = Module(test_skills, "Militia Nanite Injector", test_data)
        # catch the stdout
        try:
            output = StringIO()
            temp_stdout = sys.stdout
            sys.stdout = output
            test_module.show_stats()
        finally:
            # it's important to put the stdout back how we found it
            sys.stdout = temp_stdout

        expected_output = """Militia Nanite Injector
armor_repaired_on_revive 0.3
cpu                  20.0
pg                   4.0
slot_type            equipment
"""
        output.seek(0)
        self.assertEqual(expected_output, output.read())


WEAPON_XML = """
        <data>
            <grenades>
                <weapon name="Locus Grenade">
                    <slot_type>grenade</slot_type>
                    <cpu>9</cpu>
                    <pg>2</pg>
                    <splash_damage>400</splash_damage>
                    <blast_radius>6</blast_radius>
                    <max_ammo>3</max_ammo>
                </weapon>
            </grenades>
            <assault_rifles>
                <weapon name="Assault Rifle">
                    <slot_type>light_weapon</slot_type>
                    <cpu effected_by="Light Weapon Upgrades" effected_by2="Light Weapon Upgrades Proficiency">23</cpu>
                    <pg>3</pg>
                    <damage effected_by="Weaponry" effected_by2="Assault Rifle Proficiency">31</damage>
                    <rate_of_fire>750</rate_of_fire>
                    <reload_time effected_by="Light Weapon Rapid Reload" effected_by2="Light Weapon Rapid Reload Proficiency">3.0</reload_time>
                    <clip_size>60</clip_size>
                    <max_ammo effected_by="Light Weapon Capacity" effected_by2="Light Weapon Capacity Proficiency">300</max_ammo>
                    <accuracy_rating>56</accuracy_rating>
                    <max_range effected_by="Light Weapon Sharpshooter" effected_by2="Light Weapon Sharpshooter Proficiency">78</max_range>
                    <optimal_range_high effected_by="Light Weapon Sharpshooter" effected_by2="Light Weapon Sharpshooter Proficiency">35</optimal_range_high>
                    <optimal_range_low effected_by="Light Weapon Sharpshooter" effected_by2="Light Weapon Sharpshooter Proficiency">1</optimal_range_low>
                </weapon>
            </assault_rifles>
        </data>
        """


class TestWeapon(unittest.TestCase):
    """Tests for the Weapon class in the Module module"""

    def test_instantiation(self):
        """
        The instantiation of the class will load the data
        """
        test_data = StringIO(WEAPON_XML)
        test_skills = {'Light Weapon Upgrades': -0.05}
        test_weapon = Weapon(test_skills, "Assault Rifle", test_data)

    def test_skill_modifier(self):
        """
        The Light Weapon Upgrades modifier of -0.05 should reduce the cpu
        from 23 to 21
        """
        test_data = StringIO(WEAPON_XML)

        test_skills = {'Light Weapon Upgrades': -0.05}
        test_weapon = Weapon(test_skills, "Assault Rifle", test_data)
        self.assertEqual(21, test_weapon.get('cpu'))

    # TODO.. you haven't tested the effects of a module on weapons


if __name__=='__main__':
    unittest.main()