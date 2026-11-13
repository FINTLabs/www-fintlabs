# FINTLabs homepage

This is the FINTLabs homepage.

# Updating

All content is in `markdown` files.

## Updating existing content

To update existing content edit the `markdown` file with the content you need to update.

## Add new content

To add new content add a new `markdown` file. I addition you need to add a link to the `_sidebar.md` file.

## Publish content

When your finished updating the content, squash to `master`. Page will be deployed to beta environment automatically for testing.

To push to production, create a PR into branch `prod` and merge. Page will be published automatically.

## Docsify

https://docsify.js.org

## Run locally

`$ docsify serve` or `$ npx serve frontend`

These static preview commands do not apply the response security headers. To test
the production configuration, build and run Nginx locally:

```sh
docker build -t fintlabs-security .
docker run --rm -p 127.0.0.1:8765:80 fintlabs-security
```

## GitHub Actions policy

Every external action is pinned to a full commit SHA, with its latest reviewed
release version in a comment. The exact approved references are recorded in
[`.github/actions-allowlist.txt`](.github/actions-allowlist.txt), including an
explicit list of repository-local reusable workflows. Tags, branches, wildcard
entries, and unapproved commits or repositories are rejected.

The `Actions policy` workflow checks all workflow YAML files on pull requests and
can be run manually. The build/deploy/release pipeline also requires this check
before building or granting the deployment jobs access to secrets. The checker
parses YAML, including quoted keys and flow syntax, and rejects duplicate keys.
Its parser dependency is version-pinned and hash-locked separately from the
offline container build.

To run the checks locally with Python:

```sh
python3 -m venv /tmp/fintlabs-actions-policy
/tmp/fintlabs-actions-policy/bin/python -m pip install --require-hashes -r .github/requirements.txt
/tmp/fintlabs-actions-policy/bin/python .github/scripts/check_actions.py
/tmp/fintlabs-actions-policy/bin/python -m unittest discover -s .github/tests -v
```

Dependabot checks actions and the checker dependency weekly. For an action
update, review the upstream release and resolve its tag to a commit in the
original repository, then update both the workflow SHA/version comment and its
allow-list entry. A workflow-only update fails the policy check.

This file enforces policy in CI; it does not configure GitHub's repository-level
Actions permissions or branch protection. For GitHub's selected-actions setting,
generate the external `action@SHA` entries with
`python3 .github/scripts/check_actions.py --github-patterns` after installing
the parser. Administrators can apply that list, require full SHA pinning, and
make `Check action pins and allow-list` a required pull-request status check
using [GitHub's repository settings](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/enabling-features-for-your-repository/managing-github-actions-settings-for-a-repository).

## Security headers and dependency integrity

Nginx sends an enforced, hash-based Content Security Policy and the response
headers recommended for this site by the [OWASP HTTP Headers guide](https://cheatsheetseries.owasp.org/cheatsheets/HTTP_Headers_Cheat_Sheet.html)
and [OWASP CSP guide](https://cheatsheetseries.owasp.org/cheatsheets/Content_Security_Policy_Cheat_Sheet.html).
The generated `security-headers.conf` is included at server scope with
`add_header_inherit merge` and `always`, including asset locations and errors.
This requires Nginx 1.29.3 or newer; the Docker image supplies the supported version.

JavaScript is authorized only by SHA-384 hashes, without script host allowlists,
inline handlers, eval, or dynamic-script trust. CDN scripts and stylesheets use
exact versions, SRI, and anonymous CORS. The current runtime plugins and Mermaid
require inline CSS; this is an explicit CSS-only exception. Docsify script
execution is disabled and Mermaid remains in strict mode.
Mermaid is pinned to 12.3.0 and uses its asynchronous `run` API. Its standalone
browser bundle keeps the script-hash policy independent of module chunk imports.

The approved runtime resources are recorded in `security/assets.json`:

| Resource | Allowed delivery |
| --- | --- |
| Scripts | Exact, versioned jsDelivr and unpkg assets; script bytes must match the approved hashes |
| Theme styles | jsDelivr and cdnjs origins in CSP; each linked stylesheet still uses an exact version and SRI |
| Icon font | The Font Awesome directory on cdnjs; the current stylesheet requests 5.11.2 solid 900 WOFF2/WOFF |
| Page fetches | Same origin and the exact raw GitHub Keycloak Markdown URL |
| External images | The Shields.io and PlantUML image-service origins, and the Keycloak image directory on raw GitHub |
| Local images | Same origin, including the sidebar icons and Novari logo |
| Data images | Docsify's CSS SVG icons |

CSS, fonts, and images use broader source permissions to simplify maintenance.
The dedicated image-service origins are approved only for images, not fetches or
scripts. Shared raw GitHub hosting remains restricted to the FINTLabs document
and image paths. Whole CDN origins are never approved for JavaScript: public npm
and GitHub CDNs contain resources from unrelated publishers, and SRI on existing
tags would not require an injected script tag to carry an integrity attribute.

Ordinary outbound links do not need CSP resource permissions. The local Novari
logo is a copy of [Novari's published SVG](https://novari.no/wp-content/uploads/2024/10/novari_logo_primaer.svg).
Keep external images anonymous: the normal renderer handles Markdown images, and
the last-loaded `docsify-images.js` also covers raw HTML and PlantUML's detached
image creation before requests start. No image hosts need credentials.

After changing a local script, regenerate the metadata and review both changes:

```sh
python3 scripts/security.py
python3 scripts/security.py --check
python3 -m unittest discover -s tests -v
```

For a CDN update, review the exact release and downloaded bytes, calculate its
SHA-384 SRI digest, and explicitly update the URL and digest in the manifest and
the URL in `frontend/index.html`. Then regenerate and review the policy. Do not
replace a failed integrity hash automatically. To check the recorded CDN bytes,
redirects, and anonymous CORS support without updating any digests:

```sh
python3 scripts/security.py --check --verify-remote
```

Normal Docker builds validate the checked-in metadata and run the regression
tests without fetching CDN assets or refreshing hashes. Python and the test
files stay in the build stage and are absent from the final serving image.

### Verification and deployment

Against the locally running Nginx image:

```sh
python3 scripts/check_headers.py http://127.0.0.1:8765
```

This checks unique security headers, success/error responses, MIME types, caching,
and server version disclosure. Browser verification must additionally cover all
reachable pages, search, copy buttons, image zoom, back-to-top, anchors, Mermaid,
the five PlantUML diagrams, release badges, and the live Keycloak include. Check
the console and failed resources for CSP, integrity, CORS, and COEP errors. Use
disposable test pages to confirm unapproved scripts, inline handlers, resource
loads, form submissions, and framing are blocked; never ship those fixtures.

HSTS is `max-age=63072000; includeSubDomains`. Every `fintlabs.no` subdomain must
remain HTTPS-capable. Preload registration is not part of this configuration.
TLS terminates at the ingress; HTTP-to-HTTPS redirects must be enforced there.

After deployment, run the same header checker against both public hostnames:

```sh
python3 scripts/check_headers.py https://fintlabs.no
python3 scripts/check_headers.py https://www.fintlabs.no
curl -I http://fintlabs.no
curl -I http://www.fintlabs.no
```

Verify redirects go to HTTPS, and the access gateway preserves the headers
without replacing or duplicating them. Headers apply to each server response;
fragment routes share the HTML document's CSP. Changes to gateway cookies,
infrastructure logging, and TLS configuration are managed outside this project.

# Contribute   

- Add a [issue](https://github.com/FINTLabs/www-fintlabs/issues/new)

or

- Fork it!
- Create your feature branch: git checkout -b my-new-feature
- Commit your changes: git commit -am 'Add some feature'
- Push to the branch: git push origin my-new-feature
- Submit a pull request
