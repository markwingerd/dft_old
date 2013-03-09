#!/usr/bin/env python
#coding:utf-8

# Tests for the util module

import sys
import unittest
from cStringIO import StringIO
from util import XmlRetrieval, ElementNotFoundException


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
        # This just tests that an Exception is not raised
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
        # This just tests that an Exception is not raised
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
        # This just tests that an Exception is not raised
        xml_data = '<data><item name="banana"><colour>yellow</colour></item></data>'
        xml = StringIO(xml_data)
        obj = XmlRetrieval(xml)
        properties, skills = obj.get_target('banana')
        self.assertEqual({'colour':'yellow'}, properties)
        self.assertEqual({}, skills)

    def test_get_target_with_properties_and_skills(self):
        """
        The get_target method should find the element with the given name
        attribute and it's immediate children are returned as properties
        and the properties with the attribute 'effected_by' are returned as
        effecting skills
        """
        # This just tests that an Exception is not raised
        xml_data = '<data><item name="banana"><colour effected_by="light">yellow</colour></item></data>'
        xml = StringIO(xml_data)
        obj = XmlRetrieval(xml)
        properties, skills = obj.get_target('banana')
        self.assertEqual({'colour':['light']}, skills)

    def test_get_target_with_properties_and_multiple_skills(self):
        """
        The get_target method should find the element with the given name
        attribute and it's immediate children are returned as properties
        and the properties with the attribute 'effected_by' are returned as
        effecting skills
        """
        # This just tests that an Exception is not raised
        xml_data = '<data><item name="banana"><colour effected_by="light" effected_by2="moisture">yellow</colour></item></data>'
        xml = StringIO(xml_data)
        obj = XmlRetrieval(xml)
        properties, skills = obj.get_target('banana')
        self.assertEqual({'colour':['moisture', 'light']}, skills)



if __name__=='__main__':
    unittest.main()