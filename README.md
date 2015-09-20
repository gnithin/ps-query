## ps-query your `docker ps` output

The [`docker ps`](https://docs.docker.com/reference/commandline/ps/) command comes with set of helpful options, but there are a few things one cannot do using only flags - useful stuff like finding container ids of a particular image and useless stuff like finding the longest container name or finding all the unique names ;)

ps-query will run the docker ps (with your defined flags if necessary) and format the output depending upon the query you give it.

The query language is fairly simple, similar to basic sql syntax.

TODO:
* Basic working(subprocess)
* Creating basic language templates/operations
  * select (It will always be select, nothing else. Might as well ignore it)
  * from <table> (Not required, although can be added)
  * where clause - col logical number , date, exited
  * order by
  * limit
  * offset
  * max()
  * min()
  * having clause
  * regex support (important)
* Output type
