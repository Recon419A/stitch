"""
Stitch Version 0.0.0

The purpose of Stitch is to provide a universal, standalone includer that can be
run on any system with Python installed. Stitch is designed to help interface
with files that contain includes not supported natively by your language. When
implemented, it will run cleanly without leaving any files in the working
directory unless specified, and will be syntax agnostic.
"""

import re
import sys
import argparse

def process_file(filename, left_strip, right_strip):
    with open(filename) as f:
        file_text = f.read()
    print(expand_includes(file_text, left_strip, right_strip))


def expand_first_include(file_text, left_strip, right_strip):
    include_regex = left_strip + r'([\w,\.]*)' + right_strip
    include_match = re.search(include_regex, file_text)
    
    if include_match is None:
        return file_text
    
    begin_include = include_match.start(0)
    begin_filename = include_match.start(1)
    end_filename = include_match.end(1)
    end_include = include_match.end(0)
    
    include_statement = file_text[begin_include:end_include]
    filename = file_text[begin_filename:end_filename]
    
    with open(filename) as f:
        include_text = f.read()
        include_text = expand_includes(include_text, left_strip, right_strip)
        expanded_text = file_text.replace(include_statement, include_text, 1)
    
    return expanded_text
    

def expand_includes(file_text, left_strip, right_strip):
    new_text = expand_first_include(file_text, left_strip, right_strip)
    while new_text != file_text:
        file_text = new_text
        new_text = expand_first_include(file_text, left_strip, right_strip)
    return new_text
    
    
def handle_arguments():
    parser = argparse.ArgumentParser(description='Expand includes in a file.')
    parser.add_argument('input_file', help='the file to read from')
    parser.add_argument('-o', dest='output_file',
                        help='the file to write to')
    parser.add_argument('left_match', help='the regex introducing a comment')
    parser.add_argument('right_match', help='the regex closing a comment')
    return parser.parse_args(sys.argv[1:])
    
    
def main():
    args = handle_arguments()
    regex = re.compile(args.left_match + r'([\w,\.]*)' + args.right_match)
    process_file(args.input_file, regex)
    
# process_file("index.txt", r'#include\( *', r' *\)')
# process_file("include1.txt", r'<!-- *include\(', r'\) *-->')

main()