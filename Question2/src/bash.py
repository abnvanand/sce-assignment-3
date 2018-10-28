import os
from pwd import getpwuid
from grp import getgrgid
from stat import filemode
from datetime import datetime
from math import log10, ceil


def cd(args):
    if not args or args[0] == '~':
        # switch to home dir
        os.chdir(os.path.expanduser('~'))
    else:
        os.chdir(args[0])


def ls(args):
    """
    Supported flags= -l (long listing)
    :param args:
    :return:
    """
    flags = []
    path = '.'  # default is pwd
    old_pwd = os.getcwd()

    for i in args:
        if i[0] == '-':
            flags.append(i)  # it's a flag
        else:
            path = i  # it's the path to list

    statinfos = []
    w_nlink = w_user = w_group = w_size = 0  # for width of format specifiers of various fields in print

    os.chdir(path)  # if we don't chdir then lstat won't be able to fetch the inode info by entry name

    with os.scandir('.') as it:
        for entry in it:
            if '-l' in flags:
                statinfo = os.lstat(entry.name)
                statinfos.append((statinfo, entry))
                w_nlink = max(w_nlink, ceil(log10(statinfo.st_nlink + 1)))  # +1 to prevent math domain error
                w_size = max(w_size, ceil(log10(statinfo.st_size + 1)))  # since the log of 0 is undefined FIXME: JUGAAD
                w_user = max(w_user, len(getpwuid(statinfo.st_uid).pw_name))
                w_group = max(w_group, len(getgrgid(statinfo.st_gid).gr_name))
            else:
                print(entry.name, end=' ')

    for statinfo, entry in statinfos:
        print("{0} {1:{8}} {2:{9}} {3:{10}} {4:{11}} {5} {6}{7}".format(
            filemode(statinfo.st_mode),
            statinfo.st_nlink,
            getpwuid(statinfo.st_uid).pw_name,
            getgrgid(statinfo.st_gid).gr_name,
            statinfo.st_size,
            datetime.fromtimestamp(statinfo.st_mtime).strftime("%b %d %H:%M"),
            entry.name, "/" if os.path.isdir(entry) else "",
            w_nlink,
            w_user,
            w_group,
            w_size,
        ))

        os.chdir(old_pwd)
    print()


def pwd(args):
    if args:
        print("Too many arguments.")
        exit(1)

    print(os.getcwd())


def touch(args):
    """
    Supported flags -c = do not create any files
    :param args:
    :return:
    """
    files = flags = []
    for arg in args:
        if arg.startswith('-'):
            flags.append(arg)
        else:
            files.append(arg)

    for filename in files:
        if not os.path.isfile(filename) \
                and '-c' in flags:  # if file does not exist and -c (--no-create) option is supplied then do nothing
            continue

        with open(filename, 'a'):
            os.utime(filename, None)


def grep(args):
    """
    Supported flags:
    -n = print line number with output lines
    :param args:
    :return:
    """
    pattern = None
    files = []
    flags = []
    for arg in args:
        if arg.startswith('-'):
            flags.append(arg)
        elif pattern is None:
            pattern = arg
        else:
            files.append(arg)

    # TODO raise exception if files is still empty

    for filename in files:
        with open(filename) as fp:
            for n, line in enumerate(fp):
                if pattern in line:
                    if '-n' in flags:
                        print(n + 1, ":", line, end='')
                    else:
                        print(line, end='')


def head(args):
    """
    Supported flags: -n [-]NUM = number of lines to print
    eg: -n 4 print first 4 lines
    eg: -n -4 print all but last 4 lines
    :param args:
    :return:
    """
    n = 10  # by default head prints first 10 lines
    line_opt = False
    filename = None

    for arg in args:
        if line_opt:
            # lineopt is true means prev arg was -n
            n = int(arg)
            line_opt = False
        elif arg == '-n':
            # if this argument is -n then next argument is the actual number of lines to print
            line_opt = True
        else:
            filename = arg

    if filename is None:
        raise FileNotFoundError("Filename not specified")

    # count total number of lines in the file useful when "-n -[NUM]" is passed as args
    total_num_lines = sum(1 for line in open(filename))

    with open(filename) as fp:
        if n < 0:
            # flag -n -[NUM] means print all but last NUM lines
            n += total_num_lines

        while n > 0:
            line = fp.readline()
            print(line, end='')
            n -= 1


def tail(args):
    """
    Supported flags: -n [+]NUM = number of lines to print
    eg: -n 4 print last 4 lines
    eg: -n +4 print all starting from line number 4
    :param args:
    :return:
    """
    n = 10  # by default tail prints last 10 lines
    line_opt = False
    print_starting_at = False
    filename = None

    for arg in args:
        if line_opt:
            # lineopt is true means prev arg was -n
            n = int(arg)
            line_opt = False
            print_starting_at = arg.startswith('+')
        elif arg == '-n':
            # if this argument is -n then next argument is the actual number of lines to print
            line_opt = True
        else:
            filename = arg

    if filename is None:
        raise FileNotFoundError("Filename not specified")

    # count total number of lines in the file
    total_num_lines = sum(1 for line in open(filename))

    with open(filename) as fp:
        if print_starting_at:  # print starting at nth line
            skips = n - 1  # i.e., skip n-1 lines
        else:  # print last n lines
            skips = total_num_lines - n  # eg tota_lines = 100 , n=10 => skip 90 lines

        while skips > 0:
            fp.readline()
            skips -= 1

        for line in fp:
            print(line, end='')


def sed(args):
    pass


def tr(args):
    pass


def diff(args):
    pass


commands = {"cd": cd,
            "ls": ls,
            "pwd": pwd,
            "touch": touch,
            "grep": grep,
            "head": head,
            "tail": tail,
            "tr": tr,
            "sed": sed,
            "diff": diff}


def run(command, *args):
    # print("Command: ", command)
    # print("Args: ", args)

    if command in commands:
        commands[command](args)
    else:
        print("Invalid command:", command)
        exit(1)
