"""Record elapsed time and number of function calls
"""

import sys
from time import time
from functools import total_ordering


@total_ordering
class _WhContextManager:

    def __init__(self, func, stream):
        self._args = self._kwds = self._val = None
        self._func = func
        self._stream = stream
        self._started = self.ncall = self.elapsed = 0
        self._called = False

    def __call__(self, *args, **kwds):
        if self._called:
            return self._after_call(*args, **kwds)

        self._args = args
        self._kwds = kwds
        self._called = True
        return self

    def _after_call(self, *args, **kwds):
        self._record_start()
        self._val = self._func(*args, **kwds)
        self._record_end()
        return self._val

    def _record_start(self):
        self.ncall += 1
        self._started = time() * 1000

    def _record_end(self):
        self.elapsed += time() * 1000 - self._started

    def __enter__(self):
        self._record_start()
        self._val = self._func(* self._args, ** self._kwds)
        self._record_end()
        return self._val

    def reset(self):
        """Reset for another context"""
        self._called = False
        self.ncall = self.elapsed = 0

    def done(self):
        """Manually indicates task completion to trigger logging and reset"""
        self._stream.write(
            '[wh] {}: {} calls, {}(ms) elapsed\n'.format(
                self._func.__name__, self.ncall, self.elapsed
            )
        )
        self._stream.flush()
        self.reset()

    def __exit__(self, *_):
        self.done()

    def __eq__(self, other):
        if not self._val:
            self.__call__(* self._args, ** self._kwds)
        return self._val == other

    def __lt__(self, other):
        if not self._val:
            self.__call__(* self._args, ** self._kwds)
        return self._val < other


def trek(stream=sys.stdout):
    """wh's decorator with context"""

    def _deco(func):
        return _WhContextManager(func, stream)

    return _deco
