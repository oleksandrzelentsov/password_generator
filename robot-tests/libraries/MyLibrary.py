from robot.api.deco import keyword


class MyLibrary(object):
    @keyword('A ${string:.+} B')
    def a(self, string):
        print str.format('hello, {}', string)
