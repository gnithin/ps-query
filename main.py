#!/user/bin/env python
import subprocess
import json

class ps_sqlify:
    @classmethod
    def __get_container_full_details(cls, args = "a"):
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
        inspect_output_str, inspect_err_output_str = inspect_res.communicate()

        # TODO: Remove this block - Used for testing
        #with open("example_output.out", 'w') as fp:
        #    fp.write(inspect_output)

        inspect_output = json.loads(inspect_output_str) 

        return inspect_output
    
    @classmethod
    def __purge_container_details(cls, container_details):
        # Helper function #1
        def get_keys(ip_dict, key):
            dict_val = ip_dict
            for k in key.split("."):
                if type(dict_val) == dict and k in dict_val:
                    dict_val = dict_val[k]
                else:
                    return None
            return dict_val
        
        # Helper function #2
        def get_safe_val(ip_dict, key, default=None):
            val = get_keys(ip_dict, key)
            return val if val != None else default

        # Purge all the unnecessary fields
        # The required_fields assumes docker inspect is done
        # on a container id and not an Image id (That would give a different
        # json structure output)
        
        required_fields = [
            "Id", # container_id
            "Image", # image_id
            "Name", # container_name
            "Config.Image", # image_name
            "Config.Cmd", # command
            "Created", # created
            "State.StartedAt", #StartedAt
            "State.FinishedAt", # FinishedAt
            "State.Running", # status
            "NetworkSettings.Ports"# ports
        ]

        new_container_details = []
        
        for cd in container_details:
            t_store = {
                    rf : get_safe_val(cd, rf) \
                    for rf in required_fields \
            }
            new_container_details.append(t_store)
        
        return new_container_details

    @classmethod
    def get_container_details(cls, arg_list):
        all_det = cls.__get_container_full_details(arg_list)
        purged_det = cls.__purge_container_details(all_det)
        return purged_det


if __name__ == "__main__":
    arg_list = "l"
    container_details = ps_sqlify.get_container_details(arg_list)
    print json.dumps(container_details)

