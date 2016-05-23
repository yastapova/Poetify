import numpy as np
import matplotlib.pyplot as plt
from pcfg import runner, parsepcfg, trainpcfg, tree
from sklearn.neighbors import KNeighborsClassifier

pcfg_file_path = '../pcfg/pcfg.txt'

# calculates the scores for the given file
# fname - file to take trees from
# classY - 0 or 1 for prose or poetry
def scores_for_data(fname, classY):
    from poetifier import scorer
    print('Reading pcfg file.', flush=True)
    # read pcfg
    u_lhs, _, rules, probs, ntags, nwords = parsepcfg.parse_grammar(pcfg_file_path)
    # read classifier trees
    text = runner.read_file(fname)
    text = text.strip().split('\n')
    scores = []
    classes = []
    print('Calculating scores.',flush=True)
    # calculate scores for each tree
    for t in text:
        ptree = [tree.Tree.from_str(t)]
        rules_p, _, _, _ = trainpcfg.count_all_rules(ptree)
        ascore, mscore = scorer.calc_score(rules, probs, rules_p, u_lhs, ntags, nwords)
        scores.append([ascore, mscore])
        classes.append(classY)
    return scores, classes


# plots the classifier training data on a scatter plot
# along with the test data
# poems - scores of poem trees
# prose - scores of prose trees
# input_scores - scores of test data trees
def plot_data(poems, prose, input_scores):
    fig = plt.figure()
    ax = plt.gca()
    ax.scatter(poems[0], poems[1], c='green', alpha=0.10, edgecolors='none')
    ax.scatter(prose[0], prose[1], c='red', alpha=0.10, edgecolors='none')
    ax.scatter(input_scores[0], input_scores[1], c='blue', alpha=1, edgecolors='none', marker='D', s=40)
    ax.set_yscale('log') # log scale on y axis for mscores
    plt.ylim(1e-200,1) # y-axis limits
    plt.xlim(-0.05, 0.4) # x-axis limits
    plt.xlabel('ascore')
    plt.ylabel('mscore')
    plt.show()


# runs all of the classifying
# currently works with a k-nearest neighbor classifier
# provided by the scikit-learn package
def classify_input(s, input_scores, testing_mode):
    # calculate scores for poem and prose classifier training data
    scores1, classes1 = scores_for_data('../data/poems_classifier.trees', 1)
    scores2, classes2 = scores_for_data('../data/prose_classifier.trees', 0)
    scores = scores1 + scores2 # concatenate
    classes = classes1 + classes2 # concatenate
    scores1 = [list(x) for x in zip(*scores1)] # transpose for scatterplot
    scores2 = [list(x) for x in zip(*scores2)] # transpose for scatterplot
    #scores = [list(x) for x in zip(*scores)]
    
    # create k-nearest neighbors classifier for 5 neighbors
    nbs = 15
    neigh = KNeighborsClassifier(n_neighbors=nbs)
    neigh.fit(scores, classes) # train classifier
    pred = neigh.predict(input_scores) # predict classes of the test inputs
    probs = neigh.predict_proba(input_scores) # get probabilities of inputs being in each class
    if(not testing_mode):
        # get max prob for poem - prob[x][1]
        probs = [list(x) for x in zip(*probs)]
        prob = max(probs[1])
        probindex = probs[1].index(prob)
        
        # get the pred corresponding to the index of max
        pred = int(pred[probindex])
        probs = [probs[0][probindex], probs[1][probindex]]
        input_scores = input_scores[probindex]
        
        print('Poetified: ' + tree.Tree.from_str(s[probindex]).__str2__())
        print('Predict: ' + str(pred))
        print('Probabilities: prose: ' + str(probs[0]) + '\tpoem: ' + str(probs[1]))
    else:
        Y = [1 for x in range(0,50)]
        temp = [0 for x in range(0,50)]
        Y = Y + temp
        accuracy = neigh.score(input_scores, Y)
        print('Neighbors: ' + str(nbs) + '\tAccuracy: ' + str(accuracy*100))
        input_scores = [list(x) for x in zip(*input_scores)]
    plot_data(scores1, scores2, input_scores) # plot data