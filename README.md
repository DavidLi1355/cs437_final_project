# cs437_final_project

If you are using MacOs run
Install Tkinter
```
brew install python-tk
```
Install PyAudio
```
brew install portaudio
brew link portaudio
brew --prefix portaudio
touch $HOME/.pydistutils.cfg
```
And paste the following to $HOME/.pydistutils.cfg
```
[build_ext]
include_dirs=<PATH FROM STEP 3>/include/
library_dirs=<PATH FROM STEP 3>/lib/
```


James Rockey (jrockey2)
David Li (zhli2)
