
'''
思想很重要，算法是实现思想，得出结果，实现必须执行
tf：
1.首先画出计算图
2.图的每一个节点构建，可能是constant，可能是varible，可能是placeholder
3.在图中使用解决思想的优化方法，进行迭代
4.真正在session中,给数据并进行计算，得出结果
5.评估结果
'''

import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data

n_features=28*28
n_hidden1=300
n_hidden2=100
n_output=10




X=tf.placeholder(tf.float32,shape=(None,n_features),name='features')
y=tf.placeholder(tf.int64,shape=(None),name='y')

def neuron_layer(input,n_neurons,name,activation=None):
    with tf.name_scope(name):
        n_input=int(input.get_shape()[1])
        stddev = tf.cast(2 / tf.square(n_input),tf.float32)
        initw = tf.truncated_normal((n_input, n_neurons), stddev=stddev)  # y_=x.w+w0
        w=tf.Variable(initw)
        w0 = tf.Variable(tf.zeros([n_neurons]))
        z=tf.matmul(input,w)+w0
        if activation=='relu':
            return tf.nn.relu(z)
        else:
            return z

with tf.name_scope('dnn'):
    hidden1=neuron_layer(X,n_hidden1,'hidden1','relu')
    hidden2=neuron_layer(hidden1,n_hidden2,'hidden2','relu')
    logits=neuron_layer(hidden2,n_output,'softmax')

with tf.name_scope('loss'):
    xentropy=tf.nn.sparse_softmax_cross_entropy_with_logits(labels=y,logits=logits)
    loss=tf.reduce_mean(xentropy,name='loss')

with tf.name_scope('optimizer'):
    optimizer=tf.train.GradientDescentOptimizer(learning_rate=0.01)
    train=optimizer.minimize(loss)#这里会对tf图中的varible节点(这里指的是w和w0）进行梯度下降

with tf.name_scope('eval'):
    correct=tf.nn.in_top_k(logits,y,1)
    acc=tf.reduce_mean(tf.cast(correct,tf.float32))

init=tf.global_variables_initializer()
saver=tf.train.Saver()

mnist=input_data.read_data_sets('MNIST_DATA_BAK/')
batch_size=50
mini_batch_epoch=int(mnist.train.num_examples/batch_size)
n_epochs=40

with tf.Session() as sess:
    init.run()
    for epoch in range(n_epochs):
        for i in range(mini_batch_epoch):
            X_batch,y_batch=mnist.train.next_batch(batch_size=batch_size)
            train.run(feed_dict={X:X_batch,y:y_batch})
            if(i%50==0):
                acc_train=acc.eval(feed_dict={X:X_batch,y:y_batch})
                print(i,acc_train)#问题，为什么正确率这么低？！
        acc_test=acc.eval(feed_dict={X:mnist.test.images,y:mnist.test.labels})
        print(acc_test)