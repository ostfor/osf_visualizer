"""
Helping tools

Copyright 2019 Denis Brailovsky, denis.brailovsky@gmail.com

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""


import keras

from osf_visualizer.visdom_visualizer.async.visualization_producer import VisualizationProducer


class KerasVisualizationCallback(keras.callbacks.Callback, VisualizationProducer):
    def __init__(self, items=('loss', 'val_loss', 'iou_score', 'val_iou_score'), experiment_name="Visdom", port=8999,
                 server=None):
        keras.callbacks.Callback.__init__(self)
        VisualizationProducer.__init__(self, items, experiment_name, port, server)

    def on_train_begin(self, logs={}):
        return

    def on_train_end(self, logs={}):
        return

    def on_epoch_begin(self, epoch, logs={}):
        self.epoch = epoch
        print("[*] Start epoch %s" % epoch)
        return
