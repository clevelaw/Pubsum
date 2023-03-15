from Bio import Entrez
import json
import sys

keyword = sys.argv[1]
timeSpan = sys.argv[2]
journals = ["JAMA", "Nature", "PloS one", "Cell", "Neuron"]
output = []
out_dict = {}.fromkeys(["journal", "title", "author", "pub_date", "doi"], "No Result")


def search(query):
    """return list of results that match keyword"""
    Entrez.email = "will.j.cleveland@gmail.com"
    handle = Entrez.esearch(db='pubmed',
                            sort='pub_date',
                            retmax=timeSpan,
                            retmode='xml',
                            term=query)
    results = Entrez.read(handle)
    return results

def fetch_details(id_list):
    """return info on article based on ID"""
    ids = ','.join(id_list)
    Entrez.email = 'your.email@example.com'
    handle = Entrez.efetch(db='pubmed',
                           retmode='xml',
                           retmax=timeSpan,
                           id=ids)
    fetched = Entrez.read(handle)
    return fetched

#parses article results based on keyword and # of articles
for journal in journals:
    journal_query = f"\"{journal}\"[Journal]"
    search_term = f"{keyword}[ALL FIELDS] AND {journal_query}"
    results = search(search_term)

    #outputs a dictironary with all results
    if len(results['IdList']) == 0:
        out_dict = {
            "journal": journal,
            "title": "No Results",
            "author": "No Results",
            "pub_date": "No Results",
            "doi": "No Results",
        }
    else:
        id_list = results['IdList']
        papers = fetch_details(id_list)
        for paper in papers['PubmedArticle']:

            #DOI is frequenctly missing
            try:
                doi_dummy = paper['MedlineCitation']['Article']['ELocationID'][0]
            except:
                doi_dummy = "No DOI found"

            out_dict = {
                "journal": paper['MedlineCitation']['Article']['Journal']['Title'],
                "title": paper['MedlineCitation']['Article']['ArticleTitle'],
                "author": paper['MedlineCitation']['Article']['AuthorList'][-1],
                "pub_date": paper['MedlineCitation']['Article']['Journal']['JournalIssue']['PubDate'],
                "doi": doi_dummy
            }
            output.append(out_dict)

#json output is printed to the console and collected by js code
print(json.dumps(output))

#added to verify results of the microservice in debugging
with open("PubSum_Results.json", "w") as outfile:
    new_save = output
    json.dump(new_save, outfile)