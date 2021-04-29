# cs50-wiki
my implementation for CS50's assignment to create a wikipedia like website for storing informative articles

## Implementation

This website does not have any models. The "encyclopedia/util.py" file contains functions to
Search, create, edit and delete files. 
All the entries are in the "entries" directory and are recognized by their extension ".md"
That is, markdown files. The User has to write all the content in markdown format.

Rich Markdown Text is displayed in the template using Jinja's filter "safe"
