# params
params = {}
K = int(50)
doc_smoothing = 0.5  # alpha (theta)
z_subtopic_smoothing = 0.005  # beta (phi)
s_subtopic_smoothing = 2  # beta (phi)
subtopic_smoothing = 0.01  # for py_ version
iterations = 500
topic_num_words_to_print = 20
num_of_most_similar_tokens = 100
sigma = 3


DOCUMENTS_DIR = '/home/daniel/deepsy/TM/client_5_mini_turns/'
VOCAB_FILE = '/home/daniel/Documents/he_emb/ron_shemesh/words_list.txt'
EMB_FILE = '/home/daniel/Documents/he_emb/ron_shemesh/words_vectors.npy'

# DOCUMENTS_DIR = '/home/daniel/Documents/Data_Sets/NIPS_papers/docs_mini/'
# VOCAB_FILE = '/home/daniel/Documents/Word_Embeddings/Glove/glove.6B.50d.vocab.txt'
# EMB_FILE = '/home/daniel/Documents/Word_Embeddings/Glove/glove.6B.50d.vectors.npy'

STOP_WORDS_DIR = '/home/daniel/deepsy/TM/STOP_WORDS/'


params['K'] = K
params['doc_smoothing'] = doc_smoothing
params['z_subtopic_smoothing'] = z_subtopic_smoothing
params['s_subtopic_smoothing'] = s_subtopic_smoothing
params['subtopic_smoothing'] = subtopic_smoothing
params['iterations'] = iterations
params['topic_num_words_to_print'] = topic_num_words_to_print
params['num_of_most_similar_tokens'] = num_of_most_similar_tokens
params['sigma'] = sigma

params['VOCAB_FILE'] = VOCAB_FILE
params['EMB_FILE'] = EMB_FILE
params['STOP_WORDS_DIR'] = STOP_WORDS_DIR
params['DOCUMENTS_DIR'] = DOCUMENTS_DIR



