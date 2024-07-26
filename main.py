import tkinter as tk
from tkinter import filedialog, messagebox
import requests
from pypdf import PdfReader
import creds

VOICE_RSS_ENDPOINT = 'https://api.voicerss.org/'
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0'}


def extract_text_and_convert():
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if not file_path:
        return

    try:
        page_number = int(page_entry.get())
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid page number.")
        return

    try:
        reader = PdfReader(file_path)
        page = reader.pages[page_number - 1]
        text = page.extract_text()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to extract text from the PDF: {e}")
        return

    parameters = {
        'key': creds.API_KEY,
        'src': text,
        'hl': 'hr-hr',
        'v': 'Nikola'
    }

    try:
        response = requests.get(url=VOICE_RSS_ENDPOINT, headers=HEADERS, params=parameters, stream=True)
        response.raise_for_status()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to convert text to audio: {e}")
        return

    save_path = filedialog.asksaveasfilename(defaultextension=".mp3", filetypes=[("MP3 files", "*.mp3")])
    if not save_path:
        return

    try:
        with open(save_path, 'wb') as f:
            f.write(response.content)
        messagebox.showinfo("Success", f"Audio saved successfully to {save_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save audio file: {e}")


# Tkinter GUI
root = tk.Tk()
root.title("PDF to Audio Converter")

frame = tk.Frame(root, padx=10, pady=10)
frame.pack(padx=10, pady=10)

page_label = tk.Label(frame, text="Page Number:")
page_label.grid(row=0, column=0, sticky="e")

page_entry = tk.Entry(frame)
page_entry.grid(row=0, column=1, pady=5)

convert_button = tk.Button(frame, text="Convert to Audio", command=extract_text_and_convert)
convert_button.grid(row=1, columnspan=2, pady=10)

root.mainloop()













