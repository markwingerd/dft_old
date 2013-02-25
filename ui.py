from Tkinter import *
import ttk
import tkFont

from fitting import Fitting, DropsuitLibrary, Dropsuit, FittingLibrary
from module import ModuleLibrary, Module, WeaponLibrary, Weapon
from char import Character, CharacterLibrary, Skills

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
        #self.menu_modules()
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

    def menu_modules(self):
        """ Displays and manages the module selection menus for the main window. """
        # Get known modules names.
        module_names = StringVar(value=self.weapon_library.get_names() + self.module_library.get_names())

        # Creates the widgets needed for this menu.
        lbl_modules = Label(self, text='Modules')
        self.lbx_modules = Listbox(self, listvariable=module_names, width=25, height=18, bg='white')
        scb_modules = Scrollbar(self, orient=VERTICAL, command=self.lbx_modules.yview)

        # Grid management.
        lbl_modules.grid(column=0, row=1, columnspan=2, sticky=NW, padx=3, pady=3)
        self.lbx_modules.grid(column=0, row=2, columnspan=2, sticky=NW, padx=3, pady=3)
        scb_modules.grid(column=1, row=2, sticky=NE+S, pady=4)
        self.lbx_modules['yscrollcommand'] = scb_modules.set

        # Bindings
        self.lbx_modules.bind('<Double-1>', self.add_module)

    def fitting_display(self):
        """ Displays all the current fitting information. """
        # Set variables.
        fitting_list = StringVar(value=self.current_fit.get_all_modules())

        # Creates the widgets needed for this display.
        frm_fitting_display = Frame(self, width=350, height=300)
        self.lbx_fitting = Listbox(frm_fitting_display, listvariable=fitting_list, width=48, height=20, font='TkFixedFont', bg='white')

        # Grid management.
        frm_fitting_display.grid(column=1, row=1, sticky=W+E+N+S)
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
        nbk_stats = ttk.Notebook(self, width=252, height=300)
        #nbk_stats.grid_propagate(False)
        frm_overview = Frame(self, width=250, height=300)
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
        self.stats_display()

    def remove_module(self, *args):
        """ Removes a module from the fitting. """
        # Find what is selected.
        listbox_index = self.lbx_fitting.curselection()
        module_name = self.lbx_fitting.get(listbox_index)

        self.current_fit.remove_module(module_name)

        # Save the changes.
        self.fitting_library.save_fitting(self.current_fit)

        # Display the change.
        self.fitting_display()
        self.stats_display()

    def change_character(self, *args):
        """ Changes the current characters for this fitting. """
        name = self.cbx_character.get()
        
        # Change the character
        self.current_char = self.character_library.get_character(name)
        self.current_fit.change_character(self.current_char)

        # Display the change.
        self.fitting_display()
        self.stats_display()

    def change_fitting(self, *args):
        """ Changes the current fitting. """
        fitting_name = self.cbx_fitting.get()

        # Change the current fitting.
        self.current_fit = self.fitting_library.get_fitting(fitting_name)

        # Display the change.
        self.fitting_display()
        self.stats_display()

    def update_character(self, character):
        """ Called by CharacterEditWindow.  This will update a character with
        the changed skills. """
        # Reload character data. THIS IS A HACK. Add better methods for changing and updating characters.
        self.character_library = CharacterLibrary()
        self.current_char = self.character_library.get_character(self.current_char.name)
        self.current_fit.change_character(self.current_char)

        # Display the changes.
        self.fitting_display()
        self.stats_display()
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
        self.stats_display()
            

class DropsuitWindow(Frame):
    """ This handles the window for selecting a new dropsuit. """
    def __init__(self, parent):
        # Dropsuit Window initialization
        self.parent = parent
        self.window = Toplevel(self.parent)
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
        lbl_enter_name = Label(self.window, text='Enter Character Name')
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
        self.character_library = CharacterLibrary()
        self.character = self.character_library.get_character(character_name)

        # Call pertinent methods for this window.
        self.combobox_character()
        self.menu_skills()

    def combobox_character(self):
        """ Displays and manages the character selection for the 
        CharacterEditWindow. """
        # Get known characters.  API calls or data retrieval here.
        character_names = self.character_library.get_character_list()

        # Creates the Combobox which has all known characters and automatically
        # selects the first character. Also other widgets.
        lbl_character = Label(self.window, text='Character:')
        self.cbx_character = ttk.Combobox(self.window, values=character_names, width=14)
        self.cbx_character.set(self.character.name)

        # Grid management.
        lbl_character.grid(column=0, row=0, sticky=NW, padx=3, pady=3)
        self.cbx_character.grid(column=1, row=0, columnspan=2, sticky=NW, padx=3, pady=3)

        # Binding.
        self.cbx_character.bind('<<ComboboxSelected>>', self.change_character)

    def tree_skills(self):
        """ Shows available skills a character can use. """
        pass

    def menu_skills(self):
        """ Shows available skills a character can use. """
        # Get known skills and their level, and convert them into a tuple for 
        # display.
        display = []
        skills_dict = self.character.get_all_skills()
        for name in skills_dict:
            display.append('{:<29.29} {:1}'.format(name, skills_dict[name]))
        self.skill_names = StringVar(value=tuple(display))
        # Initialize the lbl_current_skill variable.  THIS IS A HACK to allow 
        # the change_skill method to know which skill is selected.
        self.current_skill = StringVar(value=display[0][:29].rstrip())

        # Creates the widgets needed for this menu.
        lbl_skills = Label(self.window, text='Change Skills')
        self.lbx_skills = Listbox(self.window, listvariable=self.skill_names, width=33, height=20, font='TkFixedFont', bg='white')
        scb_skills = Scrollbar(self.window, orient=VERTICAL, command=self.lbx_skills.yview)
        lbl_current_skill = Label(self.window, textvariable=self.current_skill)
        self.cbx_levels = ttk.Combobox(self.window, values=(0, 1, 2, 3, 4, 5), width=8)
        btn_change_skill = Button(self.window, text='Change', command=self.change_skill)
        btn_done = Button(self.window, text='Done', command=self.done)
        # Initialize the first selection in lbx_skills.
        self.lbx_skills.selection_set(0)

        # Grid management.
        lbl_skills.grid(column=0, row=1, columnspan=3, sticky=NW, padx=3, pady=3)
        self.lbx_skills.grid(column=0, row=2, columnspan=3, sticky=NW, padx=3, pady=3)
        scb_skills.grid(column=2, row=2, sticky=NE+S)
        self.lbx_skills['yscrollcommand'] = scb_skills.set
        lbl_current_skill.grid(column=0, row=3, columnspan=3, sticky=W, padx=3, pady=3)
        self.cbx_levels.grid(column=0, row=4, sticky=E, padx=3, pady=3)
        btn_change_skill.grid(column=1, row=4, sticky=W, padx=3, pady=3)
        btn_done.grid(column=2, row=4, sticky=E, padx=3, pady=3)

        # Bindings
        self.lbx_skills.bind('<<ListboxSelect>>', self.current_skill_changed)

    def current_skill_changed(self, *args):
        """ Called when an item in the listbox is selected. Updates the 
        combobox with the selected items level and the lbl_current_skill."""
        # Find the selected items level.
        listbox_index = self.lbx_skills.curselection()
        listbox_string = self.lbx_skills.get(listbox_index)
        skill = listbox_string[:29].rstrip()
        level = listbox_string[30].rstrip()

        # Change the combobox selection and label.
        self.cbx_levels.set(level)
        self.current_skill.set(skill)

    def change_skill(self, *args):
        """ Opens the dialog to select a skill level and changes it in the
        character class. """
        # Use the lbl_current_skill HACK to find the skill and use the combobox
        # to determine how to change the characters skill.
        skill = self.current_skill.get()
        level = self.cbx_levels.get()

        # Change the skill in the character.
        self.character.set_skill(skill, int(level))

        # Saves changes to the character.
        self.character_library.save_character(self.character)

        # Update the listbox by calling its function. Reset the selected skill.
        self.current_skill.set('')
        self.menu_skills()

    def change_character(self, *args):
        """ Changes the character. """
        # Get the name of the character to change to.
        name = self.cbx_character.get()
        
        # Change the character
        self.character = self.character_library.get_character(name)

        # Display the change.
        self.menu_skills()

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
    root.geometry('833x329+300+300')
    root.resizable(width=False, height=False)

    app = DftUi(root)
    app.grid()

    root.mainloop()