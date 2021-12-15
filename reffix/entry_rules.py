def titelcasing_fields(record):
    record.update({"title": titlecase(record['title'].replace("{", "").replace("}", ""))})
    return record


def journal_iso4(record):
    if ("journal" in record):
        abbrev = (iso4.abbreviate(record['journal']).replace(".", "").replace(" ", ". ") + ".").strip()
        record.update({"journal": abbrev})
    return record


def double_minus(record):
    """
        pages need --
    """
    if (record['ENTRYTYPE'] == "article"):

        if (not "--" in record['pages']):
            if ("-" in record['pages']):
                record['pages'] = record['pages'].replace("-", "--")

        record['pages'] = record['pages'].replace("\textemdash", "")
    return record


def capitalize_keys(record):
    record.update({'ID': record['ID'].title()})
    return record


# --------------------------------------------------------------------------------
# Checking Fields
def check_misc_fields(record, fields=("title", "author", "year"),
                      optional=("publisher", "pages", "url", "version", "urldate")):
    if (record['ENTRYTYPE'] == "misc"):
        try:
            newRecord = {field: record[field] for field in fields}
            [newRecord.update({field: record[field]}) for field in record.keys() if (field.isupper())]
            if ("howpublished" in record):
                newRecord.update({'url': record["howpublished"]})

            if ("note" in record and "Accessed" in record['note']):
                newRecord.update({'urldate': record["note"].replace("Accessed:", "").strip()})
        except Exception as err:
            raise Exception("Could not homogenize: \n" + str(record) + "\n\nERR:\n" + str(err.args))

        # optionals:
        [newRecord.update({field: record[field]}) for field in optional if (field in record)]
        record = newRecord
    return record


def check_incollection_fields(record, fields=("title", "author", "year"), optional=("publisher", "pages", "booktitle")):
    if (record['ENTRYTYPE'] == "incollection"):
        try:
            newRecord = {field: record[field] for field in fields}
            [newRecord.update({field: record[field]}) for field in record.keys() if (field.isupper())]
        except Exception as err:
            raise Exception("Could not homogenize: \n" + str(record) + "\n\nERR:\n" + str(err.args))

        # optionals:
        [newRecord.update({field: record[field]}) for field in optional if (field in record)]
        record = newRecord
    return record


def check_inproceedings_fields(record, fields=("title", "author", "year"),
                               optional=("publisher", "pages", "booktitle")):
    if (record['ENTRYTYPE'] == "inproceedings"):
        try:
            newRecord = {field: record[field] for field in fields}
            [newRecord.update({field: record[field]}) for field in record.keys() if (field.isupper())]
        except Exception as err:
            raise Exception("Could not homogenize: \n" + str(record) + "\n\nERR:\n" + str(err.args))

        # optionals:
        [newRecord.update({field: record[field]}) for field in optional if (field in record)]
        record = newRecord
    return record


def check_inbook_fields(record, fields=("title", "author", "year"), optional=("publisher", "pages", "booktitle")):
    if (record['ENTRYTYPE'] == "inbook"):
        try:
            newRecord = {field: record[field] for field in fields}
            [newRecord.update({field: record[field]}) for field in record.keys() if (field.isupper())]
        except Exception as err:
            raise Exception("Could not homogenize: \n" + str(record) + "\n\nERR:\n" + str(err.args))

        # optionals:
        [newRecord.update({field: record[field]}) for field in optional if (field in record)]
        record = newRecord
    return record


def check_article_fields(record, fields=("title", "author", "year", "journal", "volume", "pages",), optional=()):
    """
        Checks presence of required fields and removes rest
    """
    if (record['ENTRYTYPE'] == "article"):
        try:
            newRecord = {field: record[field] for field in fields}
            [newRecord.update({field: record[field]}) for field in record.keys() if (field.isupper())]

        except Exception as err:
            raise Exception("Could not homogenize: \n" + str(record) + "\n\nERR:\n" + str(err.args))

        # optionals:
        [newRecord.update({field: record[field]}) for field in optional if (field in record)]
        record = newRecord
    return record


def check_book_fields(record, fields=("title", "author", "year", "publisher"), optional=("volume", 'edition')):
    """
        Checks presence of required fields and removes rest
    """
    if (record['ENTRYTYPE'] == "book"):
        try:  # Must Have
            newRecord = {field: record[field] for field in fields}
            [newRecord.update({field: record[field]}) for field in record.keys() if (field.isupper())]
        except Exception as err:
            raise Exception("Could not homogenize: \n" + str(record) + "\n\nERR:\n" + str(err.args))

        # optionals:
        [newRecord.update({field: record[field]}) for field in optional if (field in record)]
        record = newRecord
    return record


# --------------------------------------------------------------------------------
# LATEX FIX
import logging
from bibtexparser.latexenc import latex_to_unicode, string_to_latex, protect_uppercase

logger = logging.getLogger(__name__)
from bibtexparser.customization import convert_to_unicode


def homogenize_latex_encoding(record):
    """
    Homogenize the latex enconding style for bibtex

    This function is experimental.

    :param record: the record.
    :type record: dict
    :returns: dict -- the modified record.
    """
    # First, we convert everything to unicode
    # record = convert_to_unicode(record)
    # And then, we fall back
    for val in record:
        if val not in ('ID',):
            logger.debug('Apply string_to_latex to: %s', val)
            record[val] = string_to_latex(record[val])
            if val == 'title':
                logger.debug('Before: %s', record[val])
                record[val].replace("{", "").replace("}", "")
                # record[val] = protect_uppercase(record[val])
                logger.debug('After: %s', record[val])
    return record
