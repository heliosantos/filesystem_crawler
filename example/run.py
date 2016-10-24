import sys
import os
import argparse

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from filesystem_crawler import FilesystemCrawler
from filesystem_crawler import parse_match_rules_from_file


def main():
    args = parse_arguments()
    basedirPath, matchesPath = parse_config_paths(args)

    matchrules, errors = parse_match_rules_from_file(basedirPath, matchesPath)

    print("\n[Match Rules]")
    for rule in matchrules:
        print('{type} {polarity} {pattern}'.format(
              type='d' if rule.dirsOnly else 'f' if rule.filesOnly else ' ',
              polarity='+' if rule.polarity else '-',
              pattern=rule.pattern.pattern), end='')

        print('' if rule.contentPattern is None else
              " containing '%s'" % rule.contentPattern)

    if errors:
        print("\n[Match Errors]")
        for line, error in errors:
            print('Line {line}: {error}'.format(
                line=str(line), error=str(error)))

    crawler = FilesystemCrawler(matchrules)
    matchedPaths = crawler.search(basedirPath, True)

    for path in matchedPaths:
        print(path)

    print('\n{} matches'.format(len(matchedPaths)))


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--conf_dir',
                        help='the directory with the configuration files')
    args = parser.parse_args()
    return args


def parse_config_paths(args):
    confDir = (os.path.dirname(os.path.realpath(__file__)) if
               args.conf_dir is None else args.conf_dir)

    basedirLocationPath = os.path.join(confDir, 'FilesystemCrawler.basedir')
    matchesPath = os.path.join(confDir, 'FilesystemCrawler.matches')

    basedir = confDir
    if os.path.isfile(basedirLocationPath):
        with open(basedirLocationPath) as f:
            basedir = f.read().strip()

    return basedir, matchesPath


if __name__ == '__main__':
    main()
