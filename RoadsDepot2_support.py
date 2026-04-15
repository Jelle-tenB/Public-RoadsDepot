#! /usr/bin/env python3
#  -*- coding: utf-8 -*-

import sys
import tkinter as tk
from tkinter.messagebox import showerror
from tkinter import filedialog, font
from os import path as _path, getenv
import logging
from logging.handlers import RotatingFileHandler

from dotenv import load_dotenv

import RoadsDepot2
from imports import (
    open_db_readonly,
    open_db_write,
    test_connection,
    check_log_exists,
    create_new_log,
    open_old_logdb,
    make_backup,
    shared,
    DESKTOPS_DICT, CATEGORIE_COLUMNS, CATEGORIE_DICT)

_debug = True # False to eliminate debug printing from callback functions.

# Toplevel1 is also Toplevel0. This is the main page of the app.
# Toplevel2 is the Login page.
# Toplevel3 is the Log-database Login page.
# Toplevel4 is only show once every year to make a new Log-database

from pathlib import Path

LOG_DIR = r".\logs"
LOG_FILE = LOG_DIR + r"\roadsdepot.log"

logger = logging.getLogger("RoadsDepot")
logger.setLevel(logging.DEBUG)

handler = RotatingFileHandler(
    LOG_FILE,
    maxBytes=2_000_000,
    backupCount=5,
    encoding="utf-8",
)
handler.setFormatter(
    logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s")
)
logger.addHandler(handler)

def log_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    logger.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))

def main(*args):
    '''Main entry point for the application.'''
    global root
    sys.excepthook = log_exception # Set the custom exception handler
    root = tk.Tk()
    root.report_callback_exception = log_exception
    root.protocol( 'WM_DELETE_WINDOW' , root.destroy)
    root.iconphoto(True, tk.PhotoImage(file=resource_path("logopng.png")))
    # Creates a toplevel widget.
    global _top1, _w1
    _top1 = root
    _w1 = RoadsDepot2.Toplevel0(_top1)
    # Creates a toplevel widget.
    global _top2, _w2
    _top2 = tk.Toplevel(root)
    _w2 = RoadsDepot2.Toplevel2(_top2)
    _top2.protocol( 'WM_DELETE_WINDOW' , root.destroy)
    # Creates a toplevel widget.
    global _top3, _w3
    _top3 = tk.Toplevel(root)
    _w3 = RoadsDepot2.Toplevel3(_top3)
    # Creates a toplevel widget.
    global _top4, _w4
    _top4 = tk.Toplevel(root)
    _w4 = RoadsDepot2.Toplevel4(_top4)
    _top4.protocol( 'WM_DELETE_WINDOW' , root.destroy)
    __init__()
    root.mainloop()

## SELF MADE FUNCTIONS ##########################################
def __init__():
    """Initializes the application by setting up the GUI and loading necessary data."""
    _w1.Scrolledtreeview1.configure(show="headings")
    _top1.withdraw()
    _top3.withdraw()
    _top4.withdraw()
    _top2.deiconify()
    _w2.wachtwoordEntry.configure(show="*")
    _w3.dbwwEntry.configure(show="*")
    _w2.usernameEntry.focus_set()
    # Removing Log buttons for now.
    # _w1.btnTerug.config(state=tk.DISABLED)
    _w1.radioVar.set("desktops")
    _w1.btnTerug.destroy()
    _w1.btnLog.destroy()
    _w1.terugLabel.destroy()
    _w1.logLabel.destroy()

    # This lets us use the .env file to store our SQL queries and other variables, so we dont have to hardcode them in the code.
    load_dotenv(resource_path(".env"))

    # This sets up the GUI to show the correct inputs for the default category, which is desktops.
    shared.bool_list = [_w1.Checkbutton1, _w1.Checkbutton2, _w1.Checkbutton3]
    shared.kwaliteit_list = [_w1.SpinboxA, _w1.SpinboxB, _w1.SpinboxC]
    shared.int_list = [_w1.Spinbox1, _w1.Spinbox2, _w1.Spinbox3, _w1.Spinbox4, _w1.Spinbox5, _w1.Spinbox6]
    shared.string_list = [_w1.Entry1, _w1.Entry2, _w1.Entry3, _w1.Entry4, _w1.Entry5, _w1.Entry6]

    shared.bool_placement = [i.place_info() for i in shared.bool_list]
    shared.kwaliteit_placement = [i.place_info() for i in shared.kwaliteit_list]
    shared.int_placement = [i.place_info() for i in shared.int_list]
    shared.string_placement = [i.place_info() for i in shared.string_list]

    shared.int_label_list = [_w1.ItemLabelint1, _w1.ItemLabelint2, _w1.ItemLabelint3, _w1.ItemLabelint4, _w1.ItemLabelint5, _w1.ItemLabelint6]
    shared.string_label_list = [_w1.ItemLabeltext1, _w1.ItemLabeltext2, _w1.ItemLabeltext3, _w1.ItemLabeltext4, _w1.ItemLabeltext5, _w1.ItemLabeltext6]

    shared.int_label_placement = [i.place_info() for i in shared.int_label_list]
    shared.string_label_placement = [i.place_info() for i in shared.string_label_list]

    shared.displayport_placement = [_w1.SpinboxIn.place_info(), _w1.SpinboxOut.place_info()]
    shared.displayport_label_placement = [_w1.ItemLabelin.place_info(), _w1.ItemLabelout.place_info()]

    shared.kwaliteit_label_list = [_w1.ItemLabelA, _w1.ItemLabelB, _w1.ItemLabelC]
    shared.kwaliteit_label_placement = [i.place_info() for i in shared.kwaliteit_label_list]

    for i in shared.int_list[1:]:
        i.place_forget()
    for i in shared.bool_list[1:]:
        i.place_forget()
    for i in shared.int_label_list[1:]:
        i.place_forget()
    _w1.SpinboxIn.place_forget()
    _w1.ItemLabelin.place_forget()
    _w1.SpinboxOut.place_forget()
    _w1.ItemLabelout.place_forget()

    for i in DESKTOPS_DICT["string"]:
        shared.string_label_list[DESKTOPS_DICT["string"].index(i)].configure(text=i.capitalize())
    for i in DESKTOPS_DICT["int"]:
        shared.int_label_list[DESKTOPS_DICT["int"].index(i)].configure(text=i.capitalize())
    for i in DESKTOPS_DICT["bool"]:
        shared.bool_list[DESKTOPS_DICT["bool"].index(i)].configure(text=i.capitalize())

def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller."""
    if hasattr(sys, '_MEIPASS'):
        return _path.join(sys._MEIPASS, relative_path)
    return _path.join(_path.abspath("."), relative_path)

def fill_treeview(query, params):
    """A support function that shows the search results in the Treeview."""
    try:
        with open_db_readonly(shared.key) as conn:
            cur = conn.execute(query, params)
            rows = cur.fetchall()
            if rows == []:
                showerror("Geen resultaten", "Er zijn geen resultaten gevonden.")
                return

            _w1.Scrolledtreeview1.delete(*_w1.Scrolledtreeview1.get_children())
            # This adds alternating row colors to the Treeview for better readability.
            counter = 0
            _w1.Scrolledtreeview1.tag_configure("oddrow", background="white")
            _w1.Scrolledtreeview1.tag_configure("evenrow", background="lightblue")

            for item in rows:
                _w1.Scrolledtreeview1.insert("", "end", values=item[1:], tags=(str(item[0]), "evenrow" if counter % 2 == 0 else "oddrow"))
                counter += 1

    except Exception as e:
        if _debug:
            print(f"An error occurred: {e}")
        showerror("Database Error", "Er is een fout opgetreden bij het zoeken van producten.")

def input_organizer(chosen_inputs):
    """A support function that organizes the input fields based on the category chosen by the user."""
        # ---------- logic for displayport ------------
    if chosen_inputs["displayport"]:
        _w1.SpinboxIn.place(shared.displayport_placement[0])
        _w1.ItemLabelin.place(shared.displayport_label_placement[0])
        _w1.SpinboxOut.place(shared.displayport_placement[1])
        _w1.ItemLabelout.place(shared.displayport_label_placement[1])
    else:
        _w1.SpinboxIn.place_forget()
        _w1.ItemLabelin.place_forget()
        _w1.SpinboxOut.place_forget()
        _w1.ItemLabelout.place_forget()
    # -------------------------------------------
    # ---------- logic for kwaliteit ------------
    if chosen_inputs["kwaliteit"]:
        for i in shared.kwaliteit_list:
            i.place(shared.kwaliteit_placement[shared.kwaliteit_list.index(i)])
        for idx, i in enumerate(shared.kwaliteit_label_list):
            i.place(shared.kwaliteit_label_placement[idx])
            i.configure(text=["A_kwaliteit", "B_kwaliteit", "C_kwaliteit"][idx])
    else:
        for i in shared.kwaliteit_list:
            i.place_forget()
        for i in shared.kwaliteit_label_list:
            i.place_forget()
    # -------------------------------------------
    # ---------- logic for string  --------------
    for i in chosen_inputs["string"]:
        shared.string_list[chosen_inputs["string"].index(i)].place(shared.string_placement[chosen_inputs["string"].index(i)])
        shared.string_label_list[chosen_inputs["string"].index(i)].place(shared.string_label_placement[chosen_inputs["string"].index(i)])
        shared.string_label_list[chosen_inputs["string"].index(i)].configure(text=i.capitalize())

    length = len(chosen_inputs["string"])
    for i in shared.string_label_list[length:]:
        i.place_forget()
    for i in shared.string_list[length:]:
        i.place_forget()
    # -------------------------------------------
    # ---------- logic for int  ----------------
    if len(chosen_inputs["int"]) > 5:
        longer_list = shared.kwaliteit_list + shared.int_list
        longer_placement = shared.kwaliteit_placement + shared.int_placement
        longer_label_list = shared.kwaliteit_label_list + shared.int_label_list
        longer_label_placement = shared.kwaliteit_label_placement + shared.int_label_placement
    else:
        longer_list = shared.int_list
        longer_placement = shared.int_placement
        longer_label_list = shared.int_label_list
        longer_label_placement = shared.int_label_placement

    for i in chosen_inputs["int"]:
        longer_list[chosen_inputs["int"].index(i)].place(longer_placement[chosen_inputs["int"].index(i)])
        longer_label_list[chosen_inputs["int"].index(i)].place(longer_label_placement[chosen_inputs["int"].index(i)])
        longer_label_list[chosen_inputs["int"].index(i)].configure(text=i)

    length = len(chosen_inputs["int"])
    for i in longer_label_list[length:]:
        i.place_forget()
    for i in longer_list[length:]:
        i.place_forget()
    # -------------------------------------------
    # ---------- logic for bool -----------------
    for i in chosen_inputs["bool"]:
        shared.bool_list[chosen_inputs["bool"].index(i)].place(shared.bool_placement[chosen_inputs["bool"].index(i)])
        shared.bool_list[chosen_inputs["bool"].index(i)].configure(text=i.capitalize())

    length = len(chosen_inputs["bool"])
    for i in shared.bool_list[length:]:
        i.place_forget()
    # -------------------------------------------

def clear_all_inputs():
    """Clears all input fields in the GUI."""
    # Clear string entries
    for entry in shared.string_list:
        entry.delete(0, tk.END)
    
    # Clear int spinboxes
    for spin in shared.int_list:
        spin.delete(0, tk.END)
    
    # Clear bool checkbuttons
    for check in shared.bool_list:
        check.deselect()
    
    # Clear kwaliteit spinboxes
    for spin in shared.kwaliteit_list:
        spin.delete(0, tk.END)
    
    # Clear displayport spinboxes
    _w1.SpinboxIn.delete(0, tk.END)
    _w1.SpinboxOut.delete(0, tk.END)
    _w1.ScrolledtextItem.delete("1.0", tk.END)

## SELF MADE FUNCTIONS END ########################################

## PAGE FUNCTIONS #################################################
def OnTreeviewClick(*args):
    """Toplevel1 event listener to get the values of the item select by the user in the Treeview.
    And shows the corresponding values in the correct places."""
    if _debug:
        print('Inventaris_support.OnTreeviewClick')
        for arg in args:
            print ('    another arg:', arg)
        sys.stdout.flush()

    # check if user is looking at a log db, so it doenst input wrong information.
    if not shared.is_log_active:
        region = _w1.Scrolledtreeview1.identify("region", args[0].x, args[0].y)
        if region == "heading":
            column = _w1.Scrolledtreeview1.identify_column(args[0].x)

            if shared.sort_column == column:
                shared.sorted = not shared.sorted
            else:
                shared.sorted = False
                shared.sort_column = column

            items = []
            for item in _w1.Scrolledtreeview1.get_children():
                values = _w1.Scrolledtreeview1.item(item, 'values')
                tags = _w1.Scrolledtreeview1.item(item, 'tags')
                items.append((values, tags))

            # Determine column index for sorting
            if column == '#0':
                col_idx = 0
            else:
                # Extract column number from "Col1", "Col2", etc.
                col_num = int(column.replace('#', ''))
                col_idx = col_num - 1

            # Sort by trying numeric first, then alphabetic
            try:
                sorted_items = sorted(items, key=lambda x: float(x[0][col_idx]) if col_idx < len(x[0]) else 0, reverse=shared.sorted)
            except (ValueError, TypeError):
                sorted_items = sorted(items, key=lambda x: str(x[0][col_idx]) if col_idx < len(x[0]) else '', reverse=shared.sorted)

            # Reinsert items in sorted order
            for item in _w1.Scrolledtreeview1.get_children():
                _w1.Scrolledtreeview1.delete(item)

            for values, tags in sorted_items:
                _w1.Scrolledtreeview1.insert('', 'end', values=values, tags=tags)
        else:
            # When the user clicks an item row, populate the visible input widgets based on the values currently shown in the Treeview.
            # Clear any existing inputs first.
            for entry in shared.string_list:
                try:
                    entry.delete(0, "end")
                except Exception:
                    pass

            for spin in shared.int_list + shared.kwaliteit_list:
                try:
                    spin.delete(0, "end")
                except Exception:
                    pass

            for cb in shared.bool_list:
                try:
                    cb.deselect()
                except Exception:
                    pass

            try:
                _w1.ScrolledtextItem.delete("1.0", "end")
            except Exception:
                pass

            row = _w1.Scrolledtreeview1.identify_row(args[0].y)
            if not row:
                return

            columns = list(_w1.Scrolledtreeview1["columns"])
            values = _w1.Scrolledtreeview1.item(row, "values") or []
            tags = _w1.Scrolledtreeview1.item(row, "tags") or []
            db_id = int(tags[0]) if tags else None
            if db_id:
                shared.db_id = db_id

            def _value_for(col_name: str):
                col_name_norm = col_name.strip().lower()
                for idx, col in enumerate(columns):
                    if str(col).strip().lower() == col_name_norm:
                        return values[idx] if idx < len(values) else ""
                return ""

            # Fill string fields
            for label, entry in zip(shared.string_label_list, shared.string_list):
                key = label.cget("text").strip().lower().rstrip(":")
                val = _value_for(key)
                try:
                    entry.delete(0, "end")
                    entry.insert(0, val)
                except Exception:
                    pass

            # Fill integer fields
            if CATEGORIE_DICT[shared.categorie]["kwaliteit"]:
                for label, spin in zip(shared.int_label_list, shared.int_list):
                    key = label.cget("text").strip().lower().rstrip(":")
                    val = _value_for(key)
                    try:
                        spin.delete(0, "end")
                        spin.insert(0, val)
                    except Exception:
                        pass
            else:
                for label, spin in zip(shared.int_label_list + shared.kwaliteit_label_list, shared.int_list + shared.kwaliteit_list):
                    key = label.cget("text").strip().lower().rstrip(":")
                    val = _value_for(key)
                    try:
                        spin.delete(0, "end")
                        spin.insert(0, val)
                    except Exception:
                        pass

            # Fill kwaliteit spinboxes (A/B/C)
            for label, spin in zip(shared.kwaliteit_label_list, shared.kwaliteit_list):
                key = label.cget("text").strip().lower().rstrip(":")
                val = _value_for(key)
                try:
                    spin.delete(0, "end")
                    spin.insert(0, val)
                except Exception:
                    pass

            # Fill displayport spinboxes (if visible)
            for label, spin in ((_w1.ItemLabelin, _w1.SpinboxIn), (_w1.ItemLabelout, _w1.SpinboxOut)):
                key = label.cget("text").strip().lower().rstrip(":")
                val = _value_for(key)
                try:
                    spin.delete(0, "end")
                    spin.insert(0, val)
                except Exception:
                    pass

            # Fill boolean checkboxes
            for label, checkbox in zip(shared.bool_list, shared.bool_list):
                # Checkbox text is used as key
                key = checkbox.cget("text").strip().lower().rstrip(":")
                val = _value_for(key)
                is_true = str(val).strip().lower() in ("1", "true", "yes", "y", "ja", "j")
                try:
                    if is_true:
                        checkbox.select()
                    else:
                        checkbox.deselect()
                except Exception:
                    pass

            # Fill opmerking / notes field
            opmerking_val = _value_for("opmerking")
            shared.opmerking = opmerking_val
            try:
                _w1.ScrolledtextItem.insert("1.0", opmerking_val)
            except Exception:
                pass

def on_andersBtn(*args):
    """Toplevel3 'Kies anders' button event handler."""
    if _debug:
        print('RoadsDepot2_support.on_andersBtn')
        for arg in args:
            print ('    another arg:', arg)
        sys.stdout.flush()
    # TODO: Implement the functionality for the 'Kies anders' button in Toplevel3.

def on_btnAanpassen(*args):
    """Toplevel1 'Aanpassen' button event handler."""
    if _debug:
        print('RoadsDepot2_support.on_btnAanpassen')
        for arg in args:
            print ('    another arg:', arg)
        sys.stdout.flush()

    categorie = shared.categorie
    categorie_dict = CATEGORIE_DICT[categorie]

    # Create a dictionary of the string values based on the entry values and their corresponding text labels.
    string_dict = {}
    for idx, string_field in enumerate(categorie_dict["string"]):
        field_key = string_field.rstrip(":").lower()
        if idx < len(shared.string_list):
            string_dict[field_key] = shared.string_list[idx].get()

    # Create a dictionary of the boolean values based on the checkbutton values and their corresponding text labels.
    bool_dict = {}
    for idx, bool_field in enumerate(categorie_dict["bool"]):
        field_key = bool_field.rstrip(":").lower()
        if idx == 0:
            bool_dict[field_key] = _w1.check1.get()
        elif idx == 1:
            bool_dict[field_key] = _w1.check2.get()
        elif idx == 2:
            bool_dict[field_key] = _w1.check3.get()

    # Create a dictionary of the integer values based on the spinbox values and their corresponding text labels.
    if len(categorie_dict["int"]) > 5:
        int_longer_list = shared.kwaliteit_list + shared.int_list
    else:
        int_longer_list = shared.int_list
    
    int_dict = {}
    for idx, int_field in enumerate(categorie_dict["int"]):
        field_key = int_field.rstrip(":").lower()
        if idx < len(int_longer_list):
            int_dict[field_key] = int_longer_list[idx].get()
    
    # Create a dictionary of the kwaliteit values based on the spinbox values and their corresponding text
    kwaliteit_dict = {}
    if categorie_dict["kwaliteit"]:
        for idx, label in enumerate(shared.kwaliteit_label_list):
            label_text = label.cget("text").strip().rstrip(":")
            # field_key = f"{label_text}_kwaliteit".lower()
            if idx < len(shared.kwaliteit_list):
                kwaliteit_dict[label_text] = shared.kwaliteit_list[idx].get()
    if categorie_dict["displayport"]:
        displayport_dict = {
            "displayport_in": _w1.SpinboxIn.get(),
            "displayport_out": _w1.SpinboxOut.get()
        }

    all_dict = {**string_dict, **int_dict, **bool_dict, **kwaliteit_dict, **(displayport_dict if categorie_dict["displayport"] else {})}
    try:
        if int(all_dict['A_kwaliteit']) + int(all_dict['B_kwaliteit']) + int(all_dict['C_kwaliteit']) > int(all_dict['totaal']):
            showerror("Input Error", "De som van A, B en C kwaliteit moet minder zijn dan het totaal.")
            return
    except ValueError:
        showerror("Input Error", "Een nummeriek input veld heeft iets anders gekregen dan een nummer.")
        return
    
    # Map keys to match CATEGORIE_COLUMNS casing by creating a mapping from lowercase to actual column names
    key_mapping = {col.lower(): col for col in CATEGORIE_COLUMNS[categorie]}
    mapped_all_dict = {key_mapping.get(key.lower(), key): value for key, value in all_dict.items()}
    
    # Order the dict according to CATEGORIE_COLUMNS, including all columns except opmerking with defaults
    ordered_all_dict = {col: mapped_all_dict.get(col, "") for col in CATEGORIE_COLUMNS[categorie] if col != "opmerking"}

    shared.opmerking = _w1.ScrolledtextItem.get("1.0", "end").strip()
    # Determine the correct UPDATE query and parameters based on the category, and execute it.

    if ordered_all_dict["totaal"].strip() == "":
        showerror("Input Error", "Totaal mag niet leeg zijn.")
        return
    if "soort" in ordered_all_dict and ordered_all_dict["soort"].strip() == "":
        showerror("Input Error", "Soort mag niet leeg zijn.")
        return
    if "model" in ordered_all_dict and ordered_all_dict["model"].strip() == "":
        showerror("Input Error", "Model mag niet leeg zijn.")
        return
    if "merk" in ordered_all_dict and ordered_all_dict["merk"].strip() == "":
        showerror("Input Error", "Merk mag niet leeg zijn.")
        return
    if "wattage" in ordered_all_dict and ordered_all_dict["wattage"].strip() == "":
        showerror("Input Error", "Wattage mag niet leeg zijn.")
        return

    if categorie == "mobiels":
        query = getenv("UPDATE_MOBIELS")
        params = list(ordered_all_dict.values()) + [shared.opmerking] + [shared.db_id]
    elif categorie == "desktops":
        query = getenv("UPDATE_DESKTOPS")
        params = list(ordered_all_dict.values()) + [shared.opmerking] + [shared.db_id]
    elif categorie == "beeldschermen":
        query = getenv("UPDATE_BEELDSCHERMEN")
        params = list(ordered_all_dict.values()) + [shared.opmerking] + [shared.db_id]
    elif categorie == "kabels":
        query = getenv("UPDATE_KABELS")
        params = list(ordered_all_dict.values()) + [shared.opmerking] + [shared.db_id]
    elif categorie == "laptops":
        query = getenv("UPDATE_LAPTOPS")
        params = list(ordered_all_dict.values()) + [shared.opmerking] + [shared.db_id]
    elif categorie == "muizen":
        query = getenv("UPDATE_MUIZEN")
        params = list(ordered_all_dict.values()) + [shared.opmerking] + [shared.db_id]
    elif categorie == "toetsenborden":
        query = getenv("UPDATE_TOETSENBORDEN")
        params = list(ordered_all_dict.values()) + [shared.opmerking] + [shared.db_id]
    elif categorie == "voedingen":
        query = getenv("UPDATE_VOEDINGEN")
        params = list(ordered_all_dict.values()) + [shared.opmerking] + [shared.db_id]

    try:
        with open_db_write(shared.key) as conn:
            conn.execute(query, params)
            conn.commit()
        SuccesBox = tk.Toplevel()
        SuccesBox.title("Succes")
        SuccesBox.geometry("300x100")
        tk.Label(SuccesBox, text="Het product is succesvol aangepast.\nIk sluit automatisch in 5 seconden.").pack(expand=True)
        tk.Button(SuccesBox, text="OK", command=SuccesBox.destroy).pack(pady=10)
        SuccesBox.after(5000, SuccesBox.destroy)  # Automatically close after 5 seconds
    except Exception as e:
        if _debug:
            print(f"Database Error: {e}")
        showerror("Database Error", "Er is een fout opgetreden bij het aanpassen van het product.")
        return
    
    # A check to use the correct SQL query to refresh the Treeview.
    model = _w1.zoekEntryModel.get()
    merk = _w1.zoekEntryMerk.get()
    if model.strip() != "" and merk.strip() != "":
        query = getenv("SEARCH_MODEL_MERK")
        params = [model, merk]
    elif model.strip() != "":
        query = getenv("SEARCH_MODEL")
        params = [model]
    elif merk.strip() != "":
        query = getenv("SEARCH_MERK")
        params = [merk]
    else:
        query = getenv("SEARCH_CATEGORIE")
        params = []
    query = query.format(table=shared.categorie)
    fill_treeview(query, params)

def on_btnAfsluiten(*args):
    """Toplevel1 button to exit the program."""
    if _debug:
        print('RoadsDepot2_support.on_btnAfsluiten')
        for arg in args:
            print ('    another arg:', arg)
        sys.stdout.flush()
    root.destroy()

def on_btnGaan(*args):
    """Toplevel1 'Gaan' button event handler.
    This sets the input fields to the correct ones based on the category chosen by the user."""
    if _debug:
        print('RoadsDepot2_support.on_btnGaan')
        for arg in args:
            print ('    another arg:', arg)
        sys.stdout.flush()
    clear_all_inputs()
    radio_value = _w1.radioVar.get().lower()
    if radio_value != shared.categorie:
        _w1.Scrolledtreeview1.delete(*_w1.Scrolledtreeview1.get_children())

    shared.categorie = radio_value
    chosen_inputs = CATEGORIE_DICT[radio_value]
    input_organizer(chosen_inputs)
    _w1.Menubtn_zoek.configure(text=radio_value.capitalize())

def on_btnLog(*args):
    """Toplevel1 'Kiezen' button event handler.
    Button that lets you choose a database file."""
    # Currently unused!
    # TODO: Do I even implement a log?
    if _debug:
        print('Inventaris_support.on_btnLog')
        for arg in args:
            print ('    another arg:', arg)
        sys.stdout.flush()

    shared.path = rf'''{filedialog.askopenfilename(
        title="Select Database",
        filetypes=[("Database bestanden", "*.db"), ("Alle bestanden", "*.*")])}'''

    if shared.path and shared.path.endswith(".db"):
        _top3.deiconify()
        _w3.dbEntry.configure(textvariable=tk.StringVar(value=shared.path))
        _w3.dbwwEntry.focus_set()
    else:
        return

def on_btnLogin(*args):
    """Toplevel2 login button event handler."""
    if _debug:
        print('Inventaris_support.on_btnLogin')
        for arg in args:
            print ('    another arg:', arg)
        sys.stdout.flush()

    shared.key = _w2.wachtwoordEntry.get()
    shared.gebruiker = _w2.usernameEntry.get()
    # This checks if the password is correct.
    if test_connection(key=shared.key):
        if shared.gebruiker in ["deelnemer1", "deelnemer2", "begeleider1", "begeleider2"]:
            _top1.deiconify()
            _top2.destroy()
            _w1.zoekEntryMerk.focus_set()
            if not check_log_exists():
                _top4.deiconify()
                _w4.nieuwwwEntry.focus_set()
        elif shared.gebruiker == "gebruiker":
            if not check_log_exists():
                showerror("Login Fout", "Er is geen logbestand. Neem contact op met een begeleider.")
                root.destroy()
            _w1.verwijderLabelframe.place_forget()
            _w1.btnToevoegen.destroy()
            _w1.ItemLabelNieuw.destroy()
            _w1.btnAanpassen.destroy()
            _w1.ItemLabelAanpassen.destroy()
            _w1.nieuwLabelframe.destroy()
            _top1.deiconify()
            _top2.destroy()
            _w1.zoekEntryMerk.focus_set()
        else:
            showerror("Login Fout", "Onjuiste wachtwoord of gebruikersnaam. Probeer het opnieuw.")

        make_backup(shared.key)
    else:
        showerror("Login Fout", "Onjuist wachtwoord of gebruikersnaam. Probeer het opnieuw.")

def on_btnTerug(*args):
    """Toplevel1 'Terug' button event handler.
    After choosing a Log database file, let's you return to the main Database."""
    # Currently unused!
    # TODO: Change logic to fit. Might not be needed.
    if _debug:
        print('Inventaris_support.on_btnTerug')
        for arg in args:
            print ('    another arg:', arg)
        sys.stdout.flush()

    for c in _w1.Scrolledtreeview1.get_children(''):
        _w1.Scrolledtreeview1.delete(c)

    COLUMN_HEADS = ["Categorie", "Productnummer", "Aantal", "A_Kwaliteit", "B_Kwaliteit", "C_Kwaliteit", "Locatie", "Opmerking"]
    _w1.Scrolledtreeview1.configure(columns=COLUMN_HEADS, show="headings")

    for col in COLUMN_HEADS:
        _w1.Scrolledtreeview1.heading(col, text=col)

    _w1.btnZoeken.config(state=tk.NORMAL)
    _w1.btnVerwijder.config(state=tk.NORMAL)
    _w1.nieuwLabelframe.place(relx=0.005, rely=0.431, relwidth=0.989, relheight=0.522)
    _w1.nieuwLabelframe.lift()
    shared.is_log_active = False

def on_btnVerwijder(*args):
    """Toplevel1 button to remove the selected, in the treeview, from the database."""
    # Currently doesnt add the changes to the Log, as there is no Log implemented yet. But the structure is there to do so when needed.
    if _debug:
        print('Inventaris_support.on_btnVerwijder')
        for arg in args:
            print ('    another arg:', arg)
        sys.stdout.flush()

    conn = None
    # log_conn = None

    query = ""
    params = ""
    zoekCategorie = _w1.Menubtn_zoek.cget("text").lower()
    model = _w1.zoekEntryModel.get()
    merk = _w1.zoekEntryMerk.get()
    shared.categorie = zoekCategorie

    # A check to use the correct SQL query.
    if model.strip() != "" and merk.strip() != "":
        query = getenv("SEARCH_MODEL_MERK")
        params = [model, merk]
    elif model.strip() != "":
        query = getenv("SEARCH_MODEL")
        params = [model]
    elif merk.strip() != "":
        query = getenv("SEARCH_MERK")
        params = [merk]
    else:
        query = getenv("SEARCH_CATEGORIE")
        params = []
    query = query.format(table=zoekCategorie)

    try:
        conn = open_db_write(shared.key).__enter__()
        # log_conn = open_logdb(shared.key).__enter__()
        # Removes item from the database
        conn.execute(getenv("DELETE_PRODUCT").format(table=zoekCategorie), [shared.db_id])

        # # Adds the change to the log
        # log_conn.execute(queries.ADD_LOG_ENTRY, (
        #     shared.productnummer,
        #     shared.categorie,
        #     -int(shared.akwaliteit),
        #     -int(shared.bkwaliteit),
        #     -int(shared.ckwaliteit),
        #     -int(shared.totaal),
        #     shared.gebruiker
        # ))

        # log_conn.commit()
        conn.commit()
        fill_treeview(query, params)

    except Exception as e:
        # This prevents the change from only appearing in 1 database should the other fail.
        if conn:
            conn.rollback()
        # if log_conn:
        #     log_conn.rollback()

        if _debug:
            print(f"An error occurred: {e}")
        showerror("Database Error", "Er is een fout opgetreden bij het verwijderen van het product.")
        return

    finally:
        if conn:
            conn.close()
        # if log_conn:
        #     log_conn.close()

def on_btnZoeken(*args):
    """Toplevel1 Search button to find items in the database."""
    if _debug:
        print('Inventaris_support.on_btnZoeken')
        for arg in args:
            print ('    another arg:', arg)
        sys.stdout.flush()

    clear_all_inputs()
    _w1.Scrolledtreeview1.delete(*_w1.Scrolledtreeview1.get_children())
    query = ""
    params = ""
    zoekCategorie = _w1.Menubtn_zoek.cget("text").lower()
    model = _w1.zoekEntryModel.get()
    merk = _w1.zoekEntryMerk.get()
    shared.categorie = zoekCategorie
    _w1.radioVar.set(zoekCategorie)

    # A check to use the correct SQL query.
    if model.strip() != "" and merk.strip() != "":
        query = getenv("SEARCH_MODEL_MERK")
        params = [model, merk]
    elif model.strip() != "":
        query = getenv("SEARCH_MODEL")
        params = [model]
    elif merk.strip() != "":
        query = getenv("SEARCH_MERK")
        params = [merk]
    else:
        query = getenv("SEARCH_CATEGORIE")
        params = []

    # This sets the columns of the Treeview based on the category chosen by the user.
    _w1.Scrolledtreeview1.configure(columns=CATEGORIE_COLUMNS[zoekCategorie], show="headings")
    for col in CATEGORIE_COLUMNS[zoekCategorie]:
        _w1.Scrolledtreeview1.heading(col, text=col)
        _w1.Scrolledtreeview1.column(col, width=font.Font().measure(col.title()), anchor='center')

    chosen_inputs = CATEGORIE_DICT[zoekCategorie]
    input_organizer(chosen_inputs)
    query = query.format(table=zoekCategorie)
    fill_treeview(query, params)

def on_logafsluitbtn(*args):
    # Currently unused!
    if _debug:
        print('RoadsDepot2_support.on_logafsluitbtn')
        for arg in args:
            print ('    another arg:', arg)
        sys.stdout.flush()
    root.destroy()

def on_logokbtn(*args):
    """Toplevel4 'OK' button event handler."""
    # Currently unused!
    if _debug:
        print('Inventaris_support.on_logokbtn')
        for arg in args:
            print ('    another arg:', arg)
        sys.stdout.flush()
    logww = _w4.nieuwwwEntry.get()
    check = create_new_log(ww=logww)
    if check != True:
        showerror("Databes error", f"{check}")
    else:
        _top4.withdraw()
        _top1.deiconify()

def on_menuBeeldscherm(*args):
    """A function that changes the text of the search menu button to the category chosen by the user."""
    if _debug:
        print('RoadsDepot2_support.on_menuBeeldscherm')
        for arg in args:
            print ('    another arg:', arg)
        sys.stdout.flush()
    _w1.Menubtn_zoek.configure(text="Beeldschermen")

def on_menuDesktop(*args):
    """A function that changes the text of the search menu button to the category chosen by the user."""
    if _debug:
        print('RoadsDepot2_support.on_menuDesktop')
        for arg in args:
            print ('    another arg:', arg)
        sys.stdout.flush()
    _w1.Menubtn_zoek.configure(text="Desktops")

def on_menuKabel(*args):
    """A function that changes the text of the search menu button to the category chosen by the user."""
    if _debug:
        print('RoadsDepot2_support.on_menuKabel')
        for arg in args:
            print ('    another arg:', arg)
        sys.stdout.flush()
    _w1.Menubtn_zoek.configure(text="Kabels")

def on_menuLaptop(*args):
    """A function that changes the text of the search menu button to the category chosen by the user."""
    if _debug:
        print('RoadsDepot2_support.on_menuLaptop')
        for arg in args:
            print ('    another arg:', arg)
        sys.stdout.flush()
    _w1.Menubtn_zoek.configure(text="Laptops")

def on_menuMobiel(*args):
    """A function that changes the text of the search menu button to the category chosen by the user."""
    if _debug:
        print('RoadsDepot2_support.on_menuMobiel')
        for arg in args:
            print ('    another arg:', arg)
        sys.stdout.flush()
    _w1.Menubtn_zoek.configure(text="Mobiels")

def on_menuMuis(*args):
    """A function that changes the text of the search menu button to the category chosen by the user."""
    if _debug:
        print('RoadsDepot2_support.on_menuMuis')
        for arg in args:
            print ('    another arg:', arg)
        sys.stdout.flush()
    _w1.Menubtn_zoek.configure(text="Muizen")

def on_menuToetsenbord(*args):
    """A function that changes the text of the search menu button to the category chosen by the user."""
    if _debug:
        print('RoadsDepot2_support.on_menuToetsenbord')
        for arg in args:
            print ('    another arg:', arg)
        sys.stdout.flush()
    _w1.Menubtn_zoek.configure(text="Toetsenborden")

def on_menuVoeding(*args):
    """A function that changes the text of the search menu button to the category chosen by the user."""
    if _debug:
        print('RoadsDepot2_support.on_menuVoeding')
        for arg in args:
            print ('    another arg:', arg)
        sys.stdout.flush()
    _w1.Menubtn_zoek.configure(text="Voedingen")

def on_okBtn(*args):
    """Toplevel3 'OK' button event handler."""
    # Currently unused!
    if _debug:
        print('Inventaris_support.on_okBtn')
        for arg in args:
            print ('    another arg:', arg)
        sys.stdout.flush()
    logkey = _w3.dbwwEntry.get()
    try:
        with open_old_logdb(logkey, path=shared.path) as conn:
            cur = conn.execute(queries.GET_LOG)
            log_readout = cur.fetchall()
    except Exception as e:
        if _debug:
            print(f"Database Error: {e}")
        showerror("Database Error", "Er is een fout opgetreden bij het openenen van de log.")
        return

    for c in _w1.Scrolledtreeview1.get_children(''):
        _w1.Scrolledtreeview1.delete(c)

    _w1.Scrolledtreeview1.configure(columns=queries.LOG_COLUMS, show="headings")
    for col in queries.LOG_COLUMS:
        _w1.Scrolledtreeview1.heading(col, text=col)
    for item in log_readout:
        _w1.Scrolledtreeview1.insert("", "end", values=item)

    _w1.nieuwLabelframe.place_forget()
    _w1.btnVerwijder.config(state=tk.DISABLED)
    _w1.btnZoeken.config(state=tk.DISABLED)
    _w1.btnTerug.config(state=tk.NORMAL)
    _top3.withdraw()
    shared.is_log_active = True

def usernameEnter(*args):
    """Toplevel2 username enterkey listener"""
    if _debug:
        print('RoadsDepot2_support.usernameEnter')
        for arg in args:
            print ('    another arg:', arg)
        sys.stdout.flush()
    on_btnLogin(*args)

def wachtwoordEnter(*args):
    """Toplevel2 password enterkey listener"""
    if _debug:
        print('RoadsDepot2_support.wachtwoordEnter')
        for arg in args:
            print ('    another arg:', arg)
        sys.stdout.flush()
    on_btnLogin(*args)

def zoekbalk_enterkey(*args):
    """Toplevel1 zoekbalk enterkey listener"""
    if _debug:
        print('RoadsDepot2_support.zoekbalk_enterkey')
        for arg in args:
            print ('    another arg:', arg)
        sys.stdout.flush()
    on_btnZoeken(*args)

def on_btnToevoegen(*args):
    """Toplevel1 'Toevoegen' button event handler.
    This gathers all the input from the visible input widgets based on the category, validates it, and then adds it to the database."""
    if _debug:
        print('RoadsDepot2_support.on_btnToevoegen')
        for arg in args:
            print ('    another arg:', arg)
        sys.stdout.flush()

    categorie = shared.categorie
    categorie_dict = CATEGORIE_DICT[categorie]

    # Create a dictionary of the string values based on the entry values and their corresponding text labels.
    string_dict = {}
    for idx, string_field in enumerate(categorie_dict["string"]):
        field_key = string_field.rstrip(":").lower()
        if idx < len(shared.string_list):
            string_dict[field_key] = shared.string_list[idx].get()

    # Create a dictionary of the boolean values based on the checkbutton values and their corresponding text labels.
    bool_dict = {}
    for idx, bool_field in enumerate(categorie_dict["bool"]):
        field_key = bool_field.rstrip(":").lower()
        if idx == 0:
            bool_dict[field_key] = _w1.check1.get()
        elif idx == 1:
            bool_dict[field_key] = _w1.check2.get()
        elif idx == 2:
            bool_dict[field_key] = _w1.check3.get()

    # Create a dictionary of the integer values based on the spinbox values and their corresponding text labels.
    if len(categorie_dict["int"]) > 5:
        int_longer_list = shared.kwaliteit_list + shared.int_list
    else:
        int_longer_list = shared.int_list
    
    int_dict = {}
    for idx, int_field in enumerate(categorie_dict["int"]):
        field_key = int_field.rstrip(":").lower()
        if idx < len(int_longer_list):
            int_dict[field_key] = int_longer_list[idx].get()
    
    # Create a dictionary of the kwaliteit values based on the spinbox values and their corresponding text
    kwaliteit_dict = {}
    if categorie_dict["kwaliteit"]:
        for idx, label in enumerate(shared.kwaliteit_label_list):
            label_text = label.cget("text").strip().rstrip(":")
            # field_key = f"{label_text}_kwaliteit".lower()
            if idx < len(shared.kwaliteit_list):
                kwaliteit_dict[label_text] = shared.kwaliteit_list[idx].get()
    if categorie_dict["displayport"]:
        displayport_dict = {
            "displayport_in": _w1.SpinboxIn.get(),
            "displayport_out": _w1.SpinboxOut.get()
        }

    all_dict = {**string_dict, **int_dict, **bool_dict, **kwaliteit_dict, **(displayport_dict if categorie_dict["displayport"] else {})}
    try:
        if int(all_dict['A_kwaliteit']) + int(all_dict['B_kwaliteit']) + int(all_dict['C_kwaliteit']) > int(all_dict['totaal']):
            showerror("Input Error", "De som van A, B en C kwaliteit moet minder zijn dan het totaal.")
            return
    except ValueError:
        showerror("Input Error", "Een nummeriek input veld heeft iets anders gekregen dan een nummer.")
        return
    
    # Map keys to match CATEGORIE_COLUMNS casing by creating a mapping from lowercase to actual column names
    key_mapping = {col.lower(): col for col in CATEGORIE_COLUMNS[categorie]}
    mapped_all_dict = {key_mapping.get(key.lower(), key): value for key, value in all_dict.items()}
    
    # Order the dict according to CATEGORIE_COLUMNS, including all columns except opmerking with defaults
    ordered_all_dict = {col: mapped_all_dict.get(col, "") for col in CATEGORIE_COLUMNS[categorie] if col != "opmerking"}

    shared.opmerking = _w1.ScrolledtextItem.get("1.0", "end").strip()
    # Determine the correct UPDATE query and parameters based on the category, and execute it.

    if ordered_all_dict["totaal"].strip() == "":
        showerror("Input Error", "Totaal mag niet leeg zijn.")
        return
    if "soort" in ordered_all_dict and ordered_all_dict["soort"].strip() == "":
        showerror("Input Error", "Soort mag niet leeg zijn.")
        return
    if "model" in ordered_all_dict and ordered_all_dict["model"].strip() == "":
        showerror("Input Error", "Model mag niet leeg zijn.")
        return
    if "merk" in ordered_all_dict and ordered_all_dict["merk"].strip() == "":
        showerror("Input Error", "Merk mag niet leeg zijn.")
        return
    if "wattage" in ordered_all_dict and ordered_all_dict["wattage"].strip() == "":
        showerror("Input Error", "Wattage mag niet leeg zijn.")
        return

    if categorie in ["mobiels", "desktops", "beeldschermen", "laptops", "muizen", "toetsenborden"]:
        check_query = getenv("CHECK_UNIQUE").format(table=categorie)
        check_params = (ordered_all_dict["model"], ordered_all_dict["merk"])
    elif categorie == "kabels":
        check_query = getenv("CHECK_UNIQUE_KABELS").format(table=categorie)
        check_params = (ordered_all_dict["model"], ordered_all_dict["lengte"])
    elif categorie == "voedingen":
        check_query = getenv("CHECK_UNIQUE_VOEDINGEN").format(table=categorie)
        check_params = (ordered_all_dict["soort"], ordered_all_dict["wattage"], ordered_all_dict["merk"])

    with open_db_readonly(shared.key) as conn:
        cur = conn.execute(check_query, check_params)
        existing_item = cur.fetchone()
        if existing_item:
            showerror("Input Error", "Er bestaat al een product met hetzelfde merk en model.")
            return

    if categorie == "mobiels":
        query = getenv("INSERT_MOBIELS")
        params = list(ordered_all_dict.values()) + [shared.opmerking]
    elif categorie == "desktops":
        query = getenv("INSERT_DESKTOPS")
        params = list(ordered_all_dict.values()) + [shared.opmerking]
    elif categorie == "beeldschermen":
        query = getenv("INSERT_BEELDSCHERMEN")
        params = list(ordered_all_dict.values()) + [shared.opmerking]
    elif categorie == "kabels":
        query = getenv("INSERT_KABELS")
        params = list(ordered_all_dict.values()) + [shared.opmerking]
    elif categorie == "laptops":
        query = getenv("INSERT_LAPTOPS")
        params = list(ordered_all_dict.values()) + [shared.opmerking]
    elif categorie == "muizen":
        query = getenv("INSERT_MUIZEN")
        params = list(ordered_all_dict.values()) + [shared.opmerking]
    elif categorie == "toetsenborden":
        query = getenv("INSERT_TOETSENBORDEN")
        params = list(ordered_all_dict.values()) + [shared.opmerking]
    elif categorie == "voedingen":
        query = getenv("INSERT_VOEDINGEN")
        params = list(ordered_all_dict.values()) + [shared.opmerking]

    try:
        with open_db_write(shared.key) as conn:
            conn.execute(query, params)
            conn.commit()
        SuccesBox = tk.Toplevel()
        SuccesBox.title("Succes")
        SuccesBox.geometry("300x100")
        tk.Label(SuccesBox, text="Het product is succesvol toegevoegd.\nIk sluit automatisch in 5 seconden.").pack(expand=True)
        tk.Button(SuccesBox, text="OK", command=SuccesBox.destroy).pack(pady=10)
        SuccesBox.after(5000, SuccesBox.destroy)  # Automatically close after 5 seconds
    except Exception as e:
        if _debug:
            print(f"Database Error: {e}")
        showerror("Database Error", "Er is een fout opgetreden bij het toevoegen van het product.")
        return

    # A check to use the correct SQL query.
    model = _w1.zoekEntryModel.get()
    merk = _w1.zoekEntryMerk.get()
    if model.strip() != "" and merk.strip() != "":
        query = getenv("SEARCH_MODEL_MERK")
        params = [model, merk]
    elif model.strip() != "":
        query = getenv("SEARCH_MODEL")
        params = [model]
    elif merk.strip() != "":
        query = getenv("SEARCH_MERK")
        params = [merk]
    else:
        query = getenv("SEARCH_CATEGORIE")
        params = []
    query = query.format(table=shared.categorie)
    fill_treeview(query, params)

if __name__ == '__main__':
    try:
        RoadsDepot2.start_up()
    except Exception:
        logging.critical("Unhandled exception occurred!", exc_info=True)
## PAGE FUNCTIONS END ###############################################
