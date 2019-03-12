# python ir_engine.py -w "binary" -o out.txt
from collections import OrderedDict
from collections import defaultdict
import math
class Retrieve:
   
    # Create new Retrieve object storing index and termWeighting scheme
    def __init__(self,index, termWeighting):
        self.index = index
        self.termWeighting = termWeighting
        self.candidate = {}
        self.candidate_term = defaultdict(lambda: {})
        self.tf = {}
        self.df = {}  
        self.totalD = {}
        self.D = 0
        self.d = {}
        self.q = {}
        self.result = {}
        self.initIndex()

    def initIndex(self):#count tf, df, |D| and do different method to count d(ranking value)
        if self.termWeighting == 'binary':# get the doc name to tackle with
            for term in self.index:
                for doc,freq in self.index[term].items():
                    if doc not in self.totalD:
                        self.totalD[doc] = 0
            self.D = len(self.totalD)

            for term in self.index:#compute d for ranking
                for doc,freq in self.index[term].items():
                    if doc not in self.d:
                        self.d[doc] = 1
                    else:
                        self.d[doc] += 1 

        if self.termWeighting == 'tf':
            for term in self.index:#get the doc name to tackle with
                self.tf[term] = 0 #init
                for doc,freq in self.index[term].items():
                    self.tf[term] += freq
                    if doc not in self.totalD:
                        self.totalD[doc] = 0

            for term in self.index:#compute d 
                for doc,freq in self.index[term].items():
                    if doc not in self.d:
                        self.d[doc] = freq**2
                    else:
                        self.d[doc] += freq**2  
        if self.termWeighting == 'tfidf':
            for term in self.index:
                self.tf[term] = 0 #init
                self.df[term] = 0
                for doc,freq in self.index[term].items():
                    self.tf[term] += freq
                    self.df[term] += 1
                    if doc not in self.totalD:
                        self.totalD[doc] = 0
            self.D = len(self.totalD)

            for term in self.index:#compute d 
                for doc,freq in self.index[term].items():
                    if doc not in self.d:
                        self.d[doc] = math.log10(self.D / self.df[term]) * freq
                    else:
                        self.d[doc] += math.log10(self.D / self.df[term]) * freq       

    # Method performing retrieval for specified query

    def forQuery(self, query):	
        for term in query:
            if term in self.index:
                for doc,freq in self.index[term].items():
                    if doc not in self.candidate:
                        self.candidate[doc] = 0 #room to fill in  

        if self.termWeighting == 'binary':       
            for doc in self.totalD: #get candidate_term(room)
                self.candidate_term[doc] = {}.fromkeys(query.keys(), 0)
            for term in query:# make candidate_term to 2 level
                if term in self.index.keys():
                    for doc in self.index[term].keys():
                        if doc in self.candidate_term.keys():
                            self.candidate_term[doc][term] = 1
            for term in query:#binary way(make all tf as 1)
                query[term] = 1

            for term in self.candidate_term.keys():#count rank
                d = self.d[term]
                qd = 0
                for key in self.candidate_term[term].keys():
                    if key in query.keys():
                        qd += query[key]*self.candidate_term[term][key]
                self.result[term] = qd / math.sqrt(d)

            pp = sorted(self.result.items(),key = lambda x:x[1],reverse = True)#sort
            arr = []# format output
            for i,j in pp:
                arr.append(i)
            return arr[:10]

        if self.termWeighting == 'tf':         
            for doc in self.totalD:
                self.candidate_term[doc] = {}.fromkeys(query.keys(), 0)
            for term in query:
                if term in self.index.keys():
                    for doc in self.index[term].keys():
                        if doc in self.candidate_term.keys():
                            self.candidate_term[doc][term] = self.index[term][doc]

            for term in self.candidate_term.keys():
                d = self.d[term]
                qd = 0
                for key in self.candidate_term[term].keys():
                    if key in query.keys():
                        qd += query[key] * self.candidate_term[term][key]
                self.result[term] = qd / math.sqrt(d)

            pp = sorted(self.result.items(),key = lambda x:x[1],reverse = True)
            arr = []
            for i,j in pp:
                arr.append(i)
            return arr[:10]


        if self.termWeighting == 'tfidf': 
            for doc in self.totalD:
                self.candidate_term[doc] = {}.fromkeys(query.keys(), 0)
     
            for term in query:
                if term in self.index.keys():
                    for doc in self.index[term].keys():
                        if doc in self.candidate_term.keys():
                            self.candidate_term[doc][term] = (math.log10(self.D / self.df[term]) * self.index[term][doc])
            
            for term in query.keys():
                if term in self.df.keys():
                    query[term] *= math.log10(self.D / self.df[term]) 
                else:
                    query[term] = 0

            for term in self.candidate_term.keys():
                d = self.d[term]
                qd = 0
                for key in self.candidate_term[term].keys():
                    if key in query.keys():
                        qd += self.candidate_term[term][key] * query[key] 
                self.result[term] = qd / math.sqrt(d)


            pp = sorted(self.result.items(),key = lambda x:x[1],reverse = True)
            arr = []
            for i,j in pp:
                arr.append(i)
            return arr[:10]
            









        