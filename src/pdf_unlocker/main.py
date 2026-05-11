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

def normalize_argv(argv):
    normalized = []
    for token in argv:
        if token.startswith("input_path="):
            normalized.append(token.split("=", 1)[1])
        elif token.startswith("output_path="):
            normalized.append(token.split("=", 1)[1])
        elif token.startswith("password="):
            normalized.append(token.split("=", 1)[1])
        else:
            normalized.append(token)
    return normalized


def main():
    parser = argparse.ArgumentParser(
        description="Remove password from PDF files",
        prog="unlock"
    )
    parser.add_argument("input_path", help="Path to the encrypted PDF file")
    parser.add_argument("output_path", help="Path to save the unlocked PDF file")
    parser.add_argument("password", help="Password to unlock the PDF")
    
    args = parser.parse_args(normalize_argv(sys.argv[1:]))
    remove_pdf_password(args.input_path, args.output_path, args.password)

if __name__ == "__main__":
    main()
