import argparse 
import tensorflow as tf
import os
import numpy as np
from PIL import Image

def load_image(filename):
    test_filename = os.path.join('test',filename)
    image = Image.open(test_filename)
    image = image.resize((480,480))
    image = np.array(image,np.float32)

    image = image[:,:,[2,1,0]]
    image -= [103.933,116.779,123.68]
    print image.ndim,image.shape[2]
    return image
def load_graph(frozen_graph_filename):
    # We load the protobuf file from the disk and parse it to retrieve the 
    # unserialized graph_def
    with tf.gfile.GFile(frozen_graph_filename, "rb") as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())

    # Then, we import the graph_def into a new Graph and returns it 
    with tf.Graph().as_default() as graph:
        # The name var will prefix every op/nodes in your graph
        # Since we load everything in a new graph, this is not needed
        tf.import_graph_def(graph_def, name="prefix")
    return graph

if __name__ == '__main__':
    # Let's allow the user to pass the filename as an argument
    parser = argparse.ArgumentParser()
    parser.add_argument("--frozen_model_filename", default="results/frozen_model.pb", type=str, help="Frozen model file to import")
    args = parser.parse_args()

    # We use our "load_graph" function
    graph = load_graph(args.frozen_model_filename)

    # We can verify that we can access the list of operations in the graph
    for op in graph.get_operations():
        print(op.name)
        # prefix/Placeholder
        # ...
        # prefix/fuse

    prediction = []
    x = graph.get_tensor_by_name('prefix/Placeholder:0')
    y = graph.get_tensor_by_name('prefix/fuse:0')
    prediction = tf.nn.sigmoid(y)
    #images = tf.reshape(tf.cast(y_out,tf.uint8),[480,480,1])
    #images_encode = tf.image.encode_jpeg(images)
    #fname = tf.constant('1.jpeg')
    #fwrite = tf.write_file(fname,images_encode)



    with tf.Session(graph=graph) as sess:
	img = load_image("8068.jpg")
	result = sess.run(prediction,feed_dict={x:[img]})
    em = result[0]
    print em
    em [ em < 0 ] = 0.0  
    em = 255.0 * em
    em = np.tile(em, [1, 1, 3])
    print em.shape  
    em = Image.fromarray(np.uint8(em))
    em.save(os.path.join('test','1.png'))
