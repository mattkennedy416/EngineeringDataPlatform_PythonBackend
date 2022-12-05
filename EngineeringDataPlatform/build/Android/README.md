
Buildozer comes as a Docker container

https://github.com/kivy/buildozer

clone and then:

> docker build --tag=buildozer .

The first time Buildozer is run, as it's downloading and setting up the Android build environment, 
the container needs to be run in interactive (-it) mode so that the Google licenses can be accepted. 


> docker run -it --volume C:/Users/mattk/Downloads/buildozer-master/build_dir:/home/user/hostcwd buildozer android init

> docker run -it -v "$(pwd)":/home/user/hostcwd kivy/buildozer android debug

commands can be passed to buildozer in the docker run, eg  "android debug"

