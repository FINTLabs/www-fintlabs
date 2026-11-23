#!/usr/bin/env python3
"""Require exact, approved action commits and explicitly allowed local workflows."""

import argparse
from pathlib import Path
import re

import yaml


ROOT = Path(__file__).resolve().parents[2]
REMOTE = re.compile(r"[\w-]+/[\w.-]+(?:/[\w.-]+)*@[0-9a-f]{40}\Z", re.ASCII)
LOCAL = re.compile(r"\./\.github/workflows/[\w.-]+\.ya?ml\Z", re.ASCII)


class WorkflowLoader(yaml.SafeLoader):
    """Reject duplicate keys rather than silently checking an overwritten value."""


def unique_mapping(loader, node, deep=False):
    loader.flatten_mapping(node)
    result = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in result:
            raise ValueError(f"Duplicate YAML key: {key}")
        result[key] = loader.construct_object(value_node, deep=deep)
    return result


WorkflowLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, unique_mapping)


def load_allowlist(root):
    allowed = set()
    for number, line in enumerate((root / ".github/actions-allowlist.txt").read_text().splitlines(), 1):
        reference = line.partition("#")[0].strip()
        if not reference:
            continue
        if not (REMOTE.fullmatch(reference) or LOCAL.fullmatch(reference)):
            raise ValueError(f"Allow-list line {number}: use an exact action@SHA or local workflow path")
        if reference in allowed:
            raise ValueError(f"Allow-list line {number}: duplicate {reference}")
        if LOCAL.fullmatch(reference) and not (root / reference).is_file():
            raise ValueError(f"Allow-list line {number}: missing local workflow {reference}")
        allowed.add(reference)
    if not allowed:
        raise ValueError("Action allow-list is empty")
    return allowed


def references(workflow):
    data = yaml.load(workflow.read_text(), Loader=WorkflowLoader)
    if not isinstance(data, dict) or not isinstance(data.get("jobs"), dict) or not data["jobs"]:
        raise ValueError(f"{workflow.name}: expected workflow jobs")
    for name, job in data["jobs"].items():
        if not isinstance(job, dict):
            raise ValueError(f"{workflow.name}: invalid job {name}")
        if "uses" in job:
            yield f"job {name}", job["uses"]
        steps = job.get("steps", [])
        if not isinstance(steps, list):
            raise ValueError(f"{workflow.name}: invalid steps in job {name}")
        for index, step in enumerate(steps, 1):
            if not isinstance(step, dict):
                raise ValueError(f"{workflow.name}: invalid step {index} in job {name}")
            if "uses" in step:
                yield f"job {name}, step {index}", step["uses"]


def check(root=ROOT):
    allowed = load_allowlist(root)
    workflows = sorted(path for path in (root / ".github/workflows").iterdir()
                       if path.is_file() and path.suffix in {".yml", ".yaml"})
    if not workflows:
        raise ValueError("No GitHub workflows found")
    count = 0
    for workflow in workflows:
        for location, reference in references(workflow):
            if not isinstance(reference, str) or reference not in allowed:
                raise ValueError(f"{workflow.name}, {location}: unapproved action or workflow {reference!r}")
            count += 1
    return count


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--github-patterns", action="store_true",
                        help="Print external entries for GitHub's selected-actions setting")
    args = parser.parse_args()
    try:
        count = check()
        if args.github_patterns:
            print(",\n".join(sorted(ref for ref in load_allowlist(ROOT) if REMOTE.fullmatch(ref))))
        else:
            print(f"Verified {count} action/workflow references against the exact allow-list.")
    except (ValueError, OSError, yaml.YAMLError) as error:
        raise SystemExit(str(error)) from error
