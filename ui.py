from Tkinter import *
import ttk
import tkFont

from fitting import Fitting, DropsuitLibrary, Dropsuit
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
        self.weapon_library = WeaponLibrary()
        self.module_library = ModuleLibrary()
        self.current_char = Character('No Skills')
        self.current_fit = Fitting(self.current_char, 'Assault Type-I')

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
        fileMenu.add_command(label='New Character', command=self.add_character_window)
        editMenu = Menu(menubar)
        editMenu.add_command(label='Edit Character', command=self.edit_character_window)
        editMenu.add_command(label='Delete Character', command=self.delete_character_window)

        # Add the menus
        menubar.add_cascade(label='File', menu=fileMenu)
        menubar.add_cascade(label='Edit', menu=editMenu)

    def combobox_character(self):
        """ Displays and manages the character selection for the main window. """
        # Get known characters.  API calls or data retrieval here.
        character_names = self.character_library.get_character_list()

        # Creates the Combobox which has all known characters and automatically
        # selects the first character. Also other widgets.
        lbl_character = Label(self, text='Character:')
        self.cbx_character = ttk.Combobox(self, values=character_names, width=14)
        self.cbx_character.set('No Skills')

        # Grid management.
        lbl_character.grid(column=0, row=0, sticky=NW, padx=3, pady=3)
        self.cbx_character.grid(column=1, row=0, sticky=NW, padx=3, pady=3)

        # Binding.
        self.cbx_character.bind('<<ComboboxSelected>>', self.change_character)

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
        dropsuit_window = DropsuitWindow(self)

    def add_character_window(self):
        add_character_window = AddCharacterWindow(self)

    def edit_character_window(self):
        """ Runs the class which deals with editing or adding a character. """
        character_edit_window = CharacterEditWindow(self, self.current_char.name)

    def delete_character_window(self):
        delete_character = DeleteCharacterWindow(self)


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

    def change_character(self, *args):
        """ Changes the current characters for this fitting. """
        name = self.cbx_character.get()
        
        # Change the character
        self.current_char = self.character_library.get_character(name)
        self.current_fit.change_character(self.current_char)

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
        ent_character_name = Entry(self.window, textvariable=self.character_name)
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
        self.cbx_character.grid(column=1, row=0, sticky=NW, padx=3, pady=3)

        # Binding.
        self.cbx_character.bind('<<ComboboxSelected>>', self.change_character)

    def menu_skills(self):
        """ Shows available skills a character can use. """
        # Get known skills and their level, and convert them into a tuple for 
        # display.
        display = []
        skills_dict = self.character.get_all_skills()
        for name in skills_dict:
            display.append('{:<27.27} {:1}'.format(name, skills_dict[name]))
        skill_names = StringVar(value=tuple(display))
        # Initialize the lbl_current_skill variable.  THIS IS A HACK to allow 
        # the change_skill method to know which skill is selected.
        self.current_skill = StringVar(value=display[0][:27].rstrip())

        # Creates the widgets needed for this menu.
        lbl_skills = Label(self.window, text='Change Skills')
        self.lbx_skills = Listbox(self.window, listvariable=skill_names, width=30, height=20, font='TkFixedFont')
        lbl_current_skill = Label(self.window, textvariable=self.current_skill)
        self.cbx_levels = ttk.Combobox(self.window, values=(0, 1, 2, 3, 4, 5), width=8)
        btn_change_skill = Button(self.window, text='Change', command=self.change_skill)
        btn_done = Button(self.window, text='Done', command=self.done)
        # Initialize the first selection in lbx_skills.
        self.lbx_skills.selection_set(0)

        # Grid management.
        lbl_skills.grid(column=0, row=1, columnspan=2, sticky=NW, padx=3, pady=3)
        self.lbx_skills.grid(column=0, row=2, columnspan=2, sticky=NW, padx=3, pady=3)
        lbl_current_skill.grid(column=0, row=3, columnspan=2, sticky=W, padx=3, pady=3)
        self.cbx_levels.grid(column=0, row=4, sticky=E, padx=3, pady=3)
        btn_change_skill.grid(column=1, row=4, sticky=W, padx=3, pady=3)
        btn_done.grid(column=1, row=5, sticky=E, padx=3, pady=3)

        # Bindings
        self.lbx_skills.bind('<<ListboxSelect>>', self.current_skill_changed)

    def current_skill_changed(self, *args):
        """ Called when an item in the listbox is selected. Updates the 
        combobox with the selected items level and the lbl_current_skill."""
        # Find the selected items level.
        listbox_index = self.lbx_skills.curselection()
        listbox_string = self.lbx_skills.get(listbox_index)
        skill = listbox_string[:27].rstrip()
        level = listbox_string[28].rstrip()

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


if __name__ == '__main__':
    root = Tk()
    root.title(__application_name__)

    app = DftUi(root)
    app.pack()

    root.mainloop()