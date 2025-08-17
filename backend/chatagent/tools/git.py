
from .shell import run_shell


async def git_init(cwd: str):
    async for out in run_shell("git init -b main", cwd=cwd):
        yield out


async def git_status(cwd: str):
    async for out in run_shell("git status --porcelain=v1 -b", cwd=cwd):
        yield out


async def git_commit_all(cwd: str, msg: str):
    cmd = f"git add -A && git commit -m {msg!r}"
    async for out in run_shell(cmd, cwd=cwd):
        yield out
