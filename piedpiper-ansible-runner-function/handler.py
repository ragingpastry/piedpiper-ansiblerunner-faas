import ansible_runner
import io
import queue
import os
import tempfile
import yaml

from .util import unzip_files

## Create queue and pass to handle. Handle will add events to the queue from run_ansible.
## event_stream in index.py will pull events off the queue as they come up and stream back to the client

def handle(zip_file, event_queue):
    """
    handle a request to the function
    Args:
        request (str): request body
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        unzip_files(zip_file, tmpdir)
        with open(f'{tmpdir}/run_vars.yml') as o:
            run_vars = yaml.safe_load(o)
        os.chdir(tmpdir)
        project_directories = [name for name in os.listdir(".") if os.path.isdir(name)]
        for project_directory in project_directories:
            if 'playbooks' in run_vars and run_vars['playbooks'] is not None:
                for playbook in [run_vars['playbooks']['create'], run_vars['playbooks']['destroy']]:
                    run_ansible(project_directory, f'{tmpdir}/{project_directory}/', playbook, event_queue)


def run_ansible(playbook_directory, project_directory, playbook, event_queue):
    """
    Executes ansible-runner
    :param directory: string of directory (absolute or relative) to run ansible-runner
    :return: str of results
    """

    params = {
        'project_dir': playbook_directory,
        'private_data_dir': playbook_directory,
        'playbook': playbook,
        'inventory': 'localhost',
        'verbosity': 1,
        'extravars': {
            'project_directory': project_directory
        },
    }

    rc = ansible_runner.runner_config.RunnerConfig(**params)
    rc.prepare()
    runner = ansible_runner.Runner(config=rc, event_handler=lambda x: event_queue.put(x))
    runner.run()
    return 'OK'

