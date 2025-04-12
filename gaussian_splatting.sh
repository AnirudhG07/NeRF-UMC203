# This file contains on how to setup gaussian environment with `uv`
# Important, This assumes Cuda and pytorch version are compatible. Worst case have both the latest and things should work.
#
# Git cloning
git clone https://graphdeco-inria/gaussian-splatting.git --recursive

# Environment init
uv venv --python 3.10
uv init

# Requirements add
uv pip install -r requirements.txt
## Requirements of submodules
uv pip install torch # Just do it
uv pip install setuptools # Important, somehow do it
uv pip install --no-build-isolation submodules/*

# This should do most stuff.

# For SIBR Viewers
sudo apt install -y libglew-dev libassimp-dev libboost-all-dev libgtk-3-dev libopencv-dev libglfw3-dev libavdevice-dev libavcodec-dev libeigen3-dev libxxf86vm-dev libembree-dev
# Project setup
cd SIBR_viewers
# You might have to run these two commands on your own
cmake -Bbuild . -DCMAKE_BUILD_TYPE=Release # add -G Ninja to build faster
cmake --build build -j24 --target install
