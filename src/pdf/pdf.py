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
        prev_char = prev_non_whitespace = curr_char
      case _:
        raise ValueError(f'Unexpected character {curr_char}')


    


def create_duplicate_pdf(page_offset, page_numbers):
  page_numbers = validate_page_numbers(page_numbers)