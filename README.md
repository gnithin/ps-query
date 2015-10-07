## ps-query your `docker ps` output

The [`docker ps`](https://docs.docker.com/reference/commandline/ps/) command comes with set of helpful options, but there are a few things one cannot do using only flags - useful stuff like finding container ids of a particular image and useless stuff like finding the longest container name or finding all the unique names ;)

ps-query will run the docker ps (with your defined flags if necessary) and format the output depending upon the query you give it.

The query language is fairly simple, similar to basic sql syntax.

### Installing it

* Clone repo - 
```
git clone https://github.com/gnithin/ps-query.git
```

* Go into the `ps-query` directory
```
cd ps-query
```

* (Optional) Now, if you want this script to be temporary, or contained, consider creating a [virtual environment](https://virtualenv.pypa.io/en/latest/) at this point and enter it - 
```
virtualenv venv
. venv/bin/activate
```

* Install via pip -
```
pip install --editable .
```

This will install all the dependencies and the rest of it into this directory.

### Usage

If everything went well, the following should work - 
```
ps_query -a -j
```

[Prints out the json output of all the recent containers]

* You can query like this - 
```
ps_query -q 'name = "sleepy_einstein"' -j
```

* Or using a regex - 
```
ps_query -q 'name like ".*(lee|lly).*"' -j
```

* Search for images whose names you don't remember quite well - 
(Some image name which is either `base` or `bass`?)
```
ps_query -q 'image like ".*bas[es].*"'
```

* Search for containers by their commands as well(even if you only remember 1 of it's commands) -
```
ps_query -q 'command = "/bin/bash"'
```

* Logical comparision is also available - 
  * Suppose you need to find containers of an `ubuntu` image with a certain command in it - 
 
	```
	ps_query -q 'command = "/bin/bash" and image = "ubuntu"'
	```
	
  * Suppose you need to find (certain name and image=A) or (image=B)
  
    ```
    ps_query -q 'name like ".*ha.*" and image="nithin/base_dep:0.1" or image="ubuntu"' -j
    ```
      
  * Or another variant of above - (container name) and (image=A or image=B)
  
    ```
    ps_query -q 'name like ".*ha.*" and (image="nithin/base_dep:0.1" or image="ubuntu")' -j
    ```

<!--TODO:-->
<!--* Add query examples -->
<!--* Add examples for CLI args.-->
<!--* Add examples for pylib args.-->
<!--* Enlist basic operators and features.(Probably best if it's explained in the example itself.)-->
