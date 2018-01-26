#!/usr/bin/python
# -*- coding: utf-8 -*-
from enum import Enum

class FollowType(Enum):
    ORG = 1
    USER = 2

class Follow(object):
    followType = None
    id = ""
    name = ""
    href = ""

    def __init__(self,followType,id,name,href):
        assert type(followType) == type(FollowType.ORG)

        self.followType = followType
        self.id = id
        self.name = name
        self.href = href

    def __str__(self):
        return "{name:%s,id:%s,href:%s,type:%s}" % (self.name, self.id, self.href, str(self.followType))
    def __repr__(self):
        return "{name:%s,id:%s,href:%s,type:%s}" % (self.name, self.id, self.href, str(self.followType))

