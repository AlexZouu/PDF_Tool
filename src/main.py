from cache import cache
import os
from pathlib import Path
from pdf import pdf
import shutil
import tkinter as tk
from tkinter import messagebox


def clear_cache(root):
  try:
    app_dir = os.getenv('APP_DIR')
    shutil.rmtree(app_dir)
    messagebox.showinfo(title='Success!', message='Your cache has been cleared!', parent=root)
  except Exception as e:
    messagebox.showerror(title='Oh no!', message=f'Something went wrong when clearing cache!\n\n{e}', parent=root)


def validate_int(entry): return entry == '' or entry.isdigit()


def validate_range(entry): 
  if entry == '': return True
  for char in entry:
    if not (char.isdigit() or char == ',' or char == '-' or char == ' '): return False
  return True


def choose_pdf(root, offset, page_numbers):
  try:
    pdf.create_duplicate_pdf(offset, page_numbers)
    messagebox.showinfo(title='Success!', message='The new PDF has been created!', parent=root)
  except Exception as e:
    messagebox.showerror(title='Oops!', message=f'An error has occured while trying to create a duplicate! Please try again, or contact PDF Tool tech support for help.\n\nError: {e}', parent=root)


def main():
  appdata_dir = Path(os.environ["LOCALAPPDATA"])
  app_folder = appdata_dir / 'PDFTool'
  cache_dir = app_folder / 'cache.json'
  app_folder.mkdir(parents=True, exist_ok=True)
  os.environ['APP_DIR'] = str(app_folder)
  os.environ['CACHE_DIR'] = str(cache_dir)

  root = tk.Tk()

  vint = root.register(validate_int)
  vrange = root.register(validate_range)

  root.bind_all('<Button-1>', lambda event: event.widget.focus_set())
  root.title('PDF Tool')
  root.geometry('500x345')
  
  root.columnconfigure(0, weight=1)
  root.columnconfigure(1, weight=0)
  root.columnconfigure(2, weight=0)
  root.columnconfigure(3, weight=0)
  root.columnconfigure(4, weight=1)

  title_label = tk.Label(root, text='PDF Tool', justify='center', font=('Segoe UI', 16))
  title_label.grid(row=0, column=2, pady=(20, 10))

  page_offset_description_label = tk.Label(root, text='Please enter the page offset.\nThe page offset is the page of the PDF that corresponds to the page numbered as 1 in the textbook.', wraplength=425, justify='center', font=('Segoe UI', 10))
  page_offset_description_label.grid(row=1, column=1, columnspan=3, sticky='n')

  page_offset_frame = tk.Frame(root)
  page_offset_frame.grid(row=2, column=1, columnspan=3)

  page_offset_label = tk.Label(page_offset_frame, text='Page offset: ', font=('Segoe UI', 10), justify='right')
  page_offset_label.grid(row=2, column=1, pady=(10, 0), sticky='e')

  offset = tk.IntVar(value=cache.retrieve_page_offset())
  page_offset_entry = tk.Entry(page_offset_frame, textvariable=offset, validate='key', validatecommand=(vint, '%P'), width=5, justify='center', font=('Segoe UI', 10))
  page_offset_entry.grid(row=2, column=2, pady=(10, 0), ipadx=2, ipady=2, sticky='w')

  page_numbers_description_label = tk.Label(root, text='Please enter which pages you would like to keep.\nFor page ranges, enter the range in the format of "<start>-<end>".\nFor single pages, please enter each individual page number.\nPlease separate all page ranges and numbers with a comma.', wraplength=425, justify='center', font=('Segoe UI', 10))
  page_numbers_description_label.grid(row=3, column=1, columnspan=3, pady=(10,0))

  page_numbers_frame = tk.Frame(root)
  page_numbers_frame.grid(row=4, column=1, columnspan=3)

  page_numbers_label = tk.Label(page_numbers_frame, text='Pages to keep: ', font=('Segoe UI', 10), justify='right')
  page_numbers_label.grid(row=4, column=1, pady=(10, 10), sticky='e')

  page_numbers = tk.StringVar()
  page_numbers_entry = tk.Entry(page_numbers_frame, textvariable=page_numbers, validate='key', validatecommand=(vrange, '%P'), width=40, justify='left', font=('Segoe UI', 10))
  page_numbers_entry.grid(row=4, column=2, columnspan=2, pady=(10, 10), ipadx=2, ipady=2, sticky='w')

  button_frame = tk.Frame(root)
  button_frame.grid(row=5, column=1, columnspan=3)

  choose_pdf_button = tk.Button(
      button_frame, 
      text='Choose PDF', 
      command=lambda: choose_pdf(root, offset.get(), page_numbers.get()), 
      font=('Segoe UI', 10),
      justify='center',
  )
  choose_pdf_button.grid(row=5, column=0, pady=(0, 10), padx=(0, 30))

  clear_cache_button = tk.Button(
      button_frame, 
      text='Clear Cache', 
      command=lambda: clear_cache(root), 
      font=('Segoe UI', 10),
      justify='center'
  )
  clear_cache_button.grid(row=5, column=1, pady=(0, 10))

  root.mainloop()
  

if __name__ == '__main__': 
  main()