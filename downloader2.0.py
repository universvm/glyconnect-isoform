#Packages:
import urllib,urllib2
from collections import defaultdict

#Files:
data = open("data/uniprot.csv", "r") #data from database
export = open("data/uniprot_isoform_updated2.csv", "w")
export.write("isoform;uniprot_id;length\n") #Header

#Dictionary:
uniprotdata = defaultdict(str) #creating empty dictionary with uniprot data and glyconnectID
seqDict = defaultdict(str)

#Parameters: To keep the main structure of API to work since they need an email address.
params = {
'from':'ID',
'to':'P_REFSEQ_AC',
'format':'tab',
'query':''
}

#Functions:
def parsER(page): #Defining uniprotAPI
    "Parses the fasta file given from the the uniprotAPI function"
    #Variables:
    acc_no = ""
    seq = ""
    count = 0
    #Loop:
    for line in page: #for each line of the page
        if line.startswith('<') or line.startswith('\n'): #ignoring comments such as "<addinfourl at 4456409208 "
            continue
        elif line.startswith('>'): #if line is accession number (>)
            if count > 0: #if it has already parsed a sequence once the next > is encountered
                seqDict[acc_no] += str(len(seq))
                seq = ""
                count = 0
            header = line.rstrip("\r\n")
            header = header.split("|")
            acc_no = header[1]
        else:
            seq += line.rstrip("\r\n") #since it is read line by line, each line is a bit of a sequence.
                                                 #which is then added to seq
            count += 1
    #Adding the last entry:
    seqDict[acc_no] += str(len(seq))

def uniprotAPI(acc_n): #Defining uniprotAPI
    "Creates a call to the API with the given UniProtID (acc_n) to return the length of a protein."
    settings = urllib.urlencode(params) #calling parameters
    try: #tries to call the API.
        url = 'http://www.uniprot.org/uniprot/{0}.fasta?include=yes'.format(acc_n) #URL format to include isoforms
        request = urllib2.Request(url, settings)
        contact = "email" # Please set your email address here to help us debug in case of problems.
        request.add_header('User-Agent', 'Python %s' % contact)
        response = urllib2.urlopen(request)
        parsER(response) #parsing the response
    except urllib2.HTTPError: #if API call fails, it displays which one of the entry has a problem
        print("There is an error for the {0} entry".format(acc_n))

#Main Loop:
data.readline()#Skipping first line for header ("isoform;uniprot_id" etc..)
for line in data: #for each line in the database
    line = line.rstrip("\r\n") #removing \r\n
    table = line.split(";") #splitting by ";"
    uniprotID = table[1].rstrip("\"").lstrip("\"") #removing the " to make it easier
    uniprotdata[uniprotID] += table[0] #adding
    uniprotAPI(uniprotID)

for sequence in seqDict.keys():
    if "-" in sequence: #if it is an isoform
        isoform = sequence.split("-")
        if int(isoform[1]) == 2: #if it is the second isoform
            export.write("{}-1;{};{}\n".format(isoform[0],uniprotdata[isoform[0]],seqDict[isoform[0]]))
        export.write("{};{};{}\n".format(sequence,uniprotdata[isoform[0]],seqDict[sequence]))
