# chapter-splitter
*chapter-splitter* is a small utility to split PDF books by chapters and write metadata into the generated files.

## Running with docker
```
docker run --rm \
  -v /path/to/local.pdf:/ebook_automation/pdf_file.pdf \
  -v /path/to/output:/ebook_automation/output \
  -e DOI=10.11647/OBP.0001 \
  -e ISBN=9781783748457 \
  openbookpublishers/chapter-splitter
```

Alternatively you may clone the repo, build the image using `docker build . -t some/tag` and run the command above replacing `openbookpublishers/chapter-splitter` with `some/tag`.

## Running locally
### Installation
*chapter-splitter* requires **pdftk** and **exiftool** to be installed on your system. These tools are available  in the official repositories of debian/debian-based distributions.
Run `apt-get install pdftk exiftool`.

Besides python standard libraries, *chapter-splitter* requires some extra-libraries noted in `requirements.txt`. To install them (within a virtual environment, if you prefer), run `pip3.5 install requirements.txt`.

#### Configuration
The *config.ini* file takes base configuration settings.
* *api_url* is the base URL of the API where to gather DOI metadata.
* *separator_char* is the character which separates the book DOI from the chapter-level sequential number (i.e. 10.11647/OBP.0152 **.** 01).
* *leading_zeros* is the number of leading zeros in the chapter-level DOI number progression (i.e. 01, 10, 100).
* *cover_page_n* and *copyright_page_n* note the page number for cover and copyright page.

### Use
Run the script as `python3 main.py ./input_file.pdf /output/folder --doi doi.number`. Type `python3 main.py --help` for more info.

Example:

$ `python3 main.py Hobbs-Provincial-Press.pdf /dev/shm --doi 10.11647/OBP.0152`

You may specify `--compress-output` to output a zip file containing all the curated (without the 'original', metadata less, files) chapter PDFs.

## Development
### What works
* Chapter-level DOI discovery
* PDF files merging
* Write metadata to PDF files

### What can be improved
* Add more metadata information to files (for a start: publication date, abstract, keywords)


### Git hooks
Use `pre-commit.sh` as a pre commit git hook to build a test image that will run `flake8` to enforce PEP8 style.

```
ln -sf ../../pre-commit.sh .git/hooks/pre-commit
```
