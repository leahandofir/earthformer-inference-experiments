# cuda dependencies
# install CUDA 11.6.2 https://stackoverflow.com/questions/50560395/how-to-install-cuda-in-google-colab-gpus
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/cuda-ubuntu2004.pin
mv cuda-ubuntu2004.pin /etc/apt/preferences.d/cuda-repository-pin-600
wget https://developer.download.nvidia.com/compute/cuda/11.6.2/local_installers/cuda-repo-ubuntu2004-11-6-local_11.6.2-510.47.03-1_amd64.deb
dpkg -i cuda-repo-ubuntu2004-11-6-local_11.6.2-510.47.0-1_amd64.deb
apt-key add /var/cuda-repo-ubuntu2004-11-6-local/7fa2af80.pub
apt-get update
apt-get -y install cuda-11-6
# symlink to be the current CUDA
!rm /usr/local/cuda
!ln -s /usr/local/cuda-11.6 /usr/local/cuda
# earthformer dependencies
pip install --upgrade pip
pip install torch==1.12.1+cu116 torchvision==0.13.1+cu116 torchaudio==0.12.1 torchtext==0.13.1 torchdata==0.4.1 --extra-index-url https://download.pytorch.org/whl/cu116
python3 -m pip install "pytorch_lightning>=1.6.4,<1.8.0"
python3 -m pip install xarray netcdf4 opencv-python
git clone https://github.com/amazon-science/earth-forecasting-transformer.git
cd earth-forecasting-transformer
python3 -m pip install -U -e . --no-build-isolation
pip install -v --disable-pip-version-check --no-cache-dir pytorch-extension git+https://github.com/NVIDIA/apex.git
# install aws cli to check out sevir dataset
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
