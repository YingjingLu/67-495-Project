import tensorflow as tf 
import numpy as np 
from supervised_data_generator_matrix import *
# from numpy.linalg import pinv

def np_masking(arr, mask):
	return tf.multiply(arr, tf.cast(mask, dtype = arr.dtype ))

def pinv(arr):
  s, u, v = tf.svd(arr)

  # Invert s, clear entries lower than reltol*s[0].
  tol = 1e-6
  approx = 10000000000.0
  atol = tf.reduce_max(s) * tol
  tmp = tf.scalar_mul(approx, tf.cast(s < atol, tf.float32))
  s = tf.add(np_masking(s,s>atol), tmp)
  s_inv = 1.0 / s

  # Compute v * s_inv * u_t * b from the left to avoid forming large intermediate matrices.
  print(s_inv.get_shape(), u.get_shape())
  b = tf.multiply(v, s_inv)
  return tf.matmul(b, tf.transpose(u))


def sigmoidActFunc(features, weights, bias):
  global MAX, MIN
  assert(features.shape[1] == weights.shape[1])
  (numSamples, numInputs) = features.shape
  (numHiddenNeuron, numInputs) = weights.shape
  V = tf.matmul(features, weights, transpose_b = True)
  # print("V" ,V.shape)
  # print("MAX", np.maximum(V))
  # for i in range(numHiddenNeuron):
  #   tf.assign_add(V[:, i], bias[0, i])

  H = 1 / (1+tf.exp(-(V+bias)))
  return H

sess = tf.InteractiveSession()
num_input = 41
num_output = 23
num_hidden_neuron = 96
has_init = False

train_x = tf.placeholder(tf.float32, [None, num_input])
train_y = tf.placeholder(tf.float32, [None, num_output])
test_x = tf.placeholder(tf.float32, [None, num_input])

w = tf.Variable(
					tf.random_normal([num_hidden_neuron, num_input]),
				    dtype = tf.float32)
bias = tf.Variable(
	                tf.random_normal([num_hidden_neuron])*2-1,
                    dtype = tf.float32)
beta = tf.Variable(
	                tf.random_normal([num_hidden_neuron, num_output])*2-1,
	                dtype = tf.float32)
M = tf.Variable(
	                tf.random_normal([num_hidden_neuron, num_hidden_neuron])*2-1,
	                dtype = tf.float32)

_var_list = [w, beta, bias, M]

# break down sigmoid activation function
v = tf.matmul(train_x, w, transpose_b = True)
H = 1.0 / (1.0 + tf.exp(-1.0 *(v+bias)))
Ht = tf.transpose(H)
# tf graph for pinv
# s, u, v = tf.svd(H)
# # Invert s, clear entries lower than reltol*s[0].
# tol = 1e-6
# approx = 10000000000.0
# atol = tf.reduce_max(s) * tol
# tmp = tf.scalar_mul(approx, tf.cast(s < atol, tf.float32))
# s_inv = 1.0 / tf.add(np_masking(s,s>atol), tmp)
# b = tf.multiply(v, s_inv)
# pinv = tf.matmul(b, tf.transpose(u))

# auxiliary matrix used for sequential learning


H_mul_M = tf.matmul(H, M)
M_mul_Ht = tf.matmul(M, Ht)
H_mul_M_mul_Ht = tf.matmul(H, M_mul_Ht)
eyeing = tf.matmul(pinv(tf.eye(500, dtype = tf.float32) + H_mul_M_mul_Ht), H_mul_M)
new_M = M - tf.matmul(M, tf.matmul(Ht, eyeing))

update_M = tf.assign(M, new_M)

update_beta = tf.assign(beta, beta + tf.matmul(M, tf.matmul(Ht, train_y - tf.matmul(H, beta))))

pred = tf.matmul(H, beta)

def train(features, targets):

    sess.run(update_M, {train_x: features})
    sess.run(update_beta, {train_x: features, train_y: targets})

def flatten_classification(pred_array):
  res = np.argmax(pred_array, axis = 1)
  return res

def predict(features):
  """
  Make prediction with feature matrix
  :param features: feature matrix with dimension (numSamples, numInputs)
  :return: predictions with dimension (numSamples, numOutputs)
  """
  # H = calculateHiddenLayerActivation(features)
  # prediction = tf.matmul(H, beta).eval()
  return flatten_classification(sess.run(pred, {train_x: features}))
sess.run(tf.initialize_variables(_var_list))

# TRAIN_DATA_PATH = 'data/train_x.npy'
# TRAIN_LABEL_PATH = 'data/train_y.npy'
# TEST_DATA_PATH = 'data/test_x_ig.npy'
# TRAIN_GENERATOR = Supervised_data_generator_matrix(TRAIN_DATA_PATH, TRAIN_LABEL_PATH, 500)
# # while TRAIN_GENERATOR.run_off != True:
# #   train_X, train_Y = TRAIN_GENERATOR.get_next_batch()
# #   train(train_X, train_Y)

# res = predict(np.load(TEST_DATA_PATH))
# print(res[:10])

saver = tf.train.Saver()
saver.restore(sess, 'E:\IS_CPP\src\preprocess\cpt\\')
# res = predict(np.load(TEST_DATA_PATH))
# print(res[:10])