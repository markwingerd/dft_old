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


class TestFitting(unittest.TestCase):
    """Tests for the Fitting class"""

    def setUp(self):
        """Setup data to test with"""
        self.char = Character('Test')

    def test_instantiation(self):
        """
        The instantiation of the class will load the data
        """
        test_dropsuit = Fitting("Test Fitting", self.char, 'Scout Type-I')
