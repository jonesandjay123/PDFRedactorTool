# PDFRedactorTool

A simple cross-platform Python GUI application for redacting sensitive keywords from PDF files. Built with [PyMuPDF](https://pypi.org/project/PyMuPDF/) for PDF processing and [Tkinter](https://docs.python.org/3/library/tkinter.html) for the user interface, this tool allows users to quickly remove sensitive information from PDF documents.

## Features

- **Multiple File Selection:** Easily select one or more PDF files for processing.
- **Intuitive Keyword Management:**
  - Add keywords individually using an input field and an "Add" button.
  - Remove selected keywords from the list with a "Remove" button.
- **PDF Redaction:** Automatically searches and redacts (covers with a black box) all occurrences of the specified keywords.
- **Output Files:** Saves redacted PDFs in the same directory as the input, appending `_redacted` to the original file name.

## Requirements

- Python 3.x
- [PyMuPDF](https://pypi.org/project/PyMuPDF/)
- Tkinter (usually included with Python)

## Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/yourusername/PDFRedactorTool.git
   cd PDFRedactorTool

   ```

2. **Set Up a Virtual Environment (Recommended):**

   ````bash
   python -m venv venv

   On Windows:
   ```bash
   venv\Scripts\activate
   ````

   On macOS/Linux:

   ```bash
   source venv/bin/activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

**Launch the Application:**

```bash
python main.py
```

Using the GUI:

- Click "Select PDF Files" to choose one or more PDFs.
- Enter a keyword in the "Enter Keyword:" field and click the "+" button to add it to the list.
- Remove any unwanted keyword by selecting it in the list and clicking "- Remove Selected Keyword".
- Click "Start Processing" to redact the selected keywords from the PDFs. Redacted files will be saved with \_redacted appended to their filenames.

## Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request if you have ideas for improvements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

You can adjust the repository URL, your username, and other details as needed. This setup should provide a clear, professional overview for your GitHub repo and help others understand and use your tool quickly.
