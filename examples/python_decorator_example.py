# Simple decorator example
def test_decorator(decorated_function):
    def decorator_wrapper():
        print("Simple decorator started")
        decorated_function()
        print("Simple decorator finished")
    return decorator_wrapper


@test_decorator
def test_function():
    print("Code of a function")


# Coroutine decorator example
def coroutine_decorator(decorated_function):
    def decorator_wrapper(*args,**kwargs):
        print('Coroutine decorator started')
        gen = decorated_function(*args,**kwargs)
        gen.send(None)
        print('Coroutine decorator finiched')
        return gen
    return decorator_wrapper


@coroutine_decorator
def another_test_function():
    history = []
    while True:
        x, y = (yield)
        if x == 'h':
            print (history)
            continue
        result = x + y
        print (result)
        history.append(result)


s = test_function()
c = another_test_function()

print(type(s), type(c))