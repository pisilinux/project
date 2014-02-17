# -*- coding: utf-8 -*-
#
# Copyright (C) 2006-2010 TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

"""netfilterutils module provides IPTables configuration utilities."""

import fnmatch
import os


chains = {
    'filter': ['INPUT', 'FORWARD', 'OUTPUT'],
    'mangle': ['PREROUTING', 'INPUT', 'FORWARD', 'OUTPUT', 'POSTROUTING'],
    'nat'   : ['PREROUTING', 'POSTROUTING', 'OUTPUT'],
    'raw'   : ['PREROUTING', 'OUTPUT'],
}


def parseConf(rules_str):
    '''Returns tables and rules from given configuration as a dictionary.'''
    table = ''
    rules = {}
    for rule in rules_str.split('\n'):
        rule = rule.strip()
        if not len(rule) or rule.startswith('#'):
            continue
        if rule.startswith('*'):
            table = rule[1:]
            rules[table] = []
        elif rule.startswith(':'):
            chain, policy, counter = rule[1:].split()
            if chain in chains[table]:
                rules[table].append('-P %s %s' % (chain, policy))
            else:
                rules[table].append('-N %s' % chain)
        elif rule.startswith('-A'):
            rules[table].append(rule)
    return rules


def makeConf(rules_dict):
    '''Makes configuration string from given rule dictionary.'''
    rules = []
    for table in rules_dict:
        if not len(rules_dict[table]):
            continue
        rules.append('*%s' % table)
        for rule in rules_dict[table]:
            rules.append(rule)
        rules.append('COMMIT')
    return '\n'.join(rules) + '\n'


def filterDict(rules_dict, allowed_chains={}):
    '''Filters rule dictionary.'''
    rdict = {}
    for table in rules_dict:
        rdict[table] = []
        if table not in allowed_chains:
            continue
        for rule in rules_dict[table]:
            if not rule.startswith('-A'):
                continue
            chain = rule.split()[1]
            if len(allowed_chains[table]):
                if max(map(lambda x: fnmatch.fnmatch(chain, x), allowed_chains[table])):
                    rdict[table].append(rule)
    return rdict


def diffDict(a, b):
    '''Returns difference of two dictionaries. (non-recursive)'''
    diff = {}
    for table in a:
        if table not in b:
            diff[table] = a[table]
        else:
            diff[table] = list(set(a[table]) - set(b[table]))
    return diff


def restoreRules(rules, flush=True):
    '''Loads given configuration.'''
    opts = ''
    if not flush:
        opts = '--noflush'
    p = os.popen('/sbin/iptables-restore %s' % opts, 'w')
    p.write(rules)
    p.close()


def getRules():
    '''Returns current iptables configuration.'''
    p = os.popen('/sbin/iptables-save', 'r')
    rules = p.read()
    p.close()
    return rules


def clear():
    '''Resets iptables.'''
    for table in chains:
        # Flush rules
        os.popen('/sbin/iptables -t %s -F' % table)
        os.popen('/sbin/iptables -t %s -X' % table)
        # Reset policies
        for chain in chains[table]:
            os.popen('/sbin/iptables -t %s -P %s ACCEPT' % (table, chain))

