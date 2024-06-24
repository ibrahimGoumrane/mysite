from pathlib import Path
import face_recognition
import pickle
from collections import Counter
import numpy as np
from PIL import Image, ImageDraw
import os
DEFAULT_ENCODINGS_PATH = Path("output")
BOUNDING_BOX_COLOR = "blue"
DEFAULT_TRAINING_PATH=Path('training')
TEXT_COLOR = "white"
Path('training').mkdir(exist_ok=True)
Path("output").mkdir(exist_ok=True)
Path("validation").mkdir(exist_ok=True)

class imageException(Exception):
    def __init__(self, errorImage) -> None:
        super(imageException,self).__init__(errorImage)
class FaceRecognitionHandler:
    def __init__(self, encodings_location=DEFAULT_ENCODINGS_PATH):
        self.encodings_location = encodings_location

    def save_encodings(self,encodings_location ,name_encodings):
        if not name_encodings['names']:
            return
        with Path(encodings_location[0]).joinpath(f"{encodings_location[1]}.pkl").open(mode="wb") as f:
            pickle.dump({'names':[encodings_location[1]], 'encodings': name_encodings['encodings']}, f)

    def handle_encodings(self, encoding_loc, show_file_error=True):
        old_encodings = self.load_encoded_faces(encoding_loc, show_file_error == True)
        if old_encodings:
            return old_encodings
        return {'names': [], 'encodings': []}

    def load_encoded_faces(self, encoding_loc, show_file_error=True):
        try:
            with Path(encoding_loc[0]).joinpath(f"{encoding_loc[1]}.pkl").open(mode="rb") as f:
                loaded_encodings = pickle.load(f)
        except OSError as e:
            if show_file_error:
                print(f"An IOError occurred: {e}")
            return {'names': [], 'encodings': []}
        return loaded_encodings
    def encoding_location(self,filepath:Path):
        heirarcy_list=filepath.parent.name.split('_')
        file_name='_'.join(filepath.parent.name.split('_')[-2:]) + '_encodings'
        cycle_directory=heirarcy_list[0]
        cycle_year_directory=heirarcy_list[1]
        section=heirarcy_list[2]
        return "{}/{}/{}/{}".format(DEFAULT_ENCODINGS_PATH,cycle_directory,cycle_year_directory,section) ,file_name
    def encode_known_faces(self, model="CNN"):
        for filepath in Path("training").glob("*/*"):
            #creating the heirarchy
            encoding_loc=self.encoding_location(filepath)
            print(encoding_loc)
            if not os.path.exists(encoding_loc[0]): 
                # if the demo_folder directory is not present  
                # then create it. 
                os.makedirs(encoding_loc[0])    
            image = face_recognition.load_image_file(filepath)
            face_encodings_old = self.handle_encodings(encoding_loc, show_file_error=False)
            face_locations = face_recognition.face_locations(image, model=model)
            face_encodings = face_recognition.face_encodings(image, face_locations)
            if face_encodings_old['encodings']:
                for encoding in face_encodings:
                    if any(np.array_equal(encoding, old_encoding) for old_encoding in face_encodings_old['encodings']):
                        continue  # Do not overwrite existing encoding
                    face_encodings_old['encodings'].append(encoding)
                    encoding=face_encodings_old

            # Saving the encodings
            name_encodings = {"names": encoding_loc[1], "encodings": face_encodings}
            self.save_encodings(encoding_loc ,name_encodings)


    def recognize_faces(self,cycle,cycle_year,section,image_location, model="CNN"):
        input_image = face_recognition.load_image_file(image_location)
        input_face_locations = face_recognition.face_locations(input_image, model=model)
        input_face_encodings = face_recognition.face_encodings(input_image, input_face_locations)
        if (not input_face_encodings) :
            print('the image entered is not clear, enter a clear image to recognize face ')
            raise imageException('Image not Clear')
        # pillow_image = Image.fromarray(input_image)
        # draw = ImageDraw.Draw(pillow_image)
        present_people=['']
        search_place="{}/{}/{}/{}".format(DEFAULT_ENCODINGS_PATH,cycle,cycle_year,section) 
        for files in Path(search_place).glob('*_encodings.pkl'):
            file_location = files.stem
            loaded_encodings = self.load_encoded_faces([search_place , file_location])
            if not loaded_encodings['encodings']:
                continue  # Skip if there are no encodings

            # for bounding_box, unknown_encoding in zip(input_face_locations, input_face_encodings):
            for bounding_box, unknown_encoding in zip(input_face_locations, input_face_encodings):
                searched_name = self._recognize_face(unknown_encoding, loaded_encodings)
                if searched_name:
                    print(searched_name)
                    present_people.append(searched_name)
                    break
        # del draw
        # pillow_image.show()
        return present_people


    @staticmethod
    def _recognize_face(unknown_encoding, reference_encoding):
        boolean_matches = face_recognition.compare_faces(reference_encoding['encodings'], unknown_encoding)
        votes = Counter(
            name
            for match, name in zip(boolean_matches, reference_encoding["names"])
            if match
        )
        if votes:
            name = votes.most_common(1)[0][0]
            ele_len = name.rfind('_encodings')
            return name[:ele_len]
    
    def _display_face(self ,draw :ImageDraw, bounding_box :tuple[list], name:str):
        top, right, bottom, left = bounding_box
        draw.rectangle(((left, top), (right, bottom)), outline=BOUNDING_BOX_COLOR)
        text_left, text_top, text_right, text_bottom = draw.textbbox(
            (left, bottom), name
        )
        draw.rectangle(
            ((text_left, text_top), (text_right, text_bottom)),
            fill="blue",
            outline="blue",
        )
        draw.text(
            (text_left, text_top),
            name,
            fill="white",
        )

face_handler = FaceRecognitionHandler()

# Uncomment and use one of the paths for testing
# training_path = Path("validation/ben_afflek_1.jpg")
# training_path = Path("validation/ben_afflek_2.jpg")
# training_path = Path("./validation/elon.jpg")
# face_handler.encode_known_faces()
# import time

# Your operation goes here
# For example:
# face_handler.recognize_faces('cp','2','c',training_path.absolute())
# start_time = time.time()
# face_handler.encode_known_faces()
# end_time = time.time()
# elapsed_time = end_time - start_time
# print("Time taken:", elapsed_time, "seconds")

