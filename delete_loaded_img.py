import os


def delete_in_directory(folder):
    for the_file in os.listdir(folder)[1:]:
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                if 'map' in file_path:
                    print(file_path)
                    os.unlink(file_path)
        except Exception as e:
            print(e)
