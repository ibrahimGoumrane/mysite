from pathlib import Path
import face_recognition
import pickle
from collections import Counter
import numpy as np
import os


DEFAULT_ENCODINGS_PATH = Path("FaceRecoAlgo/output")
DEFAULT_TRAINING_PATH=Path('FaceRecoAlgo/training')
DEFAULT_VALIDATION_PATH=Path('FaceRecoAlgo/validation')



DEFAULT_TRAINING_PATH.mkdir(exist_ok=True)
DEFAULT_ENCODINGS_PATH.mkdir(exist_ok=True)
DEFAULT_VALIDATION_PATH.mkdir(exist_ok=True)

class imageException(Exception):
    def __init__(self, errorImage) -> None:
        super(imageException,self).__init__(errorImage)


class FaceRecognitionHandler:
    def __init__(self, encodings_location=DEFAULT_ENCODINGS_PATH):
        self.encodings_location = encodings_location

    def encode_known_faces(self, model="CNN"):
        for filepath in DEFAULT_TRAINING_PATH.glob("*/*"):
            #creating the heirarchy
            encoding_loc=self.__encoding_location(filepath)
            print(encoding_loc)
            if not os.path.exists(encoding_loc[0]): 
                # if the demo_folder directory is not present  
                # then create it. 
                os.makedirs(encoding_loc[0])    
            image = face_recognition.load_image_file(filepath)
            face_encodings_old = self.__handle_encodings(encoding_loc, show_file_error=False)
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
            self.__save_encodings(encoding_loc ,name_encodings)


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
            loaded_encodings = self.__load_encoded_faces([search_place , file_location])
            if not loaded_encodings['encodings']:
                continue  # Skip if there are no encodings

            # for bounding_box, unknown_encoding in zip(input_face_locations, input_face_encodings):
            for bounding_box, unknown_encoding in zip(input_face_locations, input_face_encodings):
                searched_name = self.__recognize_face(unknown_encoding, loaded_encodings)
                if searched_name:
                    print(searched_name)
                    present_people.append(searched_name)
                    break
        return present_people


    def __recognize_face(self,unknown_encoding, reference_encoding):
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


    def __save_encodings(self,encodings_location ,name_encodings):
        if not name_encodings['names']:
            return
        with Path(encodings_location[0]).joinpath(f"{encodings_location[1]}.pkl").open(mode="wb") as f:
            pickle.dump({'names':[encodings_location[1]], 'encodings': name_encodings['encodings']}, f)

    def __handle_encodings(self, encoding_loc, show_file_error=True):
        old_encodings = self.__load_encoded_faces(encoding_loc, show_file_error == True)
        if old_encodings:
            return old_encodings
        return {'names': [], 'encodings': []}

    def __load_encoded_faces(self, encoding_loc, show_file_error=True):
        try:
            with Path(encoding_loc[0]).joinpath(f"{encoding_loc[1]}.pkl").open(mode="rb") as f:
                loaded_encodings = pickle.load(f)
        except OSError as e:
            if show_file_error:
                print(f"An IOError occurred: {e}")
            return {'names': [], 'encodings': []}
        return loaded_encodings
    def __encoding_location(self,filepath:Path):
        heirarcy_list=filepath.parent.name.split('_')
        file_name='_'.join(filepath.parent.name.split('_')[-2:]) + '_encodings'
        cycle_directory=heirarcy_list[0]
        cycle_year_directory=heirarcy_list[1]
        section=heirarcy_list[2]
        return "{}/{}/{}/{}".format(DEFAULT_ENCODINGS_PATH,cycle_directory,cycle_year_directory,section) ,file_name

face_handler = FaceRecognitionHandler()




# training_path = Path("FaceRecoAlgo/validation/mandy.jpg")
# training_path = Path("validation/ben_afflek_2.jpg")
# training_path = Path("./validation/elon.jpg")
# face_handler.encode_known_faces()


# face_handler.recognize_faces('cp', '1', 'A', training_path)