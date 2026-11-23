#!/usr/bin/env python3
"""Smoke-test the hardened image using Docker (or --engine podman)."""

import argparse
import json
import subprocess
import time
from urllib.error import URLError
from urllib.request import Request, urlopen

from check_headers import check as check_headers


def check(image, inspector_image, engine):
    def run(*args):
        return subprocess.run([engine, *args], check=True, text=True, capture_output=True,
                              timeout=45).stdout.strip()

    container = None
    try:
        # No bind mounts or additional writable volumes in the serving container.
        container = run("run", "--detach", "--read-only", "--cap-drop=ALL",
                        "--security-opt=no-new-privileges:true", "--memory=50m", "--cpus=0.05",
                        "--publish", "127.0.0.1::8080", image)
        inspected = json.loads(run("inspect", container))[0]
        assert inspected["Config"]["User"] == "65532:65532", "Unexpected runtime user"
        assert inspected["HostConfig"]["ReadonlyRootfs"], "Writable root filesystem"
        assert not inspected.get("Mounts"), "Unexpected application volume mounts"
        assert "8080/tcp" in inspected["Config"]["ExposedPorts"], "Missing exposed port"
        address = run("port", container, "8080/tcp").splitlines()[0]
        base_url = "http://" + address
        deadline = time.monotonic() + 30
        while True:
            try:
                with urlopen(base_url, timeout=2) as response:
                    assert response.status == 200
                break
            except (URLError, TimeoutError):
                assert json.loads(run("inspect", container))[0]["State"]["Running"], "Nginx exited"
                if time.monotonic() >= deadline:
                    raise RuntimeError("Nginx did not become ready within 30 seconds")
                time.sleep(0.25)

        check_headers(base_url)
        with urlopen(base_url + "/index.html", timeout=5) as response:
            index = response.read()
        with urlopen(base_url + "/__container_smoke_route__", timeout=5) as response:
            assert response.read() == index, "SPA fallback no longer serves index.html"
        with urlopen(Request(base_url + "/", method="HEAD"), timeout=5) as response:
            assert response.status == 200 and response.read() == b"", "HEAD request failed"
        # Diagnostic tools stay in a separate, disposable build-stage container.
        print(run("run", "--rm", "--read-only", "--network=none", "--cap-drop=ALL",
                  "--security-opt=no-new-privileges:true", "--user=65532:65532",
                  "--pid=container:" + container, "--entrypoint=python3", inspector_image,
                  "/site/scripts/inspect_container.py"))

        run("kill", "--signal=QUIT", container)
        assert run("wait", container) == "0", "Nginx did not shut down cleanly"
        # Docker returns access logs on stdout and Nginx diagnostics on stderr.
        diagnostics = subprocess.run([engine, "logs", container], check=True,
                                     text=True, capture_output=True, timeout=10)
        logs = diagnostics.stdout + diagnostics.stderr
        for failure in ["[emerg]", "[alert]", "[crit]", "[error]", "Permission denied", "Read-only file system"]:
            assert failure not in logs, (failure, logs)
        assert "exiting" in logs, "Missing graceful shutdown diagnostics"
        print("Verified startup and graceful shutdown under read-only, capability-free restrictions")
    finally:
        if container:
            subprocess.run([engine, "logs", container], check=False, timeout=10)
            subprocess.run([engine, "rm", "--force", container], check=False,
                           capture_output=True, timeout=15)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("image", help="Serving image built from the final Dockerfile stage")
    parser.add_argument("--inspector-image", default="fintlabs-security-check",
                        help="Image built with --target security-check")
    parser.add_argument("--engine", default="docker", choices=["docker", "podman"])
    args = parser.parse_args()
    try:
        check(args.image, args.inspector_image, args.engine)
    except subprocess.CalledProcessError as error:
        raise SystemExit(error.stdout + error.stderr) from error
