import json
import os


def cache_parameter(key, value):
  cache_dir = os.getenv('CACHE_DIR')
  try:
    with open(cache_dir, 'r') as cache_file:
      cache = json.load(cache_file)

    cache[key] = value

    with open(cache_dir, 'w') as cache_file:
      json.dump(cache, cache_file)
  except (FileNotFoundError, json.JSONDecodeError):   # If the file doesn't exist or is empty, write the value
    with open(cache_dir, 'w') as cache_file:
      json.dump({key: value}, cache_file)


def retrieve_parameter(key):
  cache_dir = os.getenv('CACHE_DIR')
  try:
    with open(cache_dir, 'r') as cache_file:
      cache = json.load(cache_file)
    return cache.get(key)
  except (FileNotFoundError, json.JSONDecodeError):   # If the file doesn't exist or is empty, write the value
    with open(cache_dir, 'w') as cache_file:
      json.dump({}, cache_file)
      return None


def cache_page_offset(page_offset):
  cache_parameter('pageOffset', page_offset)


def retrieve_page_offset():
  offset = retrieve_parameter('pageOffset')
  if offset: return offset
  return 1