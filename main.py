#!/user/bin/env python
import subprocess

class ps_sqlify:

    @classmethod
    def get_container_details(cls, args = "a"):
        '''
        Gets all the container details
        '''
        acceptable_args = "qal"
        prefix_args = "q"
        arg_list = ""

        args = set(prefix_args + args)

        arg_list = '-' + ''.join([arg for arg in args if arg in acceptable_args])
        
        #Run this command
        #docker ps -qa | xargs docker inspect
        ps_res = subprocess.Popen(
                    ["docker", "ps", arg_list],
                    stdout = subprocess.PIPE
                )

        inspect_res = subprocess.Popen(
                    ["xargs", "docker","inspect"],
                    stdin = ps_res.stdout,
                    stdout = subprocess.PIPE
                )
        inspect_output, inspect_err_output = inspect_res.communicate()

        # TODO: Remove this block - Used for testing
        with open("example_output.out", 'w') as fp:
            fp.write(inspect_output)

        return inspect_output

    def process_container_details(cls, container_details):
        return container_details

if __name__ == "__main__":
    argument_list = "l"
    container_details = ps_sqlify.get_container_details(argument_list)
