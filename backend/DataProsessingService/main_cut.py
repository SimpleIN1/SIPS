import conf
from loader.cut_by_contour import cut_by_contour
import sys


def main():
    size_cut = None
    if len(sys.argv) > 0:
        size_cut = int(sys.argv[1])

    path = conf.PATH_TO_CUTTING_FILES
    with open(path, 'r') as f:
        for item in f.readlines():
            src, dst = item.split(' ')
            dst = str(dst).strip('\n')
            cut_by_contour(src, dst, size_cut or 500)


if __name__ == '__main__':
    main()
