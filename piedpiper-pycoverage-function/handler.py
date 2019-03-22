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
    for (r, d, f) in os.walk(os.path.abspath(directory)):
        if len(d) == 1:
            # Step into the top level directory
            top_dir = os.path.join(r, d[0])
            os.chdir(top_dir)
            # Run pytest on the directory
            sp = subprocess.run('py.test', stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            # return the output of the runner
            return sp.stdout.decode("utf-8")
            # buffer += f'FULL {top_dir}\n'
            # buffer += f'ROOT {r}\n'
            # buffer += f'DIRS {d}\n'
            # buffer += f'FILE {r}\n'
        buffer += 'Multiple directories contained in zip file'
    return buffer
