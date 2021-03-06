from collections import OrderedDict
import torch
import torch.nn as nn
from torch.utils.data import ConcatDataset
import random
from catalyst.dl.experiment import ConfigExperiment
from dataset import *
from augmentation import train_aug, valid_aug


class Experiment(ConfigExperiment):
    def _postprocess_model_for_stage(self, stage: str, model: nn.Module):

        import warnings
        warnings.filterwarnings("ignore")

        random.seed(2411)
        np.random.seed(2411)
        torch.manual_seed(2411)

        model_ = model
        if isinstance(model, torch.nn.DataParallel):
            model_ = model_.module

        return model_

    def get_datasets(self, stage: str, **kwargs):
        datasets = OrderedDict()

        """
        image_key: 'id'
        label_key: 'attribute_ids'
        """

        image_size = kwargs.get("image_size", 224)
        train_csv = kwargs.get('train_csv', None)
        valid_csv = kwargs.get('valid_csv', None)
        root = kwargs.get('root', None)
        data_csv = kwargs.get('data_csv', None)
        data = kwargs.get('data', '2D')

        if train_csv:
            transform = train_aug(image_size)
            if data == '2D':
                train_set = StructSegTrain2D(
                    csv_file=train_csv,
                    transform=transform,
                )
            else:
                train_set = StructSegTrain3D(
                    csv_file=train_csv,
                    transform=transform,
                    mode='train'
                )
            datasets["train"] = train_set

        if valid_csv:
            transform = valid_aug(image_size)
            if data == '2D':
                valid_set = StructSegTrain2D(
                    csv_file=valid_csv,
                    transform=transform,
                )
            else:
                valid_set = StructSegTrain3D(
                    csv_file=valid_csv,
                    transform=transform,
                    mode='valid'
                )
            datasets["valid"] = valid_set

        return datasets
