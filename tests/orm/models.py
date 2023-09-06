# -*- coding: utf-8 -*-

from stoobly_orator.orm import Model


class User(Model):

    __fillable__ = ["name"]
