'''
THEANO_FLAGS=mode=FAST_RUN,device=cpu,floatX=float32, python theano_knn.py
'''

import time

import numpy 
import theano
import theano.tensor as T
import theano.sandbox.cuda

from sklearn.datasets import fetch_mldata
from sklearn.cross_validation import train_test_split
from sklearn.metrics import f1_score

mnist = fetch_mldata('MNIST original')
X, y = mnist.data.astype("float32"), mnist.target.astype("int32")
X /= X.sum(axis=1)[:, numpy.newaxis]
train_x, test_x, train_y, test_y = train_test_split(X, y, test_size=0.2, random_state=42)

#Prepare variables
train_x = theano.shared(train_x, theano.config.floatX)
test_x = theano.shared(test_x, theano.config.floatX)

#Define Graph
closest_sample = T.argmax(T.dot(test_x, train_x.T), axis=1)

#Compile Graph
f = theano.function([], closest_sample)

#Execute
ts = time.time()
closest_sample = f()
theano_time = time.time()-ts

#Evaluation
pred = train_y[closest_sample]
theano_f1 = f1_score(test_y, pred, average='macro')

print "Theano:: %.3f [sec], F1: %.3f"%(theano_time, theano_f1)
