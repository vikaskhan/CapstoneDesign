import tensorflow as tf
import numpy as np
import opencv as cv2

n_nodes_hl1 = 32

n_classes = 4
batch_size = 1

x = tf.placeholder('float',[None, 230400])
y = tf.placeholder('float')

def get_data(filename):
    array = np.load('training_data/' + filename + '.npy')
    if filename[0] == 'i':
         array = np.reshape(array, (1, 230400))
    if filename[0] == 'o':
         array = np.reshape(array, (1, 4))
    return array
	
hidden_1_layer = {'weights': tf.Variable(tf.random_normal([230400, n_nodes_hl1])),
                  'biases': tf.Variable(tf.random_normal([n_nodes_hl1]))}

output_layer = {'weights': tf.Variable(tf.random_normal([n_nodes_hl1, n_classes])),
                'biases': tf.Variable(tf.random_normal([n_classes]))}

def neural_network_model(data):

    l1 = tf.add(tf.matmul(data, hidden_1_layer['weights']), hidden_1_layer['biases'])
    l1 = tf.nn.relu(l1)

    output = tf.matmul(l1, output_layer['weights']) + output_layer['biases']

    return output

saver = tf.train.Saver()

def train_neural_network(x):
    prediction = neural_network_model(x)
    cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=prediction, labels=y))
    optimizer = tf.train.AdamOptimizer().minimize(cost)

    hm_epochs = 100

    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())

        for epoch in range(hm_epochs):
            epoch_loss = 0
            
            i = 0
            while i < 250:
                epoch_x = get_data('input' + str(i))
                epoch_y = get_data('output' + str(i))
                _, c = sess.run([optimizer, cost], feed_dict={x: epoch_x, y: epoch_y})
                epoch_loss += c
                i+=1
            saver.save(sess, './model')
            print('Epoch', epoch, 'completed out of', hm_epochs, 'loss:', epoch_loss)

        correct = tf.equal(tf.argmax(prediction,1), tf.argmax(y,1))
        accuracy = tf.reduce_mean(tf.cast(correct,'float'))
        print(accuracy)
        #print('Accuracy:',accuracy.eval({x:mnist.test.images, y:mnist.test.labels}))

def neural_network_output(filename):
    
    #data = get_data(filename)
	data = np.reshape(filename, (1, 230400))
    prediction = neural_network_model(x)
    with tf.Session() as sess:
        sess.run(tf.initialize_all_variables())
        saver.restore(sess,"./model")
        result = (sess.run(tf.arg_max(prediction.eval(feed_dict={x:data}), 1)))
        return result
#train_neural_network(x)
#neural_network_output('input150')
#get_data('output140')

def test_neural_network():
    array = []
    for i in range(250):
        array.append(i)
        output = neural_network_output('input' + str(i))
        with tf.Session() as sess:
            answer = sess.run(tf.argmax(get_data('output' + str(i)), 1))
        print(answer)
        if output == answer:
            array[i] = 1
        else:
            array[i] = 0
    accuracy = float(float(np.sum(array))/float(i))
    print('Hello')
    print(accuracy)

#test_neural_network()
