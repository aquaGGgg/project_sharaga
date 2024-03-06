from typing import Callable
import time

from colorama import Fore, init

init()

class ViewTimerMiddleware:
    def __init__(self, get_response: Callable):
        self.get_response = get_response
        self.view_timer = 0.0

    def __call__(self, request, *args, **kwargs):

        #before response
        start_time = time.monotonic()

        response = self.get_response(request, *args, **kwargs)
        # after response

        end_time = time.monotonic()
        self.view_timer = round(end_time - start_time, 4)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):

        if 0 <= self.view_timer < 0.18:
            print(Fore.GREEN + f"{view_func.__name__} processing time {round(self.view_timer, 3)} sec")
        elif 0 < self.view_timer < 0.3:
            print(Fore.YELLOW + f"{view_func.__name__} processing time {round(self.view_timer, 3)} sec")
        else:
            print(Fore.RED + f"{view_func.__name__} processing time {round(self.view_timer, 3)} sec")

