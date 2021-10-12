from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory, send_file, send_from_directory
import os
import os.path
from os import path
from werkzeug.utils import secure_filename
from PIL import Image, ImageDraw
import requests
from io import BytesIO
from model import get_embedding_list
from model import predict



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
    if request.method == 'POST':
        if 'quantity' in request.form:
            num_of_people = request.form['quantity']
            with open('num_people.txt', 'w') as f:
                f.write(str(num_of_people))
        else:
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



app.add_url_rule("/uploads/<name>", endpoint="download_file", build_only=True)



@app.route("/annotations")
def annotations():
    return render_template("annotations.html")



@app.route("/annotations", methods=['POST'])
def get_names():
    if request.method == 'POST':
        if 'fname4' in request.form:
            name4 = request.form['fname4']
            with open('name_list.txt', 'a+') as f:
                f.seek(0)
                # If file is not empty then append '\n'
                data = f.read(100)
                if len(data) > 0 :
                    f.write("\n")
                f.write(str(name4))
        elif 'fname3' in request.form:
            name3 = request.form['fname3']
            with open('name_list.txt', 'a+') as f:
                f.seek(0)
                # If file is not empty then append '\n'
                data = f.read(100)
                if len(data) > 0 :
                    f.write("\n")
                f.write(str(name3))
        elif 'fname2' in request.form:
            name2 = request.form['fname2']
            with open('name_list.txt', 'a+') as f:
                f.seek(0)
                # If file is not empty then append '\n'
                data = f.read(100)
                if len(data) > 0 :
                    f.write("\n")
                f.write(str(name2))
        elif 'fname1' in request.form:
            name1 = request.form['fname1']
            with open('name_list.txt', 'a+') as f:
                f.seek(0)
                # If file is not empty then append '\n'
                data = f.read(100)
                if len(data) > 0 :
                    f.write("\n")
                f.write(str(name1))
        return render_template("annotations.html")



@app.route("/classify", methods=['GET'])
def classify():
    # Get name_list
    with open('name_list.txt') as f:
        content = f.read()
    name_list = content.split('\n')

    # Get number of people
    with open('num_people.txt') as f:
        content_num = f.read()
    num_of_people = int(content_num)

    # Get images from instance file
    images_path = "/Users/daniel/Flask/instance/uploads"
    valid_images = [".jpg",".gif",".png",".tga", ".jpeg"]
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
    distinct_image_url_list = ["https://www.biography.com/.image/t_share/MTE4MDAzNDEwNzg5ODI4MTEw/barack-obama-12782369-1-402.jpg", "https://www.biography.com/.image/t_share/MTczNjEwODI2NTg5MDg3MTI0/michelle-obama-gettyimages-85246899.jpg", "https://media.vanityfair.com/photos/5bae610487834306acdc6754/4:3/w_1776,h_1332,c_limit/malia-obama-college-music-video.jpg", "https://www.biography.com/.image/ar_1:1%2Cc_fill%2Ccs_srgb%2Cg_face%2Cq_auto:good%2Cw_300/MTgxODkyNjEwNjk5MzA2MzEy/gettyimages-498724368.jpg"]

    distinct_image_list = []

    for url in distinct_image_url_list:
        img = requests.get(url, stream=True).raw
        distinct_image_list.append(img)

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

app.config['DOWNLOAD_FOLDER'] = '/instance/uploads'


@app.route('/download')
def hell():
    return render_template('download.html')

@app.route('/classify/download')
def download():
    path = "/Users/daniel/Flask/instance/Barack/Barack_obama1.jpeg"
    return send_file(path, as_attachment=True)



if __name__ == "__main__":
    app.run(debug=True)