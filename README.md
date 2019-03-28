# Command Line Tool for Scraping Google Patents for Claims Information

This is a simple Python command line tool for scraping Google Patents for claim information. 



## Dependencies
- Pandas
- Argparse
- lxml

Installing something like Anaconda will generally install all of these depenencies. 


## Installation and Use

### Basic Usage
Provide the `google_patents_scraper.py` script with a company you'd like to scrape, like so:
```
python google_patents_scraper.py -s MY SEARCH COMPANY --verbose
```

### Advanced Usage

All the bells and whistles can be found by calling `-h` or `--help`.

```
usage: google_patents_scraper.py [-h] [-v] -s SEARCH [SEARCH ...] [-o OUTPUT]
                                 [-n NUMBER] [-p PAUSE]

Scrapes Google Patents for Relevant Information

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         Boolean flag indicating if statements should be
                        printed to the console.
  -s SEARCH [SEARCH ...], --search SEARCH [SEARCH ...]
                        REQUIRED: The search terms to search Google Patents
  -o OUTPUT, --output OUTPUT
                        REQUIRED: Output CSV file
  -n NUMBER, --number NUMBER
                        Number of returned results
  -p PAUSE, --pause PAUSE
                        Second wait between scrape

```