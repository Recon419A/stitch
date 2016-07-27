# Stitch README

Stitch is a universal file includer. It reads a file, expands includes in that
file recursively (deep expansion) and then either prints the result or outputs
it to the specified file.

## Features
+ Works with any language
+ Recursively expands includes
+ Performs smart indentation
+ Aborts circular includes

## Use Case
Stitch is particularly helpful for the case where you need to parse code written
in one language using another language, in which instance it can be used to
expand the includes in that code. Take Aglio's support for markdown includes.
Normally, because those includes aren't a part of the markdown standard, and are
only supported by Aglio, markdown that includes them isn't parseable by other
tools like Drafter; with Stitch, it's easy and painless to make such a pipeline
work.

It's even possible to use Stitch to support your own personal include syntax
in any kind of file.

## Usage at the Command Line
Stitch is designed to run from the command line of any system that has Python 3
installed. This allows for it to be called from any language that can interface
with the command line (which is most of them), or be run manually. Usage is as
simple as running

```
python stitch.py input_file 'left_regex' 'right_regex' [-o output_file]
```

This command will cause Stitch to look at the input file, find all include
statements that have the provided left and right syntax (which are regular
expressions), and replace them with the contents of the files whose names are
wrappered by the left-hand and right-hand regular expressions. If an output file
is specified, Stitch will write to that output; if not, it will print to
standard out. Note that redirecting standard out will also capture warnings
from the program; the output option should be used if this behavior is not
desired.