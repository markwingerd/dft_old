import os, sys
import pickle
import xml.etree.ElementTree as ET

class XmlRetrieval:
    def __init__(self, file_name):
        self.file_name = get_file_loc(file_name)

    def get_target(self, target_name):
        """Will return the targets xml data. """
        # Create a dictionary of the targets properties and effecting skills.
        properties = {}
        effecting_skills = {}

        xml_tree = ET.parse(self.file_name)
        target = xml_tree.find('.//*[@name="%s"]' % target_name)

        # Extracts targets data.
        for prop in target:
            # Get any xml attributes and save them to a dict for later use.
            if 'effected_by' in prop.attrib.keys():
                effecting_skills[prop.tag] = prop.attrib.values()
            # Get the properties and convert them to a float if needed.
            if self._is_number(prop.text):
                properties[prop.tag] = round(float(prop.text), 3)
            else:
                properties[prop.tag] = prop.text

        return (properties, effecting_skills)

    def get_list(self):
        """ Returns a list of all items in an xml file. """
        names_list = []

        xml_tree = ET.parse(self.file_name)

        parents = xml_tree.findall('.//*[@name]/..')

        for parent in parents:
            for child in parent:
                names_list.append(child.attrib['name'])

        return names_list

    def get_parents(self):
        """ Returns a list of all parents in the xml file. """
        parent_list = []

        xml_tree = ET.parse(self.file_name)
        parents = xml_tree.findall('.//*[@name]/..')
        for parent in parents:
            parent_list.append(parent.tag)

        return parent_list

    def get_children(self, target):
        """ Returns all the children of a given parent. """
        children_list = []

        xml_tree = ET.parse(self.file_name)
        parent = xml_tree.findall('.//%s/' % target)
        for child in parent:
            tup = (child.attrib['name'], child.find('cpu').text, child.find('pg').text)
            children_list.append(tup)

        return children_list

    def _is_number(self, s):
        """ Returns true if a string is a number. """
        try:
            float(s)
            return True
        except ValueError:
            return False


class DataRetrieval:
    def __init__(self, file_name):
        self.file_name = get_file_loc(file_name)

        self.data = {}

        self._load()

    def save_data(self, obj):
        """ Will save all the character classes. """
        self.data[obj.name] = obj

        data_file = open(self.file_name, 'wb')
        pickle.dump(self.data, data_file)
        data_file.close()

    def delete_data(self, obj):
        del self.data[obj.name]

        data_file = open(self.file_name, 'wb')
        pickle.dump(self.data, data_file)
        data_file.close()

    def _load(self):
        """ """
        try:
            data_file = open(self.file_name, 'rb')
            self.data = pickle.load(data_file)
        except IOError:
            print 'No data file found.'


def get_file_loc(file_name):
    """ Will return the path to the desired file depending on whether this
    is an executable or in development. """
    if getattr(sys, 'frozen', None):
        basedir = sys._MEIPASS + '/data/'
    else:
        basedir = os.path.dirname('data/')
    return os.path.join(basedir, file_name)
        

if __name__ == '__main__':
    mod = XmlRetrieval('module.xml')

    #ds._get_target('Assault Type-II')

    print mod.get_target('Nanite Injector')
    print mod.get_parents()
    print mod.get_children('nanite_injector')