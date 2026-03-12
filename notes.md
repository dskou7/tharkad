Random notes follow:

llama pre-install:
apt install nvidia-cuda-toolkit

llama install: 
clone repo from github

build commands
cmake -B build -DGGML_CUDA=ON -DGGML_CUDA_ENABLE_UNIFIED_MEMORY=1
(cuda on because we have CUDA cards we want to use, unified memory because we want to be able to use RAM as well)

cmake --build build --config Release -j 23
(the -j 23 is how many threads to use. Tharkad has 24 cores so i'm gonna use em)
