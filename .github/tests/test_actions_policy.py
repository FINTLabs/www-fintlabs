import importlib.util
from pathlib import Path
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("actions_policy", ROOT / ".github/scripts/check_actions.py")
policy = importlib.util.module_from_spec(spec)
spec.loader.exec_module(policy)
APPROVED = "actions/checkout@" + "a" * 40


class ActionsPolicyTests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name)
        self.workflows = self.root / ".github/workflows"
        self.workflows.mkdir(parents=True)
        self.workflow = self.workflows / ".hidden.yaml"
        self.allowlist = self.root / ".github/actions-allowlist.txt"
        self.allowlist.write_text(APPROVED + " # reviewed version\n./.github/workflows/.hidden.yaml\n")
        self.write_reference(APPROVED)

    def write_reference(self, reference):
        self.workflow.write_text(f"jobs:\n  check:\n    steps:\n      - uses: {reference}\n")

    def test_repository_workflows_are_approved(self):
        self.assertGreater(policy.check(ROOT), 0)

    def test_approved_sha_and_hidden_workflow_are_checked(self):
        self.assertEqual(policy.check(self.root), 1)

    def test_tags_branches_and_short_shas_are_rejected(self):
        for ref in ["v7", "main", "a" * 12]:
            with self.subTest(ref=ref):
                self.write_reference("actions/checkout@" + ref)
                with self.assertRaisesRegex(ValueError, "unapproved"):
                    policy.check(self.root)

    def test_unapproved_repository_or_commit_is_rejected(self):
        for reference in ["unapproved/action@" + "a" * 40, "actions/checkout@" + "b" * 40]:
            with self.subTest(reference=reference):
                self.write_reference(reference)
                with self.assertRaisesRegex(ValueError, "unapproved"):
                    policy.check(self.root)

    def test_approved_local_workflow_is_checked(self):
        self.workflow.write_text("jobs:\n  nested:\n    uses: ./.github/workflows/.hidden.yaml\n")
        self.assertEqual(policy.check(self.root), 1)

    def test_unapproved_local_workflow_or_docker_action_is_rejected(self):
        for reference in ["./.github/workflows/other.yaml", "./local-action", "docker://alpine:latest"]:
            with self.subTest(reference=reference):
                self.write_reference(reference)
                with self.assertRaisesRegex(ValueError, "unapproved"):
                    policy.check(self.root)

    def test_quoted_keys_and_flow_yaml_do_not_bypass_policy(self):
        self.workflow.write_text('jobs: {check: {steps: [{"uses": "actions/checkout@v7"}]}}\n')
        with self.assertRaisesRegex(ValueError, "unapproved"):
            policy.check(self.root)

    def test_block_scalar_reference_does_not_bypass_policy(self):
        self.workflow.write_text("jobs:\n  check:\n    steps:\n      - uses: >-\n          actions/checkout@v7\n")
        with self.assertRaisesRegex(ValueError, "unapproved"):
            policy.check(self.root)

    def test_comments_and_shell_text_are_not_action_references(self):
        self.workflow.write_text('jobs:\n  check:\n    steps:\n      # uses: unapproved/action@main\n'
                                 '      - run: |\n          echo "uses: unapproved/action@main"\n')
        self.assertEqual(policy.check(self.root), 0)

    def test_duplicate_yaml_keys_are_rejected(self):
        self.workflow.write_text(f"jobs:\n  check:\n    steps:\n      - uses: {APPROVED}\n        uses: {APPROVED}\n")
        with self.assertRaisesRegex(ValueError, "Duplicate YAML key"):
            policy.check(self.root)

    def test_unpinned_or_wildcard_allowlist_entry_is_rejected(self):
        for reference in ["actions/checkout@v7", "actions/*", "actions/checkout@*"]:
            with self.subTest(reference=reference):
                self.allowlist.write_text(reference + "\n")
                with self.assertRaisesRegex(ValueError, "exact action@SHA"):
                    policy.check(self.root)

    def test_missing_allowlisted_workflow_is_rejected(self):
        self.allowlist.write_text("./.github/workflows/missing.yaml\n")
        with self.assertRaisesRegex(ValueError, "missing local workflow"):
            policy.check(self.root)


if __name__ == "__main__":
    unittest.main()
