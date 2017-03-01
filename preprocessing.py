import pickle
import nltk
def load_obj(name ):
    with open(name + '.pickle', 'rb') as f:
        return pickle.load(f)

def preprocess_text(text_dict):
    clean_data = {}
    total_data = ''
    for key, items in text_dict.items():
        headline = items[0]
        body = items[1]
        link = items[2]
        headline = headline.replace('.', "END_SENTENCE ")
        headline = headline.strip(" - Breitbart")
        headline = headline.strip(',!?;:)').lower()
        headline = headline.replace("'s", "")
        body = body.strip(',!?;:()').lower()
        body = body.replace('?',' END_SENTENCE ')
        body = body.replace('!',' END_SENTENCE ')
        body = body.replace('.', " END_SENTENCE ")
        body = body.replace("'s", "")
        #print body
        clean_data[key] = [headline, body, link]
        total_data+= body + ' ' + headline + ' '
    return clean_data, total_data

def chuck_single_letters(word_list):
    new_list = []
    for word in word_list:
        if len(word) > 1:
            new_list.append(word)
    return new_list

name = 'news_data'
data_dict = load_obj(name)
clean_data, total_data = preprocess_text(data_dict)
word_list = nltk.word_tokenize(total_data)
final_list = chuck_single_letters(word_list)
print len(word_list)-len(final_list), " single letter words chucked out."

fdist = nltk.FreqDist(final_list)
vocabulary = {}
for word, frequency in fdist.most_common(40000):
    if frequency>5: # After a frequency of about 5 all of the words start to become recognisable with this data
        vocabulary[word] = frequency
        print(u'{};{}'.format(word, frequency))
