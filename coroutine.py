from collections import deque
from time import time, sleep as sys_sleep


class Dispatcher(object):
    """Объект реализующий диспечер событий."""
    def __init__(self):
        self._pending = deque()
        self._deadline = time() + 3600.0

    def setup_timeout(self, corogen, timeout):
        deadline = time() + timeout
        self._deadline = min([self._deadline, deadline])
        self._pending.append([corogen, deadline])
        self._pending = deque(sorted(self._pending, key=lambda a: a[1]))

    def run(self):
        """Запускает цикл обработки событий."""
        while len(self._pending) > 0:
            timeout = self._deadline - time()
            self._deadline = time() + 3600.0
            if timeout > 0:
                sys_sleep(timeout)
            while len(self._pending) > 0:
                if self._pending[0][1] <= time():
                    corogen, _ = self._pending.popleft()
                    try:
                        coroutine._current = corogen
                        corogen.send("timeout")
                    except StopIteration:
                        pass
                    finally:
                        coroutine._current = None
                else:
                    break

dispatcher = Dispatcher()
run = lambda: dispatcher.run()