import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
from PIL import Image

def load_img(path_to_img):
    max_dim = 512
    img = tf.io.read_file(path_to_img)
    img = tf.image.decode_image(img, channels=3)
    img = tf.image.convert_image_dtype(img, tf.float32)
    shape = tf.cast(tf.shape(img)[:-1], tf.float32)
    long_dim = max(shape)
    scale = max_dim / long_dim
    new_shape = tf.cast(shape * scale, tf.int32)
    img = tf.image.resize(img, new_shape)
    img = img[tf.newaxis, :]
    return img

def tensor_to_image(tensor):
    tensor = tensor*255
    tensor = np.array(tensor, dtype=np.uint8)
    if np.ndim(tensor)>3:
        tensor = tensor[0]
    return Image.fromarray(tensor)

# Load images
content_image = load_img('dd.jpg')
style_image = load_img('tl.jpg')

# Load model
hub_model = hub.load('https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2')

# Perform style transfer
stylized_image = hub_model(tf.constant(content_image), tf.constant(style_image))[0]

# Save the result
tensor_to_image(stylized_image).save("stylized_image.png")
print("Stylized image saved as stylized_image.png")