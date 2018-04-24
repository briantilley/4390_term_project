#! /usr/bin/env python3

# Defining a "page" as 8 consecutive lines of text, send a page
# prepended with enough whitespace to clear the console.
def extract_page(source_file, page_num):

     # extract a single page
     page = ""
     lines_seen = 0
     for c in source_file:
          if lines_seen >= page_num * 8:
               page += c

          if c == '\n':
               lines_seen += 1

          if lines_seen >= (page_num + 1) * 8:
               break

     if page[-1] == '\n':
     	page = page[:-1]

     print(page)

with open("content/bohemian_rhapsody.txt", 'r') as infile:
	extract_page(infile.read(), 0)