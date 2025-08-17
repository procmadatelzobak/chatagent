import asyncio
import fcntl
import os
import pty
from typing import AsyncIterator


async def run_shell(
    cmd: str, cwd: str | None = None, env: dict | None = None, timeout: int = 600
) -> AsyncIterator[str]:
    """Run a command in a PTY and yield output chunks."""
    master_fd, slave_fd = pty.openpty()
    pid = os.fork()
    if pid == 0:
        # Child
        os.setsid()
        os.dup2(slave_fd, 0)
        os.dup2(slave_fd, 1)
        os.dup2(slave_fd, 2)
        if cwd:
            os.chdir(cwd)
        os.execvp("/bin/bash", ["/bin/bash", "-lc", cmd])
    else:
        os.close(slave_fd)
        flags = fcntl.fcntl(master_fd, fcntl.F_GETFL)
        fcntl.fcntl(master_fd, fcntl.F_SETFL, flags | os.O_NONBLOCK)
        loop = asyncio.get_event_loop()
        try:
            start = loop.time()
            while True:
                if loop.time() - start > timeout:
                    os.kill(pid, 9)
                    yield "\n[Timeout exceeded]\n"
                    break
                await asyncio.sleep(0.02)
                try:
                    data = os.read(master_fd, 4096)
                    if not data:
                        break
                    yield data.decode(errors="ignore")
                except BlockingIOError:
                    # check if process still alive
                    _, status = os.waitpid(pid, os.WNOHANG)
                    if status != 0:
                        await asyncio.sleep(0.05)
                        continue
        finally:
            os.close(master_fd)
