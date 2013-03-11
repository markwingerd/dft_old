import os, sys
import pickle
import xml.etree.ElementTree as ET
import cStringIO


class ElementNotFoundException(Exception):
    """
    Exception raised when looking for an Element with a given
    name attribute and it is not found
    """
    pass


class XmlRetrieval:
    def __init__(self, data):
        """
        Data can be a StingIO object or a string containing the relative
        path to the data file
        """
        if isinstance(data, cStringIO.InputType):
            self.data = data
        else:
            # If it's not a StringIO we will assume it's a filepath
            self.data = get_file_loc(data)

    def get_target(self, target_name):
        """Will return the targets xml data. """
        # Create a dictionary of the targets properties and effecting skills.
        properties = {}
        effecting_skills = {}

        # if we have a stream, wind it back to the beginning because
        # if it's already been read from then there will be nothing
        # left to read
        if isinstance(self.data, cStringIO.InputType):
            self.data.seek(0)

        xml_tree = ET.parse(self.data)
        target = xml_tree.find('.//*[@name="%s"]' % target_name)

        if target is None:
            raise ElementNotFoundException

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

        # if we have a stream, wind it back to the beginning because
        # if it's already been read from then there will be nothing
        # left to read
        if isinstance(self.data, cStringIO.InputType):
            self.data.seek(0)

        xml_tree = ET.parse(self.data)

        parents = xml_tree.findall('.//*[@name]/..')

        for parent in parents:
            for child in parent:
                names_list.append(child.attrib['name'])

        return names_list

    def get_parents(self):
        """ Returns a list of all parents in the xml file. """
        parent_list = []

        # if we have a stream, wind it back to the beginning because
        # if it's already been read from then there will be nothing
        # left to read
        if isinstance(self.data, cStringIO.InputType):
            self.data.seek(0)

        xml_tree = ET.parse(self.data)
        parents = xml_tree.findall('.//*[@name]/..')
        for parent in parents:
            parent_list.append(parent.tag)

        return parent_list

    def get_children(self, target):
        """ Returns all the children of a given parent. """
        children_list = []

        # if we have a stream, wind it back to the beginning because
        # if it's already been read from then there will be nothing
        # left to read
        if isinstance(self.data, cStringIO.InputType):
            self.data.seek(0)

        xml_tree = ET.parse(self.data)
        parent = xml_tree.findall('.//%s/' % target)
        for child in parent:
            tup = (child.attrib['name'],
                   child.find('cpu').text,
                   child.find('pg').text)
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
        try:
            del self.data[obj.name]
        except KeyError:
            # Can't delete it if it isn't there
            return

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
    #TODO: This duplicates a method in char._get_file_loc... needs refactoring
    if getattr(sys, 'frozen', None):
        basedir = sys._MEIPASS + '/data/'
    else:
        basedir = os.path.join(os.path.dirname(__file__),'data')
    return os.path.join(basedir, file_name)


if __name__ == '__main__':
    mod = XmlRetrieval('module.xml')

    #ds._get_target('Assault Type-II')

    print mod.get_target('Nanite Injector')
    print mod.get_parents()
    print mod.get_children('nanite_injector')