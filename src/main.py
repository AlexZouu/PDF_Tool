from cache import cache
import os
from pathlib import Path
from pdf import pdf
import tkinter as tk
from tkinter import messagebox


def validate_int(entry): return entry == '' or entry.isdigit()
def validate_range(entry): 
  if entry == '': return True
  for char in entry:
    if not (char.isdigit() or char == ',' or char == '-' or char == ' '): return False
  return True


def choose_pdf(root, offset, page_numbers):
  try:
    pdf.create_duplicate_pdf(offset, page_numbers)
  except Exception as e:
    messagebox.showerror(title='Oops!', message=f'An error has occured while trying to create a duplicate! Please try again, or contact PDF Tool tech support for help.\n\nError: {e}', parent=root)


def main():
  src_dir = str(Path(__file__).resolve().parent)
  os.environ['SRC_DIR'] = src_dir

  root = tk.Tk()

  vint = root.register(validate_int)
  vrange = root.register(validate_range)

  root.bind_all('<Button-1>', lambda event: event.widget.focus_set())
  # root.resizable(False, False)
  root.title('PDF Tool')
  root.geometry('500x365')
  
  root.columnconfigure(0, weight=1)
  root.columnconfigure(1, weight=0)
  root.columnconfigure(2, weight=0)
  root.columnconfigure(3, weight=0)
  root.columnconfigure(4, weight=1)

  title_label = tk.Label(root, text='PDF Tool', font=('Segoe UI', 16))
  # explanatory_text_label = tk.Label(root, text=config['explanatoryText'], wraplength=425, font=('Segoe UI', 12), justify='left')
  title_label.grid(row=0, column=2, pady=(20, 10))
  # explanatory_text_label.grid(row=1, column=1, columnspan=3, pady=(0, 10), sticky='w')

  page_offset_description_label = tk.Label(root, text='Which page of the PDF corresponds to the page numbered as 1 in the textbook', font=('Segoe UI', 10))
  page_offset_description_label.grid(row=1, column=1, columnspan=3)

  page_offset_label = tk.Label(root, text='Page offset: ', font=('Segoe UI', 10))
  page_offset_label.grid(row=2, column=1, pady=(10, 0))

  offset = tk.IntVar(value=cache.retrieve_page_offset())
  page_offset_entry = tk.Entry(root, textvariable=offset, validate='key', validatecommand=(vint, '%P'), font=('Segoe UI', 10))
  page_offset_entry.grid(row=2, column=2, pady=(10, 0), ipadx=2, ipady=2)

  page_numbers_description_label = tk.Label(root, text='For page ranges, enter the range in the format of "<start>-<end>". For single pages, please enter each individual page number. Please separate all page ranges and numbers with a comma.', font=('Segoe UI', 10))
  page_numbers_description_label.grid(row=3, column=1, columnspan=3, pady=(10,0))

  page_numbers_label = tk.Label(root, text='Page range: ', font=('Segoe UI', 10))
  page_numbers_label.grid(row=4, column=1, pady=(10, 0))

  page_numbers = tk.StringVar()
  page_numbers_entry = tk.Entry(root, textvariable=page_numbers, validate='key', validatecommand=(vrange, '%P'), font=('Segoe UI', 10))
  page_numbers_entry.grid(row=4, column=2, columnspan=2, pady=(10, 0), ipadx=2, ipady=2)

  choose_pdf_button = tk.Button(
      root, 
      text='Choose PDF', 
      command=lambda: choose_pdf(root, offset.get(), page_numbers.get()), 
      font=('Segoe UI', 8),
  )
  choose_pdf_button.grid(row=5, column=2)

  root.mainloop()
  

if __name__ == '__main__': 
  main()