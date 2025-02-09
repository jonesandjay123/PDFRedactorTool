# main.py
import os
import fitz  # PyMuPDF
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext

# --------------------------
# Function: Redact sensitive keywords in a PDF file.
# --------------------------
def redact_pdf(file_path, keywords, output_folder):
    """
    Process a PDF file by redacting all occurrences of the specified keywords.
    
    Parameters:
        file_path (str): The path to the input PDF file.
        keywords (list): A list of keywords to be redacted.
        output_folder (str): The folder where the redacted PDF will be saved.
    
    Returns:
        output_path (str): The path to the saved redacted PDF file.
    """
    try:
        doc = fitz.open(file_path)
        for page_num in range(len(doc)):
            page = doc[page_num]
            for kw in keywords:
                # Search for the keyword in the page (case-sensitive)
                text_instances = page.search_for(kw)
                for inst in text_instances:
                    # Add a redaction annotation with black fill to cover the sensitive text.
                    page.add_redact_annot(inst, fill=(0, 0, 0))
            # Apply the redaction annotations on the page.
            page.apply_redactions()
        
        # Create output file name: original name with _redacted appended.
        base_name = os.path.basename(file_path)
        name, ext = os.path.splitext(base_name)
        output_name = f"{name}_redacted{ext}"
        output_path = os.path.join(output_folder, output_name)
        doc.save(output_path)
        doc.close()
        return output_path
    except Exception as e:
        raise RuntimeError(f"Error processing {file_path}: {e}")

# --------------------------
# GUI Application for PDF Redaction Tool.
# --------------------------
class PDFRedactorGUI:
    def __init__(self, master):
        self.master = master
        master.title("PDF Redactor Tool")
        master.geometry("600x500")

        # File selection section
        self.select_button = tk.Button(master, text="Select PDF Files", command=self.select_files)
        self.select_button.pack(pady=5)

        self.file_label = tk.Label(master, text="No files selected")
        self.file_label.pack()

        # Keyword input section with list management
        keyword_frame = tk.Frame(master)
        keyword_frame.pack(pady=10)

        self.keyword_label = tk.Label(keyword_frame, text="Enter Keyword:")
        self.keyword_label.grid(row=0, column=0, padx=5)

        self.keyword_entry = tk.Entry(keyword_frame, width=30)
        self.keyword_entry.grid(row=0, column=1, padx=5)

        self.add_keyword_button = tk.Button(keyword_frame, text="+", width=3, command=self.add_keyword)
        self.add_keyword_button.grid(row=0, column=2, padx=5)

        # Listbox to display added keywords
        self.keyword_listbox = tk.Listbox(master, width=50, height=5)
        self.keyword_listbox.pack(pady=5)

        # Button to remove selected keyword from the listbox
        self.remove_keyword_button = tk.Button(master, text="- Remove Selected Keyword", command=self.remove_keyword)
        self.remove_keyword_button.pack(pady=5)

        # Process button
        self.process_button = tk.Button(master, text="Start Processing", command=self.process_pdfs)
        self.process_button.pack(pady=10)

        # Log output text area
        self.log_text = scrolledtext.ScrolledText(master, width=70, height=10, state='disabled')
        self.log_text.pack(pady=10)

        # Output folder (default to current working directory)
        self.output_folder = os.getcwd()
        self.files = []  # List to store selected PDF file paths

    def log(self, message):
        """Log messages to the log text area."""
        self.log_text.config(state='normal')
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state='disabled')
        self.master.update()

    def select_files(self):
        """Open a file dialog to select PDF files."""
        files = filedialog.askopenfilenames(
            title="Select PDF Files",
            filetypes=[("PDF Files", "*.pdf")])
        if files:
            self.files = list(files)
            self.file_label.config(text=f"{len(self.files)} file(s) selected")
            self.log(f"Selected files: {self.files}")
        else:
            self.log("No files selected.")

    def add_keyword(self):
        """Add the keyword from the entry to the keyword listbox."""
        keyword = self.keyword_entry.get().strip()
        if keyword:
            # Avoid duplicate keywords.
            existing_keywords = self.keyword_listbox.get(0, tk.END)
            if keyword not in existing_keywords:
                self.keyword_listbox.insert(tk.END, keyword)
                self.log(f"Added keyword: {keyword}")
                self.keyword_entry.delete(0, tk.END)
            else:
                messagebox.showinfo("Info", f"Keyword '{keyword}' is already in the list.")
        else:
            messagebox.showwarning("Warning", "Please enter a keyword.")

    def remove_keyword(self):
        """Remove the selected keyword from the listbox."""
        selected_indices = self.keyword_listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("Warning", "Please select a keyword to remove.")
            return
        for index in reversed(selected_indices):
            keyword = self.keyword_listbox.get(index)
            self.keyword_listbox.delete(index)
            self.log(f"Removed keyword: {keyword}")

    def process_pdfs(self):
        """Process each selected PDF file to redact specified keywords."""
        if not self.files:
            messagebox.showwarning("Warning", "Please select at least one PDF file.")
            return

        # Get keywords from the listbox.
        keywords = list(self.keyword_listbox.get(0, tk.END))
        if not keywords:
            messagebox.showwarning("Warning", "Please add at least one keyword to redact.")
            return

        self.log("Starting processing of files...")
        for file_path in self.files:
            self.log(f"Processing: {file_path}")
            try:
                output_file = redact_pdf(file_path, keywords, self.output_folder)
                self.log(f"Completed: Output file saved as {output_file}")
            except Exception as e:
                self.log(str(e))
        self.log("All files have been processed!")
        messagebox.showinfo("Done", "All files have been processed successfully.")

# --------------------------
# Main entry point
# --------------------------
def main():
    root = tk.Tk()
    app = PDFRedactorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
