import os, sys
import pickle
import xml.etree.ElementTree as ET

#from char import Character, Skills
#import char

class XmlRetrieval:
    def __init__(self, file_name):
        self.file_name = get_file_loc(file_name)

    def get_target(self, target_name):
        """Will return the targets xml data. """
        # Create a dictionary of the targets properties and effecting skills.
        properties = {}
        effecting_skills = {}

        xml_tree = ET.parse(self.file_name)
        # Finds the desired target in xml file
        for child in xml_tree.getroot():
            if child.attrib['name'] == target_name:
                target = child
                break

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

        for child in xml_tree.getroot():
           names_list.append(child.get('name'))

        return names_list

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
    wea = XmlRetrieval('weapon.xml')
    ds = XmlRetrieval('dropsuit.xml')
    sk = XmlRetrieval('skills.xml')


    print mod.get_target('Complex Shield Extender')
    print wea.get_target('Assault Rifle')
    print ds.get_target('Assault Type-I')
    print sk.get_target('Weaponry')

    print mod.get_list()
    print wea.get_list()
    print ds.get_list()
    print sk.get_list()

    print '\n\n\n'

    #test1 = char.Character('Test1')
    char = DataRetrieval('characters.dat')
    print char.data
    #char.save_data(test1)