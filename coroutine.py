def gen_factory():
    state = None
    while True:
        print("state:", state)
        state = yield state

gen = gen_factory()