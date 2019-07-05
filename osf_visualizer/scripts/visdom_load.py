#! /usr/bin/env python

import argparse

# SAVING
from osf_visualizer.visdom_visualizer.helpers.visdom_loader import VisdomLoader

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=('Load and Save from Visdom'))
    parser.add_argument('-s', '--save', type=str, help='env_name', default='')
    parser.add_argument('-l', '--load', type=str, help='env_name', default='', nargs="?")
    parser.add_argument('-f', '--file', type=str, help='path_to_log_file', default='')

    parser.add_argument('--server', type=str, default='localhost')
    parser.add_argument('--port', type=int, default=8999)

    args = parser.parse_args()
    loader = VisdomLoader()

    if args.save is not '':
        loader.set_visdom_instance(args.server, args.port, current_env=args.save)
        if args.file is not '':
            loader.create_log_at(args.file, args.save)
        else:
            loader.create_log(args.save)

    if args.load is not '':
        loader.set_visdom_instance(args.server, args.port)
        if args.load == 'all':
            loader.load_all_log()
        elif args.load is not None:
            loader.load_log(args.load)
        elif args.file is not '':
            loader.load_log_at(args.file)
