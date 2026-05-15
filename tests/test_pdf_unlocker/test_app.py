import pytest
import pikepdf
import runpy
import sys
import types
from pdf_unlocker.app import main, run_cli

def test_cli_launches_gui_when_no_arguments(monkeypatch, mocker):
    """Verify GUI lifecycle starts if argv contains zero parameter tokens."""
    monkeypatch.setattr(sys, "argv", ["unlock"])
    mock_run_gui = mocker.patch('pdf_unlocker.ui.pdf_unlocker_gui.run_gui')
    main()
    mock_run_gui.assert_called_once()

def test_cli_execution_with_arguments(monkeypatch, mocker):
    """Verify argument values pass down correctly into the runtime controller."""
    monkeypatch.setattr(sys, "argv", ["unlock", "-i", "in.pdf", "-o", "out.pdf", "-p", "pass"])
    mock_run_cli = mocker.patch('pdf_unlocker.app.run_cli')
    main()
    mock_run_cli.assert_called_once_with("in.pdf", "out.pdf", "pass")

def test_cli_fails_on_missing_required_arguments(monkeypatch):
    """Verify standard argparse system error routines trigger if keys are dropped."""
    monkeypatch.setattr(sys, "argv", ["unlock", "-i", "only_input.pdf"])
    with pytest.raises(SystemExit):
        main()

def test_init_frozen_mode(app, mocker):
    mocker.patch('sys.frozen', True, create=True)
    mocker.patch('sys._MEIPASS', '/mock/path', create=True)
    exists_mock = mocker.patch('os.path.exists', return_value=False)
    # Recreate instance to trigger __init__
    ui = type(app)()
    exists_mock.assert_called()


def test_icon_applied(app, mocker):
    mocker.patch('os.path.exists', return_value=True)
    icon_mock = mocker.patch.object(type(app), 'wm_iconbitmap')
    ui = type(app)()
    icon_mock.assert_called_once()


def test_run_cli_success_prints_message(mocker, capsys):
    mock_remove = mocker.patch('pdf_unlocker.app.remove_pdf_password')
    exit_mock = mocker.patch('pdf_unlocker.app.sys.exit')

    run_cli('input.pdf', 'output.pdf', 'pwd')

    captured = capsys.readouterr()
    assert "Processing: input.pdf..." in captured.out
    assert "Success! Unlocked file saved to: output.pdf" in captured.out
    mock_remove.assert_called_once_with('input.pdf', 'output.pdf', 'pwd')
    exit_mock.assert_not_called()


def test_run_cli_prompts_for_password_when_missing(mocker, capsys):
    mock_pwinput = mocker.patch('pdf_unlocker.app.pwinput.pwinput', return_value='prompted')
    mock_remove = mocker.patch('pdf_unlocker.app.remove_pdf_password')
    exit_mock = mocker.patch('pdf_unlocker.app.sys.exit')

    run_cli('input.pdf', 'output.pdf', '')

    captured = capsys.readouterr()
    assert "Processing: input.pdf..." in captured.out
    assert "Success! Unlocked file saved to: output.pdf" in captured.out
    mock_pwinput.assert_called_once_with(prompt="Enter PDF Password: ", mask="*")
    mock_remove.assert_called_once_with('input.pdf', 'output.pdf', 'prompted')
    exit_mock.assert_not_called()


def test_run_cli_password_error_exits_with_status_1(mocker, capsys):
    mocker.patch('pdf_unlocker.app.remove_pdf_password', side_effect=pikepdf.PasswordError())
    sys_exit = mocker.patch('pdf_unlocker.app.sys.exit', side_effect=SystemExit(1))

    with pytest.raises(SystemExit) as excinfo:
        run_cli('input.pdf', 'output.pdf', 'pwd')

    captured = capsys.readouterr()
    assert "Error: The password provided is incorrect." in captured.out
    assert excinfo.value.code == 1
    sys_exit.assert_called_once_with(1)


def test_run_cli_file_not_found_exits_with_status_1(mocker, capsys):
    mocker.patch('pdf_unlocker.app.remove_pdf_password', side_effect=FileNotFoundError())
    sys_exit = mocker.patch('pdf_unlocker.app.sys.exit', side_effect=SystemExit(1))

    with pytest.raises(SystemExit) as excinfo:
        run_cli('input.pdf', 'output.pdf', 'pwd')

    captured = capsys.readouterr()
    assert "Error: The input file 'input.pdf' could not be found." in captured.out
    assert excinfo.value.code == 1
    sys_exit.assert_called_once_with(1)


def test_run_cli_unexpected_exception_exits_with_status_1(mocker, capsys):
    mocker.patch('pdf_unlocker.app.remove_pdf_password', side_effect=Exception('boom'))
    sys_exit = mocker.patch('pdf_unlocker.app.sys.exit', side_effect=SystemExit(1))

    with pytest.raises(SystemExit) as excinfo:
        run_cli('input.pdf', 'output.pdf', 'pwd')

    captured = capsys.readouterr()
    assert "Error: An unexpected error occurred: boom" in captured.out
    assert excinfo.value.code == 1
    sys_exit.assert_called_once_with(1)


def test_module_executes_main_when_run_as_script(mocker, monkeypatch):
    mock_run_gui = mocker.Mock()
    fake_gui_module = types.ModuleType('pdf_unlocker.ui.pdf_unlocker_gui')
    fake_gui_module.run_gui = mock_run_gui

    monkeypatch.setitem(sys.modules, 'pdf_unlocker.ui.pdf_unlocker_gui', fake_gui_module)
    monkeypatch.setattr(sys, 'argv', ['unlock'])

    runpy.run_module('pdf_unlocker.app', run_name='__main__', alter_sys=True)

    mock_run_gui.assert_called_once()
