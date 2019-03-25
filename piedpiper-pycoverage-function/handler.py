import io
import os
import subprocess

from .util import build_temp_zipfiles, build_directories, unzip_files


def handle(request):
    """
    handle a request to the function
    Args:
        request (str): request body
    """
    try:
        zip_files = build_temp_zipfiles(request)
        temp_directories = build_directories(request)
        report  = ''
        for zip_file, temp_directory in zip(zip_files, temp_directories):
            unzip_files(zip_file, temp_directory.name)
            os.chdir(temp_directory.name)
            report = run_test_coverage('.')
    except Exception as e:
        report = e
    return report


def run_test_coverage(directory):
    """
    Runs pylint on the directory
    :param directory: string of directory (absolute or relative) to run pylint on
    :return: str of results
    """
    buffer = ''
    for (_root, _dir, _) in os.walk(os.path.abspath(directory)):
        if len(_dir) == 1:
            # Get the folder name. There should only be one.
            top_dir = os.path.join(_root, _dir[0])
            # Step into the top level directory
            os.chdir(top_dir)
            # Run pytest on the directory and return stdout and stderr
            sp = subprocess.run('py.test', stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            # return the std output of the runner.
            return sp.stdout.decode("utf-8")
        buffer += 'Multiple directories contained in zip file'
    return buffer
