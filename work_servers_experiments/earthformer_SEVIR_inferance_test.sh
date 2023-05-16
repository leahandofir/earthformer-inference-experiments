# download sevir
# download all 2019 data
aws s3 cp --no-sign-request --recursive --region us-west-2 s3://sevir/data/vil/2019 ~/leah/earthformer/earth-forecasting-transformer/datasets/sevir/data/vil/2019
aws s3 cp --no-sign-request --region us-west-2 s3://sevir/CATALOG.csv ~/leah/earthformer/datasets/sevir/CATALOG.csv
# edit config
python ~/leah/earthformer/work_servers_experiments/edit_SEVIR_config.py
# run train
MASTER_ADDR=localhost MASTER_PORT=10001 python train_cuboid_sevir.py --gpus 1 --cfg my_cfg_sevir.yaml --ckpt_name last.ckpt --save tmp_sevir