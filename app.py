from flask import render_template, url_for, flash, redirect, request, Flask, jsonify
import urllib.request as url_request
import binascii
from PIL import Image
import numpy as np
import cv2
import scipy.cluster
import os


app = Flask(__name__)


def find_dominant_color(filename):
    im = Image.open(filename)
    im = im.resize((150, 150))      # to reduce time
    ar = np.asarray(im)
    shape = ar.shape
    ar = ar.reshape(np.product(shape[:2]), shape[2]).astype(float)

    codes, dist = scipy.cluster.vq.kmeans(ar, 5)

    vecs, dist = scipy.cluster.vq.vq(ar, codes)      # assign codes
    counts, bins = np.histogram(vecs, len(codes))    # count occurrences

    index_max = np.argmax(counts)                    # find most frequent
    peak = codes[index_max]
    colour = binascii.hexlify(bytearray(int(c) for c in peak)).decode('ascii') # actual colour, (in HEX)
    return colour

def logo_border_color(filename):
    img = cv2.imread(filename)
    colour = binascii.hexlify(bytearray(int(c) for c in img[0][-2])).decode('ascii')
    return colour


@app.route('/extract', methods=['GET','POST'])
def store():
    if request.method == 'GET':
        image_url = request.args.get("src")
        image_url = image_url.replace(" ", "%20")
        url_request.urlretrieve(image_url, "image.png")
        
        dom_color = find_dominant_color("image.png")
        logo_color = logo_border_color("image.png")
        os.remove("image.png")
        return jsonify({"logo_border": "#{}".format(logo_color), 'dominant_color': "#{}".format(dom_color)})


if __name__ == "__main__":
    app.run(port=8000, debug=True)  # running the app on the local machine on port 8000