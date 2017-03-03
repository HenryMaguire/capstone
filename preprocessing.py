import pickle
import nltk
import time
def load_obj(name ):
    with open(name + '.pickle', 'rb') as f:
        return pickle.load(f)

def preprocess_text(text_dict):
    t_i = time.time()
    clean_data = {}
    total_data = ''
    for key, items in text_dict.items():
        head_body = []
        for passage in [items[0], items[1]]:
            passage = passage.lower()
            passage_list = nltk.word_tokenize(passage)
            for n,token in enumerate(passage_list):
                if token in ['.', '!', '?']:
                    passage_list[n] = '<EOS>'
            shorter_passage_list = custom_clean(passage_list)
            #print len(passage_list)-len(shorter_passage_list)
            head_body.append(shorter_passage_list)
            total_data += ' '.join(shorter_passage_list)
        clean_data[key] = [head_body[0], head_body[1], items[2]]
    print 'time for preprocessing_text was ', time.time()-t_i, ' seconds'
    return clean_data, total_data

def custom_clean(word_list):
    """
    single letter words, the word 'Breitbart' and any opening quotes are removed
    colons are kept, all remaining punctuation is removed
    """
    new_list = []
    for word in word_list:
        if len(word) > 1 and word !='breitbart':
            if word[0] =="'" and len(word)==2 and word[1] !="i":
                new_list.append(word)
            elif word[0] =="'" and len(word)>=2:
                new_list.append(word[1:])
            else:
                new_list.append(word)
        elif word in [':', 'a', 'i']:
            new_list.append(word)
        else:
            pass
    return new_list

name = 'news_data'
data_dict = load_obj(name)
clean_data, total_data = preprocess_text(data_dict)

fdist = nltk.FreqDist(total_data.split(' '))
vocabulary = {}
for word, frequency in fdist.most_common(6000):
    if frequency>5: # After a frequency of about 5 all of the words start to become recognisable with this data
        vocabulary[word] = frequency
        print(u'{};{}'.format(word, frequency))
