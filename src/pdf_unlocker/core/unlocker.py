import pikepdf

def remove_pdf_password(input_path: str, output_path: str, password: str) -> None:
    """Removes the password from a PDF file and saves it to the \
       specified path without password and raises exceptions, on 
       failure."""
    # Open the encrypted PDF
    with pikepdf.open(input_path, password=password) as pdf:
        # Save it without encryption
        pdf.save(output_path)