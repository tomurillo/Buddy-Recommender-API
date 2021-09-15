# -*- coding: utf-8 -*-
"""
    buddy-recommender.helpers
    ~~~~~~~~~~~~~~~~
    Helpers module
    https://github.com/mattupstate/overholt/blob/master/overholt/helpers.py
"""

import pkgutil
import importlib

from flask import Blueprint
from flask.json import JSONEncoder as BaseJSONEncoder


def register_blueprints(app, package_name, package_path):
    """
    Register all Blueprint instances on the specified Flask application found
    in all modules for the specified package.
    :param app: the Flask application
    :param package_name: the package name
    :param package_path: the package path
    """
    rv = []
    for _, name, _ in pkgutil.iter_modules(package_path):
        m = importlib.import_module('{}.{}'.format(package_name, name))
        for item in dir(m):
            item = getattr(m, item)
            if isinstance(item, Blueprint):
                app.register_blueprint(item)
            rv.append(item)
    return rv


class JSONEncoder(BaseJSONEncoder):
    """
    Custom :class:`JSONEncoder` which respects objects that include the
    :class:`JsonSerializer` mixin.
    """
    def default(self, obj):
        if isinstance(obj, JsonSerializer):
            return obj.to_json()
        return super(JSONEncoder, self).default(obj)


class JsonSerializer(object):
    """
    Mixing for marking a SQLAlchemy model class that implements a
    :func:`to_json` method.
    """

    __json_public__ = None
    __json_hidden__ = None
    __json_modifiers__ = None

    def get_field_names(self):
        for p in self.__mapper__.iterate_properties:
            yield p.key

    def to_json(self):
        field_names = self.get_field_names()

        public = self.__json_public__ or field_names
        hidden = self.__json_hidden__ or []
        modifiers = self.__json_modifiers__ or dict()

        rv = dict()
        for key in public:
            rv[key] = getattr(self, key)
        for key, modifier in modifiers.items():
            value = getattr(self, key)
            rv[key] = modifier(value, self)
        for key in hidden:
            rv.pop(key, None)
        return rv
