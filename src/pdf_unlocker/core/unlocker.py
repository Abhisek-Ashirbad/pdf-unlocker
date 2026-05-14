import pikepdf

def remove_pdf_password(input_path, output_path, password):
    """Removes the password from a PDF file and saves it to the \
       specified path without password."""
    try:
        # Open the encrypted PDF
        with pikepdf.open(input_path, password=password) as pdf:
            # Save it without encryption
            pdf.save(output_path)
        print(f"Success! Password removed and saved to: {output_path}")
    except Exception as e:
        print(f"Error: {e}")