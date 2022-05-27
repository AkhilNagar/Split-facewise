import face_recognition
from webapp.models import UserProfile
import numpy
import json
from json import JSONEncoder
import numpy as np


class NumpyArrayEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, numpy.ndarray):
            return obj.tolist()
        return JSONEncoder.default(self, obj)

def create_embed(name):

    data= UserProfile.objects.get(users=name)
    img=face_recognition.load_image_file(data.profile_pic)
    #print(face_recognition.face_encodings(img))
    faceencode=face_recognition.face_encodings(img)[0]
    numpyData = {"array": faceencode}
    encodejson = json.dumps(numpyData, cls=NumpyArrayEncoder)
    return encodejson

#Initialises list with all faces from db
def face_list():
    known_names = []
    known_name_encodings = []
    obj=UserProfile.objects.filter()
    n=UserProfile.objects.filter().count()
    for i in range(0,n):
        query=obj[i:i+1]
        obj1=query.get()
        known_names.append(obj1.users)
        decodedArrays = json.loads(obj1.face_encode)
        finalencode = numpy.asarray(decodedArrays["array"])
        known_name_encodings.append(finalencode)
    # print(known_names)
    # print(type(known_name_encodings[0]))
#Compares faces with the list created

def compare(img):
    #img is the group image
    userlist=[]
    known_face_encodings=[]
    face_names=[]
    obj=UserProfile.objects.filter()
    n=UserProfile.objects.filter().count()
    for i in range(0,n):
        #iterating through all userprofiles
        query=obj[i:i+1]
        obj1=query.get()
        face_names.insert(1,obj1.users)
        print(face_names)
        decodedArrays = json.loads(obj1.face_encode)
        finalencode = numpy.asarray(decodedArrays["array"])
        known_face_encodings.insert(1,finalencode)
        #print(finalencode)
        #finalencode is the faceencodings of user[i]


    unknown = face_recognition.load_image_file(img)
    unknown_encoding = face_recognition.face_encodings(unknown)


    for face_encoding in unknown_encoding:
        matches = face_recognition.compare_faces(known_face_encodings,face_encoding)
        face_distances=face_recognition.face_distance(known_face_encodings,face_encoding)
        best_match_index = np.argmin(face_distances)


        if matches[best_match_index]:
            name = face_names[best_match_index]
            userlist.insert(1,name)

    return userlist
