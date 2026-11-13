#!/usr/bin/env python3
"""Inspect Nginx from a disposable build-stage container sharing its PID namespace."""

import errno
import os
from pathlib import Path
import stat


def check():
    processes = []
    for process in Path("/proc").glob("[0-9]*"):
        try:
            status = dict(line.split(":", 1) for line in (process / "status").read_text().splitlines())
        except FileNotFoundError:
            continue
        if status["Name"].strip() != "nginx":
            continue
        for identity in ["Uid", "Gid"]:
            assert status[identity].split() == ["65532"] * 4, (process, identity, status[identity])
        for capabilities in ["CapInh", "CapPrm", "CapEff", "CapBnd", "CapAmb"]:
            assert int(status[capabilities], 16) == 0, (process, capabilities, status[capabilities])
        assert status["NoNewPrivs"].strip() == "1", (process, "NoNewPrivs")
        assert status["Seccomp"].strip() == "2", (process, "Seccomp")
        processes.append(process.name)
    assert "1" in processes and len(processes) >= 2, ("Expected Nginx master and worker", processes)

    root = Path("/proc/1/root")
    content = root / "srv/www"
    paths = [content, *content.rglob("*"), root / "etc/nginx/nginx.conf",
             root / "etc/nginx/security-headers.conf"]
    for path in paths:
        info = path.stat()
        assert info.st_uid == 0 and info.st_gid == 0, (path, "Not owned by root")
        assert not info.st_mode & (stat.S_IWGRP | stat.S_IWOTH), (path, "Group/other writable")
        assert not os.access(path, os.W_OK), (path, "Writable by runtime user")

    for path in [content / "index.html", root / "etc/nginx/nginx.conf",
                 root / "etc/nginx/security-headers.conf", content / ".security-smoke-write"]:
        try:
            descriptor = os.open(path, os.O_WRONLY | os.O_APPEND | os.O_CREAT, 0o600)
        except OSError as error:
            assert error.errno in {errno.EACCES, errno.EPERM, errno.EROFS}, (path, error)
        else:
            os.close(descriptor)
            raise AssertionError(f"Runtime user could open {path} for writing")

    for binary in ["bin/sh", "bin/bash", "bin/ash", "sbin/apk", "usr/bin/apt",
                   "usr/local/bin/python3"]:
        assert not (root / binary).exists(), (binary, "Unexpected runtime tool")
    assert (root / "dev/shm/nginx.pid").read_text().strip() == "1"
    assert "__BUILD_VERSION__" not in (content / "index.html").read_text()
    print(f"Verified {len(processes)} non-root Nginx processes, zero capabilities, no-new-privileges, "
          "seccomp, immutable content/configuration, and minimal runtime")


if __name__ == "__main__":
    check()
