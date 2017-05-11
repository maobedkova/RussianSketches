from nltk.metrics.association import BigramAssocMeasures

'''
n_ii counts (w1, w2), i.e. the bigram being scored 
n_ix counts (w1, )
n_xi counts (, w2)
n_xx counts (*, *), i.e. any bigram
'''

def get_contingency_table(candidates, bigram_corpus_size, trigram_corpus_size):
    """The function for counting contingency tables"""
    # Getting word frequencies
    word_counts = {}
    for word in candidates:
        i = 0
        for linkage in candidates[word]:
            for obj in candidates[word][linkage]:
                i += obj.abs_freq
        word_counts[word] = i
    # Getting frequencies for a contingency table
    for word in candidates:
        for linkage in candidates[word]:
            for obj in candidates[word][linkage]:
                # Contingency tables for trigrams
                if obj.third_word:
                    n_iii = obj.abs_freq
                    n_ixx = word_counts[obj.first_word]
                    n_xix = word_counts[obj.second_word]
                    n_xxi = word_counts[obj.third_word]
                    n_xxx = trigram_corpus_size
                    # Counting the Dice statistics for trigrams
                    obj.dice = 3*float(n_iii)/float(n_ixx+n_xix+n_xxi)
                # Contingency tables for bigrams
                else:
                    n_ii = obj.abs_freq
                    n_ix = word_counts[obj.first_word]
                    n_xi = word_counts[obj.second_word]
                    n_xx = bigram_corpus_size
                    # Counting the Dice statistics for bigrams
                    obj.dice = BigramAssocMeasures.dice(n_ii, (n_ix, n_xi), n_xx)

def ranging(candidates):
    """The function for ranging sketch candidates"""
    for word in candidates:
        for linkage in candidates[word]:
            ranged_candidates = sorted(candidates[word][linkage], reverse=True)
            yield ranged_candidates, linkage, word
