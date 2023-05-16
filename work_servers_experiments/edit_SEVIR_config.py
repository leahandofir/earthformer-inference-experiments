from omegaconf import OmegaConf

conf = OmegaConf.load('./cfg_sevir.yaml')
conf.dataset.start_date = [2019, 1, 1]
conf.dataset.end_date = [2019, 12, 1]
conf.dataset.train_val_split_date = [2019, 1, 31]
conf.dataset.train_test_split_date = [2019, 5, 1]
conf.optim.max_epochs = 1
conf.optim.total_batch_size = 10 # I set this because on work computers the original training does not work
conf.optim.micro_batch_size = 1
OmegaConf.save(config=conf, f='./my_cfg_sevir.yaml')