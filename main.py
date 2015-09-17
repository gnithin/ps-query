#!/user/bin/env python
import subprocess

def get_container_details():
    '''
    Run this command
    docker ps -qa | xargs docker inspect
    '''
    ps_res = subprocess.Popen(
                ["docker", "ps","-qa"],
                stdout = subprocess.PIPE
            )

    inspect_res = subprocess.Popen(
                ["xargs", "docker","inspect"],
                stdin = ps_res.stdout,
                stdout = subprocess.PIPE
            )
    inspect_output, inspect_err_output = inspect_res.communicate()

    # TODO: Remove this block - Used for testing
    #with open("example_output.out", 'w') as fp:
    #    fp.write(inspect_output)

    return inspect_output

def process_container_details(container_details):
    return container_details


if __name__ == "__main__":
    container_details = get_container_details()
