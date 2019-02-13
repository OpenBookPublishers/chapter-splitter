# chapter-splitter
*chapter-splitter* is a small utility to split PDF books by chapters and write metadata into the generated files.

## Installation
Besides python standard libraries, *chapter-splitter* requires **pdfunite** and **exiftool** to be installed on your system. These tools are available  in the official repositories of debian/debian-based distributions.

### Configuration
The *config.ini* file takes base configuration settings.
* *api_url* is the base URL of the API where to gather DOI metadata.
* *separator_char* is the character which separates the book DOI from the chapter-level sequential number (i.e. 10.11647/OBP.0152 **.** 01).
* *leading_zeros* is the number of leading zeros in the chapter-level DOI number progression (i.e. 01, 10, 100).
* *cover_file_name* and *copyright_file_name* are the filenames of the cover and copyright pages.

## Use
1. Prepare the input folder. The folder must store the pages of the book-body chapters saved as individual PDF files (tick "Create Separate PDF Files" in InDesign when exporting or use another command-line tool). The filenames don't really matter, as long as the pages can be ordered sequentially by natural sort of numbers within the filename (i.e. 'Hobbs-Provincial-Press_01.pdf', 'Hobbs-Provincial-Press_02.pdf'). Cover and copyright pages must be named as previously defined in the *config.ini* file.

2. Run the script as `python3 main.py /input/foder /output/folder --doi doi.number`. Type `python3 main.py --help` for more info.

Example:

$ `python3 main.py /home/luca/Hobbs-Provincial-Press /dev/shm --doi 10.11647/OBP.0152`

## Development
### What works
* Chapter-level DOI discovery
* PDF files merging
* Write metadata into PDF files

### What can be improved
* Add more metadata information to files (for a start: publication date, abstract, keywords)
### Design limitations
* Currently *chapter-splitter* can only work with book-body chapters (with pages numbered with arabic numerals). If the script finds DOI metadata referring to front matters (with roman numerals), stops while running the method Pdf.get_page_list(). 
