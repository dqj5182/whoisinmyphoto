from flask import Flask, render_template, request, redirect, url_for, flash, send_file
import os.path
from werkzeug.utils import secure_filename
import shutil
from PIL import Image, ImageDraw
import requests
from io import BytesIO
from model import predict
from model import get_embedding_list


app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html")



@app.route("/about")
def about():
    return render_template("about.html")



@app.route("/upload")
def upload():
    return render_template("upload.html")



@app.route("/upload", methods=['POST'])
def success():
    try:
        if request.method == 'POST':
            # Create a directory in a known location to save files to.
            uploads_dir = os.path.join(app.instance_path, 'uploads')
            os.makedirs(uploads_dir, exist_ok=True)
            # check if the post request has the file part
            file_list = request.files.getlist('file')

            # If the user does not select a file, the browser submits an
            # empty file without a filename.
            for each_file in file_list :
                filename = secure_filename(each_file.filename)
                if "DS_Store" not in filename:
                    each_file.save(os.path.join(uploads_dir, filename))
            return render_template("upload.html")
    except Exception:
        return render_template("notenoughinfo.html")


@app.route("/upload/reset")
def upload_reset():
    try:
        shutil.rmtree(os.path.join(app.instance_path, 'uploads'))
    except FileNotFoundError:
        pass
    try:
        os.remove(os.getcwd() + '/name_list.txt')
    except FileNotFoundError:
        pass
    try:
        os.remove(os.getcwd() + '/num_people.txt')
    except FileNotFoundError:
        pass
    for f in os.listdir(app.instance_path):
        if f != ".DS_Store":
            try:
                shutil.rmtree(os.path.join(app.instance_path, f))
            except FileNotFoundError:
                pass
        else:
            try:
                os.remove(os.path.join(app.instance_path, f))
            except FileNotFoundError:
                pass
    return render_template("home.html")


app.add_url_rule("/uploads/<name>", endpoint="download_file", build_only=True)



@app.route("/annotations")
def annotations():
    return render_template("annotations.html")



@app.route("/annotations", methods=['POST'])
def get_names():
    try:
        if request.method == 'POST':
            # Create a directory in a known location to save files to.
            uploads_dir = os.path.join(app.instance_path, 'each_name')
            os.makedirs(uploads_dir, exist_ok=True)
            # check if the post request has the file part
            file_list = request.files.getlist('file')

            # If the user does not select a file, the browser submits an
            # empty file without a filename.


            for each_file in file_list :
                filename = secure_filename(each_file.filename)
                if "DS_Store" not in filename:
                    each_file.save(os.path.join(uploads_dir, filename))
                each_name = (filename.split("_", 1)[1]).split(".")[0]

                with open('name_list.txt', 'a+') as f:
                        f.seek(0)
                        # If file is not empty then append '\n'
                        data = f.read(200)
                        if len(data) > 0 :
                            f.write("\n")
                        f.write(str(each_name))

            return render_template("annotations.html")
    except Exception:
        return render_template("notenoughinfo.html")

@app.route("/annotations/reset")
def annotations_reset():
    try:
        shutil.rmtree(os.path.join(app.instance_path, 'uploads'))
    except FileNotFoundError:
        pass
    try:
        os.remove(os.getcwd() + '/name_list.txt')
    except FileNotFoundError:
        pass
    try:
        os.remove(os.getcwd() + '/num_people.txt')
    except FileNotFoundError:
        pass
    for f in os.listdir(app.instance_path):
        if f != ".DS_Store":
            try:
                shutil.rmtree(os.path.join(app.instance_path, f))
            except FileNotFoundError:
                pass
        else:
            try:
                os.remove(os.path.join(app.instance_path, f))
            except FileNotFoundError:
                pass
    return render_template("home.html")

@app.route("/classify", methods=['GET'])
def classify():
    try:
        # Get images from instance file
        images_path = os.path.join(app.instance_path, 'uploads')
        valid_images = [".jpg",".png",".jpeg"]
        new_image_list = []
        new_image_name_list = []
        for f in os.listdir(images_path):
            ext = os.path.splitext(f)[1]
            if ext.lower() not in valid_images:
                continue
            new_image_list.append(os.path.join(images_path,f))

            new_image_name_list.append(f) # Add name of each image file

        # Get base embedding list
        # User input: single shot image for each distinct person

        distinct_image_list = []
        name_list = []

        images_path2 = os.path.join(app.instance_path, 'each_name')

        for f in os.listdir(images_path2):
            ext = os.path.splitext(f)[1]
            if ext.lower() not in valid_images:
                continue
            distinct_image_list.append(os.path.join(images_path2,f))
            name_list.append((f.split("_", 1)[1]).split(".")[0])


        baseembeddinglist = get_embedding_list(distinct_image_list)

        # Get prediction list
        prediction_list = []

        for new_image in new_image_list:
            prediction = predict(new_image, baseembeddinglist, name_list)
            prediction_list.append(prediction)

        # Make folders of names
        for name in name_list:
            uploads_dir = os.path.join(app.instance_path, name)
            os.makedirs(uploads_dir, exist_ok=True)

        unknown_dir = os.path.join(app.instance_path, "Unknown")
        os.makedirs(unknown_dir, exist_ok=True)

        index = 0
        # For each photo, check whether the person is in the photo
        for each_photo in new_image_list: # each_photo has multiple people inside
            who_are_in_the_photo = predict(each_photo, baseembeddinglist, name_list) # get who is in the photo
            for who in who_are_in_the_photo: # For each person we have in the photo
                filename = secure_filename(new_image_name_list[index])
                if "DS_Store" not in filename:
                    Image.open(each_photo).save(os.path.join(app.instance_path, who, filename)) # Save this image to each directory
            index += 1

        return render_template("classify.html")
    except Exception:
        return render_template("notenoughinfo.html")

app.config['DOWNLOAD_FOLDER'] = '/instance/uploads'

@app.route("/classify/reset")
def classify_reset():
    try:
        shutil.rmtree(os.path.join(app.instance_path, 'uploads'))
    except FileNotFoundError:
        pass
    try:
        os.remove(os.getcwd() + '/name_list.txt')
    except FileNotFoundError:
        pass
    try:
        os.remove(os.getcwd() + '/num_people.txt')
    except FileNotFoundError:
        pass
    for f in os.listdir(app.instance_path):
        if f != ".DS_Store":
            try:
                shutil.rmtree(os.path.join(app.instance_path, f))
            except FileNotFoundError:
                pass
        else:
            try:
                os.remove(os.path.join(app.instance_path, f))
            except FileNotFoundError:
                pass
    return render_template("home.html")


@app.route('/download')
def hell():
    return render_template('download.html')

@app.route('/classify/download')
def download():
    app.logger.info("Phase 1")
    path = os.path.join(app.instance_path, '')
    shutil.rmtree(os.path.join(app.instance_path, 'uploads'))
    shutil.rmtree(os.path.join(app.instance_path, 'each_name'))
    result = shutil.make_archive(path, 'zip', path)
    app.logger.info("Phase 2")
    os.remove(os.getcwd() + '/name_list.txt')
    for f in os.listdir(app.instance_path):
        if f != ".DS_Store":
            shutil.rmtree(os.path.join(app.instance_path, f))
        else:
            os.remove(os.path.join(app.instance_path, f))
    app.logger.info("Phase 3")
    return send_file(
        result,
        as_attachment=True,
        attachment_filename='organized.zip',
        mimetype='application/zip')
