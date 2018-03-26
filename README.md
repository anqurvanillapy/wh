# wh

*wh*, a wormhole that helps you redirect time and space.  Literally a decorator
for recording the elapsed time and the number of calls for a certain Python
function.

**Notes**: It brings *slight overheads* including additional function calls
(e.g. incrementing time) and branches (e.g. for tweaking the context).  Don't
mess with tiny little stubs or highly precise benchmarks with this module.

## Usage

### Methods

* `wh.trek(stream=sys.stdout)`: Decorator for recording the call info, which is
logged in `sys.stdout` by default.  Returns an instance of `_WhContextManager`
* `_WhContextManager.reset()`: Manually resets states for next contexts
* `_WhContextManager.done()`: Manually finishes the task and starts logging and
`self.reset()`-ting

### Attributes

* `_WhContextManager.ncall`: Number of calls
* `_WhContextManager.elapsed`: Elapsed time
* `_WhContextManager.retval`: Return value of the function.  If it is not even
called before, `TypeError` would be raised (e.g. `foo().retval` instead of
`foo.retval` right after `foo`'s declaration)

### Example

```py
import wh


@wh.trek()
def fib(n):
    """Fibonacci number"""
    return fib(n - 2) + fib(n - 1) if n > 2 else 1


# No benchmark output.
assert fib(10) == 55
fib.reset()  # reset for a next call


# Output triggered by `with`.
with fib(10) as ret:
    assert ret == 55
# Output:
#     [wh] fib: 109 calls, 0.157958984375(ms) elapsed
#


# File I/O.
f = open('foo.txt', 'w')


@wh.trek(f)
def fac(n):
    """Factorial"""
    return n * fac(n - 1) if n > 1 else 1


assert fac(4) == 24
fac.done() # manually writes to file
f.close()  # context should be managed manually
```

## Install

```bash
$ pip install wh
```

## License

MIT
