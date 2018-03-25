import unittest
import io
import wh


class TestWh(unittest.TestCase):

    def test_basic(self):

        @wh.trek()
        def fib(n):
            return fib(n - 2) + fib(n - 1) if n > 2 else 1

        self.assertEqual(fib(10), 55)
        self.assertEqual(fib.ncall, 109)
        self.assertGreater(fib.elapsed, 0)

    def test_write_to_stream(self):
        sio = io.StringIO()

        @wh.trek(sio)
        def fac(n):
            return n * fac(n - 1) if n > 1 else 1

        self.assertEqual(fac(4), 24)
        fac.done()
        self.assertEqual(sio.getvalue()[:17], '[wh] fac: 4 calls')

    def test_done(self):

        @wh.trek()
        def foo():
            return

        foo()
        foo.done()
        self.assertEqual(foo.ncall, 0)
        self.assertEqual(foo.elapsed, 0)

    def test_context(self):

        @wh.trek()
        def foo():
            return 42

        with foo() as ret:
            self.assertEqual(ret, 42)
