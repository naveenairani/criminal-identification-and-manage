# facerec.py
import cv2
import numpy as np
import os

size = 2
haar_cascade = cv2.CascadeClassifier('facedata.xml')


# Part 1: Create LBPH recognizer
def train_model():
    import cv2

    model = cv2.face.LBPHFaceRecognizer_create()
    fn_dir = 'face_samples'

    print('Training...')

    (images, labels, names, id) = ([], [], {}, 0)

    for (subdirs, dirs, files) in os.walk(fn_dir):
        # Loop through each folder named after the subject in the photos
        for subdir in dirs:
            names[id] = subdir
            subjectpath = os.path.join(fn_dir, subdir)
            # Ensure that the subjectpath exists
            if not os.path.exists(subjectpath):
                os.makedirs(subjectpath)
            # Loop through each photo in the folder
            for filename in os.listdir(subjectpath):
                # Skip non-image formats
                f_name, f_extension = os.path.splitext(filename)
                if f_extension.lower() not in ['.png', '.jpg', '.jpeg', '.gif', '.pgm']:
                    print("Skipping " + filename + ", wrong file type")
                    continue
                path = os.path.join(subjectpath, filename)
                label = id

                # Load and resize the image
                img = cv2.imread(path, 0)
                img = cv2.resize(img, (112, 92))

                # Add to training data
                images.append(img)
                labels.append(int(label))
            id += 1

    # Create Numpy arrays from the two lists above
    (images, labels) = [np.array(lis) for lis in [images, labels]]
    # OpenCV trains a model from the images
    model.train(images, labels)

    return (model, names)

# Part 2: Use LBPH recognizer on camera stream
def detect_faces(gray_frame):
    global size, haar_cascade

    # Resize to speed up detection (optional, change size above)
    mini_frame = cv2.resize(gray_frame, (int(gray_frame.shape[1] / size), int(gray_frame.shape[0] / size)))

    # Detect faces and loop through each one
    faces = haar_cascade.detectMultiScale(mini_frame)
    return faces


def recognize_face(model, frame, gray_frame, face_coords, names):
    (img_width, img_height) = (112, 92)
    recognized = []
    recog_names = []

    for i in range(len(face_coords)):
        face_i = face_coords[i]

        # Coordinates of face after scaling back by `size`
        (x, y, w, h) = [v * size for v in face_i]
        face = gray_frame[y:y + h, x:x + w]
        face_resize = cv2.resize(face, (img_width, img_height))

        # Try to recognize the face
        (label, confidence) = model.predict(face_resize)

        # print(label, confidence)
        if confidence < 95 and names[label] not in recog_names:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            recog_names.append(names[label])
            recognized.append((names[label].capitalize(), confidence))
        elif confidence >= 95:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    return frame, recognized
