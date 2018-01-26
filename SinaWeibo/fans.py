#!/usr/bin/python
# -*- coding: utf-8 -*-

class Fans(object):
    id = ""
    href = ""
    name = ""

    def __init__(self, id, name, href):
        self.id = id
        self.name = name
        self.href = href

    def __str__(self):
        return "{name:%s,id:%s,href:%s}" % (self.name, self.id, self.href)

    def __repr__(self):
        return "{name:%s,id:%s,href:%s}" % (self.name, self.id, self.href)
