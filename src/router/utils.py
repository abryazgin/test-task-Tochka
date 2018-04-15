from flask import request, abort


def get_arg(name, type_, default=None, required=False):
    arg = request.args.get(name, type=type_, default=default)
    if required and arg is None:
        abort(400, 'Parameter `{}` required'.format(name))
    return arg
