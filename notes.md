Random notes follow:

# WOL
wake on lan because i don't want a 1500 watt heater running in my house all the time
* turn on wake on lan in the BIOS
* `$sudo ethtool -s enp70s0 wol g`
* run as a service: `$sudo nano /etc/systemd/system/wol.service` 
``` [Unit]
Description=Enable Wake On Lan
Requires=network.target
After=network.target

[Service]
ExecStart=/sbin/ethtool -s enp70s0 wol g
Type=oneshot
RemainAfterExit=yes

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
```
echo 'export PATH=/usr/local/cuda/bin:$PATH' >> ~/.bashrc
echo 'export LD_LIBRARY_PATH=/usr/local/cuda/lib64${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}' >> ~/.bashrc
source ~/.bashrc
```
* check with `$nvcc --version`

# directories

llama directory is /opt/llama.cpp
* `$sudo mkdir /opt/llama.cpp`
models and config are stored in /var/lib/llama.cpp/
there's a models dir and a config dir inside the llama dir. 
* `$sudo mkdir /var/lib/llama.cpp/models`
* `$sudo mkdir /var/lib/llama.cpp/config`

Old info below:

In the ~/llama.cpp/models, I made two directories. web, where i had model .gguf files, and presets. presets has all the .ini files. 

I was trying to find a way to have llama-server read all the individual .ini files for the models, but it looks like right now it can only read one file, so everything got copied into tharkad.ini. 

# llama install: 

we are creating a user to run this service
user is llamabot
* `$sudo useradd -r -s /bin/false llamabot`
* `$sudo chown -R llamabot:llamabot /opt/llama.cpp`
* `$sudo chown -R llamabot:llamabot /var/lib/llama.cpp`

also added llamabot to the render and video groups, dunno if that was needed. We'll find out this time.

clone repo from github and build
on the new server i'm putting this in /opt/llama.cpp/

# build commands
```
 cmake -B build -DGGML_CUDA=ON -DGGML_CUDA_ENABLE_UNIFIED_MEMORY=1
```
(cuda on because we have CUDA cards we want to use, unified memory because we want to be able to use RAM as well)

```
 cmake --build build --config Release -j 23
```
(the -j 23 is how many threads to use. Tharkad has 24 cores so i'm gonna use em)


# Service stuff
soo we are crating a user to run this service
user is llamabot
* `$sudo useradd -r -s /bin/false llamabot`
* `$sudo chown -R llamabot:llamabot /opt/llama.cpp`
* `$sudo chown -R llamabot:llamabot /var/lib/llama.cpp`

also added llamabot to the render and video groups





Put the llama-server.service file in /etc/systemd/system/

Run ```$ sudo systemctl daemon-reload```

Run ```$ sudo systemctl start llama-server.service``` (or restart)

# Monitoring / logs
journalctl -u llama-server.service -f
(gives a tail of service logs for the service)

systemctl status llama-server.service
(just gives system status)
