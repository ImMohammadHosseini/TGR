
from src.constants import MODEL_SAVE_PATH
from sys import argv

if 'train' in argv[0] and not os.path.exists(MODEL_SAVE_PATH):
	os.mkdir(MODEL_SAVE_PATH)

class color:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    RED = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def plot_accuracies (accuracy_list, data_type):
	pass