# wh

*wh*, a wormhole that helps you redirect time and space.  Literally a decorator
for recording the elapsed time and the number of calls for a certain Python
function.

## Usage

* `wh.trek(stream=sys.stdout)`: Decorator for recording the call info, which is
written in `sys.stdout` by default

```py
import wh


@wh.trek()
def fib(n):
    """Fibonacci number"""
    return fib(n - 2) + fib(n - 1) if n > 2 else 1


assert fib(10) == 55
fib.done()  # call info printed to sys.stdout
# Output:
#     [wh] fib: 109 calls, 0.157958984375(ms) elapsed
#


f = open('foo.txt', 'w')


@wh.trek(f)
def fac(n):
    """Factorial"""
    return n * fac(n - 1) if n > 1 else 1


assert fac(4) == 24
fac.done()  # call info logged in foo.txt
f.close()  # context should be managed manually
```

## Install

```bash
$ pip install wh
```

## License

MIT
