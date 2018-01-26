#!/usr/bin/python
# -*- coding: utf-8 -*-

class Blog(object):
    id = ""
    text = ""
    date = ""

    def __init__(self, id, text, date):
        self.id = id
        self.text = text
        self.date = date

    def __str__(self):
        return "{id:%s,text:%s,date:%s}" % (self.id, self.text, self.date)

    def __repr__(self):
        return "{id:%s,text:%s,date:%s}" % (self.id, self.text, self.date)