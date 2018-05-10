import re
from bs4 import BeautifulSoup

import nltk, string, numpy
import multiprocessing as mp
from sklearn.feature_extraction.text import CountVectorizer
# nltk.download('punkt') # first-time use only

from sklearn.feature_extraction.text import TfidfTransformer, TfidfVectorizer
import math

import sklearn.metrics.pairwise as sklearn_pairwise

stemmer = nltk.stem.porter.PorterStemmer()


def StemTokens(tokens):
    return [stemmer.stem(token) for token in tokens]


remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)


def StemNormalize(text):
    return StemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))


# nltk.download('wordnet') # first-time use only

lemmer = nltk.stem.WordNetLemmatizer()


def LemTokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens]


remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)


def LemNormalize(text):
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))


def idf(n,df):
    result = math.log((n+1.0)/(df+1.0)) + 1
    return result


def cos_sim(documents):
    LemVectorizer = CountVectorizer(tokenizer=LemNormalize, stop_words='english')
    LemVectorizer.fit_transform(documents)
    #print(LemVectorizer.vocabulary_)

    tf_matrix = LemVectorizer.transform(documents).toarray()
    #print(tf_matrix)

    tfidfTran = TfidfTransformer(norm="l2")
    tfidfTran.fit(tf_matrix)
    #print(tfidfTran.idf_)

    tfidf_matrix = tfidfTran.transform(tf_matrix)
    #print(tfidf_matrix.toarray())
    cos_similarity_matrix = (tfidf_matrix * tfidf_matrix.T).toarray()
    #print(cos_similarity_matrix*100)
    return cos_similarity_matrix


# html에서 텍스트 추출을 위한 함수
def tag_visible(element):
    if element.parent.name in ['style','script','head','title','meta','[document]']:
        return False
    if re.match('<!--.*-->', str(element.encode('utf-8'))):
        return False
    return True


# html에서 텍스트 추출을 위한 함수
def text_only_from_html(html_text):
    soup = BeautifulSoup(html_text, 'html.parser')
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)
    return " ".join(t.strip() for t in visible_texts)


title_html_route={}

with open('address_set/duplicated_count.txt','r') as f:
    r=f.read()

word=re.split('\[Title\]|\[Count\]|\[ADDRESS_SET\]|\[HTML_DIR\]',r)

for index in range(0, int((len(word)-1)/4) ):
    title = word[1+4*index][:-1]
    html_route = word[4*(index+1)][:-1].replace('[','').replace(']','').replace('\n','').replace('\'','').replace(' ','').split(',')
    title_html_route[title] = html_route

numpy.set_printoptions(formatter={'float': '{: 0.3f}'.format}, threshold=numpy.nan)

titles = title_html_route.keys()

result_file = open('address_set/cos_sim_matrix_text_only_data.txt','w')
result_file = open('address_set/cos_sim_matrix_text_only_data_TorDocker1.txt','w')

# all file에 대한 cosin 비교
for title in titles:
    print(title+" processing...\n")
    duplicated_address_num = len(title_html_route[title])
    if duplicated_address_num > 1:
        document = []
        html_route_set = []
        for html_route in title_html_route[title]:
            with open(html_route,'r') as f:
                html_text = f.read()
                text = text_only_from_html(html_text)
                document.append(text)
                html_route_set.append(html_route)
        try:
            cos_sim_mtx = cos_sim(document)
            result_file.write('[Title]' + title + '\n[COS]\n' + str(cos_sim_mtx)[1:-1].replace(' [', '[') + '\n')
        except:
            result_file.write('[Title]' + title + '\n[COS]\n' + '[NONE TEXT HTML]\n')
        result_file.write('[HTML_DIR]'+str(html_route_set)+'\n')

result_file.close()
