# chapter-splitter
*chapter-splitter* is a tool to split PDF books into individual chapters.

Chapter data needs to be previously submitted to (Crossref)[https://www.crossref.org/] so that `chapter-splitter` can query the server and retrieve information such as chapter page ranges, title and author(s) to add to the output PDFs.

# Usage

`chapter-splitter` requires:

 - PDF of the book;
 - A metadata json file with the isbn of the book, structured as `{"isbn": "978-1-80064-422-9"}`

## Running with docker
If required, specify cover and copyright page numbers (zero based) in the Dockerfile (or override it in your `docker run [...]` command) as env variables.

```
docker run --rm \
  -v /path/to/local.pdf:/ebook_automation/pdf_file.pdf \
  -v /path/to/local.json:/ebook_automation/pdf_file.json \
  -v /path/to/output:/ebook_automation/output \
  openbookpublishers/chapter-splitter
```

Alternatively you may clone the repo, build the image using `docker build . -t some/tag` and run the command above replacing `openbookpublishers/chapter-splitter` with `some/tag`.

## Running locally
### Installation
*chapter-splitter* requires **pdftk** and **exiftool** to be installed on your system. These tools are available  in the official repositories of debian/debian-based distributions.
Run `apt-get install pdftk exiftool`.

Besides python standard libraries, *chapter-splitter* requires some extra-libraries noted in `requirements.txt`. To install them (within a virtual environment, if you prefer), run `pip3.5 install requirements.txt`.

#### Configuration
If required, define cover and copyright page numbers (zero based) as env variables: $COVER_PAGE and $COPYRIGHT_PAGE.

### Use
Run the script as `python3 main.py --input-file ./input_file.pdf --output-folder /output/folder --metadata ./metadata.json`. Type `python3 main.py --help` for more info.

Example:

$ `python3 main.py --input-file Hobbs-Provincial-Press.pdf --output-folder /dev/shm --metadata metadata.json`

You may specify `--compress-output` to output a zip file containing all the curated (without the 'original', metadata less, files) chapter PDFs.

## Dev
### Git hooks
Use `pre-commit.sh` as a pre commit git hook to build a test image that will run `flake8` to enforce PEP8 style.

```
ln -sf ../../pre-commit.sh .git/hooks/pre-commit
```
