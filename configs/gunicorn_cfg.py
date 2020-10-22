from multiprocessing import cpu_count
from os import environ


# Ref
# https://github.com/benoitc/gunicorn/blob/master/examples/example_config.py
# https://docs.gunicorn.org/en/stable/settings.html#settings

#
# Server socket
#
#   bind - The socket to bind.
#
#       A string of the form: 'HOST', 'HOST:PORT', 'unix:PATH'.
#       An IP is a valid HOST.
#
#   backlog - The number of pending connections. This refers
#       to the number of clients that can be waiting to be
#       served. Exceeding this number results in the client
#       getting an error when attempting to connect. It should
#       only affect servers under significant load.
#
#       Must be a positive integer. Generally set in the 64-2048
#       range.
#
bind = f"{environ['APP_HOST']}:{environ['APP_PORT']}"
backlog = 1024

# Server mechanics
pidfile = "/var/run/gunicorn_shorten_url.pid"


#
# Worker processes
#
#   workers - The number of worker processes that this server
#       should keep alive for handling requests.
#
#       A positive integer generally in the 2-4 x $(NUM_CORES)
#       range. You'll want to vary this a bit to find the best
#       for your particular application's work load.
#
#   worker_class - The type of workers to use. The default
#       sync class should handle most 'normal' types of work
#       loads. You'll want to read
#       http://docs.gunicorn.org/en/latest/design.html#choosing-a-worker-type
#       for information on when you might want to choose one
#       of the other worker classes.
#
#       A string referring to a Python path to a subclass of
#       gunicorn.workers.base.Worker. The default provided values
#       can be seen at
#       http://docs.gunicorn.org/en/latest/settings.html#worker-class
#
#   worker_connections - For the eventlet and gevent worker classes
#       this limits the maximum number of simultaneous clients that
#       a single process can handle.
#
#       A positive integer generally set to around 1000.
#
#   timeout - If a worker does not notify the master process in this
#       number of seconds it is killed and a new worker is spawned
#       to replace it.
#
#       Generally set to thirty seconds. Only set this noticeably
#       higher if you're sure of the repercussions for sync workers.
#       For the non sync workers it just means that the worker
#       process is still commu
#       of time required to handle a single request.
#
#   keepalive - The number of seconds to wait for the next request
#       on a Keep-Alive HTTP connection.
#
#       A positive integer. Generally set in the 1-5 seconds range.
#
workers = cpu_count()
worker_class = 'gevent'
worker_connections = 500
timeout = 20
keepalive = 2

#
#   Logging
#
# Using '-' for FILE makes gunicorn log to stderr.
errorlog = '-'
# A string of "debug", "info", "warning", "error", "critical"
loglevel = 'info'
# "-" means log to stdout.
accesslog = '-'
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# Server hooks
#
#   post_fork - Called just after a worker has been forked.
#
#       A callable that takes a server and worker instance
#       as arguments.
#
#   pre_fork - Called just prior to forking the worker subprocess.
#
#       A callable that accepts the same arguments as after_fork
#
#   pre_exec - Called just prior to forking off a secondary
#       master process during things like config reloading.
#
#       A callable that takes a server instance as the sole argument.
#


def post_fork(server, worker):
    server.log.info("Worker spawned (pid: %s)", worker.pid)


def pre_fork(server, worker):
    pass


def pre_exec(server):
    server.log.info("Forked child, re-executing.")


def when_ready(server):
    server.log.info("Server is ready. Spawning workers")


# def worker_int(worker):
#     worker.log.info("worker received INT or QUIT signal")

#     ## get traceback info
#     import threading, sys, traceback
#     id2name = {th.ident: th.name for th in threading.enumerate()}
#     code = []
#     for threadId, stack in sys._current_frames().items():
#         code.append("\n# Thread: %s(%d)" % (id2name.get(threadId,""),
#             threadId))
#         for filename, lineno, name, line in traceback.extract_stack(stack):
#             code.append('File: "%s", line %d, in %s' % (filename,
#                 lineno, name))
#             if line:
#                 code.append("  %s" % (line.strip()))
#     worker.log.debug("\n".join(code))


def worker_abort(worker):
    worker.log.info("worker received SIGABRT signal")
