import unittest

import numpy as np

import chainer
import chainer.functions as F
import chainer.links as L
import onnx_chainer
from onnx_chainer.testing import test_mxnet
import chainercv.links as C


class TestLeNet5(unittest.TestCase):

    def setUp(self):
        self.model = chainer.Sequential(
            L.Convolution2D(None, 16, 5, 1, 2),
            F.relu,
            L.Convolution2D(16, 8, 5, 1, 2),
            F.relu,
            L.Convolution2D(8, 5, 5, 1, 2),
            F.relu,
            L.Linear(None, 100),
            F.relu,
            L.Linear(100, 10)
        )
        self.x = np.zeros((1, 3, 28, 28), dtype=np.float32)
        self.fn = 'LeNet5.onnx'

    def test_compatibility(self):
        test_mxnet.check_compatibility(self.model, self.x, self.fn)


class TestVGG16(unittest.TestCase):

    def setUp(self):
        self.model = C.VGG16(
            pretrained_model=None, initialW=chainer.initializers.Uniform(1))
        self.x = np.zeros((1, 3, 224, 224), dtype=np.float32)
        self.fn = 'VGG16.onnx'

    def test_compatibility(self):
        test_mxnet.check_compatibility(self.model, self.x, self.fn)


class TestResNet50(unittest.TestCase):

    def setUp(self):
        self.model = C.ResNet50(
            pretrained_model=None, initialW=chainer.initializers.Uniform(1), arch='he')
        self.model.pool1 = lambda x: F.max_pooling_2d(x, ksize=3, stride=2, cover_all=False)
        self.x = np.zeros((1, 3, 224, 224), dtype=np.float32)
        self.fn = 'ResNet50.onnx'

    def test_compatibility(self):
        test_mxnet.check_compatibility(self.model, self.x, self.fn)
