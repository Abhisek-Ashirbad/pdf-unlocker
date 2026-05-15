import pytest
import pikepdf
from pdf_unlocker.ui.pdf_unlocker_gui import PDFUnlockerUI, run_gui

@pytest.fixture
def app(mocker):
    """Fixture initializing the app without spinning up the mainloop event loop."""
    # Prevent Tkinter from initializing structural windows during text execution
    mocker.patch('customtkinter.CTk.mainloop')
    return PDFUnlockerUI()


def test_gui_empty_paths_error(app, mocker):
    """Verify error box triggers if file paths are omitted."""
    mock_error = mocker.patch('tkinter.messagebox.showerror')
    app.input_file = ""
    app.output_file = ""
    app.unlock_pdf()
    mock_error.assert_called_once_with("Error", "Please select both input and output paths.")


def test_gui_empty_password_error(app, mocker):
    """Verify error box triggers if the password field is left blank."""
    mock_error = mocker.patch('tkinter.messagebox.showerror')
    app.input_file = "protected.pdf"
    app.output_file = "unlocked.pdf"
    mocker.patch.object(app.entry_pwd, 'get', return_value="")
    app.unlock_pdf()
    mock_error.assert_called_once_with("Error", "Password cannot be empty.")


def test_gui_incorrect_password_error(app, mocker):
    """Verify error box handling when pikepdf throws a PasswordError."""
    mock_error = mocker.patch('tkinter.messagebox.showerror')
    app.input_file = "protected.pdf"
    app.output_file = "unlocked.pdf"
    mocker.patch.object(app.entry_pwd, 'get', return_value="wrong_pwd")
    # Force our business logic to raise a PasswordError when run inside the view
    mocker.patch('pdf_unlocker.ui.pdf_unlocker_gui.remove_pdf_password', side_effect=pikepdf.PasswordError("Invalid"))
    app.unlock_pdf()
    mock_error.assert_called_once_with("Error", "Incorrect password. Please try again.")


def test_gui_success_message(app, mocker):
    """Verify success alert path operates cleanly when validation passes."""
    mock_info = mocker.patch('tkinter.messagebox.showinfo')
    mocker.patch('pdf_unlocker.ui.pdf_unlocker_gui.remove_pdf_password', return_value=None)
    app.input_file = "/path/to/protected.pdf"
    app.output_file = "/path/to/unlocked.pdf"
    mocker.patch.object(app.entry_pwd, 'get', return_value="correct_pwd")
    app.unlock_pdf()
    mock_info.assert_called_once_with("Success", "Password removed successfully!\nSaved to: unlocked.pdf")


def test_gui_file_not_found_error(app, mocker):
    mock_error = mocker.patch('tkinter.messagebox.showerror')
    app.input_file = "missing.pdf"
    app.output_file = "out.pdf"
    mocker.patch.object(app.entry_pwd, 'get', return_value="pwd")
    mocker.patch(
        'pdf_unlocker.ui.pdf_unlocker_gui.remove_pdf_password',
        side_effect=FileNotFoundError()
    )
    app.unlock_pdf()
    mock_error.assert_called_once_with(
        "Error", "The specified input file was not found."
    )


def test_gui_unexpected_exception(app, mocker):
    mock_error = mocker.patch('tkinter.messagebox.showerror')
    app.input_file = "file.pdf"
    app.output_file = "out.pdf"
    mocker.patch.object(app.entry_pwd, 'get', return_value="pwd")
    mocker.patch(
        'pdf_unlocker.ui.pdf_unlocker_gui.remove_pdf_password',
        side_effect=Exception("boom")
    )
    app.unlock_pdf()
    mock_error.assert_called_once()
    assert "An unexpected error occurred" in mock_error.call_args[0][1]


def test_password_field_cleared_on_success(app, mocker):
    mocker.patch('tkinter.messagebox.showinfo')
    delete_mock = mocker.patch.object(app.entry_pwd, 'delete')
    mocker.patch.object(app.entry_pwd, 'get', return_value="pwd")
    mocker.patch(
        'pdf_unlocker.ui.pdf_unlocker_gui.remove_pdf_password',
        return_value=None
    )
    app.input_file = "in.pdf"
    app.output_file = "out.pdf"
    app.unlock_pdf()
    delete_mock.assert_called_once_with(0, 'end')


def test_select_input_file_chosen(app, mocker):
    mocker.patch(
        'tkinter.filedialog.askopenfilename',
        return_value="/tmp/test.pdf"
    )
    configure_mock = mocker.patch.object(app.lbl_input, 'configure')
    app.select_input()
    assert app.input_file == "/tmp/test.pdf"
    configure_mock.assert_called_once()

def test_run_gui_starts_mainloop(mocker):
    mock_ui = mocker.Mock()
    mocker.patch('pdf_unlocker.ui.pdf_unlocker_gui.PDFUnlockerUI', return_value=mock_ui)
    run_gui()
    mock_ui.mainloop.assert_called_once()

def test_select_input_no_file(app, mocker):
    mocker.patch(
        'tkinter.filedialog.askopenfilename',
        return_value=""
    )
    configure_mock = mocker.patch.object(app.lbl_input, 'configure')
    app.select_input()
    assert app.input_file == ""
    configure_mock.assert_not_called()


def test_select_output_file_chosen(app, mocker):
    mocker.patch(
        'tkinter.filedialog.asksaveasfilename',
        return_value="/tmp/out.pdf"
    )
    configure_mock = mocker.patch.object(app.lbl_output, 'configure')
    app.select_output()
    assert app.output_file == "/tmp/out.pdf"
    configure_mock.assert_called_once()


