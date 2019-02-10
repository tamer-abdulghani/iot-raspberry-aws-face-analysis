import shutil
import boto3
from time import gmtime, strftime
from os.path import join

from modules.db import Database

db = Database()


def index_faces_with_aws(images, collection, label):
    client = boto3.client('rekognition')
    try:
        client.create_collection(CollectionId=collection)
    except:
        print("Collection already exists!")

    for img in images:
        full_image_url = join("static/images/tmp", img)
        print(full_image_url)
        with open(full_image_url, 'rb') as image:
            response = client.index_faces(Image={'Bytes': image.read()}, CollectionId=collection,
                                          ExternalImageId=label, DetectionAttributes=['ALL'])
            current = strftime("%Y-%m-%d %H:%M:%S", gmtime())
            db.insert_train_info(current, label, collection, response['FaceRecords'][0]['Face']['FaceId'],
                                     response['FaceRecords'][0]['Face']['ImageId'])

    # remove all tmp images after indexing them with AWS
    shutil.rmtree("static/images/tmp")


def search_faces_with_aws(image, collection):
    client = boto3.client('rekognition')

    print('[+] Running face checks against image...')

    result, face_details = check_face(client, image)

    if result:
        print('[+] Face(s) detected with %r confidence...' % (round(face_details['FaceDetails'][0]['Confidence'], 2)))
        print('[+] Checking for a face match...')
        resu, face_match = check_matches(client, image, collection)

        if resu:
            print('[+] Identity matched %s with %r similarity and %r confidence...' % (
                face_match['FaceMatches'][0]['Face']['ExternalImageId'],
                round(face_match['FaceMatches'][0]['Similarity'], 1),
                round(face_match['FaceMatches'][0]['Face']['Confidence'], 2)))
            current = strftime("%Y-%m-%d %H:%M:%S", gmtime())
            is_allowed = False
            if face_details['FaceDetails'][0]['Smile']['Value']:
                is_allowed = True
            db.insert_access_info(current, face_match['FaceMatches'][0]['Face']['ExternalImageId'], is_allowed, str(face_details))
            return resu, face_match, face_details
        else:
            print('[-] No face matches detected...')
            return None, None, None
    else:
        print("[-] No faces detected...")
        return None, None, None


def check_face(client, file):
    face_detected = False
    with open(file, 'rb') as image:
        response = client.detect_faces(Image={'Bytes': image.read()}, Attributes=['ALL'])
        if not response['FaceDetails']:
            face_detected = False
        else:
            face_detected = True

    return face_detected, response


def check_matches(client, file, collection):
    face_matches = False
    with open(file, 'rb') as image:
        response = client.search_faces_by_image(CollectionId=collection, Image={'Bytes': image.read()}, MaxFaces=1,
                                                FaceMatchThreshold=85)
        if not response['FaceMatches']:
            face_matches = False
        else:
            face_matches = True

    return face_matches, response
