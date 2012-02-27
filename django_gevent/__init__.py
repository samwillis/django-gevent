__author__ = 'Sam Willis'
__version__ = (0, 1, 0, 'alpha')

def get_version():
    version = '%s.%s' % (__version__[0], __version__[1])
    if __version__[2]:
        version = '%s.%s' % (version, __version__[2])
    if __version__[3] and __version__[3] != 'final':
        version = '%s %s' % (version, __version__[3])
    return version