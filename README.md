# RussianSketches
The algorithm of syntactic sketches for Russian.

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
rs = RussianSketches(<corpus_name.conll>, tag_for_noun,
                                          tag_for_adjective,
                                          tag_for_verb,
                                          tag_for_adverb,
                                          tag_for_preposition,
                                          tag_for_praedicative,
                                          tag_for_punctuation)  # initialization of the RS class
rs.retrieve_candidates()        # function for retrieving candidates from a corpus
rs.count_association_measures() # function for counting association measures for candidates
rs.filtering()                  # function for filtering linkages for candidates
rs.show_results()               # function for printing out the results
rs.writing_down_results()       # function for writing down the sketch files
```

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
get_sketches_by_word(<wanted word>, <path to skethces directory>, <number of sketch examples to show>)
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


