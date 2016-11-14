#!/usr/bin/env python

import argparse
import json
import os

from getMemoryAllocation import MemoryAllocation


# Get config from json file
def get_config_from_file(filename):
    with open(filename) as config_file:
        return json.load(config_file)


def main():
    parser = argparse.ArgumentParser(description='Gets various stats from VCD.')
    parser.add_argument("-v", "--verbose", action="count", default=0,
                        help="Increase verbosity of the output")
    parser.add_argument("-c", "--config", default=os.path.dirname(os.path.abspath(__file__)) + os.sep + 'getMemoryAllocation.cfg',
                        help="Please provide full path to configfile")
    args = parser.parse_args()

    config = get_config_from_file(args.config)
    # Get memory allocation from specified vdc (virtual data center) in vcd (virtual cloud director)
    MemoryAllocation(args.verbose, config['base_url'], config['user'], config['password'],
                     config['organization'], config['headers'], config['url_filter'])


if __name__ == '__main__':
    main()
