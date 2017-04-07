import unittest
from noseparallel import ParallelPlugin


class Foo(object):
    def method(self):
        pass

# the test below depends on this name
class Foo2(object):
    def method(self):
        pass


class PluginTest(unittest.TestCase):

    def f(self):
        pass

    def test_want_method_should_accept_on_either_nodes_but_not_both(self):
        plugin = ParallelPlugin()
        plugin.salt = 'test'
        plugin.total_nodes = 2

        plugin.node_index = 0
        rv0 = plugin.wantMethod(Foo.method)

        plugin.node_index = 1
        rv1 = plugin.wantMethod(Foo.method)

        self.assertEqual({None, False}, {rv0, rv1})

        plugin.node_index = 0
        f2_v0 = plugin.wantMethod(Foo2.method)
        plugin.node_index = 1
        f2_v1 = plugin.wantMethod(Foo2.method)
        self.assertEqual({None, False}, {f2_v0, f2_v1})
        # Foo2.method should hash to a different node from Foo.method
        # this depends on the hash function
        self.assertNotEqual(f2_v0, rv0)


    def test_want_function_should_accept_on_either_nodes_but_not_both(self):

        def f():
            pass

        plugin = ParallelPlugin()
        plugin.salt = 'test'
        plugin.total_nodes = 2

        plugin.node_index = 0
        rv0 = plugin.wantFunction(f)

        plugin.node_index = 1
        rv1 = plugin.wantFunction(f)

        self.assertEqual({None, False}, {rv0, rv1})
