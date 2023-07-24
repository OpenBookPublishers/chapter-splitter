# chapter-splitter
*chapter-splitter* is a tool to split PDF books into individual chapters.

Chapter data needs to be previously submitted to [Crossref](https://www.crossref.org/) or [Thoth](https://thoth.pub/) so that `chapter-splitter` can query the server and retrieve information such as chapter page ranges, title and author(s) to add to the output PDFs.

# Usage

The help page $ `python3 ./main.py --help` reports:
```
Usage: main.py [OPTIONS] DOI

Arguments:
  DOI  [required]

Options:
  --input-file PATH               [default: ./file.pdf]
  --output-folder PATH            [default: ./output/]
  --database TEXT                 [default: thoth]
  --write-urls / --no-write-urls  [default: write-urls]
  --help                          Show this message and exit.
```

so a running command would look something like this:

$ `python3 ./main.py --input-file my_file.pdf --output-folder ~/output \
                     --database crossref 10.11647/obp.0309`

or querying Thoth:

$ `python3 ./main.py --input-file my_file.pdf --output-folder ~/output \
                     --database thoth 10.11647/obp.0309`

`chapter-splitter` would try to append both the front cover of the original PDF and the copyright page to the output files. Page numbers (of these pages in the original document) are defined with the environment variables `COVER_PAGE` and `ENV COPYRIGHT_PAGE` (number, zero based).

$ `COVER_PAGE=0`
$ `COPYRIGHT_PAGE=4`

The `--write_urls` option attempts to write the appropriate OBP-specific Landing Page URL and Full Text URL to Thoth for each chapter created. For this, it is necessary to provide Thoth login credentials via the environment variables `THOTH_EMAIL` and `THOTH_PWD`.

$ `THOTH_EMAIL=email@example.com`
$ `THOTH_PWD=password`
$ `python3 ./main.py --input-file my_file.pdf --output-folder ~/output \
                     --database thoth --write-urls 10.11647/obp.0309`

## Running with docker
Running the command reported above in docker would be:
```
docker run --rm \
  -e THOTH_EMAIL=email@example.com \
  -e THOTH_PWD=password \
  -v /path/to/local.pdf:/ebook_automation/file.pdf \
  -v /path/to/output:/ebook_automation/output \
  openbookpublishers/chapter-splitter \
  main.py 10.11647/obp.0309
```

Alternatively you may clone the repo, build the image using `docker build . -t some/tag` and run the command above replacing `openbookpublishers/chapter-splitter` with `some/tag`.

## Running locally
### Installation
*chapter-splitter* requires **exiftool** to be installed on your system. These tools are available  in the official repositories of debian/debian-based distributions.
Run `apt-get install exiftool`.

Besides python standard libraries, *chapter-splitter* requires some extra-libraries noted in `requirements.txt`. To install them (within a virtual environment, if you prefer), run `pip3.5 install requirements.txt`.

## Dev
### Git hooks
Use `pre-commit.sh` as a pre commit git hook to build a test image that will run `flake8` to enforce PEP8 style.

```
ln -sf ../../pre-commit.sh .git/hooks/pre-commit
```
