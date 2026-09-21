import json
import os
from pathlib import Path


def cache_parameter(key, value):
  src_dir = os.getenv('SRC_DIR')
  try:
    with open(f'{src_dir}/cache/cache.json', 'r') as cache_file:
      cache = json.load(cache_file)

    cache[key] = value

    with open(f'{src_dir}/cache/cache.json', 'w') as cache_file:
      json.dump(cache, cache_file)
  except (FileNotFoundError, json.JSONDecodeError):   # If the file doesn't exist or is empty, write the value
    with open(f'{src_dir}/cache/cache.json', 'w') as cache_file:
      json.dump({key: value}, cache_file)


def retrieve_parameter(key):
  src_dir = os.getenv('SRC_DIR')
  try:
    with open(f'{src_dir}/cache/cache.json', 'r') as cache_file:
      cache = json.load(cache_file)
    return cache.get(key)
  except (FileNotFoundError, json.JSONDecodeError):   # If the file doesn't exist or is empty, write the value
    with open('cache/cache.json', 'w') as cache_file:
      json.dump({}, cache_file)
      return None


def cache_page_offset(page_offset):
  cache_parameter('pageOffset', page_offset)


def retrieve_page_offset():
  return retrieve_parameter('pageOffset')