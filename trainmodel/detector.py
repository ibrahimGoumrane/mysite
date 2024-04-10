from pathlib import Path
import face_recognition
import pickle
from collections import Counter
import numpy as np


DEFAULT_ENCODINGS_PATH = Path("output")
Path('training').mkdir(exist_ok=True)
Path("output").mkdir(exist_ok=True)
Path("validation").mkdir(exist_ok=True)


class FaceRecognitionHandler:
    def __init__(self, encodings_location=DEFAULT_ENCODINGS_PATH):
        self.encodings_location = encodings_location

    def save_encodings(self, name_encodings):
        if not name_encodings['names']:
            return

        with self.encodings_location.joinpath(f"{name_encodings['names'][0]}.pkl").open(mode="wb") as f:
            pickle.dump({'names': name_encodings['names'], 'encodings': name_encodings['encodings']}, f)

    def handle_encodings(self, name, show_file_error=True):
        old_encodings = self.load_encoded_faces(name, show_file_error == True)
        if old_encodings:
            return old_encodings
        return {'names': [], 'encodings': []}

    def load_encoded_faces(self, name, show_file_error=True):
        try:
            with self.encodings_location.joinpath(f"{name}.pkl").open(mode="rb") as f:
                loaded_encodings = pickle.load(f)
        except OSError as e:
            if show_file_error:
                print(f"An IOError occurred: {e}")
            return {'names': [], 'encodings': []}
        return loaded_encodings

    def encode_known_faces(self, model="CNN"):
        for filepath in Path("training").glob("elon_musk/*"):
            name = filepath.parent.name + '_encodings'
            image = face_recognition.load_image_file(filepath)
            face_encodings_old = self.handle_encodings(name, show_file_error=False)
            face_locations = face_recognition.face_locations(image, model=model)
            face_encodings = face_recognition.face_encodings(image, face_locations)

            if face_encodings_old['encodings']:
                for encoding in face_encodings:
                    if any(np.array_equal(encoding, old_encoding) for old_encoding in face_encodings_old['encodings']):
                        continue  # Do not overwrite existing encoding
                    face_encodings_old['encodings'].append(encoding)

            # Saving the encodings
            name_encodings = {"names": [name], "encodings": face_encodings}
            self.save_encodings(name_encodings)

    def recognize_faces(self, image_location, model="CNN"):
        input_image = face_recognition.load_image_file(image_location)
        input_face_locations = face_recognition.face_locations(input_image, model=model)
        input_face_encodings = face_recognition.face_encodings(input_image, input_face_locations)

        for files in self.encodings_location.glob('*_encodings.pkl'):
            file_name = files.stem
            loaded_encodings = self.load_encoded_faces(file_name)
            if not loaded_encodings['encodings']:
                continue  # Skip if there are no encodings

            for bounding_box, unknown_encoding in zip(input_face_locations, input_face_encodings):
                searched_name = self._recognize_face(unknown_encoding, loaded_encodings)
                if searched_name:
                    print(searched_name, bounding_box)
                    break

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



face_handler = FaceRecognitionHandler()

# Uncomment and use one of the paths for testing
# training_path = Path("validation/ben_afflek_1.jpg")
# training_path = Path("validation/ben_afflek_2.jpg")
training_path = Path("validation/elon-musk-celeb-fan-boys.jpg")

face_handler.recognize_faces(training_path.absolute())
