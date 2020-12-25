import spacy
from heapq import nlargest
from collections import Counter

def summarize(text, num_sentences):
    nlp = spacy.load("en_core_web_lg")
    doc = nlp(text)
    pos_tag = ["PROPN", "ADJ", "NOUN", "VERB"]
    keyword = [token.text for token in doc if not token.is_stop and not token.is_punct and token.pos_ in pos_tag]

    word_freqs = Counter(keyword)
    max_freq = word_freqs.most_common(1)[0][1]
    word_freqs = {i:j/max_freq for i,j in word_freqs.items()}

    sent_scores = {}
    for sent in doc.sents:
        for word in sent:
            if word.text in word_freqs.keys():
                if sent in sent_scores.keys():
                    sent_scores[sent] += word_freqs[word.text]
                else:
                    sent_scores[sent] = word_freqs[word.text]
    return " ".join([i.text for i in nlargest(num_sentences, sent_scores, key=sent_scores.get)])