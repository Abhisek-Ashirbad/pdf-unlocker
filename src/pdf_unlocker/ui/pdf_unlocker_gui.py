import customtkinter as ctk
import os
import pikepdf
import sys

from pdf_unlocker.core.unlocker import remove_pdf_password
from tkinter import filedialog, messagebox

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class PDFUnlockerUI(ctk.CTk):
    """Graphical User Interface for PDF Password Removal using CustomTkinter."""

    def __init__(self):
        """Initialize the main application window and its widgets."""
        super().__init__()
        self.title("PDF Password Remover")
        self.geometry("500x350")
        self.resizable(True, True)
        
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.abspath(".")
            
        # Point to where the icon asset is stored inside the build layout
        icon_path = os.path.join(base_path, "pdf_unlocker", "assets", "unlock_icon_256.ico")
        
        # Apply the icon to the window framework
        if os.path.exists(icon_path):
            self.wm_iconbitmap(icon_path)

        self.input_file = ""
        self.output_file = ""
        self.create_widgets()


    def create_widgets(self):
        """Set up the GUI components: buttons, labels, and entry fields."""
        self.btn_input = ctk.CTkButton(self, text="Select Protected PDF", command=self.select_input)
        self.btn_input.pack(pady=(20, 5))
        self.lbl_input = ctk.CTkLabel(self, text="No file selected", text_color="gray")
        self.lbl_input.pack(pady=(0, 15))

        self.btn_output = ctk.CTkButton(self, text="Select Save Destination", command=self.select_output)
        self.btn_output.pack(pady=5)
        self.lbl_output = ctk.CTkLabel(self, text="No destination selected", text_color="gray")
        self.lbl_output.pack(pady=(0, 15))

        self.lbl_pwd = ctk.CTkLabel(self, text="Enter PDF Password:")
        self.lbl_pwd.pack(pady=2)
        self.entry_pwd = ctk.CTkEntry(self, placeholder_text="Password", show="•", width=250)
        self.entry_pwd.pack(pady=5)

        self.btn_unlock = ctk.CTkButton(self, text="Unlock PDF", fg_color="green", hover_color="darkgreen", command=self.unlock_pdf)
        self.btn_unlock.pack(pady=25)


    def select_input(self):
        """Open a file dialog to select the protected PDF file."""
        file = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if file:
            self.input_file = file
            self.lbl_input.configure(text=os.path.basename(file), text_color="white")


    def select_output(self):
        """Open a file dialog to select the save destination for the unlocked PDF."""
        file = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")])
        if file:
            self.output_file = file
            self.lbl_output.configure(text=os.path.basename(file), text_color="white")


    def unlock_pdf(self):
        """Attempt to remove the password from the selected PDF using the provided password."""
        if not self.input_file or not self.output_file:
            messagebox.showerror("Error", "Please select both input and output paths.")
            return
            
        password = self.entry_pwd.get()
        if not password:
            messagebox.showerror("Error", "Password cannot be empty.")
            return

        try:
            # Execute the shared decoupled logic function
            remove_pdf_password(self.input_file, self.output_file, password)
            
            messagebox.showinfo("Success", f"Password removed successfully!\nSaved to: {os.path.basename(self.output_file)}")
            self.entry_pwd.delete(0, 'end')
        except pikepdf.PasswordError:
            messagebox.showerror("Error", "Incorrect password. Please try again.")
        except FileNotFoundError:
            messagebox.showerror("Error", "The specified input file was not found.")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred:\n{str(e)}")


def run_gui():
    """Launch the PDF Unlocker GUI application."""
    ui_app = PDFUnlockerUI()
    ui_app.mainloop()
