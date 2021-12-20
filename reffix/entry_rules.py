from collections import OrderedDict

import nltk
nltk.download('wordnet')

import iso4
from titlecase import titlecase


def titelcasing_fields(record):
    record.update({"title": "{\\em "+titlecase(record['title']+" \\em}")})

    if("journal" in record):
        record.update({"journal": titlecase(record['journal'])})
    
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

def fixLatexChars(record):
    comment_list = ["&", "_"]
    
    replacmentDict = OrderedDict({
        "\\textasciigrave": "^",
        "\\textbackslash": "\\",
        "\\textquotesingle": "'",
        "\\textdollar ":"$",  
        "\\textendash":"-",
        "{\\L}ambda":"\\lambda",
        "$\\{B}eta ": "$\\beta",
        "{D}na": "{DNA}",
        "{D}NA": "{DNA}",
        "{Q}m": "{QM}",
        "{Q}M": "{QM}",
        "{M}m": "{MM}",
        "{M}D": "{MD}",
        "{M}d": "{MD}",
        "{I}i": "{II}",
        "{I}I": "{II}",
        "{N}mr": "{NMR}",
        "{N}MR": "{NMR}",
         "N{M}r": "{NMR}",
        " {E}m ": "{EM}",
        " {E}M ": "{EM}",
        "{A}MB{E}R": "{AMBER}",
        "{G}AF{F}": "{GAFF}",
        "{A}TB": "{ATB}",
        "C{H}AR{M}M": "{CHARMM}",
        "{O}PL{S}" : "{OPLS}",
        "{S}HA{K}E": "{SHAKE}",
        "{R}AT{T}LE": "{RATTLE}",
        "P{H}": "{PH}",
        "{O}pen{M}M": "{OpenMM}",
        "{S}T2": "{ST}2",
        "{R}e-{E}ds": "{RE}-{EDS}",
        "{Q}lig{F}EP": "{QligFEP}",
        "{D}3R": "{D3R}",
        "{N}-Methyltransferase" : "{N}-{M}ethyltransferase",
        "{N}AM{D}":"{NAMD}",
        "{L}eu{s}": "{LEUS}",
        "{Q}res{F}EP":"{QresFEP}",
        "{G}B3":"{GB}3",
        "{M}DF{P}": "{MDFP}",
        "H{T}RP{V}1": "{HTRPV1}",
        "{A}T1":"{AT1}",
        "F{E}Setup": "{FESetup}",
        "{P}yAuto{F}EP": "{P}y{A}uto{F}EP",
        "F{E}W": "{FEW}",
        "{P}mx": "{Pmx}",
        "{E}DS": "{EDS}",
        "{A}ZD": "{AZD}",
        "{P}yE{M}MA":"{P}y{EMMA}",
        "M{D}Traj":"{MDT}raj",
        "Eds": "{EDS}",
        "{O}ME{G}A": "{OMEGA}",
        "Rdkit": "{R}dkit",
        "{J}SO{N}": "{JSON}",
        "Methylations":"{M}ethylations",
        "{M}s-$\Lambda$-{L}eu{s}" : "{MS}-$\lambda$-{LEUS}",
        "S{A}MP{L}4": "{SAMPL}4",
        "G{R}OM{O}S": "{GROMOS}",
        "{G}RO{M}OS": "{GROMOS}",
        "B{R}o5":"{bRO}5",
        "{C}HK1":"{CHK1}",
        "{S}pc":"{SPC}",
        "L{l}vm": "{LLVM}",
        "{J}IT": "{JIT}",
        "Wire": "WIRE",
        "{G}mx": "{GMX}",
        "L{A}MM{P}S": "{LAMMPS}",
        "A{P}I":"{API}",
        "H{D}F": "{HDF}",
        "{R}inikerlab/{P}yGromos{T}ools: {P}yGromos{T}ools": "rinikerlab/pygromostools: {P}y{G}romos{T}ools",
        "arXiv": "ar{X}iv",
        "{C}oM{F}A": "{CoMFA}",
        "{C}oM{S}IA": "{CoMSIA}",
        "3d-{Q}sar": "3{D}-{QSAR}",
        "ä" : "\\\"a", 
        "Ä" : "\\\"A",
        "ö" : "\\\"o",
        "Ö" : "\\\"O",
        "ü" : "\\\"u",
        "Ü" : "\\\"U",
        "è" : "\\\'e",
        "à" : "\\\'a",
        "é" : "\\\`e",
        "á" : "\\`a",
        'ç' : '\\c{c}',
        'ô' : '\\^{o}',
        "ŏ" : '\\u{o}',
        "É" : "{\\'E}",
        "ß" : "{\ss}", 
        "\\\\":"\\",

    })
    
    for field_key in record:
        field = record[field_key]
        for replace in comment_list:
            if(replace in field):
                for i,c in enumerate(field):
                    if(replace == c and field[i-1] !="\\"):
                        field = field[:i]+"\\"+field[i:]
        record.update({field_key:field})
            
    for field_key in record:
        field = record[field_key]
        if(any([key in field for key in replacmentDict])):
            for replace in replacmentDict:
                field = field.replace(replace, replacmentDict[replace])
            record.update({field_key:field})

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


def check_inbook_fields(record, fields=("title", "author", "year", "chapter", "pages"), optional=("publisher", "pages", "booktitle")):
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
