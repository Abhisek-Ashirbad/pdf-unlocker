import argparse
import sys

from .core.unlocker import remove_pdf_password


def main():
    parser = argparse.ArgumentParser(
        description="Remove password from PDF file(s)",
        prog="unlock"
    )
    parser.add_argument("-i", "--input_path", required=True, help="Path to the protected PDF")
    parser.add_argument("-o", "--output_path", required=False, default="unlocked.pdf", help="Path to save the unlocked PDF")
    parser.add_argument("-p", "--password", required=True, help="The PDF password")
    
    args = parser.parse_args()
    remove_pdf_password(args.input_path, args.output_path, args.password)


if __name__ == "__main__":
    main()
