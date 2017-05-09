from nltk.metrics.association import BigramAssocMeasures

'''
n_ii counts (w1, w2), i.e. the bigram being scored 
n_ix counts (w1, )
n_xi counts (, w2)
n_xx counts (*, *), i.e. any bigram
'''

def get_contingency_table(candidates, corpus_size):
    """The function for counting contingency tables"""
    # Get word frequencies
    word_counts = {}
    for word in candidates:
        i = 0
        for linkage in candidates[word]:
            for obj in candidates[word][linkage]:
                i += obj.abs_freq
        word_counts[word] = i
    # Get frequencies for a contingency table
    for word in candidates:
        for linkage in candidates[word]:
            for obj in candidates[word][linkage]:
                n_ii = obj.abs_freq
                n_ix = word_counts[obj.first_word]
                n_xi = word_counts[obj.second_word]
                n_xx = corpus_size
                # Count Dice statistics
                obj.dice = BigramAssocMeasures.dice(n_ii, (n_ix, n_xi), n_xx)

def ranging(candidates):
    """The function for ranging sketch candidates"""
    for word in candidates:
        for linkage in candidates[word]:
            # print (word, linkage, candidates[word][linkage])
            ranged_candidates = sorted(candidates[word][linkage])
            yield ranged_candidates, linkage, word
