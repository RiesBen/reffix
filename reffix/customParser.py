from bibtexparser.customization import journal, type as bibtexType, author #homogenize_latex_encoding

def build_Parser():
    myParser = BibTexParser()

    def rulez(record):
        record = bibtexType(record)
        record = capitalize_keys(record)

        record = homogenize_latex_encoding(record)
        record = check_article_fields(record)
        record = check_book_fields(record)
        record = check_incollection_fields(record)
        record = check_inproceedings_fields(record)
        record = check_inbook_fields(record)


        record = double_minus(record)
        record = titelcasing_fields(record)
        record = journal_iso4(record)

        return record

    myParser.customization = rulez
    return myParser
