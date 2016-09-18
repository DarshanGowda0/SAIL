#NLTK IMPORTS
import nltk
from nltk.corpus import stopwords


#PATTERNS
from pattern.en import parsetree
from pattern.en import tenses, PAST, PL

#IMPORTING STUFF
from sklearn.feature_extraction import DictVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer


#SCIKIT-LEARN IMPORTS
from sklearn.svm import SVC


class vectorizer():
	def __init__(self):
		self.stopwords = stopwords.words('english')
		self.vec = DictVectorizer()
        
	def tenseses(self,strs):
		if 'present' in str(tenses(strs)):
		    ten = 'PRESENT'
		elif 'past' in tenses(strs):
		    ten = "PAST"
		else:
		    ten = "FUTURE"
		return ten

	def dialogue_act_features(self,post):
		stop = nltk.word_tokenize(post)
		post = []
		for i in stop:
		    if i not in self.stopwords:
			post.append(i)
		    else:
			pass
			#regect_list.append(i)
		posts = ""
		for i in post:
		    posts += i
		    posts += " "
		processed = parsetree(posts, relations=True, lemmata=True)
		features = {}
		for sents in processed:
		    x = sents
		    for i in x.chunks:
			j = i.pos
			if j == "VP":
			    tense = self.tenseses(i.string)
			else:
			    tense = ""
			h = i.words
			for words in h:
			    apd_str =  str(words.lemma) +"-"+ str(words.pos)
			    #+ "-" +tense
			    #if words.pos[:1] == "NN" or words.pos[:1] == "VP":
			    features['word({})'.format(str(words.lemma))] =  str(words.pos)
			#pos['features({})'.format(j)] = True
		    return features
	def vectorize(self,feat_list):
		pos_vectorized = self.vec.fit_transform(feat_list)
		return pos_vectorized
	def reVectorize(self,feat_list):
		pos_vectorized = self.vec.transform(feat_list)
		return pos_vectorized
	def train_gen(self,x):
	    iterations = []
	    for i in x:
		#print
		m1 = i[0]
		m1.reverse()
		x1 = i[1]
		x1.reverse()
		while True:
		    if len(x1) == 0 and len(m1) == 0:
			break
		    temp = []
		    temp2 = []
		    while True:
			try:
			    temp.append(m1.pop())
			    #print temp[-1]
			    if temp[1] == 0:
			        break
			except Exception as e:
			    break
		    while True:
			try:
			    temp2.append(x1.pop())
			    #print temp2[-1]
			    if temp2[-1][1] == 0:
			        break
			except Exception as e:
			    break
		    #print len(x1)
		    me_str = ""
		    m_str = "" 
		    for i in temp:
			me_str += " "
			me_str += i[0]
		    for i in temp2:
			m_str += i[0]
		    iterations.append((self.dialogue_act_features(me_str),m_str))
	    x = []
	    y = []
	    for i in iterations:
	    	  x.append(i[0])
	    	  y.append(i[1])
	    return_dictionary_buffer = {}
	    return_dictionary_buffer['x'] = x
	    return_dictionary_buffer['y'] = y  
	    return return_dictionary_buffer

def dict_builder(y):
    count = 0
    indexDict = {}
    reverseDict = {}
    indexList = []
    for i in y:
        try:
            indexList.append(reverseDict[i])
        except Exception as e:
            indexList.append(count)
            reverseDict[i] = count
            count += 1
    for i in reverseDict:
        indexDict[reverseDict[i]] = i
    return (indexList,indexDict) 

class predictions():
    
    def __init__(self):
        self.vectors = vectorizer()
        
    #get the vector for predictions
    def get_predict_vector(self,string):
        return self.vectors.reVectorize(self.vectors.dialogue_act_features(string))
    
    def get_val_for_index(self,array):
        for i in array:
            www = self.index_to_val[i]
        return www
    
    def predict(self,string):
        vector = self.get_predict_vector(string)
        res = self.clf.predict(vector)
        inter_val = self.clf.predict_proba(vector)[0]
        print inter_val
        list_of_highest = []
        refference_list = []
        if 1 == 1:
            print inter_val
            for j in inter_val:
                refference_list.append(float(j))
            refference_list.sort(reverse=True)
            for i in range(0,3):
                list_of_highest.append(
                        (refference_list[i],
                                        self.get_val_for_index(
                                                [inter_val.tolist().index(refference_list[i])]
                                                )
                                                )
                        )
                
        return (self.get_val_for_index(res),str(inter_val[res[0]]),list_of_highest)
    
    def learn(self,x):
        temp = self.vectors.train_gen(x)
        X = self.vectors.vectorize(temp['x'])
        Y,self.index_to_val = dict_builder(temp['y'])
        self.clf = SVC(probability=True).fit(X, Y)
    def learn_from_db(self,x,xy_list):
        temp = self.vectors.train_gen(x)
        for i in xy_list['x']:
            temp['x'].append(self.vectors.dialogue_act_features(i))
        for i in xy_list['y']:
            temp['y'].append(i)
        X = self.vectors.vectorize(temp['x'])
        Y,self.index_to_val = dict_builder(temp['y'])
        self.clf = SVC(probability=True).fit(X, Y)
