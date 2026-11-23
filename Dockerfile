FROM python:3.13-alpine@sha256:9ef1a599f863231c3d91e941389bfdc4a2d6070557243d54df1a4e57015b960e AS security-check

ARG BUILD_VERSION=development

WORKDIR /site
COPY ./frontend/ ./frontend/
COPY ./security/ ./security/
COPY ./scripts/security.py ./scripts/security.py
COPY ./scripts/inspect_container.py ./scripts/inspect_container.py
COPY ./security-headers.conf ./security-headers.conf
COPY ./tests/ ./tests/
RUN python3 -m unittest discover -s tests -v \
    && python3 scripts/security.py --check
RUN python3 - <<'PY'
import os
from pathlib import Path

root = Path("frontend")
index = root / "index.html"
index.write_text(index.read_text().replace("__BUILD_VERSION__", os.environ["BUILD_VERSION"]))
for path in [root, *root.rglob("*")]:
    path.chmod(0o555 if path.is_dir() else 0o444)
PY

FROM cgr.dev/chainguard/nginx:latest@sha256:c9b4886a227029de68781204ace0c221c36efbddddd82cc40baa5f510cb30a46

# A dedicated document root excludes the base image's default page symlinks.
COPY --from=security-check --chown=0:0 /site/frontend/ /srv/www/
COPY --chown=0:0 --chmod=0444 ./nginx.conf /etc/nginx/nginx.conf
COPY --from=security-check --chown=0:0 --chmod=0444 /site/security-headers.conf /etc/nginx/security-headers.conf

USER 65532:65532
RUN ["/usr/sbin/nginx", "-t", "-e", "/dev/stderr"]
EXPOSE 8080
STOPSIGNAL SIGQUIT

# Exec form: the runtime image has no shell or package manager.
ENTRYPOINT ["/usr/sbin/nginx"]
CMD ["-c", "/etc/nginx/nginx.conf", "-e", "/dev/stderr", "-g", "daemon off;"]
