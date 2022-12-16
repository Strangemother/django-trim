import shlex, subprocess
import sys


def read_one_stream_command(command):
    """Open a cli command, executing the task waiting for a returncode completion
      Inputs are processed through the pip.

        subprocess.STD_INPUT_HANDLE
            The standard input device. Initially, this is the console input
            buffer, CONIN$.
        subprocess.STD_OUTPUT_HANDLE
            The standard output device. Initially, this is the active console
            screen buffer, CONOUT$.
        subprocess.STD_ERROR_HANDLE
            The standard error device. Initially, this is the active console
            screen buffer, CONOUT$.
        subprocess.SW_HIDE
            Hides the window. Another window will be activated.
        subprocess.STARTF_USESTDHANDLES
            Specifies that the STARTUPINFO.hStdInput, STARTUPINFO.hStdOutput,
            and STARTUPINFO.hStdError attributes contain additional information.
        subprocess.STARTF_USESHOWWINDOW
            Specifies that the STARTUPINFO.wShowWindow attribute contains
            additional information.
        subprocess.CREATE_NEW_CONSOLE
            The new process has a new console, instead of inheriting its
            parent’s console (the default).
        subprocess.CREATE_NEW_PROCESS_GROUP
            A Popen creationflags parameter to specify that a new process
            group will be created. This flag is necessary for using os.kill()
            on the subprocess.
            This flag is ignored if CREATE_NEW_CONSOLE is specified.
        subprocess.ABOVE_NORMAL_PRIORITY_CLASS
            A Popen creationflags parameter to specify that a new process will
            have an above average priority.
        subprocess.BELOW_NORMAL_PRIORITY_CLASS
            A Popen creationflags parameter to specify that a new process will
            have a below average priority.
        subprocess.HIGH_PRIORITY_CLASS
            A Popen creationflags parameter to specify that a new process will
            have a high priority.
        subprocess.IDLE_PRIORITY_CLASS
            A Popen creationflags parameter to specify that a new process will
            have an idle (lowest) priority.
        subprocess.NORMAL_PRIORITY_CLASS
            A Popen creationflags parameter to specify that a new process will
            have an normal priority. (default)
        subprocess.REALTIME_PRIORITY_CLASS
            A Popen creationflags parameter to specify that a new process will
            have realtime priority. You should almost never use
            REALTIME_PRIORITY_CLASS, because this interrupts system threads
            that manage mouse input, keyboard input, and background disk
            flushing. This class can be appropriate for applications that
            “talk” directly to hardware or that perform brief tasks that
            should have limited interruptions.
        subprocess.CREATE_NO_WINDOW
            A Popen creationflags parameter to specify that a new process will
            not create a window.
        subprocess.DETACHED_PROCESS
            A Popen creationflags parameter to specify that a new process will
            not inherit its parent’s console. This value cannot be
            used with CREATE_NEW_CONSOLE.
        subprocess.CREATE_DEFAULT_ERROR_MODE
            A Popen creationflags parameter to specify that a new process does
            not inherit the error mode of the calling process. Instead, the
            new process gets the default error mode. This feature is
            particularly useful for multithreaded shell applications that
            run with hard errors disabled.
        subprocess.CREATE_BREAKAWAY_FROM_JOB
            A Popen creationflags parameter to specify that a new process is
            not associated with the job.
    """
    # si = subprocess.STARTUPINFO()
    flags = 0 # subprocess.DETACHED_PROCESS

    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        creationflags=flags,
        ## not required when processing by read(1)
        # bufsize=1,
        ## Adding universal newlines will evoke _str_ from the `out`
        # universal_newlines=True,
    )

    byte_count = 0
    count = 0
    while True:
        out = process.stdout.read(1)
        if out == '' and process.poll() != None:
            break
        byte_count += 1

        if byte_count > 75_000:
            break

        if len(out) > 0:
            sys.stdout.write(clean(out, ''))
            sys.stdout.flush()
        else:
            count += 1
            if count % 20 == 0:
                print('blanked.')
                break
    return proc_wait(process)


def proc_wait(proc, timeout=10):
    try:
        outs, errs = proc.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        proc.kill()
        outs, errs = proc.communicate()
    return outs, errs


def clean(text, default=None):
    t=text
    if isinstance(text, bytes):
        t = text.decode('utf')
    return default if len(t) == 0 else t
