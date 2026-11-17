"""Tests for the parts that keep posts honest: the queue, approval, no duplicates."""

import tempfile
import unittest
from pathlib import Path

import subpost


class Queue(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        subpost.QUEUE = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def test_draft_waits_for_a_person(self):
        subpost.draft("rpg", "Free dice roller", url="https://example.com")
        item = subpost.load(subpost.drafts()[0])
        self.assertIsNone(item["approved_by"])
        self.assertIsNone(item["posted"])

    def test_approval_names_the_person(self):
        subpost.draft("rpg", "Free dice roller", url="https://example.com")
        name = subpost.drafts()[0].stem
        subpost.approve(name, "Sam")
        self.assertEqual(subpost.load(subpost.drafts()[0])["approved_by"], "Sam")

    def test_same_post_never_goes_to_two_subreddits(self):
        subpost.draft("rpg", "Free dice roller", url="https://example.com")
        with self.assertRaises(SystemExit):
            subpost.draft("dnd", "Free dice roller", url="https://example.com")

    def test_needs_content(self):
        with self.assertRaises(SystemExit):
            subpost.draft("rpg", "Empty")


if __name__ == "__main__":
    unittest.main()
