# RussianSketches

This project aims to introduce the new instrument of sketch generation on the basis of a language corpus. The main feature of the new sketch generation instrument is using of syntactic information from a sentence to find sketches. The new instrument of syntactic sketches provides the opportunity to range sketch output with one of nine association measures (Dice, chi-squared, likelihood ratio, t-score, PMI, MI, Jaccard, Fisher, Poisson-Stirling) and can filter out the least relevant syntactic relations for different Russian parts of speech. Moreover, this instrument is universal because it can be used for every Russian corpus, even without syntactic tagging. In this case, tagging is implemented by RuSyntax, which occurred to be the most high-quality tagging instrument for Russian. The recall of the sketch generation instrument is over 80% what is a good result for sketches on the basis of small Russian corpus.

## The algorithm of sketch generation -- sketch_generator.py
This algorithm generates sketches on the basis of a given corpus.
### How to use
With the command line:
```
python3 sketch_generator.py <corpus_name.conll>
```
With a Python interpreter:
```
import RussianSketches
import SketchEntry
parsing(<path to RuSyntax>, <input file>, <output file>)  # function for parsing if it is needed
rs = RussianSketches(<corpus_name.conll>, <tag_for_noun>,
                                          <tag_for_adjective>,
                                          <tag_for_verb>,
                                          <tag_for_adverb>,
                                          <tag_for_preposition>,
                                          <tag_for_praedicative>,
                                          <tag_for_punctuation>)  # initialization of the RS class
rs.retrieve_candidates()        # function for retrieving candidates from a corpus
rs.count_association_measures() # function for counting association measures for candidates
rs.filtering()                  # function for filtering linkages for candidates
rs.show_results()               # function for printing out the results
rs.writing_down_results()       # function for writing down the sketch files
```

Dictionaries **possible_bigrams** in line 31 and **possible_trigrams** in line 38 can be changed if new linkages or parts of speech are needed.

## The algorithm of sketch search -- sketch_searcher.py
This algorithm shows the sketches for a wanted word.
### How to use
With the command line:
```
python3 sketch_searcher.py <wanted word> <path to skethces directory> <ranging metric> <number of sketch examples to show>
```
With a Python interpreter:
```
import SketchEntry
import get_sketches_by_word
metric = 'dice'
ignored_linkages = [] # can contain any linkages that shoul be ignored
get_sketches_by_word(<wanted word>, <path to skethces directory>, <number of sketch examples to show>, ignored_linkages)
```
It is possible to choose one of the nine following metrics for ranging:
* 'dice'
* 'chi' - chi-squared
* 'poisson-stirling'
* 'jaccard'
* 'fisher'
* 'pmi'
* 'mi'
* 'likelihood-ratio'
* 't-score'
