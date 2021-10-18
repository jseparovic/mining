#!/usr/bin/python

from sys import argv, exit
import re
from time import sleep
import os


LOG = '/var/log/miner/t-rex/t-rex.log'


clear = lambda: os.system('clear')


# 7-bit C1 ANSI sequences
ansi_escape = re.compile(r'''
    \x1B  # ESC
    (?:   # 7-bit C1 Fe (except CSI)
        [@-Z\\-_]
    |     # or [ for CSI, followed by a control sequence
        \[
        [0-?]*  # Parameter bytes
        [ -/]*  # Intermediate bytes
        [@-~]   # Final byte
    )
''', re.VERBOSE)


def average(lst):
    return sum(lst) / len(lst)


def get_mhs(value, unit):
    if unit == "MH/s":
        return float(value)
    elif unit == "GH/s":
        return float(value) * 1000


def get_t_rate():
    summary_blocks = {}

    with open(LOG) as f:
        lines = [line.rstrip() for line in f]

    address = None

    for line in lines:
        _line = ansi_escape.sub('', line)
        if 'Mining at' in _line:
            # New summary block
            count = 0
            address, diff = _line.split(',')
            address = address.replace('Mining at ', '')
            if not summary_blocks.get(address):
                summary_blocks[address] = []

        if address and 'GPU' in _line:
            count += 1

        if address and 'Hashrate' in _line:
            hashrate, shares_min, avg_p, acg_e = _line.split(',')
            hashrate = hashrate.replace('Hashrate: ', '')
            value, unit = hashrate.split(' ')
            hashrate_mhs = get_mhs(value, unit)
            average_mhs = hashrate_mhs / count
            summary_blocks[address].append(average_mhs)

    return summary_blocks


def parse_url_for_coin(url):
    if 'eth' in url:
        return 'ETH'
    elif 'erg' in url:
        return 'ERG'
    elif 'rvn' in url:
        return 'RVN'
    else:
        return url


def get_t_rate_summary():
    result = []
    t_rates = get_t_rate()

    for key in t_rates.keys():
        result.append({parse_url_for_coin(key): round(average(t_rates[key]), 2)})

    return result


if __name__ == "__main__":
    hostname = os.popen('hostname').read().rstrip()
    value = get_t_rate_summary()
    print("%s" % ({hostname: value}))

