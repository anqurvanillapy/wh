import unittest
import io
import wh


class TestWormhole(unittest.TestCase):

    def test_trek(self):

        @wh.trek()
        def fib(n):
            return fib(n - 2) + fib(n - 1) if n > 2 else 1

        self.assertEqual(fib(10), 55)
        self.assertEqual(fib.ncall, 109)
        self.assertGreater(fib.ms, 0)

    def test_write_to_stream(self):
        sio = io.StringIO()

        @wh.trek(sio)
        def fac(n):
            return n * fac(n - 1) if n > 1 else 1

        self.assertEqual(fac(4), 24)
        fac.done()
        sio.seek(0)
        self.assertEqual(sio.read(17), '[wh] fac: 4 calls')
