from tkinter import *
from tkinter import filedialog, messagebox
from PyPDF2 import PdfReader
from gtts import gTTS
import os

DARK_GREY = "#272727"


def extract_text_from_pdf(file_path, file_name, new_folder):
    # Extracts text from the selected PDF file converts the file to audio

    reader = PdfReader(file_path)

    # determine number of pages
    number_of_pages = len(reader.pages)

    extracted_text = ""

    # runs loop according to number of pages & creates audio file for every page to expedite process & reduce waiting time + file size
    for x in range(number_of_pages):

        # Create new folder if it doesn't exist
        os.makedirs(new_folder, exist_ok=True)

        # extracts the text from the page
        extracted_text += reader.pages[x].extract_text()

        if extracted_text:
            # Update UI with current page status
            status_label.config(text=f"Processing page {x + 1} of {number_of_pages}... Please wait.")
            window.update()  # Refresh the window to show updates

        # Define output file path for audio file
        audio_file_path = os.path.join(new_folder, f'{file_name} page {x}.mp3')

        # Notify user that an existing file will be overwritten
        if os.path.exists(audio_file_path):
            messagebox.showinfo("Overwriting File",f"'{file_name} page {x}.mp3' already exists and will be overwritten.")

        try:
            # Convert text to speech
            text2speech = gTTS(text=extracted_text, lang='en')
        except AssertionError:
            messagebox.showerror("Error", "No text to convert to speech.")
            status_label.config(text=f"Error, No text to convert to speech in file.")
            window.update()  # Refresh UI
            return

        # Save the speech to an MP3 file
        text2speech.save(audio_file_path)

        # reset text variable
        extracted_text = ""


def upload_pdf_and_convert():
    # Open file explorer to select a PDF file
    file_path = filedialog.askopenfilename(
        title="Select a PDF file",
        filetypes=[("PDF Files", "*.pdf")]  # Only allow PDF files
    )

    if not file_path:  # Check if no file was selected
        messagebox.showerror("Error", "No file selected. Please select a valid PDF file.")
        return

    if not file_path.lower().endswith('.pdf'):  # Check if the selected file is not a PDF
        messagebox.showerror("Error", "Invalid file type. Please select a PDF file.")
        return

    # get file name
    file_name = os.path.splitext(os.path.basename(file_path))[0] + " audio"
    # get directory path
    directory_path = os.path.dirname(file_path)
    # new folder path + new file name places in same folder as original document
    new_folder = f"{directory_path}/{file_name}"

    status_label.config(text="Preparing your audio files... Please wait.")
    window.update()  # Refresh UI

    if file_path:  # If a file was selected
        extract_text_from_pdf(file_path, file_name, new_folder)
        if status_label.cget("text") == "Error, No text to convert to speech in file.":
            status_label.config(text="Error, No text to convert to speech in file.")
            window.update()  # Refresh UI
        else:
            status_label.config(text=f"Success your files are in \n{new_folder}")
            window.update()  # Refresh UI


# creates UI for app
window = Tk()
window.title("PDF to AUDIO CONVERTER")
window.geometry("1200x250")
window.config(bg=DARK_GREY)
window.iconbitmap('headphones.ico')

# title
title = Label(text="PDF to AUDIO CONVERTER", foreground="green", bg=DARK_GREY, font=("Arial", 31, "bold"), pady=10)
title.pack()

# Status label for showing progress updates
status_label = Label(window, text="click below to select your PDF file & convert to audio", fg="white", bg=DARK_GREY, font=("Arial", 13, "bold"))
status_label.pack(pady=10)

# start button triggers Start function which triggers countdown
start_upload = Button(text="upload & convert", command=upload_pdf_and_convert, width=75, bg="green", fg="white")
start_upload.pack(pady=10)

window.mainloop()
