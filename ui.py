from Tkinter import *
import ttk
import tkFont

from fitting import Fitting, DropsuitLibrary, Dropsuit
from module import ModuleLibrary, Module, WeaponLibrary, Weapon
from char import Character

__application_name__ = 'Dust Fitting Tool'


class DftUi(Frame):
    """ This is the Main Window for the Dust Fitting Tool. """
    def __init__(self, parent):
        # Main window initialization.
        Frame.__init__(self, parent)
        self.parent = parent
        self.current_char = Character()
        self.current_char.set_skill('Dropsuit Command', 1)
        self.current_char.set_skill('Profile Dampening', 0)
        self.current_char.set_skill('Nanocircuitry', 1)
        self.current_char.set_skill('Circuitry', 4)
        self.current_char.set_skill('Combat Engineering', 2)
        self.current_char.set_skill('Vigor', 0)
        self.current_char.set_skill('Endurance', 0)
        self.current_char.set_skill('Shield Boost Systems', 3)
        self.current_char.set_skill('Shield Enhancements', 4)
        self.current_char.set_skill('Light Weapon Sharpshooter', 4)
        self.current_char.set_skill('Weaponry', 5)
        self.current_char.set_skill('Assault Rifle Proficiency', 2)
        self.current_fit = Fitting(self.current_char, 'Assault Type-I')
        self.weapon_library = WeaponLibrary()
        self.module_library = ModuleLibrary()

        # Call pertinent methods to display main window.
        self.menubar_main()
        self.combobox_character()
        self.combobox_fitting()
        self.menu_modules()
        self.fitting_display()
        self.stats_display()

    def menubar_main(self):
        """ Displays and manages the upper menubar. """
        # Initial configurations.
        menubar = Menu(self.parent)
        self.parent.config(menu=menubar)
        self.parent.option_add('*tearOff', False)

        # First menu contents
        fileMenu = Menu(menubar)
        fileMenu.add_command(label='New Dropsuit', command=self.new_dropsuit_window)
        fileMenu.add_command(label='New Vehicle')
        fileMenu.add_command(label='New Character')

        # Add the menus
        menubar.add_cascade(label='File', menu=fileMenu)

    def combobox_character(self):
        """ Displays and manages the character selection for the main window. """
        # Get known characters.  API calls or data retrieval here.
        character_names = ('Reimus Klinsman', 'Richard C Mongler', 'Test')

        # Creates the Combobox which has all known characters and automatically
        # selects the first character. Also other widgets.
        lbl_character = Label(self, text='Character:')
        cbx_character = ttk.Combobox(self, values=character_names, width=14)
        cbx_character.current(0)

        # Grid management.
        lbl_character.grid(column=0, row=0, sticky=NW, padx=3, pady=3)
        cbx_character.grid(column=1, row=0, sticky=NW, padx=3, pady=3)

    def combobox_fitting(self):
        """ Displays and manages the current fitting to be displayed on the
        main window. """
        # Get known fits. API calls or data retrieval here.
        fitting_names = ('Testing fit', )

        # Creates nessessary widgets.
        lbl_fitting = Label(self, text='Fitting:')
        cbx_fitting = ttk.Combobox(self, values=fitting_names)
        cbx_fitting.current(0)

        # Grid management.
        lbl_fitting.grid(column=2, row=0, sticky=NE, padx=3, pady=3)
        cbx_fitting.grid(column=3, row=0, sticky=NW, padx=3, pady=3)

    def menu_modules(self):
        """ Displays and manages the module selection menus for the main window. """
        # Get known modules names.
        module_names = StringVar(value=self.weapon_library.get_names() + self.module_library.get_names())

        # Creates the widgets needed for this menu.
        lbl_modules = Label(self, text='Modules')
        self.lbx_modules = Listbox(self, listvariable=module_names, width=25, height=20)

        # Grid management.
        lbl_modules.grid(column=0, row=1, columnspan=2, sticky=NW, padx=3, pady=3)
        self.lbx_modules.grid(column=0, row=2, columnspan=2, sticky=NW, padx=3, pady=3)

        # Bindings
        self.lbx_modules.bind('<Double-1>', self.add_module)

    def fitting_display(self):
        """ Displays all the current fitting information. """
        # Set variables.
        fitting_list = StringVar(value=self.current_fit.get_all_modules())

        # Creates the widgets needed for this display.
        frm_fitting = Frame(self, width=350, height=300, borderwidth=2, relief='sunken')
        frm_fitting.grid_propagate(False) #Forces the frame to keep its size.
        self.lbx_fitting = Listbox(frm_fitting, listvariable=fitting_list, width=48, height=20, font='TkFixedFont')
        self.lbx_fitting.grid_propagate(False)

        # Grid management.
        frm_fitting.grid(column=2, row=1, columnspan=2, rowspan=2, sticky=W+E+N+S, padx=3, pady=3)
        self.lbx_fitting.grid(column=0, row=0, sticky=W+E+N+S)

        # Bindings
        self.lbx_fitting.bind('<Double-1>', self.remove_module)

    def stats_display(self):
        """ Displays fitting stats. """
        # Initialize variables.
        cpu_text = '%s/%s' % (self.current_fit.current_cpu, self.current_fit.max_cpu)
        pg_text = '%s/%s' % (self.current_fit.current_pg, self.current_fit.max_pg)
        cpu_over = self.current_fit.get_cpu_over()
        pg_over = self.current_fit.get_pg_over()

        # Creates the holding widgets.
        nbk_stats = ttk.Notebook(self, width=250, height=300)
        nbk_stats.grid_propagate(False)
        frm_overview = Frame(self, width=250, height=300)
        nbk_stats.add(frm_overview, text='Overview')
        # Creates widgets for Resources.
        lfr_resources = ttk.Labelframe(frm_overview, text='Resources')
        lbl_cpu1 = Label(lfr_resources, text='CPU:')
        lbl_cpu2 = Label(lfr_resources, text=cpu_text)
        lbl_cpu3 = Label(lfr_resources, text=cpu_over)
        lbl_pg1 = Label(lfr_resources, text='PG:')
        lbl_pg2 = Label(lfr_resources, text=pg_text)
        lbl_pg3 = Label(lfr_resources, text=pg_over)
        # Creates widgets for Defenses.
        lfr_defenses = ttk.Labelframe(frm_overview, text='Defenses')
        lbl_shield1 = Label(lfr_defenses, text='Shield HP:')
        lbl_shield2 = Label(lfr_defenses, text=self.current_fit.get_shield_hp())
        lbl_recharge1 = Label(lfr_defenses, text='Recharge:')
        lbl_recharge2 = Label(lfr_defenses, text=self.current_fit.get_shield_recharge())
        lbl_armor1 = Label(lfr_defenses, text='Armor HP:')
        lbl_armor2 = Label(lfr_defenses, text=self.current_fit.get_armor_hp())
        lbl_repair1 = Label(lfr_defenses, text='Repair:')
        lbl_repair2 = Label(lfr_defenses, text=self.current_fit.get_armor_repair_rate())

        # Grid management.
        nbk_stats.grid(column=4, row=0, rowspan=3, sticky=W+E+N+S, padx=3, pady=3)
        # Resource grid management.
        lfr_resources.grid(column=0, row=0, sticky=EW)
        lbl_cpu1.grid(column=0, row=0, sticky=W)
        lbl_cpu2.grid(column=1, row=0)
        lbl_cpu3.grid(column=2, row=0, sticky=E)
        lbl_pg1.grid(column=0, row=1, sticky=W)
        lbl_pg2.grid(column=1, row=1)
        lbl_pg3.grid(column=2, row=1, sticky=E)
        # Defenses grid management.
        lfr_defenses.grid(column=0, row=1, sticky=EW)
        lbl_shield1.grid(column=0, row=0, sticky=W)
        lbl_shield2.grid(column=1, row=0, sticky=E)
        lbl_recharge1.grid(column=0, row=1, sticky=W)
        lbl_recharge2.grid(column=1, row=1, sticky=E)
        lbl_armor1.grid(column=0, row=2, sticky=W)
        lbl_armor2.grid(column=1, row=2, sticky=E)
        lbl_repair1.grid(column=0, row=3, sticky=W)
        lbl_repair2.grid(column=1, row=3, sticky=E)

    def new_dropsuit_window(self):
        """ Handles creating a whole new dropsuit. """
        self.dropsuit_window = DropsuitWindow(self)

    def load_new_dropsuit(self, dropsuit):
        """ Called from the DropsuitWindow class.  This will load the dropsuit
        given by DropsuitWindow into the current fit. """
        # Change the fit to hold the selected dropsuit.
        self.current_fit = Fitting(self.current_char, dropsuit)

        # Call the fitting_display and stats_display functions.
        self.fitting_display()
        self.stats_display()

    def add_module(self, *args):
        """ Adds a module to the fitting. """
        # Find what is selected.
        listbox_index = self.lbx_modules.curselection()
        module_name = self.lbx_modules.get(listbox_index)

        # Check to see if its a module or weapon, get the item requested.
        if module_name in self.module_library.get_names():
            self.current_fit.add_module(module_name)
        else:
            self.current_fit.add_weapon(module_name)

        # Display the change.
        self.fitting_display()
        self.stats_display()

    def remove_module(self, *args):
        """ Removes a module from the fitting. """
        # Find what is selected.
        listbox_index = self.lbx_fitting.curselection()
        module_name = self.lbx_fitting.get(listbox_index)

        self.current_fit.remove_module(module_name)

        # Display the change.
        self.fitting_display()
        self.stats_display()

class DropsuitWindow(Frame):
    """ This handles the window for selecting a new dropsuit. """
    def __init__(self, parent):
        # Dropsuit Window initialization
        self.parent = parent
        self.window = Toplevel(self.parent)
        self.dropsuit_library = DropsuitLibrary()

        # Call pertinent methods for this window.
        self.menu_dropsuits()

    def menu_dropsuits(self):
        """ Handles the main menu items to select a dropsuit. """
        # Get known dropsuit names.
        dropsuit_names = StringVar(value=self.dropsuit_library.get_names())

        # Creates the widgets needed for this menu.
        lbl_dropsuits = Label(self.window, text='Select Dropsuit')
        self.lbx_dropsuits = Listbox(self.window, listvariable=dropsuit_names, height=10)

        # Grid management.
        lbl_dropsuits.grid(column=0, row=0, sticky=(N, W), padx=3, pady=3)
        self.lbx_dropsuits.grid(column=0, row=1, sticky=(W), padx=3, pady=3)

        # Bindings
        self.lbx_dropsuits.bind('<Double-1>', self.select_dropsuit)

    def select_dropsuit(self, *args):
        # Find what is selected.
        listbox_index = self.lbx_dropsuits.curselection()
        dropsuit_name = self.lbx_dropsuits.get(listbox_index)

        # Pass the dropsuit to the main class DftUi
        self.parent.load_new_dropsuit(dropsuit_name)


if __name__ == '__main__':
    root = Tk()
    root.title(__application_name__)

    app = DftUi(root)
    app.pack()

    root.mainloop()