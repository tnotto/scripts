import re
import csv
import collections, itertools
import nltk.classify.util, nltk.metrics
from nltk.classify import NaiveBayesClassifier
from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures
from nltk.probability import FreqDist, ConditionalFreqDist
from random import shuffle
import pickle
 
def evaluate_classifier(featx):
    pos_words = []
    for line in pos_revs:
        # pos_words.append(nltk.tokenize.wordpunct_tokenize(re.sub(r"(?:\@|https?\://)\S+", "", line)))
        pos_words.append(word_tokenize.tokenize(re.sub(r"(?:\@|https?\://)\S+", "", line)))
        
    neg_words = []
    for line in neg_revs:
        # neg_words.append(nltk.tokenize.wordpunct_tokenize(re.sub(r"(?:\@|https?\://)\S+", "", line)))
        neg_words.append(word_tokenize.tokenize(re.sub(r"(?:\@|https?\://)\S+", "", line)))

    negfeats = [(featx(words), 'neg') for words in neg_words]
    posfeats = [(featx(words), 'pos') for words in pos_words]
    shuffle(negfeats)
    shuffle(posfeats)
 
    negcutoff = len(negfeats)*3/4
    poscutoff = len(posfeats)*3/4

    trainfeats = negfeats[:negcutoff] + posfeats[:poscutoff]
    testfeats = negfeats[negcutoff:] + posfeats[poscutoff:]
 
    classifier = NaiveBayesClassifier.train(trainfeats)
    refsets = collections.defaultdict(set)
    testsets = collections.defaultdict(set)
 
    for i, (feats, label) in enumerate(testfeats):
        refsets[label].add(i)
        observed = classifier.classify(feats)
        testsets[observed].add(i)
 
    print 'accuracy:', nltk.classify.util.accuracy(classifier, testfeats)
    print 'pos precision:', nltk.metrics.precision(refsets['pos'], testsets['pos'])
    print 'pos recall:', nltk.metrics.recall(refsets['pos'], testsets['pos'])
    print 'neg precision:', nltk.metrics.precision(refsets['neg'], testsets['neg'])
    print 'neg recall:', nltk.metrics.recall(refsets['neg'], testsets['neg'])
    classifier.show_most_informative_features(30)
    
    with open('sentiment.pickle', 'wb') as f:
        pickle.dump(classifier, f)
 
def word_feats(words):
    return dict([(word.lower(), True) for word in words])
 
def best_word_feats(words):
    return dict([(word.lower(), True) for word in words if word in bestwords])
 
def best_bigram_word_feats(words, score_fn=BigramAssocMeasures.chi_sq, n=200):
    bigram_finder = BigramCollocationFinder.from_words(words)
    bigrams = bigram_finder.nbest(score_fn, n)
    d = dict([(bigram, True) for bigram in bigrams])
    d.update(best_word_feats(words))
    return d
     
word_tokenize = nltk.RegexpTokenizer('[A-Za-z]\w+')

word_fd = FreqDist()
label_word_fd = ConditionalFreqDist()

with open('training.1600000.processed.noemoticon.csv', 'rU') as csvdata:
    text_reader = csv.reader(csvdata)
    neg_revs = []
    pos_revs = []
    neg_words = []
    pos_words = []
    for row in text_reader:
        if row[0] == '0':
            neg_revs.append(row[5])
            # neg_words.append(nltk.tokenize.wordpunct_tokenize(re.sub(r"(?:\@|https?\://)\S+", "", row[5])))
            neg_words.append(word_tokenize.tokenize(re.sub(r"(?:\@|https?\://)\S+", "", row[5])))
        elif row[0] == '4':
            pos_revs.append(row[5])
            # pos_words.append(nltk.tokenize.wordpunct_tokenize(re.sub(r"(?:\@|https?\://)\s+", "", row[5])))
            pos_words.append(word_tokenize.tokenize(re.sub(r"(?:\@|https?\://)\S+", "", row[5])))

pos_words = list(itertools.chain.from_iterable(pos_words))
neg_words = list(itertools.chain.from_iterable(neg_words))

for word in pos_words:
    word_fd.inc(word.lower())
    label_word_fd['pos'].inc(word.lower())
 
for word in neg_words:
    word_fd.inc(word.lower())
    label_word_fd['neg'].inc(word.lower())
 
pos_word_count = label_word_fd['pos'].N()
neg_word_count = label_word_fd['neg'].N()

total_word_count = pos_word_count + neg_word_count
 
word_scores = {}
 
for word, freq in word_fd.iteritems():
    pos_score = BigramAssocMeasures.chi_sq(label_word_fd['pos'][word],
        (freq, pos_word_count), total_word_count)
    neg_score = BigramAssocMeasures.chi_sq(label_word_fd['neg'][word],
        (freq, neg_word_count), total_word_count)

    word_scores[word] = pos_score + neg_score
 
best = sorted(word_scores.iteritems(), key=lambda (w,s): s, reverse=True)[:10000]
bestwords = set([w for w, s in best])

def start():
    # print 'evaluating single word features'
    # evaluate_classifier(word_feats)
 
    print 'evaluating best word features'
    evaluate_classifier(best_word_feats)
# 
#     print 'evaluating best words + bigram chi_sq word features'
#     evaluate_classifier(best_bigram_word_feats)

def best_words():
    return bestwords
