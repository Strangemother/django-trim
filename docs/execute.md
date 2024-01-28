# Execute

> Performing a subprocess command can be tricky. `trim.read_one_stream_command` assists with executing a `subprocess.Popen`. It provides a flushing pipe for free, to correctly read streams from the command.

Sometimes it's tricky to issues commands to a new process, using `subprocess.Popen` is a solid choice, but can be complicated to setup correctly.

The `trim.read_one_stream_command` function opens a new pipe for a given command, and performs a single byte flushing. This is vital for correctly wrapping interactive Windows commands, allowing you to wait upon or interact with a process.


## Usage

```py
from trim.execute import read_one_stream_command as read_one

read_one('powershell')
```
