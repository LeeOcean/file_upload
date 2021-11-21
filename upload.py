# _*_ coding : UTF-8 _*_
# 开发人员 : Peter Lee
# 开发时间 : 2021/7/5 15:50
# 文件名称 : upload.py


import flask
from flask import Flask, Response, request, render_template
from werkzeug.utils import secure_filename
import os
import time
import random

app = Flask(__name__)
host = 'http://127.0.0.1'

# 设置图片保存文件夹
UPLOAD_FOLDER = '/data/server/image/complaint/'
basepath = os.path.dirname(__file__)
# UPLOAD_FOLDER = 'image'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['JSON_SORT_KEYS'] = False

# 设置允许上传的文件格式
ALLOW_EXTENSIONS = ['png', 'jpg', 'jpeg', 'bmp', 'gif', 'webp', 'wmf', 'tif', 'psd']


# 判断文件后缀是否在列表中
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[-1].lower() in ALLOW_EXTENSIONS


# 上传图片
@app.route("/image/upload", methods=['POST', "GET"])
def uploads():
    if request.method == 'POST':
        # 获取post过来的文件名称，从name=file参数中获取
        file = request.files['file']
        if file and allowed_file(file.filename):
            # secure_filename方法会去掉文件名中的中文
            file_name = secure_filename(file.filename)
            # ext 取后缀
            ext = os.path.splitext(file_name)[1]
            # 定义文件名，年月日时分秒随机数
            fn = time.strftime('%Y%m%d%H%M%S')
            fn = fn + '_%d' % random.randint(0, 10000)
            fn_new = fn + ext
            file_name = fn_new
            # 保存图片
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file_name))
            # windows
            # os.rename(basepath + '\\' + UPLOAD_FOLDER + '\\' + file_name,
            #           basepath + '\\' + UPLOAD_FOLDER + '\\' + fn_new)

            # Linux
            # os.rename(basepath + '/' + UPLOAD_FOLDER + '/' + file_name,
            #           basepath + '/' + UPLOAD_FOLDER + '/' + fn_new)
            # upload_path = os.path.join(basepath, 'image', file_name)
            # file.save(upload_path)
            path = fn_new
            result = {
                # "code": 200,
                # "status": "success",
                "image_path": path
            }
            return flask.jsonify(data=result)
        else:
            # result = {
            # "code": 0,
            # "status": "failed",
            #          "error_reason": "格式错误，请重试"
            #         }
            return "格式错误，请重试", 500
    return "403 Forbidden", 403


# 批量上传图片
@app.route('/image/multiuploads', methods=['POST'])
def multiuploads():
    fn = time.strftime('%Y%m%d%H%M%S')
    image_dict = []
    uploaded_files = request.files.getlist('file[]')
    filenames = []
    file = request.files.getlist('file')
    if request.method == 'POST':
        for file in file:
            if file and allowed_file(file.filename):
                # secure_filename方法会去掉文件名中的中文
                file_name = secure_filename(file.filename)
                # ext 取后缀
                ext = os.path.splitext(file_name)[1]
                # 定义文件名，年月日时分秒随机数
                fn = time.strftime('%Y%m%d%H%M%S')
                fn = fn + '_%d' % random.randint(0, 10000)
                fn_new = fn + ext
                file_name = fn_new
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], file_name))
                path = file_name
                # filenames.append(file_name)
                # image_path = host + '/image/upload_list' + '/' + path
                image_dict.append(path)
            else:
                return "格式错误，请重试", 500
        return flask.jsonify(image_list_path=image_dict)
    return "403 Forbidden", 403


# 查看图片
@app.route("/image/upload_list/<imageId>")
def get_frame(imageId):
    # 图片上传保存的路径
    with open(r'/data/server/image/complaint/{}'.format(imageId), 'rb') as f:
        image = f.read()
        resp = Response(image, mimetype="image/jpg")
        return resp


if __name__ == "__main__":
    app.run(threaded=True)
