import base64
import io
import math
import os
import uuid

import PIL.ImageDraw
import flask
import numpy
import requests as requests
from flask import Flask
from PIL import Image, ImageFont

from io import BytesIO
import datetime
import base64


app = Flask(__name__)

@app.route('/', methods=['GET'])
def hello():
    return 'Hello, World!'

@app.route('/detect',methods = ['POST'])
def detect():
    if flask.request.method == 'POST':
        contract_files = flask.request.files["contract"].read()
        size_contract_heigth = flask.request.form['size_contract_heigth']
        size_contract_width = flask.request.form['size_contract_width']

        # contract_encode.show()
        # file_name_contract = str(uuid.uuid4()) + '.jpg'
        contract_encode = Image.open(io.BytesIO(contract_files)).convert('RGB')
        contract_encode.thumbnail((int(size_contract_width), int(size_contract_heigth)), Image.LANCZOS)
        # contract_encode.thumbnail((int(size_contract_width),int(size_contract_heigth)), Image.LANCZOS)
        # contract_encode.save(file_name_contract, format='JPEG', subsampling=0, quality=95)
        # im_contract = Image.open(file_name_contract).convert('RGB')

        # image asign
        asign_files = flask.request.files["asign"].read()
        asign_encode = Image.open(io.BytesIO(asign_files)).convert('RGB')
        asign_encode.thumbnail((312, 156), Image.LANCZOS)
        # asign_encode.show()
        size_asign_height = flask.request.form['size_asign_height']
        size_asign_width = flask.request.form['size_asign_width']
        # scale_width = (396 - float(size_asign_width)) * 4
        # scale_height = (596 - float(size_asign_height)) * 3
        height_nhan = float(size_asign_height) * 2
        width_nhan = float(size_asign_width) * 2
        # print(width_nhan)

        im_contract = contract_encode.copy()
        im_contract.paste(asign_encode, (int(width_nhan), int(height_nhan)))
        # os.remove(file_name_contract)
        # paste_image.show()
        buffered = BytesIO()
        im_contract.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue())
        return flask.jsonify({'action': True, 'image':  img_str.decode("utf-8")})
    else:
        return flask.jsonify({'action': False})

@app.route('/get_image_time',methods = ['GET'])
def get_image_time():
    width = flask.request.args.get('width')
    height = flask.request.args.get('height')
    im_new = Image.new(mode="RGB", size=(int(width), int(height)), color=(255, 255, 255))
    im_cp = im_new.copy()
    draw = PIL.ImageDraw.Draw(im_cp)
    x, y = int(int(width) / 2), int((int(height) + 100) / 2)
    if x > y:
        font_size = y
    elif y > x:
        font_size = x
    else:
        font_size = x
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    truetype_url = 'https://github.com/googlefonts/roboto/blob/main/src/hinted/Roboto-Black.ttf?raw=true'
    r = requests.get(truetype_url, allow_redirects=True)
    font = ImageFont.truetype(io.BytesIO(r.content), (font_size // 3))
    draw.text((x, int(height) // 2), str(now), fill=(0, 0, 0), font=font, anchor='ms')

    # unique_filename = os.path.join(app.root_path +'./image_time', str(uuid.uuid4()) +".png")
    # im_cp.show()
    # return "Xuân"
    # im_cp.save(unique_filename)
    buffered = BytesIO()
    im_cp.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue())
    return flask.jsonify({'action': True, 'path':  img_str.decode("utf-8")})

# @app.route('/get_image_show')
# def get_image():
#     filename = flask.request.args.get('filename')
#     return flask.send_file(filename, mimetype='image')

@app.route('/add_time_to_image', methods=['POST'])
def add_time_to_image():
    # return send_file(filename, mimetype='image/gif')
    image_file = flask.request.form['image_base64']
    img = Image.open(BytesIO(base64.b64decode(image_file))).convert('RGB')
    img.thumbnail((624, 312), Image.LANCZOS)
    w1, h1 = img.size
    image_time = flask.request.form["image_time"]
    image_time = Image.open(BytesIO(base64.b64decode(image_time))).convert('RGB')
    w2, h2 = image_time.size
    img_type: str = flask.request.form['type']
    img_and_time = img.copy()
    if(img_type == 'center'):
        img_and_time.paste(image_time, (w1 // 4 - 85, (h1 // 4) - h2))
    elif(img_type == 'left'):
        img_and_time.paste(image_time, (w1 // 4 - w2, (h1 // 4) - 95))
    buffered = BytesIO()
    img_and_time.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue())
    return flask.jsonify({'path': img_str.decode("utf-8")})

@app.route('/up_add_time_to_image', methods=['POST'])
def up_add_time_to_image():
    # return send_file(filename, mimetype='image/gif')
    image_file = flask.request.form['image_base64']
    width_img = flask.request.form['width_img']
    height_img = flask.request.form['height_img']
    img = Image.open(BytesIO(base64.b64decode(image_file))).convert('RGB')
    print("Tới đây chưa")
    img.thumbnail((int(width_img), int(height_img)), Image.LANCZOS)
    print("Tới đây chưa 1")
    image_time = flask.request.form["image_time"]
    width_time = flask.request.form['width_time']
    height_time = flask.request.form['height_time']
    image_time = Image.open(BytesIO(base64.b64decode(image_time))).convert('RGB')
    image_time.thumbnail((int(width_time), int(height_time)), Image.LANCZOS)

    local_x = flask.request.form['local_x']
    local_y = flask.request.form['local_y']
    img_and_time = img.copy()
    img_and_time.paste(image_time,(int(local_x), int(local_y)))
    buffered = BytesIO()
    img_and_time.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue())
    return flask.jsonify({'path': img_str.decode("utf-8")})

@app.route('/rotate_image', methods=['POST'])
def rotate_image():
    type_rotate: str = flask.request.form['type']
    image_time = flask.request.form["image_time"]
    image_time = Image.open(BytesIO(base64.b64decode(image_time))).convert('RGB')
    if(type_rotate == 'left'):
        img_rotate = Image.fromarray(numpy.rot90(image_time))
        buffered = BytesIO()
        img_rotate.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue())
        return flask.jsonify({'action': True,'path': img_str.decode("utf-8")})
    if(type_rotate == 'right'):
        img_rotate = Image.fromarray(numpy.rot90(image_time, 3))
        buffered = BytesIO()
        img_rotate.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue())
        return flask.jsonify({'action': True, 'path': img_str.decode("utf-8")})

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app.run(host='192.168.1.40')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
