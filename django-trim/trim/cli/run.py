"""

Experiments:
    res = self.run_poll_command(command)

    res = self.run_command(command)

    subcall_stream(command)

    read_one_stream_command(command)

    gen = self.run_command2(command)
    for line in iter(gen):
        print(line, end='')

Raw method:
    print(res)
    res = subprocess.run(command, shell=True, capture_output=True)
    print('  code: ', res.returncode)
    out = clean(res.stdout)
    err = clean(res.stderr)
    print('  out:  ', out)
    print('  error:', err)
    print(' ', dir(res))

"""
import subprocess
import sys

import pkg_resources


def main():
    print('Inject')

__requires__ = 'trim'
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.exit(
        load_entry_point('django-trim==0.1', 'console_scripts', 'trim')()
    )

def inj():
    # Create the fake entry point definition
    ep = pkg_resources.EntryPoint.parse('dummy = dummy_module:DummyPlugin')

    # Create a fake distribution to insert into the global working_set
    d = pkg_resources.Distribution()

    # Add the mapping to the fake EntryPoint
    d._ep_map = {'console_scripts': {'dummy': ep}}

    # Add the fake distribution to the global working_set
    pkg_resources.working_set.add(d, 'dummy')


def test_entry_point():
    distribution = pkg_resources.Distribution(__file__)
    entry_point = pkg_resources.EntryPoint.parse(
        'plugin1=plugins.plugin1:plugin1_class',
        dist=distribution)
    distribution._ep_map = {'my_project.plugins': {'plugin1': entry_point}}
    pkg_resources.working_set.add(distribution)


def subcall_stream(cmd, fail_on_error=True):
    # Run a shell command, streaming output to STDOUT in real time
    # Expects a list style command, e.g. `["docker", "pull", "ubuntu"]`
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        bufsize=1,
        universal_newlines=True)
    for line in p.stdout:
        sys.stdout.write(line)
    p.wait()


    return exit_code

def read_one_stream_command(command):
    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
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
    # process.wait()

def run_poll_command(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE)
    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            print(clean(output.strip()))
    rc = process.poll()
    return rc

def run_command(command):
    try:

        process = subprocess.Popen(command,
                        stdout=subprocess.PIPE,
                        stdin=subprocess.PIPE,
                        stderr=subprocess.STDOUT,
                        shell=True,
                        encoding='utf8')
        while True:
            inner = True
            pack = ''
            while inner:
                char = process.stdout.readline(1)
                pack += char
                if char == '\n':
                    print(pack, end='')
                if char is None:
                    print(pack)
                inner = False
            print(pack, end='')
            output = process.stdout.readline(64)
            if output == '' and process.poll() is not None:
                print("no output")
                break
            if output:
                print(output.strip())
        rc = process.poll()
        return rc
    except KeyboardInterrupt:
        # process.terminate()
        print('KeyboardInterrupt')

def run_command2(cmd):
    popen = subprocess.Popen(cmd,
            stdout=subprocess.PIPE,
            # stdin=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            shell=True,
            encoding='utf8',
            bufsize=1,
            )
    stdout = popen.stdout
    for stdout_line in iter(stdout.readline, ""):
        yield stdout_line
        stdout.flush()

    stdout.flush()
    popen.stdout.close()
    return_code = popen.wait()
    if return_code:
        raise subprocess.CalledProcessError(return_code, cmd)
    return return_code

if __name__ == '__main__':
    main()
