'''
    Script for checking if the Inference computations run properly for the trained graph.
'''

from Summary_Generator.Tensorflow_Graph import order_planner_without_copynet
from Summary_Generator.Text_Preprocessing_Helpers.pickling_tools import *
from Summary_Generator.Tensorflow_Graph.utils import *
from Summary_Generator.Model import *
import numpy as np
import tensorflow as tf


# random_seed value for consistent debuggable behaviour
seed_value = 3

np.random.seed(seed_value) # set this seed for a device independant consistent behaviour

''' Set the constants for the script '''
# various paths of the files
data_path = "../Data" # the data path

data_files_paths = {
    "table_content": os.path.join(data_path, "train.box"),
    "nb_sentences" : os.path.join(data_path, "train.nb"),
    "train_sentences": os.path.join(data_path, "train.sent")
}

base_model_path = "Models"
plug_and_play_data_file = os.path.join(data_path, "plug_and_play.pickle")


# Set the train_percentage mark here.
train_percentage = 90



''' Extract and setup the data '''
# Obtain the data:
data = unPickleIt(plug_and_play_data_file)

field_encodings = data['field_encodings']
field_dict = data['field_dict']

content_encodings = data['content_encodings']

label_encodings = data['label_encodings']
content_label_dict = data['content_union_label_dict']
rev_content_label_dict = data['rev_content_union_label_dict']

# vocabulary sizes
field_vocab_size = data['field_vocab_size']
content_label_vocab_size = data['content_label_vocab_size']


X, Y = synch_random_shuffle_non_np(zip(field_encodings, content_encodings), label_encodings)

train_X, train_Y, dev_X, dev_Y = split_train_dev(X, Y, train_percentage)
train_X_field, train_X_content = zip(*train_X)
train_X_field = list(train_X_field); train_X_content = list(train_X_content)

# Free up the resources by deleting non required stuff
del X, Y, field_encodings, content_encodings, train_X

# print train_X_field, train_X_content, train_Y, dev_X, dev_Y
