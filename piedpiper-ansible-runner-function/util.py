import os
import tempfile
import zipfile


def unzip_files(zip_file, tmpdir):
    temp_file = tempfile.NamedTemporaryFile()
    temp_file.write(zip_file.read())
    temp_file.flush()
    zip_ref = zipfile.ZipFile(temp_file.name, 'r')
    zip_ref.extractall(tmpdir)
    zip_ref.close()

