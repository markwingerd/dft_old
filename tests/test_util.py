#!/usr/bin/env python
#coding:utf-8

# Tests for the util module

import sys
import unittest
from cStringIO import StringIO
from util import XmlRetrieval, ElementNotFoundException


TEST_MODULE_DATA = """
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


class TestXmlRetrieval(unittest.TestCase):
    """Tests for the XmlRetrieval class"""

    def test_instantiate_from_file(self):
        """Instantiate the class with a filename to read the data from"""
        # This just tests that an Exception is not raised
        obj = XmlRetrieval("skills.xml")
        self.assertTrue(obj)

    def test_instantiate_from_stream(self):
        """Instantiate the class with a data stream to read the data from"""
        # This just tests that an Exception is not raised
        xml = StringIO("<data />")
        obj = XmlRetrieval(xml)
        self.assertTrue(obj)

    def test_get_target_by_name(self):
        """
        The get_target method should find the element with the given name
        attribute
        """
        xml_data = '<data><item name="banana"></item></data>'
        xml = StringIO(xml_data)
        obj = XmlRetrieval(xml)
        properties, skills = obj.get_target('banana')
        self.assertEqual({}, properties)
        self.assertEqual({}, skills)

    def test_get_target_by_name_not_exist(self):
        """
        Test get_target method with a name that does not exist in
        the XML packet.
        This should raise a ElementNotFoundException
        """
        xml_data = '<data><item name="banana"></item></data>'
        xml = StringIO(xml_data)
        obj = XmlRetrieval(xml)
        with self.assertRaises(ElementNotFoundException):
            properties, skills = obj.get_target('apple')

    def test_get_target_with_properties(self):
        """
        The get_target method should find the element with the given name
        attribute and it's immediate children are returned as properties
        """
        xml_data = '<data><item name="banana"><colour>yellow</colour>' + \
            '</item></data>'
        xml = StringIO(xml_data)
        obj = XmlRetrieval(xml)
        properties, skills = obj.get_target('banana')
        self.assertEqual({'colour': 'yellow'}, properties)
        self.assertEqual({}, skills)

    def test_get_target_with_properties_and_skills(self):
        """
        The get_target method should find the element with the given name
        attribute and it's immediate children are returned as properties
        and the properties with the attribute 'effected_by' are returned as
        effecting skills
        """
        xml_data = '<data><item name="banana"><colour effected_by="light">' + \
            'yellow</colour></item></data>'
        xml = StringIO(xml_data)
        obj = XmlRetrieval(xml)
        properties, skills = obj.get_target('banana')
        self.assertEqual({'colour': ['light']}, skills)

    def test_get_target_with_properties_and_multiple_skills(self):
        """
        The get_target method should find the element with the given name
        attribute and it's immediate children are returned as properties
        and the properties with the attribute 'effected_by' are returned as
        effecting skills
        """
        xml_data = '<data><item name="banana"><colour effected_by="light" ' + \
            'effected_by2="moisture">yellow</colour></item></data>'
        xml = StringIO(xml_data)
        obj = XmlRetrieval(xml)
        properties, skills = obj.get_target('banana')
        self.assertEqual({'colour': ['moisture', 'light']}, skills)

    def test_get_list(self):
        """
        The get_list method should return a list of elements in the XML
        that have the name attribute set
        """

        xml = StringIO(TEST_MODULE_DATA)
        obj = XmlRetrieval(xml)
        names_list = obj.get_list()
        self.assertEqual(["Militia Nanite Injector",
                          "Militia Repair Tool",
                          "Basic Light Damage Modifier"], names_list)

    def test_get_list_none(self):
        """
        This test ensures that if there are no elements with the name attribute
        set the get_list method returns an empty list
        """
        xml_data = """<data></data>"""
        xml = StringIO(xml_data)
        obj = XmlRetrieval(xml)
        names_list = obj.get_list()
        self.assertEqual([], names_list)

    def test_get_parents(self):
        """
        The get_parents method will return the names of the parents to elements
        with the name attribute set
        """
        xml = StringIO(TEST_MODULE_DATA)
        obj = XmlRetrieval(xml)
        parents_list = obj.get_parents()
        self.assertEqual(["nanite_injector",
                          "repair_tool",
                          "weapons_upgrades"], parents_list)

    def test_get_parents_no_name(self):
        """
        Test the get_parents method which should not include parents for
        elements that don't have a name attribute.
        In this test the 'repair tool' category does not have a child with
        a name attribute so 'repair tool' should not be in the returned list.
        """
        xml_data = """
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
                <module>
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
        xml = StringIO(xml_data)
        obj = XmlRetrieval(xml)
        parents_list = obj.get_parents()
        self.assertNotIn("repair_tool", parents_list)

    def test_get_parents_none(self):
        """
        Test the get_parents method which should return an empty list if there
        are no elements with the name attribute
        """
        xml_data = """<data></data>"""
        xml = StringIO(xml_data)
        obj = XmlRetrieval(xml)
        parents_list = obj.get_parents()
        self.assertNotIn("repair_tool", parents_list)

    def test_get_children(self):
        """
        The get_children method will return (name, cpu, pg) tuple for all the
        children in a named category
        """
        xml = StringIO(TEST_MODULE_DATA)
        obj = XmlRetrieval(xml)
        children_list = obj.get_children('repair_tool')
        # pg and cpu are returned as strings
        self.assertEqual([("Militia Repair Tool", '15', '7')],
                         children_list)

    def test_get_children_multiples(self):
        """
        The get_children method will return (name, cpu, pg) tuple for all the
        children in a named category.
        This tests multiple children in the category
        """
        xml_data = """
        <data>
            <nanite_injector>
                <module name="Militia Nanite Injector">
                    <slot_type>equipment</slot_type>
                    <cpu effected_by="Nanocircuitry">20</cpu>
                    <pg>4</pg>
                    <armor_repaired_on_revive>0.30</armor_repaired_on_revive>
                </module>
                <module name="Nanite Injector">
                    <slot_type>equipment</slot_type>
                    <cpu effected_by="Nanocircuitry">10</cpu>
                    <pg>2</pg>
                    <armor_repaired_on_revive>0.50</armor_repaired_on_revive>
                </module>
            </nanite_injector>
        </data>
        """
        xml = StringIO(xml_data)
        obj = XmlRetrieval(xml)
        children_list = obj.get_children('nanite_injector')
        # pg and cpu are returned as strings
        self.assertEqual(
            [
                ("Militia Nanite Injector", '20', '4'),
                ("Nanite Injector", '10', '2'),
            ],
            children_list
        )

    def test_get_children_none(self):
        """
        Tests the get_children method will return an empty list when the given
        category contains no children
        """
        xml_data = """
        <data>
            <nanite_injector>
            </nanite_injector>
        </data>
        """
        xml = StringIO(xml_data)
        obj = XmlRetrieval(xml)
        children_list = obj.get_children('nanite_injector')
        # pg and cpu are returned as strings
        self.assertEqual([], children_list)

    def test_get_children_not_found(self):
        """
        Tests the get_children method will return an empty list when the given
        category does not exist
        """
        xml_data = """
        <data>
            <nanite_injector>
            </nanite_injector>
        </data>
        """
        xml = StringIO(xml_data)
        obj = XmlRetrieval(xml)
        children_list = obj.get_children('I do not exist')
        # pg and cpu are returned as strings
        self.assertEqual([], children_list)


if __name__ == '__main__':
    unittest.main()
