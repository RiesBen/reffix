# reffix

This small repository handles BibTex files for latex code projects. 
It homogenizes the entries of a BibTex database, can merge multiple BibTex databases or find duplicated entries.

## Install package
Required packages can be installed with anaconda from the file: 
environment.yml

    conda env create -n reffix -f environment.yml
    
## Usage
the scripts have 3 phases:
1. parsing of entries: this phase also cleans the bibtex library via a parser and the provided rules.
2. modifying the database: here you can find duplicates and reduce the library to only used citations in certain tex files.
3. write out a bibtex file. 

## **Warning** Known Issues
Things that need to be checked manually:
* sometimes abbreviations are not correctly capitalized (if you don't need special natbib treatment, try deactivating homogenize_latex_encoding in the parser or check function:  reffix/entry_rules.py/fixLatexChar
* The content is not checked. it depends on what you provide!( you could think about activating crossref functionality of bibtexparser)


## Acknowledgments
I want to mention the BibTeX parser project (https://github.com/sciunto-org/python-bibtexparser), which is the foundation of this repository.
(docs:  https://bibtexparser.readthedocs.io/en/master/)
