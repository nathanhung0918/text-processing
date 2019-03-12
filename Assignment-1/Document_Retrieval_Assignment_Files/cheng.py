import math
import collections

class Retrieve:
    # Create new Retrieve object storing index and termWeighting scheme
    def __init__(self, index, termWeighting):
        self.index = index
        self.termWeighting = termWeighting
        self.document_size_d, self.document_frequency, self.D, self.document_list, self.collection_frequency = self.initial_init_param()

    # to initial all param will be using next
    def initial_init_param(self):
        collection_frequency = collections.defaultdict(lambda: 0)
        document_frequency = collections.defaultdict(lambda: 0)
        document_size_d = collections.defaultdict(lambda: 0)
        document_list = []
        for word in self.index.keys():
            for document_index in self.index[word]:
                document_list.append(document_index)
                collection_frequency[word] += self.index[word][document_index]
                if self.termWeighting == 'tf':
                    if document_index in document_size_d.keys():
                        document_size_d[document_index] += self.index[word][document_index]**2
                    else:
                        document_size_d[document_index] = self.index[word][document_index]**2
                if self.termWeighting == 'binary':
                    if document_index in document_size_d.keys():
                        document_size_d[document_index] += 1
                    else:
                        document_size_d[document_index] = 1
            document_frequency[word] = len(self.index[word])
        D = len(list(set(document_list)))*1.0
        if self.termWeighting == 'tfidf':
            for word in self.index.keys():
                for document_index in self.index[word]:
                    if document_index in document_size_d.keys():
                        document_size_d[document_index] += self.index[word][document_index]*math.log10(D/document_frequency[word])
                    else:
                        document_size_d[document_index] = self.index[word][document_index]*math.log10(D/document_frequency[word])

        return document_size_d, document_frequency, D, list(set(document_list)), collection_frequency

    # get candidate list for every query
    def get_candidate_score_dict(self,query):
        candidate_list = []
        for query_word in query.keys():
            if query_word in self.index.keys():
                candidate_list += self.index[query_word].keys()
            else:
                continue
        return {}.fromkeys(list(set(candidate_list)), 0)

    # get {document_index:{word:frequency}} instruct for query
    def get_candidate_dict(self,query):
        candidate_dict = collections.defaultdict(lambda: {})
        for document_index in self.document_list:
            candidate_dict[document_index] = {}.fromkeys(query.keys(), 0)
        return candidate_dict

    def query_convert_by_weighting(self,query):
        if self.termWeighting == 'binary':
            return {}.fromkeys(query.keys(), 1)
        if self.termWeighting == 'tf':
            return query
        if self.termWeighting == 'tfidf':
            true_frequency = query
            for word in query.keys():
                if word in self.document_frequency.keys():
                    query[word] = true_frequency[word]*math.log10(self.D / self.document_frequency[word])
                else:
                    query[word] = 0
            return query

    # Method performing retrieval for specified query
    def forQuery(self, query):
        if self.termWeighting not in ['binary', 'tf', 'tfidf']:
            print ('choose the right term weight method ')
            exit()
        # prepare the data structure for query
        candidate_score_dict = self.get_candidate_score_dict(query)
        candidate_dict = self.get_candidate_dict(query)

        for word in query:
            if word in self.index.keys():
                for document_index in self.index[word].keys():
                    if document_index in candidate_dict.keys():
                        if self.termWeighting == 'binary':
                            candidate_dict[document_index][word] = 1
                        if self.termWeighting == 'tf':
                            candidate_dict[document_index][word] = self.index[word][document_index]
                        if self.termWeighting == 'tfidf':
                            candidate_dict[document_index][word] = self.index[word][document_index]*math.log10(self.D/self.document_frequency[word])

        query = self.query_convert_by_weighting(query)
        for candidate in candidate_dict.keys():
            d = self.document_size_d[candidate]
            qd = 0
            for word in candidate_dict[candidate].keys():
                if word in query.keys():
                    qd += query[word]*candidate_dict[candidate][word]
            candidate_score_dict[candidate] = qd/math.sqrt(d)
        rank_list = sorted(candidate_score_dict.items(), key=lambda x: x[1], reverse=True)[:10]
        result_list = []
        for item in rank_list:
            result_list.append(item[0])

        return result_list