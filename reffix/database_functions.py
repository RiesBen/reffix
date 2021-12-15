
#imports
import re, copy
from collections import defaultdict
from bibtexparser.bibdatabase import BibDatabase


# Clean for Duplicates!
def remove_duplicates(bib_database, verbose=True):
    print("Filter DB for duplicates")
    print("\tBefore Elements in DB: ", len(bib_database.entries))
    new_bib_database = BibDatabase()
    new_bib_database.entries_dict.update(copy.deepcopy(bib_database.entries_dict))
    new_bib_database.entries = copy.deepcopy(bib_database.entries)

    # find duplicates
    entry_counts = defaultdict(int)  # {key:0 for key in bib_database.entries_dict.keys()}
    key_entries = defaultdict(list)

    for entry in bib_database.entries:
        entry_counts[entry["ID"]] += 1
        key_entries[entry["ID"]].append(entry)

    duplicates_keys = [k for k, v in entry_counts.items() if (v > 1)]
    if (len(duplicates_keys) > 0):
        if (verbose): print("Found " + str(len(duplicates_keys)) + " Duplicates!\nKeys: \t" + " ".join(duplicates_keys))

        for dKey in duplicates_keys:
            if (verbose): print("found duplicate for: " + str(dKey))
            ref = key_entries[dKey][0]
            for entry in key_entries[dKey][1:]:
                not_equal = []
                for k in ref:
                    if (k in entry and ref[k] != entry[k]):
                        continue
                        not_equal.append(k)
                    elif (not k in ref):
                        ref.update({k: entry[k]})
                    else:
                        not_equal.append(k)
                if (len(not_equal) > 0 or len(ref) != len(entry)):
                    continue

                    raise Exception(
                        "Fields are not identical!:\n" + "  ".join(map(str, not_equal)) + "\nReference:\n" + str(
                            ref) + "\n----------------------------------\nEntry:\n" + str(entry))

        new_bib_database.entries = list(sorted(list(new_bib_database.entries_dict.values()), key=lambda x: x['ID']))
    print("\tAfter Elements in DB: ", len(new_bib_database.entries))
    return new_bib_database

# Check for required!
# collect citations from a tex file

def remove_non_used_citations(bib_database, tex_file_paths):
    if(isinstance(tex_file_paths, str)):
        tex_file_paths = [tex_file_paths]

    used_citation_keys = []
    for tex_path in tex_file_paths:
        used_citation_keys.extend(get_used_citations(tex_path))
    used_citation_keys = list(set(used_citation_keys))
    database = filter_database_for_required_citations(bib_database, used_citation_keys)
    return database


def get_used_citations(tex_file_path):
    used_citations = []
    with open(tex_file_path, 'r', encoding="utf-8") as tex_file:
        lines = tex_file.readlines()
        for line in lines:
            if ("\cite{" in line):
                citations = re.findall('cite\{(.*?)\}', line)
                # split multi citations
                for citation in citations:
                    if ("," in citation):
                        used_citations.extend(list(map(lambda x: x.strip(), citation.split(","))))
                    else:
                        used_citations.append(citation)
            if ("\citenum{" in line):
                citations = re.findall('citenum\{(.*?)\}', line)
                # split multi citations
                for citation in citations:
                    if ("," in citation):
                        used_citations.extend(list(map(lambda x: x.strip(), citation.split(","))))
                    else:
                        used_citations.append(citation)
    unique_citations = set(used_citations)
    return unique_citations


def filter_database_for_required_citations(bib_database, used_citation_keys):
    new_bib_database = BibDatabase()
    print("Filter DB for used in TEX")
    print("\tBefore Elements in DB: ", len(bib_database.entries))
    new_unique_entries = {}
    missing = []

    for citation_key in used_citation_keys:
        if (citation_key.title() in bib_database.entries_dict.keys()):
            new_unique_entries.update({citation_key: bib_database.entries_dict[citation_key.title()]})
        else:
            if (citation_key != ''):
                missing.append(citation_key)

    if (len(missing) > 0):
        raise Exception("\tFUN! you are missing a citation: \n" + str(missing))

    # setattr(new_bib_database, 'entries_dict', new_unique_entries)
    new_bib_database.entries = list(sorted(list(new_unique_entries.values()), key=lambda x: x['ID']))
    print("\tAfter Elements in DB: ", len(new_bib_database.entries))

    return new_bib_database


