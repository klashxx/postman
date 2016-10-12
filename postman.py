#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""mail sender helper"""
from __future__ import print_function

def postman(mboxes,
            subject,
            body=None,
            attach=None,
            embed=None,
            poster='noresponse@postman.org',
            smtp_servers=None,
            important=False,
            login=None,
            passwd=None,
            logger=None):

    args = locals()
    import os
    import re
    import logging

    if not isinstance(logger, logging.Logger):
        logger = logging.getLogger('postman')
        logger.setLevel(logging.DEBUG)
        loghndl = logging.StreamHandler()
        loghndl.setFormatter(logging.Formatter('%(levelname)s - %(message)s'))
        logger.addHandler(loghndl)

    logger.debug(args)

    if not subject:
        subject = 'No subject'

    if not isinstance(str if mboxes is None else mboxes, list):
        raise ValueError('mailboxes are needed!')

    mregex = (r'^[_a-z0-9-]+(\.[_a-z0-9-]+)*@'
               '[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$')

    mboxes = [mbox for mbox in mboxes if re.match(mregex, mbox)]
    logger.debug('valid regex boxes: {0}'.format(str(mboxes)))
    if not mboxes:
        raise ValueError('No valid boxes!')

    try:
        import dns.resolver
    except ImportError:
        pass
    else:
        valid_dns = []
        for domain in list(set([mbox.split('@')[1] for mbox in mboxes])):
            try:
                dns.resolver.query(domain, 'MX')
            except Exception as error:
                logger.error('BAD domain [{0}]: {1}'.format(domain, error))
            else:
                valid_dns.append(domain)
                logger.debug('Valid box domain: {0}'.format(domain))

        if not valid_dns:
            raise ValueError('No valid domains!')

        mboxes = [mbox for mbox in mboxes if mbox.split('@')[1] in valid_dns]
        if not mboxes:
            raise ValueError('No valid domains in remaining boxes!')

    if attach is None:
        attach = []
    elif not isinstance(attach, list):
        raise ValueError('attachments should be in list')

    if embed is None:
        embed = []
    elif not isinstance(embed, list):
        raise ValueError('embedments should be in list')

    if isinstance(poster, list):
        if len(poster) > 1:
            raise ValueError('Just one poster, please')
        poster = poster[0]

    if not smtp_servers:
        smtp_servers = [os.environ.get('SMTP_SERVER')]
        if smtp_servers[0] is None:
            raise ValueError('No smtp server specified')
    elif not isinstance(smtp_servers, list):
        raise ValueError('smtp servers should be in list')

    import csv
    import time
    import socket
    import smtplib
    import mimetypes
    from email import encoders
    from email.mime.base import MIMEBase
    from email.mime.text import MIMEText
    from email.mime.image import MIMEImage
    from email.mime.multipart import MIMEMultipart
    from email.utils import formatdate

    try:
        host = socket.gethostname()
    except:
        host = 'Unknown'

    msg = MIMEMultipart('mixed')
    msg['Subject'] = '[{0}][{1}] {2}'.format(time.strftime('%Y%m%d-%H%M%S'),
                                             host,
                                             subject)
    msg['From'] = poster
    msg['To'] = ','.join(mboxes)
    if important:
        msg['X-Priority'] = '1'
        msg['X-MSMail-Priority'] = 'High'
    msg['X-Generated-By'] = host
    msg['Date'] = formatdate(localtime=True)

    return None

def cli():
    cli_docs = """postman™ ...just another mail sender.

Usage:
  postman  <subject> --mbox=<mail> ... [options] ...

Options:
  --body BODY          body of the mail
  --poster POSTER      mailbox of the sender [default: noresponse@postman.org]
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

    postman(args['--mbox'],
            args['<subject>'],
            body=args['--body'],
            attach=args['--attach'],
            embed=args['--embed'],
            poster=args['--poster'],
            smtp_servers=args['--smtp'],
            important=args['--important'],
            login=args['--login'],
            passwd=args['--passwd'])

    return None


if __name__ == '__main__':
    cli()
