from pathlib import Path
import subprocess
import unittest

import yaml


ROOT = Path(__file__).resolve().parents[2]


class KubernetesConfigTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.applications = {}
        for environment in ["beta", "api"]:
            result = subprocess.run(
                ["kubectl", "kustomize", str(ROOT / "kustomize/overlays" / environment)],
                check=True, capture_output=True, text=True, timeout=30,
            )
            applications = [resource for resource in yaml.safe_load_all(result.stdout)
                            if resource and resource.get("kind") == "Application"]
            if len(applications) != 1:
                raise AssertionError(f"Expected one Application in {environment}")
            cls.applications[environment] = applications[0]

    def test_both_environments_keep_service_and_container_on_8080(self):
        for environment, application in self.applications.items():
            with self.subTest(environment=environment):
                self.assertEqual(application["metadata"]["name"], "www-fintlabs")
                self.assertEqual(application["metadata"]["namespace"], "fintlabs-no")
                self.assertEqual(application["spec"]["port"], 8080)
                self.assertEqual(application["spec"]["probes"]["readiness"]["path"], "/")

    def test_api_routes_both_public_hostnames_through_flaiserator(self):
        routes = self.applications["api"]["spec"]["ingress"]["routes"]
        self.assertEqual([route["host"] for route in routes], ["fintlabs.no", "www.fintlabs.no"])


if __name__ == "__main__":
    unittest.main()
