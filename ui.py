from Tkinter import *
import ttk
import tkFont

from fitting import Fitting, DropsuitLibrary, Dropsuit, FittingLibrary
from module import ModuleLibrary, Module, WeaponLibrary, Weapon
from char import Character, CharacterLibrary, SkillLibrary

__application_name__ = 'Dust Fitting Tool'


class DftUi(Frame):
    """ This is the Main Window for the Dust Fitting Tool. """
    def __init__(self, parent):
        # Main window initialization.
        Frame.__init__(self, parent)
        self.parent = parent
        self.character_library = CharacterLibrary()
        self.fitting_library = FittingLibrary()
        self.weapon_library = WeaponLibrary()
        self.module_library = ModuleLibrary()
        self.current_char = Character('No Skills')
        self.current_fit = self.fitting_library.get_fitting(self.fitting_library.get_fitting_list()[0])

        # Call pertinent methods to display main window.
        self.menubar_main()
        self.combobox_character()
        self.combobox_fitting()
        self.tree_modules()
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
        fileMenu.add_command(label='New Character', command=self.add_character_window)
        editMenu = Menu(menubar)
        editMenu.add_command(label='Edit Character', command=self.edit_character_window)
        editMenu.add_command(label='Delete Character', command=self.delete_character_window)
        editMenu.add_command(label='Delete Fitting', command=self.delete_fitting_window)

        # Add the menus
        menubar.add_cascade(label='File', menu=fileMenu)
        menubar.add_cascade(label='Edit', menu=editMenu)

    def combobox_character(self):
        """ Displays and manages the character selection for the main window. """
        # Get known characters.  API calls or data retrieval here.
        character_names = self.character_library.get_character_list()

        # Creates the Combobox which has all known characters and automatically
        # selects the first character. Also other widgets.
        frm_character = Frame(self)
        lbl_character = Label(frm_character, text='Character:')
        self.cbx_character = ttk.Combobox(frm_character, values=character_names, width=14)
        self.cbx_character.set('No Skills')

        # Grid management.
        frm_character.grid(column=0, row=0)
        lbl_character.grid(column=0, row=0, sticky=NW, padx=3, pady=3)
        self.cbx_character.grid(column=1, row=0, sticky=NW, padx=3, pady=3)

        # Binding.
        self.cbx_character.bind('<<ComboboxSelected>>', self.change_character)

    def combobox_fitting(self):
        """ Displays and manages the current fitting to be displayed on the
        main window. """
        # Get known fits. API calls or data retrieval here.
        fitting_names = self.fitting_library.get_fitting_list()

        # Creates nessessary widgets.
        frm_fitting = Frame(self)
        lbl_fitting = Label(frm_fitting, text='Fitting:')
        self.cbx_fitting = ttk.Combobox(frm_fitting, values=fitting_names)
        self.cbx_fitting.set(self.current_fit.name)

        # Grid management.
        frm_fitting.grid(column=1, row=0)
        lbl_fitting.grid(column=2, row=0, sticky=NE, padx=3, pady=3)
        self.cbx_fitting.grid(column=3, row=0, sticky=NW, padx=3, pady=3)

        # Binding.
        self.cbx_fitting.bind('<<ComboboxSelected>>', self.change_fitting)

    def tree_modules(self):
        """ """
        frm_modules = Frame(self)
        self.tre_modules = ttk.Treeview(frm_modules, height=14, columns=('cpu', 'pg'))
        scb_modules = Scrollbar(frm_modules, orient=VERTICAL, command=self.tre_modules.yview)
        self.tre_modules.column('#0', width=150, minwidth=150)
        self.tre_modules.column('cpu', width=30, minwidth=30)
        self.tre_modules.column('pg', width=30, minwidth=30)
        self.tre_modules.heading('cpu', text='CPU')
        self.tre_modules.heading('pg', text='PG')
        for parent in self.weapon_library.get_parents():
            self.tre_modules.insert('', 'end', parent, text=parent, tag='ttk')
            for child in self.weapon_library.get_children(parent):
                self.tre_modules.insert(parent, 'end', child[0], text=child[0], tag='ttk')
                self.tre_modules.set(child[0], 'cpu', child[1])
                self.tre_modules.set(child[0], 'pg', child[2])
        for parent in self.module_library.get_parents():
            self.tre_modules.insert('', 'end', parent, text=parent, tag='ttk')
            for child in self.module_library.get_children(parent):
                self.tre_modules.insert(parent, 'end', child[0], text=child[0], tag='ttk')
                self.tre_modules.set(child[0], 'cpu', child[1])
                self.tre_modules.set(child[0], 'pg', child[2])

        # Grid management.
        frm_modules.grid(column=0, row=1)
        self.tre_modules.grid(column=0, row=0, sticky=NW, padx=3, pady=3)
        scb_modules.grid(column=1, row=0, sticky=NE+S, pady=4)
        self.tre_modules.configure(yscrollcommand=scb_modules.set)

        # Bindings
        self.tre_modules.bind('<Double-1>', self.add_module)

    def fitting_display(self):
        """ Displays all the current fitted modules. """
        # Create widgets
        frm_fitting = Frame(self)
        self.tre_fitting = ttk.Treeview(frm_fitting, height=14, columns=('name', 'cpu', 'pg'))
        self.tre_fitting.column('#0', width=30, minwidth=30)
        self.tre_fitting.column('name', width=300, minwidth=300)
        self.tre_fitting.column('cpu', width=30, minwidth=30)
        self.tre_fitting.column('pg', width=30, minwidth=30)
        self.tre_fitting.heading('name', text='Item Name')
        self.tre_fitting.heading('cpu', text='CPU')
        self.tre_fitting.heading('pg', text='PG')
        for i, item in enumerate(self.current_fit.get_all_modules()):
            self.tre_fitting.insert('', 'end', i+1, text=item[0])
            self.tre_fitting.set(i+1, 'name', item[1])
            self.tre_fitting.set(i+1, 'cpu', item[2])
            self.tre_fitting.set(i+1, 'pg', item[3])

        # Grid management
        frm_fitting.grid(column=1, row=1, sticky=W+E+N+S)
        self.tre_fitting.grid(column=0, row=0)

        # Bindings
        self.tre_fitting.bind('<Double-1>', self.remove_module)

    def stats_display(self, tab_id=0):
        """ """
        # Create widgets
        self.nbk_stats = ttk.Notebook(self, width=300)
        frm_overview = Frame(self.nbk_stats)
        frm_offense = Frame(self.nbk_stats)
        frm_defense = Frame(self.nbk_stats)
        frm_systems = Frame(self.nbk_stats)
        self.nbk_stats.add(frm_overview, text='Overview')
        self.nbk_stats.add(frm_offense, text='Offense')
        self.nbk_stats.add(frm_defense, text='Defense')
        self.nbk_stats.add(frm_systems, text='Systems')
        self.nbk_stats.select(tab_id)
        # Do overview stuff here
        for i, item in enumerate(self.current_fit.get_overview_abilities()):
            lbf = ttk.Labelframe(frm_overview, text=item[0])
            for j, stat in enumerate(item[1]):
                Label(lbf, text=stat[0]).grid(column=j%2, row=int(j/2), sticky=W, padx=10)
                Label(lbf, text=stat[1]).grid(column=j%2, row=int(j/2), sticky=E)
            lbf.grid(column=0, row=i, sticky=W+E+N+S)
            lbf.columnconfigure(0, minsize=147)
            lbf.columnconfigure(1, minsize=147)
        # Creates widgets for Offensive abilities.
        for i, item in enumerate(self.current_fit.get_offensive_abilities()):
            lbf = ttk.Labelframe(frm_offense, text=item[0])
            for j, stat in enumerate(item[1]):
                Label(lbf, text=stat[0]).grid(column=j%2, row=int(j/2), sticky=W, padx=10)
                Label(lbf, text=stat[1]).grid(column=j%2, row=int(j/2), sticky=E)
            lbf.grid(column=0, row=i, sticky=W+E+N+S)
            lbf.columnconfigure(0, minsize=147)
            lbf.columnconfigure(1, minsize=147)
        # Creates widgets for Defensive abilities.
        for i, item in enumerate(self.current_fit.get_defensive_abilities()):
            lbf = ttk.Labelframe(frm_defense, text=item[0])
            for j, stat in enumerate(item[1]):
                Label(lbf, text=stat[0]).grid(column=j%2, row=int(j/2), sticky=W, padx=10)
                Label(lbf, text=stat[1]).grid(column=j%2, row=int(j/2), sticky=E)
            lbf.grid(column=0, row=i, sticky=W+E+N+S)
            lbf.columnconfigure(0, minsize=147)
            lbf.columnconfigure(1, minsize=147)
        # Creates widgets for Systems/Equipment Abilities
        for i, item in enumerate(self.current_fit.get_systems_abilities()):
            lbf = ttk.Labelframe(frm_systems, text=item[0])
            for j, stat in enumerate(item[1]):
                Label(lbf, text=stat[0]).grid(column=j%2, row=int(j/2), sticky=W, padx=10)
                Label(lbf, text=stat[1]).grid(column=j%2, row=int(j/2), sticky=E)
            lbf.grid(column=0, row=i, sticky=W+E+N+S)
            lbf.columnconfigure(0, minsize=147)
            lbf.columnconfigure(1, minsize=147)

        # Grid management
        self.nbk_stats.grid(column=2, row=0, rowspan=3, sticky=W+E+N+S)

    def stats_display2(self):
        """ Displays fitting stats. """
        # Initialize variables.
        cpu_text = '%s/%s' % (self.current_fit.current_cpu, self.current_fit.max_cpu)
        pg_text = '%s/%s' % (self.current_fit.current_pg, self.current_fit.max_pg)
        cpu_over = self.current_fit.get_cpu_over()
        pg_over = self.current_fit.get_pg_over()

        # Creates the holding widgets.
        nbk_stats = ttk.Notebook(self)
        #nbk_stats.grid_propagate(False)
        frm_overview = Frame(self)
        nbk_stats.add(frm_overview, text='Overview')
        # Creates widgets for Dropsuit Type.
        lfr_dropsuit_type = ttk.Labelframe(frm_overview, text='Dropsuit Type:')
        lbl_dropsuit_type = Label(lfr_dropsuit_type, text=self.current_fit.ds_name).grid(column=0, row=0)
        # Creates widgets for Resources.
        lfr_resources = ttk.Labelframe(frm_overview, text='Resources')
        lbl_cpu1 = Label(lfr_resources, text='CPU:').grid(column=0, row=0, sticky=W)
        lbl_cpu2 = Label(lfr_resources, text=cpu_text).grid(column=1, row=0)
        lbl_pg1 = Label(lfr_resources, text='PG:').grid(column=2, row=0, sticky=W, padx=10)
        lbl_pg2 = Label(lfr_resources, text=pg_text).grid(column=3, row=0)
        lbl_cpu3 = Label(lfr_resources, text=cpu_over).grid(column=1, row=1, sticky=E)
        lbl_pg3 = Label(lfr_resources, text=pg_over).grid(column=3, row=1, sticky=E)
        lfr_resources.columnconfigure(0, minsize=30)
        lfr_resources.columnconfigure(1, minsize=90)
        lfr_resources.columnconfigure(2, minsize=20)
        lfr_resources.columnconfigure(3, minsize=75)
        # Creates widgets for main offenses.
        lfr_offenses = ttk.Labelframe(frm_overview, text='Main Offense')
        lbl_weapon = Label(lfr_offenses, text=self.current_fit.get_primary_weapon_name()).grid(column=0, row=0, columnspan=4)
        lbl_dmg1 = Label(lfr_offenses, text='Damage: ').grid(column=0, row=1, sticky=W)
        lbl_dmg2 = Label(lfr_offenses, text=self.current_fit.get_primary_stats('damage')).grid(column=1, row=1, sticky=E)
        lbl_rof1 = Label(lfr_offenses, text='RoF:').grid(column=2, row=1, sticky=W, padx=10)
        lbl_rof2 = Label(lfr_offenses, text=self.current_fit.get_primary_stats('rate_of_fire')).grid(column=3, row=1, sticky=E)
        lbl_dps1 = Label(lfr_offenses, text='DPS: ').grid(column=0, row=2, sticky=W)
        lbl_dps2 = Label(lfr_offenses, text=self.current_fit.get_primary_dps()).grid(column=1, row=2, sticky=E)
        lbl_dpm1 = Label(lfr_offenses, text='DPMag: ').grid(column=2, row=2, sticky=W, padx=10)
        lbl_dpm2 = Label(lfr_offenses, text=self.current_fit.get_primary_dpm()).grid(column=3, row=2, sticky=E)
        lfr_offenses.columnconfigure(0, minsize=60)
        lfr_offenses.columnconfigure(1, minsize=45)
        lfr_offenses.columnconfigure(2, minsize=60)
        lfr_offenses.columnconfigure(3, minsize=60)
        # Creates widgets for Defenses.
        lfr_defenses = ttk.Labelframe(frm_overview, text='Defenses')
        lbl_shield1 = Label(lfr_defenses, text='Shield HP:').grid(column=0, row=0, sticky=W)
        lbl_shield2 = Label(lfr_defenses, text=self.current_fit.get_shield_hp()).grid(column=1, row=0, sticky=E)
        lbl_recharge1 = Label(lfr_defenses, text='Recharge:').grid(column=2, row=0, sticky=W, padx=10)
        lbl_recharge2 = Label(lfr_defenses, text=self.current_fit.get_shield_recharge()).grid(column=3, row=0, sticky=E)
        lbl_armor1 = Label(lfr_defenses, text='Armor HP:').grid(column=0, row=1, sticky=W)
        lbl_armor2 = Label(lfr_defenses, text=self.current_fit.get_armor_hp()).grid(column=1, row=1, sticky=E)
        lbl_repair1 = Label(lfr_defenses, text='Repair:').grid(column=2, row=1, sticky=W, padx=10)
        lbl_repair2 = Label(lfr_defenses, text=self.current_fit.get_armor_repair_rate()).grid(column=3, row=1, sticky=E)
        lfr_defenses.columnconfigure(0, minsize=70)
        lfr_defenses.columnconfigure(1, minsize=50)
        lfr_defenses.columnconfigure(2, minsize=70)
        lfr_defenses.columnconfigure(3, minsize=35)
        # Creates widgets for Sensors.
        lfr_sensors = ttk.Labelframe(frm_overview, text='Sensors')
        lbl_prof1 = Label(lfr_sensors, text='Scan Profile: ').grid(column=0, row=0, sticky=W)
        lbl_prof2 = Label(lfr_sensors, text=self.current_fit.get_scan_profile()).grid(column=1, row=0, sticky=E)
        lbl_prec1 = Label(lfr_sensors, text='Scan Precision: ').grid(column=0, row=1, sticky=W)
        lbl_prec2 = Label(lfr_sensors, text=self.current_fit.get_scan_precision()).grid(column=1, row=1, sticky=E)
        lbl_radi1 = Label(lfr_sensors, text='Scan Radius: ').grid(column=0, row=2, sticky=W)
        lbl_radi2 = Label(lfr_sensors, text=self.current_fit.get_scan_radius()).grid(column=1, row=2, sticky=E)
        
        # Grid management.
        nbk_stats.grid(column=2, row=0, rowspan=3, sticky=W+E+N+S, padx=3, pady=3)
        lfr_dropsuit_type.grid(column=0, row=0, sticky=EW)
        lfr_resources.grid(column=0, row=1, sticky=EW)
        lfr_offenses.grid(column=0, row=2, sticky=EW)
        lfr_defenses.grid(column=0, row=3, sticky=EW)
        lfr_sensors.grid(column=0, row=4, sticky=EW)
        frm_overview.columnconfigure(0, minsize=250)

    def new_dropsuit_window(self):
        """ Handles creating a whole new dropsuit. """
        dropsuit_window = DropsuitWindow(self)

    def add_character_window(self):
        """ """
        add_character_window = AddCharacterWindow(self)

    def edit_character_window(self):
        """ Runs the class which deals with editing or adding a character. """
        character_edit_window = CharacterEditWindow(self, self.current_char.name)

    def delete_character_window(self):
        """ """
        delete_character = DeleteCharacterWindow(self)

    def delete_fitting_window(self):
        """ """
        delete_fitting = DeleteFittingWindow(self)

    def load_new_dropsuit(self, fitting_name, dropsuit):
        """ Called from the DropsuitWindow class.  This will load the dropsuit
        given by DropsuitWindow into the current fit. """
        # Change the fit to hold the selected dropsuit.
        self.current_fit = Fitting(fitting_name, self.current_char, dropsuit)
        self.fitting_library.save_fitting(self.current_fit)

        # Call the fitting_display and stats_display functions.
        self.combobox_fitting()
        self.fitting_display()
        self.stats_display()

    def add_module(self, *args):
        """ Adds a module to the fitting. """
        # Find what is selected.
        module_name = self.tre_modules.selection()[0]

        # Check to see if its a module or weapon, get the item requested.
        if module_name in self.module_library.get_names():
            self.current_fit.add_module(module_name)
        else:
            self.current_fit.add_weapon(module_name)

        # Save the changes.
        self.fitting_library.save_fitting(self.current_fit)

        # Display the change.
        self.fitting_display()
        self.stats_display(self.nbk_stats.index('current'))

    def remove_module(self, *args):
        """ Removes a module from the fitting. """
        # Find what is selected.
        tree_id = self.tre_fitting.selection()[0]
        module_name = self.tre_fitting.item(tree_id)['values'][0]

        self.current_fit.remove_module(module_name)

        # Save the changes.
        self.fitting_library.save_fitting(self.current_fit)

        # Display the change.
        self.fitting_display()
        self.stats_display(self.nbk_stats.index('current'))

    def change_character(self, *args):
        """ Changes the current characters for this fitting. """
        name = self.cbx_character.get()
        
        # Change the character
        self.current_char = self.character_library.get_character(name)
        self.current_fit.change_character(self.current_char)

        # Display the change.
        self.fitting_display()
        self.stats_display(self.nbk_stats.index('current'))

    def change_fitting(self, *args):
        """ Changes the current fitting. """
        fitting_name = self.cbx_fitting.get()

        # Change the current fitting.
        self.current_fit = self.fitting_library.get_fitting(fitting_name)

        # Display the change.
        self.fitting_display()
        self.stats_display(self.nbk_stats.index('current'))

    def update_character(self, character):
        """ Called by CharacterEditWindow.  This will update a character with
        the changed skills. """
        # Reload character data. THIS IS A HACK. Add better methods for changing and updating characters.
        self.character_library = CharacterLibrary()
        self.current_char = self.character_library.get_character(self.current_char.name)
        self.current_fit.change_character(self.current_char)

        # Display the changes.
        self.fitting_display()
        self.stats_display(self.nbk_stats.index('current'))
        # Reloads the character dropdown menu. Needed if a new character is added.
        self.combobox_character()

    def update_fitting(self, fitting):
        """ Called by DeleteFittingWindow. """
        self.fitting_library = FittingLibrary()

        # Selects a fitting and makes it active.
        misc_fitting = self.fitting_library.get_fitting_list()[0]
        self.current_fit = self.fitting_library.get_fitting(misc_fitting)

        # Display the changes.
        self.combobox_fitting()
        self.fitting_display()
        self.stats_display(self.nbk_stats.index('current'))
            

class DropsuitWindow(Frame):
    """ This handles the window for selecting a new dropsuit. """
    def __init__(self, parent):
        # Dropsuit Window initialization
        self.parent = parent
        self.window = Toplevel(self.parent)
        self.window.resizable(width=False, height=False)
        self.fitting_library = FittingLibrary()
        self.dropsuit_library = DropsuitLibrary()

        # Call pertinent methods for this window.
        self.menu_dropsuits()

    def menu_dropsuits(self):
        """ Handles the main menu items to select a dropsuit. """
        # Get known dropsuit names.
        self.fitting_name = StringVar()
        dropsuit_names = StringVar(value=self.dropsuit_library.get_names())

        # Creates the widgets needed for this menu.
        lbl_enter_name = Label(self.window, text='Enter Dropsuit Fitting Name')
        ent_fitting_name = Entry(self.window, textvariable=self.fitting_name, bg='white')
        lbl_dropsuits = Label(self.window, text='Select Dropsuit')
        self.lbx_dropsuits = Listbox(self.window, listvariable=dropsuit_names, height=10, bg='white')
        scb_dropsuits = Scrollbar(self.window, orient=VERTICAL, command=self.lbx_dropsuits.yview)
        btn_cancel = Button(self.window, text='Cancel', command=self.cancel)
        btn_okay = Button(self.window, text='Okay', command=self.okay)

        # Grid management.
        lbl_enter_name.grid(column=0, row=0, columnspan=2, sticky=W)
        ent_fitting_name.grid(column=0, row=1, columnspan=2, sticky=EW)
        lbl_dropsuits.grid(column=0, row=2, columnspan=2, sticky=(N, W), padx=3, pady=3)
        self.lbx_dropsuits.grid(column=0, row=3, sticky=EW, padx=3, pady=3)
        scb_dropsuits.grid(column=1, row=3, sticky=NE+S)
        self.lbx_dropsuits['yscrollcommand'] = scb_dropsuits.set
        btn_cancel.grid(column=0, row=4)
        btn_okay.grid(column=0, row=4, columnspan=2, sticky=E)

    def cancel(self, *args):
        """ """
        self.window.destroy()

    def okay(self, *args):
        # Find what is selected.
        listbox_index = self.lbx_dropsuits.curselection()
        dropsuit_name = self.lbx_dropsuits.get(listbox_index)

        # Pass the dropsuit to the main class DftUi
        self.parent.load_new_dropsuit(self.fitting_name.get(), dropsuit_name)

        self.window.destroy()


class AddCharacterWindow(Frame):
    """ Handles the window for adding a character.  Gets the characters name
    from the user, and opens the character edit window. """
    def __init__(self, parent):
        self.parent = parent
        self.window = Toplevel(self.parent)
        self.window.resizable(width=False, height=False)
        self.character_library = CharacterLibrary()

        # Call pertinent methods for this window.
        self.entrybox_name()

    def entrybox_name(self):
        """ Gets name from the user with an entrybox, adds Okay and Cancel buttons. """
        self.character_name = StringVar()

        lbl_enter_name = Label(self.window, text='Enter Character Name')
        ent_character_name = Entry(self.window, textvariable=self.character_name, bg='white')
        btn_cancel = Button(self.window, text='Cancel', command=self.cancel)
        btn_okay = Button(self.window, text='Okay', command=self.okay)

        # Grid management
        lbl_enter_name.grid(column=0, row=0, columnspan=2, sticky=W)
        ent_character_name.grid(column=0, row=1, columnspan=2, sticky=EW)
        btn_cancel.grid(column=0, row=2, sticky=E)
        btn_okay.grid(column=1, row=2, sticky=E)

    def cancel(self, *args):
        self.window.destroy()

    def okay(self, *args):
        """ Saves the blank character, opens the CharacterEditWindow, closes
        itself. """
        new_character = Character(self.character_name.get())
        self.character_library.save_character(new_character)
        character_edit_window = CharacterEditWindow(self.parent, self.character_name.get())
        self.window.destroy()


class CharacterEditWindow(Frame):
    """ This handles the window for editing a character. """
    def __init__(self, parent, character_name):
        # CharacterEdit Window initialization
        self.parent = parent
        self.window = Toplevel(self.parent)
        self.window.resizable(width=False, height=False)
        self.character_library = CharacterLibrary()
        self.skill_library = SkillLibrary()
        self.character = self.character_library.get_character(character_name)

        # Call pertinent methods for this window.
        self.combobox_character()
        self.tree_skills()
        self.select_skills()
        #self.menu_skills()

    def combobox_character(self):
        """ Displays and manages the character selection for the 
        CharacterEditWindow. """
        # Get known characters.  API calls or data retrieval here.
        character_names = self.character_library.get_character_list()

        # Creates the Combobox which has all known characters and automatically
        # selects the first character. Also other widgets.
        frm_character = Frame(self.window)
        lbl_character = Label(frm_character, text='Character:')
        self.cbx_character = ttk.Combobox(frm_character, values=character_names, width=14)
        self.cbx_character.set(self.character.name)

        # Grid management.
        frm_character.grid(column=0, row=0)
        lbl_character.grid(column=0, row=0, sticky=NW, padx=3, pady=3)
        self.cbx_character.grid(column=1, row=0, columnspan=2, sticky=NW, padx=3, pady=3)

        # Binding.
        self.cbx_character.bind('<<ComboboxSelected>>', self.change_character)

    def tree_skills(self):
        """ Shows available skills a character can use. """
        frm_skills = Frame(self.window)
        self.tre_skills = ttk.Treeview(frm_skills, height=14, columns=('level'))
        scb_skills = Scrollbar(frm_skills, orient=VERTICAL, command=self.tre_skills.yview)
        self.tre_skills.column('#0', width=250, minwidth=150)
        self.tre_skills.column('level', width=30, minwidth=30)
        self.tre_skills.heading('level', text='Lvl')
        for parent in self.skill_library.get_all_skill_categories():
            self.tre_skills.insert('', 'end', parent, text=parent, tag='ttk')
            for child in self.skill_library.get_skill_by_category(parent):
                self.tre_skills.insert(parent, 'end', child, text=child, tag=('ttk', child))
                self.tre_skills.set(child, 'level', self.character.get_skill_level(child))

        # Grid management.
        frm_skills.grid(column=0, row=1)
        self.tre_skills.grid(column=0, row=0, sticky=NW, padx=3, pady=3)
        scb_skills.grid(column=1, row=0, sticky=NE+S, pady=4)
        self.tre_skills.configure(yscrollcommand=scb_skills.set)

        # Deals with prerequisites and the text color
        self.color_skills()

        # Bindings
        self.tre_skills.bind('<<TreeviewSelect>>', self.current_skill_changed)

    def select_skills(self):
        """ Shows the modules which allow you select a skill level, and approve
        the changes to a character. """
        # Get the skill that selected.

        # Add widgets needed for this window
        frm_widgets = Frame(self.window)
        self.cbx_levels = ttk.Combobox(frm_widgets, values=(0, 1, 2, 3, 4, 5), width=8)
        btn_done = Button(frm_widgets, text='Done', command=self.done)

        # Grid management.
        frm_widgets.grid(column=0, row=2)
        self.cbx_levels.grid(column=0, row=1)
        btn_done.grid(column=1, row=1)

        # Bindings
        self.cbx_levels.bind('<<ComboboxSelected>>', self.change_skill)

    def current_skill_changed(self, *args):
        """ Called when an item in the listbox is selected. Updates the 
        combobox with the selected items level and the lbl_current_skill."""
        # Find the selected items level.
        current_skill = self.tre_skills.selection()[0]
        if current_skill not in self.character.get_all_skills():
            pass
        else: #
            self.cbx_levels.set(self.character.get_skill_level(current_skill))

    def change_skill(self, *args):
        """ Opens the dialog to select a skill level and changes it in the
        character class. """
        # Use the lbl_current_skill HACK to find the skill and use the combobox
        # to determine how to change the characters skill.
        skill = self.tre_skills.selection()[0]
        level = self.cbx_levels.get()

        # Change the skill in the character.
        self.character.set_skill(skill, int(level))

        # Saves changes to the character.
        self.character_library.save_character(self.character)

        # Update the level column for the skill
        self.tre_skills.set(skill, 'level', level)

        # Updates which skills have prerequisites met or unmet (black, red)
        for skill in self.skill_library.skill_dict.values():
            prereqs_met = True
            for prereq_skill, prereq_level in skill.prerequisites:
                if self.character.get_skill_level(prereq_skill) < prereq_level:
                    prereqs_met = False
            if prereqs_met:
                self.tre_skills.tag_configure(skill.name, foreground='black')
            else:
                self.tre_skills.tag_configure(skill.name, foreground='red')

    def color_skills(self):
        """ Moves through all known skills and colors the skills based on
            whether they have their prerequisites met or not. """
        for skill in self.skill_library.skill_dict.values():
            for prereq_name, prereq_level in skill.prerequisites:
                if self.character.get_skill_level(prereq_name) < prereq_level:
                    # Character does not have the prerequisites met to unlock
                    # this skill.
                    self.tre_skills.tag_configure(skill.name, foreground='red')
                    break
            else:
                # All prerequisites have been met.
                self.tre_skills.tag_configure(skill.name, foreground='black')

    def change_character(self, *args):
        """ Changes the character. """
        # Get the name of the character to change to.
        name = self.cbx_character.get()
        
        # Change the character
        self.character = self.character_library.get_character(name)

        # Display the change.
        self.tree_skills()

    def done(self, *args):
        """ Close window, call a function from the main UI to pass the modified
        character class. """
        self.parent.update_character(self.character)
        self.window.destroy()


class DeleteCharacterWindow(Frame):
    """ Handles the window for deleting a character. """
    def __init__(self, parent):
        self.parent = parent
        self.window = Toplevel(self.parent)
        self.window.resizable(width=False, height=False)
        self.character_library = CharacterLibrary()

        # Call pertinent methods for this window.
        self.combobox_select_name()

    def combobox_select_name(self):
        """ Gets name from the user with an entrybox, adds Okay and Cancel buttons. """
        character_list = self.character_library.get_character_list()

        lbl_enter_name = Label(self.window, text='Select character to delete')
        self.cbx_select_character = ttk.Combobox(self.window, values=character_list)
        btn_cancel = Button(self.window, text='Cancel', command=self.cancel)
        btn_delete = Button(self.window, text='Okay', command=self.delete)

        # Grid management
        lbl_enter_name.grid(column=0, row=0, columnspan=2, sticky=W)
        self.cbx_select_character.grid(column=0, row=1, columnspan=2, sticky=EW)
        btn_cancel.grid(column=0, row=2, sticky=E)
        btn_delete.grid(column=1, row=2, sticky=E)

    def cancel(self, *args):
        self.window.destroy()

    def delete(self, *args):
        """  """
        name = self.cbx_select_character.get()
        character = self.character_library.get_character(name)
        self.character_library.delete_character(character)

        # Update main window to show some other character.
        other_character = self.character_library.get_character_list()[0]
        self.parent.update_character(other_character)
        self.window.destroy()


class DeleteFittingWindow(Frame):
    """ Handles the window for deleting a Fitting. """
    def __init__(self, parent):
        self.parent = parent
        self.window = Toplevel(self.parent)
        self.window.resizable(width=False, height=False)
        self.fitting_library = FittingLibrary()

        # Call pertinent methods for this window.
        self.combobox_select_fitting()

    def combobox_select_fitting(self):
        """ Gets fitting from the user with an entrybox, adds Okay and Cancel buttons. """
        fitting_list = self.fitting_library.get_fitting_list()

        lbl_enter_name = Label(self.window, text='Select fitting to delete')
        self.cbx_select_fitting = ttk.Combobox(self.window, values=fitting_list)
        btn_cancel = Button(self.window, text='Cancel', command=self.cancel)
        btn_delete = Button(self.window, text='Okay', command=self.delete)

        # Grid management
        lbl_enter_name.grid(column=0, row=0, columnspan=2, sticky=W)
        self.cbx_select_fitting.grid(column=0, row=1, columnspan=2, sticky=EW)
        btn_cancel.grid(column=0, row=2, sticky=E)
        btn_delete.grid(column=1, row=2, sticky=E)

    def cancel(self, *args):
        self.window.destroy()

    def delete(self, *args):
        """  """
        name = self.cbx_select_fitting.get()
        fitting = self.fitting_library.get_fitting(name)
        self.fitting_library.delete_fitting(fitting)

        # Update main window to show some other fitting.
        other_fitting = self.fitting_library.get_fitting_list()[0]
        self.parent.update_fitting(other_fitting)
        self.window.destroy()


if __name__ == '__main__':
    root = Tk()

    root.title(__application_name__)
    root.resizable(width=False, height=False)

    app = DftUi(root)
    app.grid()

    root.mainloop()