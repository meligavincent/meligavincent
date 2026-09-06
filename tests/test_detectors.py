import unittest

from scripts.detectors import ai, cloud_native, javascript, languages, python


class DetectorTests(unittest.TestCase):
    def test_direct_dependencies_and_lockfiles_are_detected(self):
        files = {"apps/web/package.json": '{"dependencies":{"next":"*","react":"*"},"devDependencies":{"tailwindcss":"*"}}', "pnpm-lock.yaml": "lockfileVersion: 9"}
        self.assertEqual({item.technology for item in javascript.detect(files)}, {"Next.js", "React", "Tailwind CSS", "pnpm"})

    def test_cloud_provider_requires_provider_specific_evidence(self):
        files = {"infrastructure/main.tf": 'terraform {}\nprovider "aws" {}\nresource "aws_eks_cluster" "main" {}'}
        self.assertEqual({item.technology for item in cloud_native.detect(files)}, {"Terraform", "AWS", "Amazon EKS"})

    def test_ai_agents_need_more_than_an_openai_dependency(self):
        self.assertNotIn("AI Agents", {item.technology for item in ai.detect({"pyproject.toml": 'openai = "*"'})})
        self.assertIn("AI Agents", {item.technology for item in ai.detect({"services/agent/tools.py": "def tool_call(): pass"})})

    def test_language_allowlist(self):
        found = {item.technology for item in languages.detect({"Python": 10, "Makefile": 4, "C++": 2})}
        self.assertEqual(found, {"Python", "C++"})

    def test_uv_requires_its_own_evidence(self):
        self.assertNotIn("uv", {item.technology for item in python.detect({"pyproject.toml": 'uvicorn = "*"'})})
        self.assertIn("uv", {item.technology for item in python.detect({"uv.lock": "version = 1"})})
