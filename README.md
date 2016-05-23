# Poetify

Poetifier is a poetry translator that I created as the final project for my CSE 390: Natural Language Processing class. The "translation" means that it is given an input sentence of prose and then "translates" it to a version that is more poetic than the original. This project was written in Python 3.5 and uses Dependency Parsing and a K-Nearest Neighbors classifier.

I used the [University of Oxford Text Archive](https://ota.ox.ac.uk/) to find prose test data and the [Stanford Lexicalized Parser](http://nlp.stanford.edu/software/lex-parser.shtml) to create parse trees for my test and training data.

## Important Data Files

* `data/ContempAmateur.txt` and `data/ContempPoet.txt`
  * Raw text used for poetry data
* `data/prose_test.txt`
  * Raw text used for all prose data
  * Includes first 10 chapters of _The Adventures of Hucklberry Finn_ and a few beginning chapters of _Treasure Island_ from the [University of Oxford Text Archive](https://ota.ox.ac.uk/)
* `data/train.trees`
  * Trees for the training data for the PCFG
* `data/prose_classifier.trees` and `data/poems_classifier.trees`
  * Training data for the KNN classifier
* `data/class_test.trees`
  * Test data for the classifier
* `pcfg/pcfg.txt`
  * Representation of a trained PCFG
  * This is the filename that is references by the rest of the application, so if you train your own, make sure to call it pcfg.txt
  * The PCFG training application outputs a new PCFG file always with the same name, so be careful not to overwrite it
* `poetifier/parseX.trees`
  * These 7 files are the parse trees for each of the 7 input sentences that this was tested with
  * The sentence text is provided in the `poetifier/__main__.py` file

## Packages

###1. converter
 * used to convert from Stanford Parser's format to the one used by the other packages  

###2. pcfg
 * used to train a PCFG  
 * counts rules used in a parse tree  

###3. poetifier  
 * creates permutations of the input sentence  
 * calculates the poetic score  
 * creates and trains the KNN classifier  
 * predicts the class of the permutations of the input sentence  
 * plots the data  

## Order of Execution

1. Parse training data for the PCFG
2. Create a PCFG from parse trees of training data
3. Parse training data for the classifier
4. Parse the input sentence that you want to be "poetified"
5. Run the converter on the output of steps 2 and 3
6. Run the main application on the output of step 4

## How to Use

### Create Parse Tree for a Sentence
- use the Stanford Lexicalized Parser to create the parse tree (use the PCFG model)
- run the format converter on the parsed input like this:
	- make sure you have Python 3.5
	- navigate to the converter folder in a terminal
	- run this command:
		`python format_converter.py -c {path_to_stanford_parse} {output_file}`
	  replacing the file paths appropriately
	- the fixed parse tree will be written to the output file you provide

(NOTE: This will work for any number of sentences. By default, the Stanford Parser will divide the input into parses by punctuation. If the input to parse is poetry in verses, the Stanford Parser's settings must be changed to divide the input on newlines.)
	
### Create and Train a PCFG
- create a training file from verses of poetry
- navigate to the pcfg folder in a terminal
- run this command: `python trainpcfg.py -train {input_file}`
	
### Test the Classifier
- open the `__main__.py` file in the poetifier package
- on line 17, set the parameter in `run_switcher()` to be the path to the test data (or just switch out the commented and uncommented lines)
- run `__main__.py` (I did this in Eclipse PyDev) and the output will be displayed on the console
	
### "Poetify" an Input Sentence
- open the `__main__.py` file in the poetifier package
- on line 17, set the parameter in `run_switcher()` to be the path to the file containing the input sentence parse tree
- run `__main__.py` (I did this in Eclipse PyDev) and the output will be displayed on the console
(NOTE: This requires that input sentences be passed in one at a time, so the only thing in the input file should be the parse tree of the ONE sentence you want to parse.)
