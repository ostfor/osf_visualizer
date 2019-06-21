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


import threading
import time, visdom

import numpy as np


class VisdomConsumer(threading.Thread):
    def __init__(self, port, server, experement_name, items, queue=None, wait_time=None):
        super(VisdomConsumer, self).__init__()
        self.wait_time = wait_time
        self.last_time = None

        self.viz = visdom.Visdom(port=port, server=server)
        self.items = items
        self.title = experement_name

        win = self.viz.line(
            Y=np.column_stack([np.array([0]) for _ in range(len(items))]),
            X=np.column_stack([np.array([0]) for _ in range(len(items))]),
            env=self.title,
            opts=dict(
                title=self.title,
                caption='Metrics',
                xlabel='Iteration',
                ylabel='Value',
                update='append',
                legend=self.items)
        )

        self.win = win
        self.queue = queue

    @property
    def timeout(self):

        if self.wait_time is None:
            return False
        if self.last_time is None:
            self.last_time = time.time()
            return False

        flag = time.time() - self.last_time > self.wait_time
        #print(self.wait_time, flag, time.time() - self.last_time)
        return flag

    def run(self):
        while not self.timeout:
            if not self.queue.empty():
                item = self.queue.get()
                x = item[0]
                y = item[1]
                self.viz.line(
                    X=x,
                    Y=y,
                    win=self.win,
                    update='append',
                    env=self.title,
                )
                self.last_time = time.time()
            else:
                time.sleep(1)