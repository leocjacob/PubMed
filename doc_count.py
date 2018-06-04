from Bio import Entrez
def search(query):
    Entrez.email = 'leoccjj@gmail.com'
    handle = Entrez.esearch(db='pubmed', 
                            sort='relevance', 
                            retmax='20',
                            retmode='xml', 
                            term=query)
    results = Entrez.read(handle)
    return results

if __name__ == '__main__':
    query = input("Please enter your query: ")
    results = search(query)
    print("*************************************************")
    print("QueryTranslation :\n",results["QueryTranslation"])
    extract_query = results["QueryTranslation"].split('"')[1::2]
    extract_query=list(set(extract_query))
    print("*************************************************")
    print("Number of Documents for :")
    for term in extract_query:
        results = search(term)
        print("%s = %s" %(term,results["Count"]))
    print("*************************************************")