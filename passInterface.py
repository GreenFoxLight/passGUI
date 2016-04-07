#!/bin/python

import os
from subprocess import Popen
from subprocess import PIPE

"""
pass interface

This module is responsible for calling "pass"
and parsing the provided output
"""

def _call_pass_native(args = []):
    BUFSIZE = 4096
    cmd = ["pass"]
    for arg in args:
        cmd.append(arg)
    try:
        pipe = Popen(cmd, bufsize=BUFSIZE, stdout=PIPE).stdout
        out = pipe.read()
        pipe.close()
        return out
    except FileNotFoundError:
        return None

def _call_pass(args = []):
    native = _call_pass_native(args)
    if native == None:
        return None
    out = ""
    for code in native:
        out += chr(code)
    return out

def _get_version():
    out = _call_pass(["version"])
    if out == None:
        return None
    # search for string "v<number>.<number>.<number>"
    in_version = False
    version = ""
    for c in out:
        if c == 'v':
            in_version = True
            continue
        elif not in_version:
            continue
        if str(c).isdigit() or c == '.':
            version += str(c)
        else:
            if version != "":
                return version
            else:
                version = ""
                in_version = False
    return None

def _check_version():
    version = _get_version()
    if version == None:
        return False
    elif version.startswith("1.6"):
        return True
    return False

def _get_sub_dirs(d):
    try:
        return [name for name in os.listdir(d)
                if os.path.isdir(os.path.join(d, name))]
    except FileNotFoundError:
        return []

def _get_files(d):
    try:
        return [name for name in os.listdir(d)
                if not os.path.isdir(os.path.join(d, name))]
    except FileNotFoundError:
        return []

def get_passwords(root):
    passwords = []
    __check_pass_dir(root, passwords)
    for i in range(len(passwords)):
        passwords[i] = passwords[i][len(root)+1:len(passwords[i])-4]
    return passwords

def get_password(p):
    out = _call_pass([p])
    return out

def __check_pass_dir(path, passwords):
    sub_dirs = _get_sub_dirs(path)
    files = _get_files(path)
    for f in files:
        if f.endswith(".gpg"):
            passwords.append(path + "/" + f)
    for d in sub_dirs:
        __check_pass_dir(os.path.join(path, d), passwords)

if __name__ == '__main__':
    if not _check_version():
        print("The installed version of pass is not supported")
    get_passwords("/home/gfl/.password-store")
    print(get_password("web/foo"))
