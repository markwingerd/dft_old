#!/usr/bin/env python
#coding:utf-8

# Unittests for the module module

import sys
import unittest
from mock import patch
from module import Module
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
</data>
"""


class TestModule(unittest.TestCase):
    """Tests for the Module class in the Module module.. hoho"""

    @patch("util.get_file_loc")
    def test_instantiation(self, get_file_loc):
        """
        The instantiation of the class will load the data
        """
        # Patch the get_file_loc function to return a stream object
        # containing the Module XML.  This will work because ElementTree
        # will take either a filename or a file-like object
        get_file_loc.return_value = StringIO(MODULE_XML)

        test_skills = {'Nanocircuitry': -0.05}
        test_module = Module(test_skills, "Militia Nanite Injector")

    @patch("util.get_file_loc")
    def test_skill_modifier(self, get_file_loc):
        """
        The Nanocircuitry modifier of -0.05 should reduce the cpu
        from 20 to 19
        """
        # Patch the get_file_loc function to return a stream object
        # containing the Module XML.  This will work because ElementTree
        # will take either a filename or a file-like object
        get_file_loc.return_value = StringIO(MODULE_XML)

        test_skills = {'Nanocircuitry': -0.05}
        test_module = Module(test_skills, "Militia Nanite Injector")
        self.assertEqual(19, test_module.get('cpu'))

    @patch("util.get_file_loc")
    def test_skill_modifier_no_matching_skill(self, get_file_loc):
        """
        The instantiate the Module but the skills passed in do not
        contain the skill referenced in the module.
        When this happens
        """
        # Patch the get_file_loc function to return a stream object
        # containing the Module XML.  This will work because ElementTree
        # will take either a filename or a file-like object
        get_file_loc.return_value = StringIO(MODULE_XML)

        test_skills = {}
        test_module = Module(test_skills, "Militia Nanite Injector")
        self.assertEqual(20, test_module.get('cpu'))

    @patch("util.get_file_loc")
    def test_show_stats(self, get_file_loc):
        """
        Outputs the stats of a module
        """
        # Patch the get_file_loc function to return a stream object
        # containing the Module XML.  This will work because ElementTree
        # will take either a filename or a file-like object
        get_file_loc.return_value = StringIO(MODULE_XML)

        test_skills = {}
        test_module = Module(test_skills, "Militia Nanite Injector")
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


if __name__=='__main__':
    unittest.main()