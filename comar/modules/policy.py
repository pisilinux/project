#!/usr/bin/python
# -*- coding: utf-8 -*-

def check(action_id):
    def decorate(func):
        func.policy_action_id = action_id
        return func
    return decorate
