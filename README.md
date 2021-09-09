# chapter-splitter
*chapter-splitter* splits PDF books into individual chapters PDFs. The output files are supplied with relevant metadata.

## Rationale
There are scenarios where it is desirable to distribute book chapters individually. This utility serves exactly to this purpose, performing the task programmatically and offering the best possible output (reading ad discoverability).

## What the output PDFs look like
The software outputs the PDFs of the chapters which comes with a DOI. Chapter body text is preceded with the cover image of the book and a copyright statement.

## What metadata is included
Basic metadata include _authors_, _chapter title_, _publisher name_, _licence_ and _DOI_. Additional metadata consists of _chapter abstract_. Technical metadata
reports _creation date_ and _production software_ ([PDFtk](https://packages.debian.org/buster/pdftk)).

## Running with docker
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
The *config.ini* file takes base configuration settings.
* *api_url* is the base URL of the API where to gather DOI metadata.
* *cover_page_n* and *copyright_page_n* note the page number for cover and copyright page.

### Use
Run the script as `python3 main.py ./input_file.pdf /output/folder -m ./metadata.json`. Type `python3 main.py --help` for more info.

Example:

$ `python3 main.py Hobbs-Provincial-Press.pdf /dev/shm -m metadata.json`

You may specify `--compress-output` to output a zip file containing all the curated (without the 'original', metadata less, files) chapter PDFs.

## Dev
### Git hooks
Use `pre-commit.sh` as a pre commit git hook to build a test image that will run `flake8` to enforce PEP8 style.

```
ln -sf ../../pre-commit.sh .git/hooks/pre-commit
```
