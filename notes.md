Random notes follow:

# llama pre-install:
apt install nvidia-cuda-toolkit

(this broke when llama.cpp wanted cuda 13, but we had cuda 12 intalled. More to come on this.)


# llama install: 
clone repo from github  and build

# build commands
```
 cmake -B build -DGGML_CUDA=ON -DGGML_CUDA_ENABLE_UNIFIED_MEMORY=1
```
(cuda on because we have CUDA cards we want to use, unified memory because we want to be able to use RAM as well)

```
 cmake --build build --config Release -j 23
```
(the -j 23 is how many threads to use. Tharkad has 24 cores so i'm gonna use em)

# directories

In the ~/llama.cpp/models, I made two directories. web, where i had model .gguf files, and presets. presets has all the .ini files. 

I was trying to find a way to have llama-server read all the individual .ini files for the models, but it looks like right now it can only read one file, so everything got copied into tharkad.ini. 

# Service stuff
Put the llama-server.service file in /etc/systemd/system/

Run ```$ sudo systemctl daemon-reload```

Run ```$ sudo systemctl start llama-server.service``` (or restart)

# Monitoring / logs
journalctl -u llama-server.service -f
(gives a tail of service logs for the service)

systemctl status llama-server.service
(just gives system status)
