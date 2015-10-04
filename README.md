## ps-query your `docker ps` output

The [`docker ps`](https://docs.docker.com/reference/commandline/ps/) command comes with set of helpful options, but there are a few things one cannot do using only flags - useful stuff like finding container ids of a particular image and useless stuff like finding the longest container name or finding all the unique names ;)

ps-query will run the docker ps (with your defined flags if necessary) and format the output depending upon the query you give it.

The query language is fairly simple, similar to basic sql syntax.

TODO:
* Add query examples -
  * name = "sleepy_einstein"
  * image = "ubuntu"
  * image = "nithin/base_dep:0.1"
  * command = "/bin/bash"
  * name like ".*lee.*"
  * name like ".*(lee|lly).*"
* Add examples for CLI args.
* Add examples for pylib args.
* Enlist basic operators and features.(Probably best if it's explained in the example itself.)
