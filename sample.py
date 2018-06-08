
from Bio import Entrez, Medline
import re

def readmesh():             #FUNCTION TO READ THE MESH TERMS FROM THE FILE abstract.txt
    dic=[]
    flag=False
    f = open("abstract.txt","r")
    tab=open("symoltable.txt","w")
    for line in f:
        if(line.startswith('PMID')):
            tab.write(line)
        if (line.startswith('MH'))and(not line.startswith('MHDA')):
            flag=True
        if flag:
           dic.append(line)
           tab.write(line.replace("MH  - ",""))
        if line.endswith('\n'):
            flag=False
    return dic                     #END OF readmesh()


def make_dictionary():        #FUNCTION TO CREATE DICTIONARY    
    tab=open("symoltable.txt","r")
    dic={}
    for line in tab:
        if(line.startswith('PMID')): #IF LINE IS A PMID
            pmid=line           
        elif(line in dic):      #IF LINE IS A MESH TERM AND ALREADY ENCOUNTERED
             dic[line]=dic[line]+","+str(pmid.strip("PMID- "))
        elif(not line in dic ):         #IF LINE IS A MESH TERM AND NEWLY ENCOUNTERED
             dic[line]=str(pmid.strip("PMID- "))
    tab.close()
    return dic


def list_traverse(list):           #FUNCTION TO PRINT ELEMENTS OF THE LIST PASSED
    for x in list:
        print (x)
        print("\n")                #END OF list_traverse()



def search(query):                               #FUCNTION TO SEARCH THE QUERY PASSED
    Entrez.email = 'arjunrajasekhar87@gmail.com'
    handle = Entrez.esearch(db='pubmed', 
                            sort='relevance', 
                            retmax='5',
                            retmode='xml', 
                            term=query)
    results = Entrez.read(handle)
    return results                            #END OF search()



def fetch_rec(rec_id, entrez_handle):                  #FUNCTION TO FETCH THE ABSTRACTS
    fetch_handle = Entrez.efetch(db='pubmed', id=rec_id,
                                 rettype='Medline', retmode='text',
                                 webenv=entrez_handle['WebEnv'],
                                 query_key=entrez_handle['QueryKey'])
    rec = fetch_handle.read()
    return rec                  #END OF fetch_rec()                                



if __name__ == '__main__':                          #MAIN FUNCTION
    query = input("\nPLEASE ENTER YOUR QUERY : ")
    print("\n")
    results = search(query)
    print("QueryTranslation :\n",results["QueryTranslation"])
    print("\n")
    print("******************************************************************")
   
    extract_query = results["QueryTranslation"].split("OR")    #SPLITTING THE TERMS WITH OR
    extract_query1=[]
    final=[]

    for term in extract_query:                      #SPLITTING THE TERMS WITH AND
        extract_query2 = term.split("AND")
        extract_query1 = extract_query1+extract_query2

    for term in extract_query1:         #REMOVING (,)
        term=term.replace('(','')
        term=term.replace(')','')
        final.append(term)            #APPENDING THE TERMS TO THE LIST final
    
    final = [x.strip(' ') for x in final]       #REMOVING WHITE SPACES BETWEEN
    final=list(set(final))

    print("Extracted Query:\n")
    print(final)
    print("\n")
    print("*********************************************************************")

    print("Documents Retrieved\n")
    for term in final:
        results = search(term)
        print("%s = %s" %(term,results["Count"]))
    print("\n")

    id_list=results["IdList"]
    print ("id list:\n",id_list)
    out_handle = open("abstract.txt","w")
    abstracts=[]
    for rec_id in id_list:
        fetch_handle = Entrez.efetch(db='pubmed',rettype='Medline', retmode='text',id=rec_id)
        data = fetch_handle.read()
        fetch_handle.close()
        out_handle.write(data)
    out_handle.close()
    dictionary=readmesh()           #STORING THE MESH TERMS IN LIST NAMED dictionary
    # list_traverse(dictionary)        #PRINT THE TERMS IN dictionary
    dic= make_dictionary()
    tab=open("dictionary.txt","w")
    for x in dic:              #WRITING THE DICTIONARY TO A FILE NAMED dictionary.txt
        tab.write(x+" => \n")
        tab.write(dic[x]+"\n\n")