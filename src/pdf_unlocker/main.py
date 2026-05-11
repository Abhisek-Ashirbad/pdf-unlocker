import sys
import argparse
import pikepdf

def remove_pdf_password(input_path, output_path, password):
    try:
        # Open the encrypted PDF
        with pikepdf.open(input_path, password=password) as pdf:
            # Save it without encryption
            pdf.save(output_path)
        print(f"Success! Password removed and saved to: {output_path}")
    except Exception as e:
        print(f"Error: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="Remove password from PDF file(s)",
        prog="unlock"
    )
    parser.add_argument("-i", "--input_path", required=True, help="Path to the protected PDF")
    parser.add_argument("-o", "--output_path", required=True, help="Path to save the unlocked PDF")
    parser.add_argument("-p", "--password", required=True, help="The PDF password")
    
    args = parser.parse_args()
    remove_pdf_password(args.input_path, args.output_path, args.password)


if __name__ == "__main__":
    main()
