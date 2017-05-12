from nltk.metrics.association import BigramAssocMeasures, TrigramAssocMeasures

def count_statistics(candidates, bigram_corpus_size, trigram_corpus_size):
    """The function for counting contingency tables"""
    print ('=== Counting association measure ===')
    # Getting word frequencies
    word_counts = {}
    for word in candidates:
        i = 0
        for linkage in candidates[word]:
            for obj in candidates[word][linkage]:
                i += obj.abs_freq
                if not obj.third_word:
                    word_counts[obj.first_word + '_' + obj.second_word] = obj.abs_freq
        word_counts[word] = i
    # Getting frequencies for a contingency table
    for word in candidates:
        for linkage in candidates[word]:
            for obj in candidates[word][linkage]:
                # Contingency tables for trigrams
                if obj.third_word:
                    n_iii = obj.abs_freq                    # counts (w1, w2, w3)
                    n_ixx = word_counts[obj.first_word]     # counts (w1, , )
                    n_xix = word_counts[obj.second_word]    # counts ( , w2, )
                    n_xxi = word_counts[obj.third_word]     # counts ( , , w3)
                    if obj.first_word + '_' + obj.second_word in word_counts:
                        n_iix = word_counts[obj.first_word + '_' + obj.second_word]
                    else:
                        n_iix = 0
                    if obj.first_word + '_' + obj.third_word in word_counts:
                        n_ixi = word_counts[obj.first_word + '_' + obj.third_word]
                    else:
                        n_ixi = 0
                    if obj.first_word + '_' + obj.third_word in word_counts:
                        n_xii = word_counts[obj.second_word + '_' + obj.third_word]
                    else:
                        n_xii = 0
                    print (n_xii, n_ixi, n_iix)
                    n_xxx = trigram_corpus_size             # counts any trigram

                    # Counting association measures for trigrams
                    obj.dice = 3*float(n_iii)/float(n_ixx+n_xix+n_xxi)
                    obj.chi = TrigramAssocMeasures.chi_sq(n_iii,
                                                          (n_iix, n_ixi, n_xii),
                                                          (n_ixx, n_xix, n_xxi),
                                                          n_xxx)
                    obj.jaccard = TrigramAssocMeasures.jaccard(n_iii,
                                                               (n_iix, n_ixi, n_xii),
                                                               (n_ixx, n_xix, n_xxi),
                                                               n_xxx)
                    obj.likelihood_ratio = TrigramAssocMeasures.likelihood_ratio(n_iii,
                                                                                 (n_iix, n_ixi, n_xii),
                                                                                 (n_ixx, n_xix, n_xxi),
                                                                                 n_xxx)
                    obj.mi = TrigramAssocMeasures.mi_like(n_iii,
                                                          (n_iix, n_ixi, n_xii),
                                                          (n_ixx, n_xix, n_xxi),
                                                          n_xxx)
                    obj.pmi = TrigramAssocMeasures.pmi(n_iii,
                                                       (n_iix, n_ixi, n_xii),
                                                       (n_ixx, n_xix, n_xxi),
                                                       n_xxx)
                    obj.poisson_stirling = TrigramAssocMeasures.poisson_stirling(n_iii,
                                                                                 (n_iix, n_ixi, n_xii),
                                                                                 (n_ixx, n_xix, n_xxi),
                                                                                 n_xxx)
                    obj.t_test = TrigramAssocMeasures.student_t(n_iii,
                                                                (n_iix, n_ixi, n_xii),
                                                                (n_ixx, n_xix, n_xxi),
                                                                n_xxx)

                # Contingency tables for bigrams
                else:
                    n_ii = obj.abs_freq                 # counts (w1, w2)
                    n_ix = word_counts[obj.first_word]  # counts (w1, )
                    n_xi = word_counts[obj.second_word] # counts (, w2)
                    n_xx = bigram_corpus_size           # counts any bigram
                    # Counting the Dice statistics for bigrams
                    obj.dice = BigramAssocMeasures.dice(n_ii, (n_ix, n_xi), n_xx)
                    obj.chi = BigramAssocMeasures.chi_sq(n_ii, (n_ix, n_xi), n_xx)
                    obj.t_test = BigramAssocMeasures.student_t(n_ii, (n_ix, n_xi), n_xx)
                    obj.poisson_stirling = BigramAssocMeasures.poisson_stirling(n_ii, (n_ix, n_xi), n_xx)
                    obj.pmi = BigramAssocMeasures.pmi(n_ii, (n_ix, n_xi), n_xx)
                    obj.mi = BigramAssocMeasures.mi_like(n_ii, (n_ix, n_xi), n_xx)
                    obj.likelihood_ratio = BigramAssocMeasures.likelihood_ratio(n_ii, (n_ix, n_xi), n_xx)
                    obj.jaccard = BigramAssocMeasures.jaccard(n_ii, (n_ix, n_xi), n_xx)
                    obj.fisher = BigramAssocMeasures.fisher(n_ii, (n_ix, n_xi), n_xx)

def ranging(candidates):
    """The function for ranging sketch candidates"""
    for word in candidates:
        for linkage in candidates[word]:
            ranged_candidates = sorted(candidates[word][linkage], reverse=True)
            yield ranged_candidates, linkage, word
