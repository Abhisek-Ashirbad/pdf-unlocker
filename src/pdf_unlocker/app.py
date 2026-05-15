import argparse
import pikepdf
import pwinput
import sys

from pdf_unlocker.core.unlocker import remove_pdf_password


def run_cli(input_path, output_path, password):
    # Fallback to masked terminal prompt if -p wasn't explicitly typed
    if not password:
        password = pwinput.pwinput(prompt="Enter PDF Password: ", mask="*")

    print(f"Processing: {input_path}...")
    try:
        # Execute the exact same shared logic function
        remove_pdf_password(input_path, output_path, password)
        print(f"Success! Unlocked file saved to: {output_path}")
    except pikepdf.PasswordError:
        print("Error: The password provided is incorrect.")
        sys.exit(1)
    except FileNotFoundError:
        print(f"Error: The input file '{input_path}' could not be found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error: An unexpected error occurred: {e}")
        sys.exit(1)


def main():
    # If no arguments are provided, launch the GUI
    if len(sys.argv) == 1:
        from pdf_unlocker.ui.pdf_unlocker_gui import run_gui
        run_gui()
        return

    parser = argparse.ArgumentParser(
        description="Remove password from PDF file(s)",
        prog="unlock"
    )
    parser.add_argument("-i", "--input_path", required=True, help="Path to the protected PDF")
    parser.add_argument("-o", "--output_path", required=False, default="unlocked.pdf", help="Path to save the unlocked PDF")
    parser.add_argument("-p", "--password", required=True, help="The PDF password")
    
    args = parser.parse_args()
    run_cli(args.input_path, args.output_path, args.password)


if __name__ == "__main__":
    main()
