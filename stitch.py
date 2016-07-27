"""
Stitch Version 0.2.0

The purpose of Stitch is to provide a universal, standalone includer that can be
run on any system with Python installed. Stitch is designed to help interface
with files that contain includes not supported natively by your language. When
implemented, it will run cleanly without leaving any files in the working
directory unless specified, and will be syntax agnostic.
"""

import re
import sys
import os
import argparse

def process_file(filename, include_regex, args):
    working_directory = os.path.dirname(filename)
    with open(filename) as f:
        file_text = f.read()
    return expand_includes(file_text, include_regex, working_directory, args,
                           ())


def expand_first_include(file_text, include_regex, working_directory, args,
                         recursive_list):
    include_match = include_regex.search(file_text)
    
    if include_match is None:
        return file_text
    
    begin_include = include_match.start(0)
    begin_filename = include_match.start(1)
    end_filename = include_match.end(1)
    end_include = include_match.end(0)
    
    include_statement = file_text[begin_include:end_include]
    filename = file_text[begin_filename:end_filename]
    indentation_string = get_indentation_string(file_text, include_match)

    file_path = os.path.join(working_directory, filename)
    working_directory = os.path.dirname(file_path)
    
    with open(file_path) as f:
        include_text = f.read()
        if file_path in recursive_list:
            include_text = ''
            print('WARN: circular inclusion of ' + file_path + ' in ' + 
                  recursive_list[-1] + 
                  ' is being replaced by empty string')
        if not args.noindent:
            include_text = add_line_beginning(include_text, indentation_string,
                                              first_line_beginning='')
        include_text = expand_includes(include_text, include_regex,
                                       working_directory, args,
                                       recursive_list + (file_path,))

        expanded_text = file_text.replace(include_statement, include_text, 1)
    
    return expanded_text
    

def expand_includes(file_text, include_regex, working_directory, args,
                    recursive_list):
    new_text = expand_first_include(file_text, include_regex,
                                    working_directory, args,
                                    recursive_list)
    while new_text != file_text:
        file_text = new_text
        new_text = expand_first_include(file_text, include_regex,
                                        working_directory, args,
                                        recursive_list)
    return new_text


def get_indentation_string(file_text, include_match):
    break_position = file_text.rfind('\n', 0, include_match.start(0))
    indentation_string = file_text[break_position + 1:include_match.start(0)]
    return indentation_string

    
def add_line_beginning(file_text, line_beginning,
                       first_line_beginning=None, last_line_beginning=None):
    """
    Prepends a string to each line in a file.
    
    Optional arguments for first and last line modify these lines from the
    default value.
    """

    lines = file_text.split('\n')

    if first_line_beginning is None:
        first_line_beginning = line_beginning
    if last_line_beginning is None:
        last_line_beginning = line_beginning

    lines[0] = first_line_beginning + lines[0]
    for i in range(1, len(lines) - 1):
        lines[i] = line_beginning + lines[i]
    lines[-1] = last_line_beginning + lines[-1]

    return '\n'.join(lines)
    
    
def handle_arguments():
    parser = argparse.ArgumentParser(description='Expand includes in a file.')
    parser.add_argument('input_file', help='the file to read from')
    parser.add_argument('-o', dest='output_file',
                        help='the file to write to')
    parser.add_argument('left_match', help='the regex introducing a comment')
    parser.add_argument('right_match', help='the regex closing a comment')
    parser.add_argument('--noindent', action='store_true',
                        help='don\'t apply auto-indentation)')
    return parser.parse_args(sys.argv[1:])
    
    
def main():
    args = handle_arguments()
    regex = re.compile(args.left_match + '(\S*)' + args.right_match)
    expanded_text = process_file(args.input_file, regex, args)
    if args.output_file is not None:
        with open(args.output_file, mode='w') as f:
            f.write(expanded_text)
    else:
        print(expanded_text)
    
main()
