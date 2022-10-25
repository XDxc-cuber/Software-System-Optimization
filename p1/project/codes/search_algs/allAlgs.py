from .GridSearch import GridSearch
from .GreedySearch import GreedySearch

ALGS_LIST = [
    'Grid Search',
    'Greedy Search',
]

algs_dict = {
    ALGS_LIST[0]: GridSearch,
    ALGS_LIST[1]: GreedySearch
}