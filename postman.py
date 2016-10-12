#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""mail sender helper"""


def cli():
    cli_docs = """postman™ ...just another mail sender.

Usage:
  postman  <subject> --mbox=<mail> ... [options] ...

Options:
  --body BODY          body of the mail
  --poster POSTER      mailbox of the sender [default: noresponse@postman.com]
  --attach=<files>     file to attach
  --embed=<files>      file to embed
  --smtp SERVER        smtp server
  --important          Mark mail as important.  [default:false]
  --login LOGIN        user smtp login
  --passwd PASS        user smtp passwd
  --version            show program's version number and exit
  -h, --help           show this help message and exit
  """

    from docopt import docopt, DocoptExit
    from schema import Schema, And, Use, SchemaError, Optional

    schema = Schema({'<subject>': str,
                     '--mbox': [str],
                     '--help': int,
                     '--version': int,
                     Optional('--body'): And([str], lambda n: len(n) <= 1),
                     Optional('--poster'): And([str], lambda n: len(n) == 1),
                     Optional('--attach'):
                     [Use(open, error='attach should be readable')],
                     Optional('--embed'):
                     [Use(open, error='embeded should be readable')],
                     Optional('--smtp'): [str],
                     Optional('--important'): int,
                     Optional('--login'): And([str], lambda n: len(n) <= 1),
                     Optional('--passwd'): And([str], lambda n: len(n) <= 1)})

    args = docopt(cli_docs)
    try:
        schema.validate(args)
    except SchemaError:
        raise DocoptExit

    return None


if __name__ == '__main__':
    cli()
