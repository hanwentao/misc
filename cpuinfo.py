#!/usr/bin/env python
# coding: utf-8
# Wentao Han (wentao.han@gmail.com)

import sys

def read_cpus(path):
    cpus = []
    with open(path) as cpuinfo_file:
        while True:
            cpu = {}
            while True:
                line = cpuinfo_file.readline()
                if not line.rstrip():
                    break
                key, dummy, value = line.partition(':')
                key = key.strip()
                value = value.strip()
                cpu[key] = value
            if cpu:
                cpus.append(cpu)
            if not line:
                break
    return cpus

def count_cpus(cpus):
    stats = {}
    physical_ids = set()
    core_ids_in_first_socket = set()
    first_physical_id = ''
    for cpu in cpus:
        physical_ids.add(cpu['physical id'])
        if not first_physical_id:
            first_physical_id = cpu['physical id']
        if cpu['physical id'] == first_physical_id:
            core_ids_in_first_socket.add(cpu['core id'])
    stats['sockets'] = len(physical_ids)
    stats['cores per socket'] = len(core_ids_in_first_socket)
    return stats

def main(argv=sys.argv[1:]):
    cpus = read_cpus('/proc/cpuinfo')
    stats = count_cpus(cpus)
    print '%s %dx%d' % (cpus[0]['model name'],
                        stats['cores per socket'],
                        stats['sockets'])

if __name__ == '__main__':
    sys.exit(main())
