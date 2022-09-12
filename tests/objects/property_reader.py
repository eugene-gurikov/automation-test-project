import configparser

config = configparser.RawConfigParser()
config.read('tests/config.properties')


def get_prop(prop):
    return config.get('default', prop)
