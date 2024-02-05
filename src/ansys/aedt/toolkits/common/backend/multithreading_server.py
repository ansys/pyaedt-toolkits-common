# Copyright (C) 2023 - 2024 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# -*- coding: utf-8 -*-
import queue
import socket
import socketserver
import threading
import wsgiref.simple_server

# techniques described here are taken from:
# https://gist.github.com/coffeesnake/3093598
# https://bottlepy.org/docs/dev/recipes.html
# https://adamj.eu/tech/2019/05/27/the-simplest-wsgi-middleware/
# https://stackoverflow.com/questions/25155267/how-to-send-a-signal-to-the-main-thread-in-python-without-using-join
# https://en.wikipedia.org/wiki/Callable_object#In_Python

# The contents of this file are copyrighted by their respective owners.


class ThreadingWSGIServer(socketserver.ThreadingMixIn, wsgiref.simple_server.WSGIServer):
    pass


class Invoker:
    def __init__(self, func):
        self._func = func
        self._event = threading.Event()

    def invoke(self):
        self._result = self._func()
        self._event.set()

    def get_result(self):
        self._event.wait()
        return self._result


class SingleThreadResponseExecutor(object):
    def __init__(self, app):
        self._app = app
        self._queue = queue.Queue()

    def __call__(self, environ, start_response):
        invoker = Invoker(lambda: self._app(environ, start_response))
        self._queue.put(invoker)
        return invoker.get_result()

    def execute_responses_on_this_thread(self):
        print("Press ctrl+c to terminate.")
        while True:
            try:
                self._queue.get().invoke()
            except KeyboardInterrupt:
                print("Got keyboard interrupt.")
                break


class MultithreadingServer:
    def run(self, host, port, app):
        executor = SingleThreadResponseExecutor(app)
        server_cls = ThreadingWSGIServer
        if ":" in host:  # Fix wsgiref for IPv6 addresses.
            if getattr(server_cls, "address_family") == socket.AF_INET:

                class server_cls(server_cls):
                    address_family = socket.AF_INET6

        httpd = wsgiref.simple_server.make_server(host, port, app=executor, server_class=server_cls)

        print("Listening on {}:{}.".format(host, port))
        server_thread = threading.Thread(target=httpd.serve_forever)
        # ensure thread dies on termination
        # normally this would be dodgy but this thread doesn't hold anything other than sockets
        # the expectation is that the sockets will get released on process termination
        # - strange if they didn't
        server_thread.daemon = True
        server_thread.start()

        executor.execute_responses_on_this_thread()
