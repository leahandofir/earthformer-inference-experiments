# earthformer dependencies
pip install --upgrade pip
python3 -m pip install torch==2.0.0+cu118 torchvision -f https://download.pytorch.org/whl/torch_stable.html
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
