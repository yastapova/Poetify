import numpy as np
import matplotlib.pyplot as plt
from pcfg import runner, parsepcfg, trainpcfg, tree
from sklearn.neighbors import KNeighborsClassifier

pcfg_file_path = '../pcfg/pcfg.txt'

def scores_for_data(fname, classY):
    from poetifier import scorer
    print('Reading pcfg file.', flush=True)
    u_lhs, _, rules, probs, ntags, nwords = parsepcfg.parse_grammar(pcfg_file_path)
    
    text = runner.read_file(fname)
    text = text.strip().split('\n')
    scores = []
    classes = []
    print('Calculating scores.',flush=True)
    for t in text:
        ptree = [tree.Tree.from_str(t)]
        rules_p, _, _, _ = trainpcfg.count_all_rules(ptree)
        ascore, mscore = scorer.calc_score(rules, probs, rules_p, u_lhs, ntags, nwords)
        scores.append([ascore, mscore])
        classes.append(classY)
    return scores, classes

#sample = [[1,3,5],[2,4,6]]
#sampley = [0,1,0]

def plot_data(poems, prose, input_scores):
    fig = plt.figure()
    ax = plt.gca()
    ax.scatter(poems[0], poems[1], c='green', alpha=0.10, edgecolors='none')
    ax.scatter(prose[0], prose[1], c='red', alpha=0.10, edgecolors='none')
    ax.scatter(input_scores[0], input_scores[1], c='blue', alpha=1, edgecolors='none', marker='D', s=40)
    ax.set_yscale('log')
    plt.ylim(1e-200,1)
    plt.xlim(-0.05, 0.4)
    plt.xlabel('ascore')
    plt.ylabel('mscore')
    plt.show()

def classify_input(s, input_scores):
    scores1, classes1 = scores_for_data('../data/poems_classifier.trees', 1)
    scores2, classes2 = scores_for_data('../data/prose_classifier.trees', 0)
    scores = scores1 + scores2
    classes = classes1 + classes2
    scores1 = [list(x) for x in zip(*scores1)]
    scores2 = [list(x) for x in zip(*scores2)]
    #scores = [list(x) for x in zip(*scores)]
    print(np.shape(scores))
    print(np.shape(classes))
    neigh = KNeighborsClassifier(n_neighbors=5)
    neigh.fit(scores, classes)
    pred = neigh.predict(input_scores)
    probs = neigh.predict_proba(input_scores)
    print('Predict: ' + str(pred) + '\tWith probabilities: ' + str(probs))
    plot_data(scores1, scores2, input_scores)