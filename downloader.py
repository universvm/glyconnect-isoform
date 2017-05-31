#Packages:
import urllib,urllib2
from Bio import SeqIO #Biopython
from collections import defaultdict

uniprotdata = defaultdict(str) #creating empty dictionary with uniprot data and glyconnectID

data = open("data/uniprot.csv", "r")
# export = open("data/uniprot_isoform_updated.csv", "w")
# export.write("isoform;uniprot_id;length\n")

data.readline()#Skipping first line for header (isoform;uniprot_id etc..)
#TODO: use either one-liner or define a function (?)
uniprotID = ''
for line in data:
    line = line.rstrip("\r\n")
    #maybe use dictionary here?
    table = line.split(";")
    uniprotID = table[1].rstrip("\"").lstrip("\"")
    uniprotdata[uniprotID] += table[0]

print(uniprotdata)

#Parameters: To keep the main structure of API to work since they need an email address.
# params = {
# 'from':'ID',
# 'to':'P_REFSEQ_AC',
# 'format':'tab',
# 'query':''
# }

#data = urllib.urlencode(params) #Redundant...

# for glycan in uniprotID:
#     #print(glycan)
#     try:
#         url = 'http://www.uniprot.org/uniprot/{0}.fasta?include=yes'.format(glycan) #URL format to include isoforms
#         request = urllib2.Request(url, data)
#         contact = "email" # Please set your email address here to help us debug in case of problems.
#         request.add_header('User-Agent', 'Python %s' % contact)
#         response = urllib2.urlopen(request)
#         page = response.read()
#         export.write(page)
#     except urllib2.HTTPError:
#         print("There is an error for the {0} entry".format(glycan))

for record in SeqIO.parse("data/sequences.fasta", "fasta"):
    if "Isoform" in record.description: #if the sequence is an isoform
        isoform = record.description.split("|") #divide header by "|"
        second = isoform[1].split("-")  #This variable is to ensure that the isoform 1 is written once only in the export.
        # if int(second[1]) == 2: #if this is the first isoform, meaning it has "-2"
        #     export.write("{}-1;{};{}\n".format(currentSeq,uniprotdata[currentSeq],currentLen)) #export its data first.
        print(currentLen)
        print(currentSeq)
        # export.write("{0};{1};{2}\n".format(isoform[1],uniprotdata[currentSeq],len(record.seq))) #format "isoform"; "uniprot_id"; "length"
    else:
        split = record.description.split("|") #creating a new variable
        currentSeq = split[1] #currentSeq stores the UniProt ID of all the sequences which are not isoforms.
                              #If isoforms are seen on the next line they will matched to the currentSeq.
        currentLen = len(record.seq)
