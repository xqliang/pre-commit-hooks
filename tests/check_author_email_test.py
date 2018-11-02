from __future__ import absolute_import
from __future__ import unicode_literals

from pre_commit_hooks.check_author_identity import check_author_identity
from pre_commit_hooks.check_author_identity import main
from pre_commit_hooks.util import cmd_output


def test_valid_identity(temp_git_dir):
    with temp_git_dir.as_cwd():
        cmd_output('git', 'config', '--add', 'user.name', 'test')
        cmd_output('git', 'config', '--add', 'user.email', 'test@example.com')
        assert check_author_identity() == 0


def test_custom_regexp(temp_git_dir):
    with temp_git_dir.as_cwd():
        cmd_output('git', 'config', '--add', 'user.name', 'test')
        cmd_output('git', 'config', '--add', 'user.email', 'test@example.com')
        assert check_author_identity(name_regexp=r'\s+') == 2
        assert check_author_identity(email_regexp=r'^.+@foobar.com$') == 3


def test_not_configured(temp_git_dir, mocker):
    mocker.patch('pre_commit_hooks.check_author_identity.cmd_output', return_value='')
    with temp_git_dir.as_cwd():
        assert check_author_identity() == 1


def test_invalid_name(temp_git_dir):
    with temp_git_dir.as_cwd():
        cmd_output('git', 'config', '--add', 'user.name', '')
        cmd_output('git', 'config', '--add', 'user.email', 'test@example.com')
        assert check_author_identity() == 2


def test_invalid_email(temp_git_dir):
    with temp_git_dir.as_cwd():
        cmd_output('git', 'config', '--add', 'user.name', 'test')
        cmd_output('git', 'config', '--add', 'user.email', 'test')
        assert check_author_identity() == 3


def test_failing_cmdline_email_regexp(temp_git_dir):
    with temp_git_dir.as_cwd():
        cmd_output('git', 'config', '--add', 'user.name', 'test')
        cmd_output('git', 'config', '--add', 'user.email', 'test@example.com')
        rc = main([
            '--email-regexp=.+@foobar.com',
        ])
        assert rc == 3


def test_passing_cmdline_email_regexp(temp_git_dir):
    with temp_git_dir.as_cwd():
        cmd_output('git', 'config', '--add', 'user.name', 'test')
        cmd_output('git', 'config', '--add', 'user.email', 'test@example.com')
        rc = main([
            '--email-regexp=.+@example.com',
        ])
        assert rc == 0


def test_failing_cmdline_name_regexp(temp_git_dir):
    with temp_git_dir.as_cwd():
        cmd_output('git', 'config', '--add', 'user.name', 'test')
        cmd_output('git', 'config', '--add', 'user.email', 'test@example.com')
        rc = main([
            '--name-regexp=[A-Z].+',
        ])
        assert rc == 2


def test_passing_cmdline_name_regexp(temp_git_dir):
    with temp_git_dir.as_cwd():
        cmd_output('git', 'config', '--add', 'user.name', 'Test')
        cmd_output('git', 'config', '--add', 'user.email', 'test@example.com')
        rc = main([
            '--name-regexp=[A-Z].+',
        ])
        assert rc == 0


def test_filenames_ignored(temp_git_dir):
    with temp_git_dir.as_cwd():
        cmd_output('git', 'config', '--add', 'user.name', 'test')
        cmd_output('git', 'config', '--add', 'user.email', 'test@example.com')
        rc = main([
            '.gitignore',
        ])
        assert rc == 0
