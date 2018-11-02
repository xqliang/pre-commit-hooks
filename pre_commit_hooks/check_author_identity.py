from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import argparse
import re

from pre_commit_hooks.util import cmd_output


DEFAULT_NAME_REGEXP = r'.+'
DEFAULT_EMAIL_REGEXP = r'^.+@[a-zA-Z0-9-_]+\.[a-zA-Z0-9-_.]+$'


def check_author_identity(
    name_regexp=DEFAULT_NAME_REGEXP,
    email_regexp=DEFAULT_EMAIL_REGEXP,
):
    name = cmd_output('git', 'config', '--get', 'user.name')
    email = cmd_output('git', 'config', '--get', 'user.email')

    retv = 0
    if not name or not email:
        print ('''name or email not configured!

Use the commands:
    git config --global user.name "Your Name"
    git config --global user.email "you@yourdomain.com"
to introduce yourself to Git before committing.
''')
        retv = 1
    elif not re.match(name_regexp, name):
        print ('User name %r not match %r' % (name, name_regexp))
        retv = 2
    elif not re.match(email_regexp, email):
        print ('User email %r not match %r' % (email, email_regexp))
        retv = 3

    return retv


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--name-regexp', default=DEFAULT_NAME_REGEXP,
        help='Allowed user name pattern.',
    )
    parser.add_argument(
        '--email-regexp', default=DEFAULT_EMAIL_REGEXP,
        help='Allowed user email pattern.',
    )
    parser.add_argument('filenames', nargs='*', help='Filenames ingored')

    args = parser.parse_args(argv)
    return check_author_identity(args.name_regexp, args.email_regexp)


if __name__ == '__main__':
    exit(main())
