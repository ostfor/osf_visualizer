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

import queue
import socket

import numpy as np

from osf_visualizer.visdom_visualizer.async.visdom_consumer import VisdomConsumer
from osf_visualizer.visdom_visualizer.helpers.visdom_loader import VisdomLoader

CAPACITY = 1000000
VISDOMBAK_TEMPLATE = "/tmp/{}.visdombak"


class VisualizationProducer(object):
    def __init__(self, items=('loss', 'val_loss', 'iou_score', 'val_iou_score'), experiment_name="Visdom", port=8999,
                 server=None, wait_time=None):
        self.__server = server
        self.__port = port
        self.__items = list(items)
        self.__experiment_name = experiment_name
        self.request_queue = queue.Queue(CAPACITY)
        self.should_send_to_visdom = True

        # Visdom name
        if self.__server is None:
            self.__server = socket.gethostname()

        # Service
        self.visdom_reporter = VisdomConsumer(port, self.__server, experiment_name, self.__items,
                                              queue=self.request_queue, wait_time=wait_time)
        self.visdom_reporter.start()

        self.__epoch = 0

        print("Visdom path: http://", self.visdom_url)

    @property
    def visdom_url(self):
        return "{}:{}/env/{}".format(self.__server, self.__port, self.__experiment_name)

    def visdom_checkpoint(self, path=None):
        if path is None:
            path = VISDOMBAK_TEMPLATE.format(self.__experiment_name)

        loader = VisdomLoader(self.visdom_reporter.viz)
        print("Save env {} to {}".format(self.__experiment_name, path))
        loader.create_log_at(path, self.__experiment_name)

    def vis_image(self, images, title="Test"):
        if len(images[0].shape) == 2:
            images = np.expand_dims(np.array(images), 1)
        elif len(images[0].shape) == 3:
            images = np.transpose(np.array(images), (0, 3, 1, 2))
        self.visdom_reporter.viz.images(images,
                                        env=self.visdom_reporter.title,
                                        win=self.visdom_reporter.win + "img",
                                        opts=dict(
                                            title=title,
                                            caption=title + 'Images')
                                        # update='replace')
                                        )

    def on_epoch_end(self, epoch, logs={}):
        iteration = epoch + self.__epoch
        if self.should_send_to_visdom and not self.request_queue.full():
            X = [np.array([iteration]) for _ in range(len(self.__items))]
            Y = [np.array([logs.get(name)]) for name in self.__items]

            self.request_queue.put([
                np.column_stack(X),
                np.column_stack(Y)
            ])

        else:
            self.should_send_to_visdom = False
        return


if __name__ == '__main__':
    for i1 in range(2):
        cb = VisualizationProducer(["loss", "acc"], "Visman{}".format(i1), wait_time=10)
        for i in range(1, 100):
            cb.on_epoch_end(i, {"loss": 1.0 / i, "acc": 0.01 * i})
