import os
import pytest
import pikepdf
from pdf_unlocker.core.unlocker import remove_pdf_password

@pytest.fixture
def pdf_paths(tmp_path):
    """Fixture to create real temporary test PDFs."""
    input_path = os.path.join(tmp_path, "protected.pdf")
    output_path = os.path.join(tmp_path, "unlocked.pdf")
    # Create a fresh mini-PDF and encrypt it with a password
    with pikepdf.new() as pdf:
        pdf.add_blank_page()
        encryption = pikepdf.Encryption(owner="secret", user="secret", allow=pikepdf.Permissions(0))
        pdf.save(input_path, encryption=encryption)        
    return input_path, output_path


def test_remove_password_success(pdf_paths):
    """Test successful password removal."""
    input_path, output_path = pdf_paths
    # Run code under test
    remove_pdf_password(input_path, output_path, "secret")
    # Verify file was written and can open without a password
    assert os.path.exists(output_path)
    with pikepdf.open(output_path) as pdf:
        assert not pdf.is_encrypted


def test_remove_password_incorrect(pdf_paths):
    """Test that an incorrect password raises a PasswordError."""
    input_path, output_path = pdf_paths
    with pytest.raises(pikepdf.PasswordError):
        remove_pdf_password(input_path, output_path, "wrong_password")


def test_remove_password_file_not_found(tmp_path):
    """Test that a missing file raises a FileNotFoundError."""
    missing_input = os.path.join(tmp_path, "does_not_exist.pdf")
    output_path = os.path.join(tmp_path, "unlocked.pdf")
    with pytest.raises(FileNotFoundError):
        remove_pdf_password(missing_input, output_path, "secret")


def test_remove_password_unexpected_exception(pdf_paths, monkeypatch):
    """Test that any hidden underlying saving errors are successfully bubbled up."""
    input_path, output_path = pdf_paths
    # Simulate a deep unexpected file system crash during execution
    def mock_save(*args, **kwargs):
        raise RuntimeError("Unexpected disk failure")        
    monkeypatch.setattr(pikepdf.Pdf, "save", mock_save)
    
    with pytest.raises(RuntimeError, match="Unexpected disk failure"):
        remove_pdf_password(input_path, output_path, "secret")
