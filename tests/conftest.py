import os
import sys

# Ensure local source packages under src/ are discoverable when running pytest
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
SRC_DIR = os.path.join(ROOT_DIR, "src")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

import pytest
import customtkinter as ctk
from pdf_unlocker.ui.pdf_unlocker_gui import PDFUnlockerUI


@pytest.fixture
def app(mocker):
    """Initialize a PDFUnlockerUI instance without creating a real Tkinter window."""
    mocker.patch('customtkinter.CTk.__init__', return_value=None)
    mocker.patch('customtkinter.CTk.title', return_value=None)
    mocker.patch('customtkinter.CTk.geometry', return_value=None)
    mocker.patch('customtkinter.CTk.resizable', return_value=None)
    mocker.patch('customtkinter.CTk.wm_iconbitmap', return_value=None)
    mocker.patch('customtkinter.CTk.mainloop', return_value=None)
    mocker.patch.object(PDFUnlockerUI, 'create_widgets', return_value=None)

    ui = PDFUnlockerUI()
    ui.input_file = ""
    ui.output_file = ""
    ui.entry_pwd = mocker.Mock()
    ui.entry_pwd.get.return_value = ""
    ui.entry_pwd.delete = mocker.Mock()
    ui.lbl_input = mocker.Mock()
    ui.lbl_output = mocker.Mock()
    return ui
