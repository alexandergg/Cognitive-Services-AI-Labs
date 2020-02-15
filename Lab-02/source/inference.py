import tensorflow as tf
import numpy as np
import os

from PIL import Image

filename = 'model.pb'
labels_filename = 'labels.txt'

graph_def = tf.GraphDef()
labels = []

# Import the TF graph
with tf.gfile.FastGFile(filename, 'rb') as f:
    graph_def.ParseFromString(f.read())
    tf.import_graph_def(graph_def, name='')

# Create a list of labels.
with open(labels_filename, 'rt') as lf:
    for l in lf:
        labels.append(l.strip())

# Load from a file
imageFile = "./images/Test/test_image.jpg"
image = Image.open(imageFile)

# Resize 
image = image.resize((224, 224), resample=Image.BILINEAR)

# Convert to numpy array - tensor
image_tensor = np.asarray(image)

# Convert RGB -> BGR
r,g,b = np.array(image_tensor).T
image_tensor = np.array([b,g,r]).transpose()

print("Numpy array mode=BGR shape={}".format(image_tensor.shape))

# These names are part of the model and cannot be changed.
output_layer = 'loss:0'
input_node = 'Placeholder:0'

with tf.Session() as sess:
    prob_tensor = sess.graph.get_tensor_by_name(output_layer)
    predictions, = sess.run(prob_tensor, {input_node: [image_tensor] })
    
print(predictions)

# Print the highest probability label
highest_probability_index = np.argmax(predictions)
print('Classified as: ' + labels[highest_probability_index])

# Or you can print out all of the results mapping labels to probabilities.
label_index = 0
for p in predictions:
    truncated_probablity = np.float64(np.round(p,4))
    print(labels[label_index], truncated_probablity)
    label_index += 1