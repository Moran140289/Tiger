

class A(object):
    @classmethod
    def init_list_a(cls, val):
        cls.ani = [val]

    @classmethod
    def print_list_a(cls, val):
        cls.init_list_a(val=4)
        print(cls.ani)

if __name__ == '__Main__':
    A.print_list_a()