#!/usr/bin/env python
import subprocess
import json
from pprint import pprint
import parse_sql_query


class ps_query:
    # Static properties
    container_data = []
    purged_data = []

    @classmethod
    def __detect_docker_install(cls):
        '''
        Check if docker is installed

        Returns
            A boolean indicating docker installation statusw
        '''
        cmd = ["docker", "-v"]
        try:
            sp_res = subprocess.Popen(cmd, stdout=subprocess.PIPE)
            docker_resp, err = sp_res.communicate()
        except OSError:
            # Would probably be a good idea to log something here.
            pass
        except Exception:
            pass
        else:
            if not err:
                return True

        return False

    @classmethod
    def __get_container_full_details(cls, args="a"):
        '''
        Get the container details in JSON format (from docker inspect)

        Parameters:
            *args
                Optional argument that will be used to get the information that
                the docker command needs.
                Default value is `a`.
                The acceptable values that will be interpreted are - a,l

        Returns:
            A list of dicts output of the docker inspect command.
        '''

        acceptable_args = "qal"
        prefix_args = "q"
        arg_list = ""

        args = set(prefix_args + args)

        arg_list = '-' + ''.join(arg for arg in args if arg in acceptable_args)

        # Run this command
        # docker ps -qa | xargs docker inspect
        ps_res = subprocess.Popen(
                    ["docker", "ps", arg_list],
                    stdout=subprocess.PIPE
                )

        inspect_res = subprocess.Popen(
                    ["xargs", "docker", "inspect"],
                    stdin=ps_res.stdout,
                    stdout=subprocess.PIPE
                )
        inspect_output_str, inspect_err_output_str = inspect_res.communicate()

        # TODO: Remove this block - Used for testing
        # with open("example_output.out", 'w') as fp:
        #    fp.write(inspect_output)

        inspect_output = json.loads(inspect_output_str)

        return inspect_output

    @classmethod
    def __purge_container_details(cls, container_details):
        '''
        Purges the docker inspect output of the unnecessary values.
        Parameters:
            container_details
                This is a list of dicts, which is represented by the output of
                `docker inspect`.

        Returns:
            List of dicts output with only the important properties
        '''
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
            return val if val is not None else default

        # Purge all the unnecessary fields
        # The required_fields assumes docker inspect is done
        # on a container id and not an Image id (That would give a different
        # json structure output)

        required_fields = [
            "Id",  # container_id
            "Image",  # image_id
            "Name",  # container_name
            "Config.Image",  # image_name
            "Config.Cmd",  # command
            "Created",  # created
            "State.StartedAt",  # StartedAt
            "State.FinishedAt",  # FinishedAt
            "State.Running",  # status
            "NetworkSettings.Ports"  # ports
        ]

        new_container_details = []

        for cd in container_details:
            t_store = {
                    rf : get_safe_val(cd, rf)
                    for rf in required_fields
            }
            new_container_details.append(t_store)

        return new_container_details

    @classmethod
    def get_container_details(cls, arg_str, query={}):
        '''
        Get the relavant container details

        Parameters:
            arg_str
                A string representing the input arguments needed for docker ps
                output

        Returns:
            A List of dicts that are relavant
        '''
        docker_installation = cls.__detect_docker_install()

        if not docker_installation:
            msg = (
                "\nYou don't seem to have docker installed.\n" +
                "The command -\n" +
                "docker -v\n" +
                "failed to run properly :'(\n"
            )
            return msg, False

        cls.container_data = cls.__get_container_full_details(arg_str)
        cls.purged_data = cls.__purge_container_details(
            cls.container_data
        )

        qry_data = parse_sql_query.parse_query(query, data=cls.purged_data)

        return qry_data, True

if __name__ == "__main__":
    # arg_list = "l"
    arg_list = "a"

    # Example query
    # query = 'Name = "insane_bhabha"'
    query = 'name = "sleepy_einstein"'
    query = 'image = "ubuntu"'
    query = 'image = "nithin/base_dep:0.1"'
    query = "name='silly_leakey'"
    query = 'command = "/bin/bash"'
    query = 'name like ".*lee.*"'
    query = 'name like ".*(lee|lly).*"'
    query = 'command like ".*\-n.*"'
    query = "CREATED < '2015-09-14'"
    query = "container_id like '.*d825131b21154b0ed2.*'"
    query = 'image_id like ".*0f441c71.*"'

    container_details, status = ps_query.get_container_details(
            arg_list,
            query
    )

    pprint(container_details)
    print "\n"
    print "*" * 50
    print "\n%d Results match\n" % len(container_details)
    print "*" * 50
