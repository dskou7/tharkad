Random notes follow:

# WOL
wake on lan because I don't want a 1600 watt heater running in my house all the time
* turn on wake on lan in the BIOS
* `$sudo ethtool -s enp70s0 wol g`
* run as a service: `$sudo nano /etc/systemd/system/wol.service` 
``` 
[Unit]
Description=LLaMA.cpp Server Router
After=network.target
Wants=network.target

[Service]
Type=simple
User=donny
WorkingDirectory=/home/donny/llama.cpp
ExecStart=/home/donny/llama.cpp/build/bin/llama-server --host 0.0.0.0 --port 8080 --models-preset /home/donny/llama.cpp/models/presets/tharkad.ini --no-ui
Restart=always
RestartSec=5
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

* turn on the service `$sudo systemctl daemon-reload`
* `$sudo systemctl enable wol.service`
* `$sudo systemctl start wol.service`


# llama pre-install:
Drivers

* `$cat /proc/driver/nvidia/version` (this came up with nothing on first run)
* run apt updates
* `$sudo ubuntu-drivers list --gpgpu`
* `$sudo ubuntu-drivers install --gpgpu`
* reboot

CUDA

* install keyring for nvidia
```
$wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2604/x86_64/cuda-keyring_1.1-1_all.deb
$sudo dpkg -i cuda-keyring_1.1-1_all.deb
$sudo apt update
```

* check available `$apt-cache policy nvidia-open cuda-toolkit | grep -E '^\S|Candidate'`
* install nvidia-open `$sudo apt install nvidia-open` 
* reboot and run `$nvidia-smi`. This should list graphics cards installed
* install cuda toolkit `$sudo apt install cuda-toolkit` 
* put cuda stuff in the PATH (need to update this for putting stuff in everyone's path for server)

SINGLE USER
```
echo 'export PATH=/usr/local/cuda/bin:$PATH' >> ~/.bashrc
echo 'export LD_LIBRARY_PATH=/usr/local/cuda/lib64${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}' >> ~/.bashrc
source ~/.bashrc
```

MULTI USER
* `$sudo nano /etc/environment`

```
add /usr/local/cuda/bin to path string
add LD_LIBRARY_PATH="/usr/local/cuda/lib64" if there is no LD_LIBRARY_PATH
add CUDACXX="/usr/local/cuda/bin/nvcc" if there is no CUDACXX
```

* check with `$nvcc --version`
* make sure you got the right CUDACXX with `$which nvcc`

Install cmake
* `sudo apt install cmake`

# Directories

llama directory is /opt/llama.cpp
* `$sudo mkdir /opt/llama.cpp`

models and config are stored in /var/lib/llama.cpp/
there's a models dir and a config dir inside the llama dir. 

* `$sudo mkdir -p /var/lib/llama.cpp/models`
* `$sudo mkdir /var/lib/llama.cpp/config`

Old info below:

In the ~/llama.cpp/models, I made two directories. web, where i had model .gguf files, and presets. presets has all the .ini files. 

I was trying to find a way to have llama-server read all the individual .ini files for the models, but it looks like right now it can only read one file, so everything got copied into tharkad.ini. 

# Llama install: 

we are creating a user to run this service
user is llamabot
* `$sudo useradd -r -s /bin/false llamabot`
* `$sudo chown -R llamabot:llamabot /opt/llama.cpp`
* `$sudo chown -R llamabot:llamabot /var/lib/llama.cpp`

also added llamabot to the render and video groups, dunno if that was needed. We'll find out this time.

clone repo from github and build
* `$cd /opt/`
* `$sudo git clone https://github.com/ggml-org/llama.cpp`

on the new server i'm putting this in /opt/llama.cpp/

# build commands

* `sudo cmake -B build -DGGML_CUDA=ON -DGGML_CUDA_ENABLE_UNIFIED_MEMORY=1`

(cuda on because we have CUDA cards we want to use, unified memory because we want to be able to use RAM as well)

* `sudo cmake --build build --config Release -j 23`

(the -j 23 is how many threads to use. Tharkad has 24 cores so i'm gonna use em)


# Service stuff

Put the llama-server.service file (from this repo) in /etc/systemd/system/

Run `$ sudo systemctl daemon-reload`

Run ```$ sudo systemctl start llama-server.service``` (or restart)

# Monitoring / logs
journalctl -u llama-server.service -f
(gives a tail of service logs for the service)

systemctl status llama-server.service
(just gives system status)

# Actually running some models

Download the model from hugging face into /var/lib/llama.cpp/models 
* `$cd /var/lib/llama.cpp/models`

for example this downloads Qwern 3.8 UD Q8. Just copy the download link from hugging face.
* `sudo wget https://huggingface.co/unsloth/Qwen3.8-27B-GGUF/resolve/main/Qwen3.8-27B-UD-Q8_K_XL.gguf`

Update tharkad.ini in the presets directory

Restart the service

Maybe it works now