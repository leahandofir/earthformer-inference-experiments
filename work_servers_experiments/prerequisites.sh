# no need to install CUDA
# cd to our env
cd ~/leah/earthformer
# install dependencies as "usual"
pip install --upgrade pip
pip install torch==1.12.1+cu116 torchvision==0.13.1+cu116 torchaudio==0.12.1 torchtext==0.13.1 torchdata==0.4.1 --extra-index-url https://download.pytorch.org/whl/cu116
python3 -m pip install "pytorch_lightning>=1.6.4,<1.8.0"
python3 -m pip install xarray netcdf4 opencv-python
git clone https://github.com/amazon-science/earth-forecasting-transformer.git
cd earth-forecasting-transformer
python3 -m pip install -U -e . --no-build-isolation --extra-index-url --trusted-host # extra flags are important for pip freeze https://stackoverflow.com/questions/35656557/pip-freeze-breaks-with-package-installation
pip install -v --disable-pip-version-check --no-cache-dir pytorch-extension git+https://github.com/NVIDIA/apex.git
# install aws cli to check out sevir dataset
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
