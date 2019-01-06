from PIL import Image
import torch
import torchvision.transforms as transforms

import sys
sys.path.append('.')
import pretrainedmodels
import pretrainedmodels.utils as utils

class Tagger:
    def __init__(self, arch, batch_size=128, workers=16):
        self.arch = arch
        self.model = pretrainedmodels.__dict__[arch](num_classes=1000, pretrained='imagenet')
        self.model.eval()
        self.tf = utils.TransformImage(self.model)

        # Load Imagenet Synsets
        with open('data/imagenet_synsets.txt', 'r') as f:
            self.synsets = f.readlines()

    def process(self, target_dir):
        loader = torch.utils.data.DataLoader(datasets.ImageFolder(target_dir, self.tf),
                                             batch_size=batch_size,
                                             shuffle=False,
                                             num_workers=workers,
                                             pin_memory=True)


        # len(synsets)==1001
        # sysnets[0] == background
        synsets = [x.strip() for x in synsets]
        splits = [line.split(' ') for line in synsets]
        key_to_classname = {spl[0]:' '.join(spl[1:]) for spl in splits}

        with open('data/imagenet_classes.txt', 'r') as f:
            class_id_to_key = f.readlines()

        class_id_to_key = [x.strip() for x in class_id_to_key]

        # Make predictions
        output = model(input) # size(1, 1000)
        max, argmax = output.data.squeeze().max(0)
        class_id = argmax[0]
        class_key = class_id_to_key[class_id]
        classname = key_to_classname[class_key]

        print("'{}': '{}' is a '{}'".format(arch, path_img, classname))
