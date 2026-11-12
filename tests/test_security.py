import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("security", ROOT / "scripts/security.py")
security = importlib.util.module_from_spec(spec)
spec.loader.exec_module(security)


class SecurityTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        for path in ["frontend/index.html", "frontend/js/docsify-config.js",
                     "frontend/js/to-top.js", "frontend/js/docsify-images.js",
                     "security/assets.json", "security-headers.conf"]:
            destination = self.root / path
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / path, destination)

    def edit_index(self, before, after):
        path = self.root / "frontend/index.html"
        source = path.read_text()
        self.assertIn(before, source)
        path.write_text(source.replace(before, after))

    def edit_manifest(self, edit):
        path = self.root / "security/assets.json"
        manifest = json.loads(path.read_text())
        edit(manifest)
        path.write_text(json.dumps(manifest))

    def test_checked_in_policy_matches_assets(self):
        security.synchronize(ROOT, check=True)

    def test_generation_is_idempotent_and_offline(self):
        with patch.object(security, "urlopen", side_effect=AssertionError("Unexpected network request")):
            before = security.render(self.root)
            security.synchronize(self.root)
            self.assertEqual(before, security.render(self.root))
            security.synchronize(self.root, check=True)

    def test_script_changes_require_sri_and_csp_update(self):
        path = self.root / "frontend/js/to-top.js"
        path.write_text(path.read_text() + "\n// Deliberate regression fixture.\n")
        with self.assertRaisesRegex(ValueError, "Stale security metadata"):
            security.synchronize(self.root, check=True)
        security.synchronize(self.root)
        expected = security.digest(path.read_bytes())
        self.assertIn(expected, (self.root / "frontend/index.html").read_text())
        self.assertIn("'" + expected + "'", (self.root / "security-headers.conf").read_text())
        security.synchronize(self.root, check=True)

    def test_modified_integrity_is_rejected(self):
        self.edit_index('integrity="sha384-', 'integrity="sha384-changed')
        with self.assertRaisesRegex(ValueError, "Stale security metadata"):
            security.synchronize(self.root, check=True)

    def test_modified_policy_is_rejected(self):
        path = self.root / "security-headers.conf"
        path.write_text(path.read_text().replace("default-src 'none'", "default-src https:"))
        with self.assertRaisesRegex(ValueError, "Stale security metadata"):
            security.synchronize(self.root, check=True)

    def test_inline_code_and_event_handlers_are_rejected(self):
        for snippet in ['<script>alert(1)</script>', '<img src="x" onerror="alert(1)">']:
            with self.subTest(snippet=snippet):
                original = (ROOT / "frontend/index.html").read_text()
                (self.root / "frontend/index.html").write_text(original.replace("</body>", snippet + "</body>"))
                with self.assertRaisesRegex(ValueError, "Inline"):
                    security.render(self.root)

    def test_unapproved_script_is_rejected(self):
        self.edit_index("</body>", '<script src="https://example.invalid/script.js"></script></body>')
        with self.assertRaisesRegex(ValueError, "not approved"):
            security.render(self.root)

    def test_unapproved_stylesheet_is_rejected(self):
        self.edit_index("</head>", '<link rel="stylesheet" href="https://example.invalid/style.css"></head>')
        with self.assertRaisesRegex(ValueError, "not approved"):
            security.render(self.root)

    def test_protocol_relative_script_is_rejected(self):
        self.edit_index('src="/js/to-top.js', 'src="//example.invalid/js/to-top.js')
        with self.assertRaisesRegex(ValueError, "explicit HTTPS"):
            security.render(self.root)

    def test_floating_dependency_version_is_rejected(self):
        self.edit_manifest(lambda m: m["assets"][0].update(url=m["assets"][0]["url"].replace("@5.1.0", "@5")))
        with self.assertRaisesRegex(ValueError, "exact version"):
            security.render(self.root)

    def test_broad_resource_permissions_are_rejected(self):
        for source in ["https:", "https://*.example.com/images/", "https://example.com/",
                       "https://raw.githubusercontent.com"]:
            with self.subTest(source=source):
                shutil.copyfile(ROOT / "security/assets.json", self.root / "security/assets.json")
                self.edit_manifest(lambda m: m["resources"]["img-src"].append(source))
                with self.assertRaisesRegex(ValueError, "explicit HTTPS"):
                    security.render(self.root)

    def test_image_origin_approvals_do_not_extend_to_fetches(self):
        for origin in security.IMAGE_ORIGINS:
            with self.subTest(origin=origin):
                shutil.copyfile(ROOT / "security/assets.json", self.root / "security/assets.json")
                self.edit_manifest(lambda m: m["resources"]["connect-src"].append(origin))
                with self.assertRaisesRegex(ValueError, "explicit HTTPS"):
                    security.render(self.root)

    def test_simplified_sources_preserve_fetch_boundary(self):
        config = (ROOT / "security-headers.conf").read_text()
        csp = config.split('Content-Security-Policy "', 1)[1].split('" always;', 1)[0]
        directives = dict((section.strip().split()[0], section.strip().split()[1:])
                          for section in csp.split(";") if section.strip())
        self.assertEqual(set(directives["style-src"]), {
            "'self'", "'unsafe-inline'", "https://cdn.jsdelivr.net", "https://cdnjs.cloudflare.com",
        })
        self.assertEqual(directives["font-src"], ["https://cdnjs.cloudflare.com/ajax/libs/font-awesome/"])
        self.assertTrue(security.IMAGE_ORIGINS.issubset(directives["img-src"]))
        self.assertEqual(directives["connect-src"], [
            "'self'",
            "https://raw.githubusercontent.com/FINTLabs/flais-keycloak/main/docs/external/no/fint/federation/federation.md",
        ])
        self.assertNotIn("https://raw.githubusercontent.com", directives["img-src"])

    def test_script_policy_only_contains_hashes(self):
        config = (ROOT / "security-headers.conf").read_text()
        csp = config.split('Content-Security-Policy "', 1)[1].split('" always;', 1)[0]
        directives = dict((section.strip().split()[0], section.strip().split()[1:])
                          for section in csp.split(";") if section.strip())
        self.assertGreater(len(directives["script-src"]), 1)
        for value in directives["script-src"]:
            self.assertTrue(security.DIGEST.fullmatch(value.strip("'")), value)
        self.assertEqual(directives["script-src-attr"], ["'none'"])
        self.assertIn("'unsafe-inline'", directives["style-src"])
        for name in ["default-src", "frame-ancestors", "object-src", "form-action", "worker-src"]:
            self.assertEqual(directives[name], ["'none'"])
        self.assertNotIn("preload", config)

    def test_remote_verification_never_replaces_a_changed_digest(self):
        manifest = (self.root / "security/assets.json").read_bytes()
        with patch.object(security, "urlopen") as request:
            response = request.return_value.__enter__.return_value
            response.url = json.loads(manifest)["assets"][0]["url"]
            response.read.return_value = b"Unexpected CDN contents"
            with self.assertRaisesRegex(ValueError, "integrity mismatch"):
                security.verify_remote(self.root)
        self.assertEqual(manifest, (self.root / "security/assets.json").read_bytes())


if __name__ == "__main__":
    unittest.main()
