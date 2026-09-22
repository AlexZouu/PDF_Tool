from cache import cache
from datetime import datetime
from pypdf import PdfReader, PdfWriter
from tkinter import filedialog


def get_pdf():
  file_types = [('PDF', '*.pdf')]
  pdf_path = filedialog.askopenfilename(title="Select File", filetypes=file_types)   # Prompt the user to select the sheet with the stats
  pdf = PdfReader(pdf_path)
  return pdf_path, pdf


def validate_page_numbers(page_numbers):
  if not page_numbers: raise ValueError('Page numbers cannot be empty!')

  cleaned_page_numbers = page_numbers.strip()
  if cleaned_page_numbers[-1] == ',': cleaned_page_numbers = cleaned_page_numbers[:-1]

  if not cleaned_page_numbers[0].isdigit(): raise ValueError('The first page number must be an integer!')

  prev_char = prev_non_whitespace =  cleaned_page_numbers[0]

  is_page_range = False

  for curr_char in cleaned_page_numbers[1:]:
    match curr_char:
      case ' ':
        prev_char = curr_char
      case val if val.isdigit():
        if prev_char == ' ' and prev_non_whitespace.isdigit(): raise ValueError('Page numbers may not be split by spaces!')
        prev_char = prev_non_whitespace = curr_char
      case '-':
        if is_page_range: raise ValueError('Page range must only contain one "-"!')
        if prev_non_whitespace == ',': raise ValueError('Page range must start with an integer!')
        is_page_range = True
        prev_char = prev_non_whitespace = curr_char
      case ',':
        if prev_non_whitespace == '-': raise ValueError('Page range must end with an integer!')
        is_page_range = False
        prev_char = prev_non_whitespace = curr_char
      case _:
        raise ValueError(f'Unexpected character {curr_char}')

  return [item for item in ''.join(cleaned_page_numbers.split()).split(',') if item]


def get_pages_to_keep(page_offset, page_numbers, pdf_len):
  pages_to_keep = []

  if page_offset < 1: raise ValueError('The page offset must be at least 1!')

  page_offset -= 2

  for numbers in page_numbers:
    if '-' in numbers:
      page_range = [int(item) + page_offset for item in numbers.split('-')]
      page_range[1] += 1
      if page_range[0] >= pdf_len or page_range[1] >= pdf_len: raise ValueError('Page ranges can\'t exceed total length of the pdf!')
      if page_range[1] < page_range[0]: raise ValueError('The second page number in a range must be larger than the first page number!')
      if page_range[0] == page_range[1]: 
        pages_to_keep.append(page_range[0])
      else:
        pages_to_keep.extend(range(page_range[0], page_range[1]))
    else:
      page_num = int(numbers) + page_offset
      if page_num >= pdf_len: raise ValueError('Page numbers can\'t exceed total length of the pdf!')
      pages_to_keep.append(page_num)

  return pages_to_keep


def write_new_pdf(pdf_path, pdf, pages_to_keep):
  new_path = pdf_path[:-4] + ' ' + datetime.now().strftime("%Y-%m-%d %H-%M-%S") + '.pdf'
  pdf_writer = PdfWriter()

  for index, page in enumerate(pdf.pages):
    if index in pages_to_keep: pdf_writer.add_page(page)

  with open(new_path, "wb") as new_file:
    pdf_writer.write(new_file)


def create_duplicate_pdf(page_offset, page_numbers):
  page_numbers = validate_page_numbers(page_numbers)
  pdf_name, pdf = get_pdf()
  pages_to_keep = get_pages_to_keep(page_offset, page_numbers, len(pdf.pages))
  write_new_pdf(pdf_name, pdf, pages_to_keep)
  cache.cache_page_offset(page_offset)