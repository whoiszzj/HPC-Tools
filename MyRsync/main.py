import os
import argparse
from sys import exit

env_dist = os.environ
HOME = env_dist.get('HOME')
CWD = os.getcwd()

parser = argparse.ArgumentParser(description='This is a rsync tool')
parser.add_argument('-s', '--source', default=CWD, help='source root directory')
parser.add_argument('-d', '--destination', default='/groups/g4800000' + CWD, help='destination root directory')
parser.add_argument('-m', '--mode', default='push', choices=['push', 'pull'], help='push or pull')
parser.add_argument('-c', type=str, nargs='+', default=None, help='the content to be rsynced')

args = parser.parse_args()

if __name__ == '__main__':
    if args.c is None:
        exit(0)
    if args.mode == 'push':
        for c in args.c:
            src_path = os.path.join(args.source, c)
            if not os.path.exists(src_path):
                print('path %s not exists' % src_path)
                continue
            dst_path = os.path.join(args.destination, c)
            # if dst_path's parent directory not exists, create it
            if not os.path.exists(os.path.dirname(dst_path)):
                print('\033[1;31mPath %s not exists, make it\033[0m' % os.path.dirname(dst_path))
                os.makedirs(os.path.dirname(dst_path))
            if not os.path.isdir(src_path):
                print('\033[1;32mCopy file\033[0m:', src_path, '->', dst_path)
                os.system('rsync %s %s' % (src_path, dst_path))
            else:
                print('\033[1;34mRsync directory\033[0m:', src_path, '->', dst_path)
                os.system('rsync -aqu --progress %s/ %s/' % (src_path, dst_path))
    elif args.mode == 'pull':
        for c in args.c:
            src_path = os.path.join(args.destination, c)
            if not os.path.exists(src_path):
                print('path %s not exists' % src_path)
                continue
            dst_path = os.path.join(args.source, c)
            # if dst_path's parent directory not exists, create it
            if not os.path.exists(os.path.dirname(dst_path)):
                print('\033[1;31mPath %s not exists, make it\033[0m' % os.path.dirname(dst_path))
                os.makedirs(os.path.dirname(dst_path))
            if not os.path.isdir(src_path):
                print('\033[1;32mCopy file\033[0m:', src_path, '->', dst_path)
                os.system('rsync %s %s' % (src_path, dst_path))
            else:
                print('\033[1;34mRsync directory\033[0m:', src_path, '->', dst_path)
                os.system('rsync -aqu --progress %s/ %s/' % (src_path, dst_path))
    else:
        print('mode error')

