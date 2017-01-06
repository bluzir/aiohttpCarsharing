def fibon(n):
    a = b = 1
    for i in range(n):
        yield a
        a, b = b, a + b


def square(n):
    for i in range(n):
        yield i*2


def grep(pattern):
    print("Searching for", pattern)
    while True:
        line = (yield)
        if pattern in line:
            print(line)

search = grep('coroutine')
next(search)
search.send("I love you")
search.send("Don't you love me?")
search.send("I love coroutines instead!")
search.close()