import unittest
from unittest.mock import patch, MagicMock
from pathlib import Path

# Mock the gemini module if needed
import sys
sys.path.append(str(Path(__file__).resolve().parent.parent / '.github' / 'scripts'))
sys.modules['gemini'] = MagicMock()

from code_smell_analyzer import CodeChangeAnalyzer, SmartAnalysisRunner


class TestCodeChangeAnalyzer(unittest.TestCase):
    
    @patch('subprocess.check_output')
    def test_get_pr_changes_no_changes(self, mock_check_output):
        """Test when no changes are detected."""
        # Simulate no changes in the diff
        mock_check_output.return_value = ""

        analyzer = CodeChangeAnalyzer(repo_path=Path("/path/to/repo"))
        changes = analyzer.get_pr_changes(base_sha="abc123", head_sha="def456")
        
        # Expect an empty dictionary when no changes are found
        self.assertEqual(changes, {})

    @patch('subprocess.check_output')
    def test_get_pr_changes_ignore_non_java(self, mock_check_output):
        """Test that non-Java files are ignored."""
        mock_check_output.return_value = """
+++ b/src/SomeFile.java
@@ -10,6 +10,7 @@ public class SomeClass {
+    private String newField;
}
+++ b/src/SomeFile.py
@@ -20,7 +20,9 @@ def some_function():
+    print('This is Python code');
}
"""
        analyzer = CodeChangeAnalyzer(repo_path=Path("/path/to/repo"))
        changes = analyzer.get_pr_changes(base_sha="abc123", head_sha="def456")

        # Expect only the Java file to be included in the changes
        expected_changes = {
            "src/SomeFile.java": [(10, 16)],
        }

        self.assertEqual(changes, expected_changes)


class TestSmartAnalysisRunner(unittest.TestCase):
    def test_merge_ranges(self):
        """Test that overlapping ranges are merged properly."""
        runner = SmartAnalysisRunner()

        # Example of overlapping ranges
        ranges = [(10, 15), (12, 20), (22, 25)]

        merged_ranges = runner._merge_ranges(ranges)
        
        # Expect the first two ranges to merge, the third one should remain as is
        expected = [(10, 20), (22, 25)]
        self.assertEqual(merged_ranges, expected)

    @patch('code_smell_analyzer.SmartContextExtractor')
    def test_analyze_pr_changes_issue_found(self, mock_context_extractor):
        """Test analyzing PR changes when issues are detected but mocked context is returned."""
        mock_context_extractor_instance = mock_context_extractor.return_value
        mock_context_extractor_instance.extract_smart_context.return_value = "mocked context"

        repo_path = Path("/path/to/repo")
        changes = {
            "src/SomeFile.java": [{'startLine': 10, 'endLine': 16, 'ruleId': 'java:S1144', 'description': 'Unused private method'}],
        }

        # Mock analyzing file content, returning no issues
        mock_analyze_file_content = MagicMock(return_value=[])

        runner = SmartAnalysisRunner()
        runner._analyze_file_content = mock_analyze_file_content

        issues = runner.analyze_pr_changes(repo_path, changes)

        # Expect an issue to be found with mocked context
        expected_issues = [{
            'file': '/path/to/repo/src/SomeFile.java',
            'ruleId': 'java:S1144',
            'description': 'Unused private method',
            'context': 'mocked context'
        }]

        # Assert that the issues match the expected mocked output
        self.assertEqual(issues, expected_issues)

    @patch('code_smell_analyzer.SmartContextExtractor')
    def test_analyze_pr_changes_no_code_smells(self, mock_context_extractor):
        """Test analyzing PR changes when no code smells are present."""
        mock_context_extractor_instance = mock_context_extractor.return_value
        mock_context_extractor_instance.extract_smart_context.return_value = ""  # No context needed since no issues

        repo_path = Path("/path/to/repo")
        changes = {
            "src/SomeFile.java": [],  # No code smells detected for this file
        }

        # Mock analyzing file content, returning no issues
        mock_analyze_file_content = MagicMock(return_value=[])

        runner = SmartAnalysisRunner()
        runner._analyze_file_content = mock_analyze_file_content

        issues = runner.analyze_pr_changes(repo_path, changes)

        # Expect no issues to be found since no code smells were provided
        self.assertEqual(issues, [])



if __name__ == '__main__':
    unittest.main()
