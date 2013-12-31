
try:
    from nose.tools import istest
    from nose.tools import nottest
except:
    def istest(func):
        func.__test__ = True
        return func
    def nottest(func):
        func.__test__ = False
        return func

