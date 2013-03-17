#!/usr/bin/env python
#coding:utf-8

# Tests for the fitting module

import sys
import unittest
from cStringIO import StringIO
from fitting import (
    Dropsuit,
    DropsuitNotFound,
    DropsuitLibrary,
    Fitting
)
from char import Character
from module import ModuleNotExistException


DROPSUIT_XML = """
<data>
    <scout>
        <dropsuit name="Scout Type-I">
            <cpu effected_by="Circuitry">115</cpu>
            <pg effected_by="Combat Engineering">30</pg>
            <heavy_weapon>0</heavy_weapon>
            <light_weapon>1</light_weapon>
            <sidearm>1</sidearm>
            <grenade>1</grenade>
            <equipment>1</equipment>
            <hi_slot>1</hi_slot>
            <low_slot>2</low_slot>
            <shield_hp effected_by="Shield Control">100</shield_hp>
            <armor_hp effected_by="Field Mechanics">90</armor_hp>
            <shield_recharge effected_by="Shield Boost Systems">40</shield_recharge>
            <shield_recharge_delay>4.0</shield_recharge_delay>
            <shield_depleted_recharge_delay>10.0</shield_depleted_recharge_delay>
            <armor_repair_rate>0.0</armor_repair_rate>
            <movement_speed>5.6</movement_speed>
            <sprint_speed>7.8</sprint_speed>
            <sprint_duration>19.5</sprint_duration>
            <stamina effected_by="Endurance" effected_by2="Vigor">195.0</stamina>
            <stamina_recovery_rate effected_by="Vigor">18.0</stamina_recovery_rate>
            <scan_profile effected_by="Dropsuit Command" effected_by2="Profile Dampening">45</scan_profile>
            <scan_precision effected_by="Profile Analysis">45</scan_precision>
            <scan_radius effected_by="Long Range Scanning">25.0</scan_radius>
            <melee_damage effected_by="Hand To Hand Combat">135.0</melee_damage>
            <meta_level>1</meta_level>
        </dropsuit>
    </scout>
</data>
"""


class TestDropsuit(unittest.TestCase):
    """Tests for the Dropsuit class"""

    def setUp(self):
        """Setup data to test with"""
        self.char = Character('Test')

    def test_instantiation(self):
        """
        The instantiation of the class will load the data
        """
        test_data = StringIO(DROPSUIT_XML)
        test_dropsuit = Dropsuit(self.char, "Scout Type-I", test_data)

    def test_instantiation_not_found(self):
        """
        Test giving the name of a dropsuit that isn't in the data
        """
        test_data = StringIO(DROPSUIT_XML)
        with self.assertRaises(DropsuitNotFound):
            test_dropsuit = Dropsuit(self.char, "I dont exist", test_data)

    def test_show_stats(self):
        """
        Outputs the stats of a Dropsuit
        """
        test_data = StringIO(DROPSUIT_XML)
        test_dropsuit = Dropsuit(self.char, "Scout Type-I", test_data)
        # catch the stdout
        try:
            output = StringIO()
            temp_stdout = sys.stdout
            sys.stdout = output
            test_dropsuit.show_stats()
        finally:
            # it's important to put the stdout back how we found it
            sys.stdout = temp_stdout

        expected_output = """armor_hp 90.0
armor_repair_rate 0.0
cpu 115.0
equipment 1.0
grenade 1.0
heavy_weapon 0.0
hi_slot 1.0
light_weapon 1.0
low_slot 2.0
melee_damage 135.0
meta_level 1.0
movement_speed 5.6
pg 30.0
scan_precision 45.0
scan_profile 45.0
scan_radius 25.0
shield_depleted_recharge_delay 10.0
shield_hp 100.0
shield_recharge 40.0
shield_recharge_delay 4.0
sidearm 1.0
sprint_duration 19.5
sprint_speed 7.8
stamina 195.0
stamina_recovery_rate 18.0
"""
        output.seek(0)

        self.maxDiff = None
        self.assertEqual(expected_output, output.read())

    def test_skill_modifier(self):
        """
        The Circuitry modifier of 0.05 should reduce the cpu
        from 115 to 120.75
        """
        # set the characters Circuitry skill to 1
        self.char.set_skill('Circuitry',1)
        test_data = StringIO(DROPSUIT_XML)
        test_dropsuit = Dropsuit(self.char, "Scout Type-I", test_data)
        self.assertEqual(120.75, test_dropsuit.stats.get('cpu'))


class TestDropsuitLibrary(unittest.TestCase):
    """Tests for the DropsuitLibrary class"""

    def test_instantiation(self):
        """
        The instantiation of the class will load the data
        """
        test_data = StringIO(DROPSUIT_XML)
        test_dropsuit = DropsuitLibrary(test_data)

    def test_get_names(self):
        """
        Test fetching all the dropsuit names from the library
        """
        test_data = StringIO(DROPSUIT_XML)
        test_dropsuit = DropsuitLibrary(test_data)
        self.assertEquals(("Scout Type-I",), test_dropsuit.get_names())


# Please Note:
# The fitting tests are very basic because the module was not written
# With testing in mind and it is quite difficult to test it properly.
# More tests can be written over time but the fitting module really needs
# to be refactored so it is a little more Object Orientated and easier
# to test.


class TestFitting(unittest.TestCase):
    """Tests for the Fitting class"""

    def setUp(self):
        """Setup data to test with"""
        self.char = Character('Test')

    def test_instantiation(self):
        """
        The instantiation of the class will load the data
        """
        test_fitting = Fitting("Test Fitting", self.char, 'Scout Type-I')


class TestFittingAddModules(unittest.TestCase):
    """Tests for adding Modules to Fittings"""

    def setUp(self):
        """Setup data to test with"""
        self.char = Character('Test')
        self.fitting = Fitting("Test Fitting", self.char, 'Scout Type-I')

    def test_add(self):
        """Add a module to the fitting"""
        self.fitting.add_module('Militia Nanite Injector')
        all_modules = self.fitting.get_all_modules()

        # We should have the "Militia Nanite Injector" in the list of
        # fitted modules.... somewhere.
        # The return value of get_all_modules is not the best to manipulate
        # This test could be better if it returned objects instead of strings
        expected = "Militia Nanite Injector"
        self.assertIn(expected, ','.join(all_modules))

    def test_add_not_exist(self):
        """Add a module that doesn't exist to the fitting"""
        with self.assertRaises(ModuleNotExistException):
            self.fitting.add_module('Rocket Pants')

    def test_add_increases_cpu(self):
        """Adding a module should increase the used cpu"""
        current_cpu = self.fitting.current_cpu
        self.fitting.add_module('Militia Nanite Injector')
        new_cpu = self.fitting.current_cpu

        # This is not a great test.  Since we are not overriding the module data
        # and it's loading it from the xml file it could change without us knowing.
        # Therefore I'm only going to test that the cpu increases and I'm not going
        # to test the amount in which it increases... as this could break later
        self.assertGreater(new_cpu, current_cpu)

    def test_add_increases_pg(self):
        """Adding a module should increase the used pg"""
        current_pg = self.fitting.current_pg
        self.fitting.add_module('Militia Nanite Injector')
        new_pg = self.fitting.current_pg

        # This is not a great test.  Since we are not overriding the module data
        # and it's loading it from the xml file it could change without us knowing.
        # Therefore I'm only going to test that the pg increases and I'm not going
        # to test the amount in which it increases... as this could break later
        self.assertGreater(new_pg, current_pg)


class TestFittingRemoveModules(unittest.TestCase):
    """Tests for removing Modules from Fittings"""

    def setUp(self):
        """Setup data to test with"""
        self.char = Character('Test')
        self.fitting = Fitting("Test Fitting", self.char, 'Scout Type-I')
        self.fitting.add_module('Militia Nanite Injector')

    def test_remove(self):
        """Remove a module from the fitting"""
        self.fitting.remove_module("Militia Nanite Injector")
        all_modules = self.fitting.get_all_modules()

        expected = "Militia Nanite Injector"
        self.assertNotIn(expected, ','.join(all_modules))

    def test_remove_not_exist(self):
        """Remove a module that isn't even on the fitting"""
        # This should not error
        self.fitting.remove_module("Banana Gun")
        all_modules = self.fitting.get_all_modules()

        expected = "Banana Gun"
        self.assertNotIn(expected, ','.join(all_modules))


class TestFittingAddWeapon(unittest.TestCase):
    """Tests for adding Weapons to Fittings"""

    def setUp(self):
        """Setup data to test with"""
        self.char = Character('Test')
        self.fitting = Fitting("Test Fitting", self.char, 'Scout Type-I')

    def test_add(self):
        """Add a weapon to the fitting"""
        self.fitting.add_weapon('Assault Rifle')
        all_modules = self.fitting.get_all_modules()

        # We should have the "Assault Rifle" in the list of
        # fitted modules.... somewhere.
        # The return value of get_all_modules is not the best to manipulate
        # This test could be better if it returned objects instead of strings
        expected = "Assault Rifle"
        self.assertIn(expected, ','.join(all_modules))

    def test_add_not_exist(self):
        """Add a weapons that doesn't exist to the fitting"""
        with self.assertRaises(ModuleNotExistException):
            self.fitting.add_module('Spud Gun')

    def test_wrong_slot(self):
        """Add a weapon to a dropsuit that doesn't have a slot of that type"""
        # We'll add a heavy weapon to the Scout Suit which doesn't have a Heavy Slot
        # This should error but won't add the Heavy Weapon either
        self.fitting.add_weapon('Forge Gun')
        all_modules = self.fitting.get_all_modules()

        expected = "Forge Gun"
        self.assertNotIn(expected, ','.join(all_modules))


class TestFittingCPUOver(unittest.TestCase):
    """Tests for the CPU Over method"""

    def setUp(self):
        """Setup data to test with"""
        self.char = Character('Test')
        self.fitting = Fitting("Test Fitting", self.char, 'Scout Type-I')

    def test_zero(self):
        """If the max and used CPU are the same it should return zero"""
        self.fitting.max_cpu = 100.0
        self.fitting.current_cpu = 100.0
        self.assertEqual(None, self.fitting.get_cpu_over())

    def test_postive(self):
        """If the used CPU is higher than the max CPU"""
        self.fitting.max_cpu = 100.0
        self.fitting.current_cpu = 110.0
        self.assertEqual("10.0% over", self.fitting.get_cpu_over())

    def test_negative(self):
        """If the used CPU is lower than the max CPU we should get zero"""
        self.fitting.max_cpu = 100.0
        self.fitting.current_cpu = 90.0
        self.assertEqual(None, self.fitting.get_cpu_over())



class TestFittingPGOver(unittest.TestCase):
    """Tests for the PG Over method"""

    def setUp(self):
        """Setup data to test with"""
        self.char = Character('Test')
        self.fitting = Fitting("Test Fitting", self.char, 'Scout Type-I')

    def test_zero(self):
        """If the max and used PG are the same it should return zero"""
        self.fitting.max_pg = 100.0
        self.fitting.current_pg = 100.0
        self.assertEqual(None, self.fitting.get_pg_over())

    def test_postive(self):
        """If the used PG is higher than the max PG"""
        self.fitting.max_pg = 100.0
        self.fitting.current_pg = 110.0
        self.assertEqual("10.0% over", self.fitting.get_pg_over())

    def test_negative(self):
        """If the used PG is lower than the max PG we should get zero"""
        self.fitting.max_pg = 100.0
        self.fitting.current_pg = 90.0
        self.assertEqual(None, self.fitting.get_pg_over())


class TestFittingPrimaryWeapon(unittest.TestCase):
    """Tests for getting the primary Weapon from a Fitting"""

    def setUp(self):
        """Setup data to test with"""
        self.char = Character('Test')
        self.fitting = Fitting("Test Fitting", self.char, 'God Type-I')

    def test_light_primary_weapon(self):
        """If just a light weapon fitted then that is the primary weapon"""
        self.fitting.add_weapon('Assault Rifle')
        self.assertEqual('Assault Rifle', self.fitting.get_primary_weapon_name())

    def test_heavy_primary_weapon(self):
        """If just a heavy weapon fitted then that is the primary weapon"""
        self.fitting.add_weapon('Forge Gun')
        self.assertEqual('Forge Gun', self.fitting.get_primary_weapon_name())

    def test_heavy_and_light_primary_weapon(self):
        """If both heavy and light weapon fitted then heavy is the primary weapon"""
        self.fitting.add_weapon('Assault Rifle')
        self.fitting.add_weapon('Forge Gun')
        self.assertEqual('Forge Gun', self.fitting.get_primary_weapon_name())


class TestFittingPrimaryWeaponStat(unittest.TestCase):
    """Tests for getting stats from the primary Weapon from a Fitting"""

    def setUp(self):
        """Setup data to test with"""
        self.char = Character('Test')
        self.fitting = Fitting("Test Fitting", self.char, 'God Type-I')

    def test_light_primary_weapon(self):
        """If just a light weapon fitted then get the CPU"""
        self.fitting.add_weapon('Assault Rifle')
        # fix the cpu value so we can test it for a known value
        self.fitting.light_weapon[0].stats['cpu'] = 20
        self.assertEqual(20, self.fitting.get_primary_stats('cpu'))

    def test_heavy_primary_weapon(self):
        """If just a heavy weapon fitted then get the CPU"""
        self.fitting.add_weapon('Forge Gun')
        # fix the cpu value so we can test it for a known value
        self.fitting.heavy_weapon[0].stats['cpu'] = 40
        self.assertEqual(40, self.fitting.get_primary_stats('cpu'))

    def test_heavy_and_light_primary_weapon(self):
        """If both heavy and light weapon fitted then heavy is the primary weapon"""
        self.fitting.add_weapon('Assault Rifle')
        self.fitting.add_weapon('Forge Gun')
        self.assertEqual('Forge Gun', self.fitting.get_primary_weapon_name())


class TestFittingPrimaryDPS(unittest.TestCase):
    """Tests for getting primary weapon DPS"""

    def setUp(self):
        """Setup data to test with"""
        self.char = Character('Test')
        self.fitting = Fitting("Test Fitting", self.char, 'God Type-I')

    def test_light_primary_weapon(self):
        """If just a light weapon fitted then get the DPS"""
        self.fitting.add_weapon('Assault Rifle')
        # fix the stats values so we can test it for a known value
        self.fitting.light_weapon[0].stats['damage'] = 20.0
        self.fitting.light_weapon[0].stats['rate_of_fire'] = 600.0
        self.assertEqual(200.0, self.fitting.get_primary_dps())

    def test_heavy_primary_weapon(self):
        """If just a heavy weapon fitted then get the CPU"""
        self.fitting.add_weapon('Forge Gun')
        # fix the stats values so we can test it for a known value
        self.fitting.heavy_weapon[0].stats['damage'] = 100.0
        self.fitting.heavy_weapon[0].stats['rate_of_fire'] = 60.0
        self.assertEqual(100.0, self.fitting.get_primary_dps())

    def test_heavy_and_light_primary_weapon(self):
        """If both heavy and light weapon fitted then heavy is the primary weapon"""
        self.fitting.add_weapon('Assault Rifle')
        self.fitting.light_weapon[0].stats['damage'] = 20.0
        self.fitting.light_weapon[0].stats['rate_of_fire'] = 600.0
        self.fitting.add_weapon('Forge Gun')
        self.fitting.heavy_weapon[0].stats['damage'] = 100.0
        self.fitting.heavy_weapon[0].stats['rate_of_fire'] = 60.0
        self.assertEqual(100.0, self.fitting.get_primary_dps())


class TestFittingPrimaryDPM(unittest.TestCase):
    """Tests for getting primary weapon DPM"""

    def setUp(self):
        """Setup data to test with"""
        self.char = Character('Test')
        self.fitting = Fitting("Test Fitting", self.char, 'God Type-I')

    def test_light_primary_weapon(self):
        """If just a light weapon fitted then get the DPM"""
        self.fitting.add_weapon('Assault Rifle')
        # fix the stats values so we can test it for a known value
        self.fitting.light_weapon[0].stats['damage'] = 20.0
        self.fitting.light_weapon[0].stats['clip_size'] = 24.0
        self.assertEqual(480.0, self.fitting.get_primary_dpm())

    def test_heavy_primary_weapon(self):
        """If just a heavy weapon fitted then get the CPU"""
        self.fitting.add_weapon('Forge Gun')
        # fix the stats values so we can test it for a known value
        self.fitting.heavy_weapon[0].stats['damage'] = 100.0
        self.fitting.heavy_weapon[0].stats['clip_size'] = 3.0
        self.assertEqual(300.0, self.fitting.get_primary_dpm())

    def test_heavy_and_light_primary_weapon(self):
        """If both heavy and light weapon fitted then heavy is the primary weapon"""
        self.fitting.add_weapon('Assault Rifle')
        self.fitting.light_weapon[0].stats['damage'] = 20.0
        self.fitting.light_weapon[0].stats['clip_size'] = 24.0
        self.fitting.add_weapon('Forge Gun')
        self.fitting.heavy_weapon[0].stats['damage'] = 100.0
        self.fitting.heavy_weapon[0].stats['clip_size'] = 3.0
        self.assertEqual(300.0, self.fitting.get_primary_dpm())


class TestFittingAdditiveStat(unittest.TestCase):
    """Tests for getting an additive stat"""

    def setUp(self):
        """Setup data to test with"""
        self.char = Character('Test')
        self.fitting = Fitting("Test Fitting", self.char, 'God Type-I')

    def test_get_shield_hp(self):
        """Get the shield hp from the fitting"""
        self.fitting.dropsuit.stats['shield_hp'] = 200
        self.assertEqual(200, self.fitting.get_shield_hp())

    def test_get_shield_hp_with_module(self):
        """Add a module that adds to shield hp"""
        self.fitting.dropsuit.stats['shield_hp'] = 200
        self.fitting.add_module('Basic Shield Extender')
        # Poor test.  Relies on the values in the XML file
        # Should refactor this to enter a known value
        # At the time of writing the module adds 22
        self.assertEqual(222, self.fitting.get_shield_hp())


class TestFittingStackingStat(unittest.TestCase):
    """Tests for getting a stacking stat"""

    def setUp(self):
        """Setup data to test with"""
        self.char = Character('Test')
        self.fitting = Fitting("Test Fitting", self.char, 'God Type-I')

    def test_get_shield_recharge(self):
        """Get the shield hp from the fitting"""
        self.fitting.dropsuit.stats['shield_recharge'] = 0.5
        self.assertEqual(0.5, self.fitting.get_shield_recharge())

    def test_get_shield_hp_with_module(self):
        """Add a module that adds to shield hp"""
        self.fitting.dropsuit.stats['shield_recharge'] = 0.5
        self.fitting.add_module('Complex Shield Recharger')
        # Poor test.  Relies on the values in the XML file
        # Should refactor this to enter a known value
        # At the time of writing the module adds 0.42
        self.assertEqual(0.71, self.fitting.get_shield_recharge())

    def test_get_shield_hp_with_two_modules(self):
        """Add two modules that adds to shield hp. Stacking penalties come into play"""
        self.fitting.dropsuit.stats['shield_recharge'] = 0.5
        self.fitting.add_module('Complex Shield Recharger')
        self.fitting.add_module('Complex Shield Recharger')
        # Poor test.  Relies on the values in the XML file
        # Should refactor this to enter a known value
        # At the time of writing the module adds 0.42
        self.assertEqual(0.97, self.fitting.get_shield_recharge())

    def test_get_shield_hp_with_three_modules(self):
        """Add three modules that adds to shield hp. Stacking penalties come into play"""
        self.fitting.dropsuit.stats['shield_recharge'] = 0.5
        self.fitting.add_module('Complex Shield Recharger')
        self.fitting.add_module('Complex Shield Recharger')
        self.fitting.add_module('Complex Shield Recharger')
        # Poor test.  Relies on the values in the XML file
        # Should refactor this to enter a known value
        # At the time of writing the module adds 0.42
        self.assertEqual(1.20, self.fitting.get_shield_recharge())

    def test_get_shield_hp_with_four_modules(self):
        """Add four modules that adds to shield hp. Stacking penalties come into play"""
        self.fitting.dropsuit.stats['shield_recharge'] = 0.5
        self.fitting.add_module('Complex Shield Recharger')
        self.fitting.add_module('Complex Shield Recharger')
        self.fitting.add_module('Complex Shield Recharger')
        self.fitting.add_module('Complex Shield Recharger')
        # Poor test.  Relies on the values in the XML file
        # Should refactor this to enter a known value
        # At the time of writing the module adds 0.42
        self.assertEqual(1.34, self.fitting.get_shield_recharge())
