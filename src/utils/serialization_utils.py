import pickle

class SerializationUtils:
    @staticmethod
    def save_to_file(obj, filename):
        try:
            with open(filename, 'wb') as file:
                pickle.dump(obj, file)
            print(f"Object saved to {filename}.")
        except Exception as e:
            print(f"Error saving object: {e}")

    @staticmethod
    def load_from_file(filename):
        try:
            with open(filename, 'rb') as file:
                obj = pickle.load(file)
            print(f"Object loaded from {filename}.")
            return obj
        except Exception as e:
            print(f"Error loading object: {e}")
            return None
