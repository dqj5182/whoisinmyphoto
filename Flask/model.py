from facenet_pytorch import MTCNN, InceptionResnetV1
import face_recognition
import torch
import PIL.Image
import torch.nn.functional as F
torch.set_num_threads(1)

# Initialization (we are using pre-trained face recognition model)
mtcnn = MTCNN()
resnet = InceptionResnetV1(pretrained='vggface2').eval()
resnet.classify = True


# Get Embedding
def get_embedding_list(image_list_input):
    embeddinglist = []
    for images in image_list_input:
        im = PIL.Image.open(images)
        width, height = im.size
        if width > 1000 or height > 1000:
            im = im.resize((round(im.size[0]*0.3), round(im.size[1]*0.3)))
        elif width > 500 or height > 500:
            im = im.resize((round(im.size[0]*0.6), round(im.size[1]*0.6)))
        im = im.resize((round(im.size[0]*0.5), round(im.size[1]*0.5)))
        im_cropped = mtcnn(im)
        #im_cropped = im_cropped.resize((round(im_cropped.size[0]*0.5), round(im_cropped.size[1]*0.5)))
        im_embedding = resnet(im_cropped.unsqueeze(0))
        embeddinglist.append(im_embedding) # Important part: making baseembeddinglist
    return embeddinglist


# Predicting
# Input from users: newfaceimage, baseembeddinglist, name_list
def predict(newfaceimage, baseembeddinglist, name_list):
    #assert len(baseembeddinglist) == len(name_list) # Make sure to have same number of people in mind

    horizontal_mid_coord_list = []
    face_image_list = []

    # Find who is in the "newfaceimage" image
    image = face_recognition.load_image_file(newfaceimage)

    face_locations = face_recognition.face_locations(image)

    # Get each faces in the "newfaceimage" image
    for face_location in face_locations:
        horizontal_mid_coord = (face_location[1] + face_location[3])/2
        horizontal_mid_coord_list.append(horizontal_mid_coord)

    face_locations = [x for _, x in sorted(zip(horizontal_mid_coord_list, face_locations))]

    for face_location in face_locations:
        top, right, bottom, left = face_location
        face_image = image[top:bottom, left:right]
        face_image_list.append(face_image)

    mtcnn = MTCNN()

    # Initializing variable
    number_of_faces = 0

    face_embedding_list = []

    # Create an inception resnet (in eval mode):
    resnet = InceptionResnetV1(pretrained='vggface2').eval()

    for each_face_image in face_image_list: # For all the faces in the "newfaceimage" image, get face embedding
        img = PIL.Image.fromarray(each_face_image.astype('uint8'), 'RGB')
        img_cropped = mtcnn(img)
        try:
            resnet.classify = True
            img_probs = resnet(img_cropped.unsqueeze(0))

            face_embedding_list.append(img_probs)

            number_of_faces += 1
        except AttributeError:
            continue

    prediction_list = []
    # For all faces in the image, predict whose face is each of them
    for each_new_face_embedding in face_embedding_list:
        cosine_similarity_list = []
        for each_embedding in baseembeddinglist:
            cosine_similarity_list.append(torch.mean(F.cosine_similarity(each_new_face_embedding, each_embedding, dim=0)))

        if max(cosine_similarity_list) > 0.05:
            prediction_index = cosine_similarity_list.index(max(cosine_similarity_list))
            prediction_result = name_list[prediction_index] # Prediction result (for users)
            prediction_list.append(prediction_result)
        else:
            prediction_result = "Unknown"
            prediction_list.append(prediction_result)

    return prediction_list # This contains who are in the photo
