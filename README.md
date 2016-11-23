## What is postman?

_**postman™**_ is a `python` *script* that can also be used as a *module*.

## What is its purpose?

Send emails *programmatically*, not more not less.

## Can I add attachments?

Sure.

## What about authentication?

**Currently** only *user* - *password* method is implemented **but** you can pass these values via `SMTP_LOGIN` and `SMTP_PASS` *environment variables*.

:warning: **NOTE**: To use `smtp.gmail.com` you must enable [less secure apps](https://www.google.com/settings/security/lesssecureapps).

## Tell me about the installation

Easy, *clone* it:

`git clone https://github.com/klashxx/postman.git `

Then `pip`:

`pip install postman`

If you just need an *upgrade*:

`pip install postman --upgrade`

## Ok, how does this thing works?

### As a script:

```
$ postman 
Usage:
  postman  <subject> --mbox=<mail> ... [options] ...
```

```
$ postman -h
postman™ ...just another mail sender.

Usage:
  postman  <subject> --mbox=<mail> ... [options] ...

Options:
  --body BODY          body of the mail
  --poster POSTER      mailbox of the sender [default: noreply@postman.org]
  --attach=<files>     file to attach
  --embed=<files>      file to embed
  --smtp SERVER:PORT   smtp server
  --important          Mark mail as important.  [default:false]
  --login LOGIN        user smtp login
  --passwd PASS        user smtp passwd
  --version            show program's version number and exit
  -h, --help           show this help message and exit
```

#### Examples

```
$ SMTP_LOGIN=usertest \
> SMTP_PASS=345j2u3vxvHH98ym8Oxc2 \
> postman "Just a test" --mbox=usertest@gmail.com --smtp=smtp.gmail.com:587
DEBUG - {'body': [], 'passwd': [], 'poster': ['noreply@postman.org'], 'smtp_servers': ['smtp.gmail.com:587'], 'attach': [], 'mboxes': ['usertest@gmail.com'], 'important': 0, 'embed': [], 'logger': None, 'login': [], 'subject': 'Just a test'}
DEBUG - valid regex boxes: ['usertest@gmail.com']
DEBUG - smtp_connection ok: smtp.gmail.com
INFO - postman™ successful

```

### As a module:

```
>>> from postman import postman
>>> help(postman)
Help on function postman in module postman:

postman(mboxes, subject, body=None, attach=None, embed=None, poster='noreply@postman.org', smtp_servers=None, important=False, login=None, passwd=None, logger=None)
    postman™: the email sender.
    
    Args:
        mboxes (list): list of recipients.
        subject (str): subject of the mail.
        body  (str): body text of the email (could be html).
        attach (list|optional): list of files to be attached.
        embed (list|optional): list of images to be embedded.
        poster (str|optional):  address of the email sender.
        smtp_servers (list|optional): list of smtp servers senders. Could be 
         passed via `SMTP_SERVER` env var.
        important (bool|optional): to flag the message as important.
        login (str|optional): login value on smtp server. Could be passed via
         `SMTP_LOGIN` env var.
        passwd (str|optional): passwd value on smtp server. Could be passed via
         `SMTP_PASS` env var.
        logger (logging.Logger|optional): logger to attach.
    
    Returns:
        None
```

```
$ SMTP_LOGIN=usertest SMTP_PASS=345j2u3vxvHH98ym8Oxc2 python
Python 2.7.10 (default, Jul 30 2016, 18:31:42) 
[GCC 4.2.1 Compatible Apple LLVM 8.0.0 (clang-800.0.34)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> from postman import postman
>>> postman(['usertest@gmail.com'], 'Just a test', smtp_servers=['smtp.gmail.com:587'])
DEBUG - {'body': None, 'passwd': None, 'poster': 'noreply@postman.org', 'smtp_servers': ['smtp.gmail.com:587'], 'attach': None, 'mboxes': ['usertest@gmail.com'], 'important': False, 'embed': None, 'logger': None, 'login': None, 'subject': 'Just a test'}
DEBUG - valid regex boxes: ['usertest@gmail.com']
DEBUG - smtp_connection ok: smtp.gmail.com
INFO - postman™ successful
```
