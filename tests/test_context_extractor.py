import unittest
from pathlib import Path
from unittest.mock import patch, mock_open

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent / '.github' / 'scripts'))

from context_extractor import SmartContextExtractor
from smell_context_rules import SMELL_CONTEXT_RULES


class TestSmartContextExtractor(unittest.TestCase):

    def setUp(self):
        self.extractor = SmartContextExtractor()
        self.file_path = Path("/fake/path/ExampleClass.java")
    
    @patch("builtins.open", new_callable=mock_open, read_data="".join([
        "public class ExampleClass {\n",
        "    private void methodOne() {\n",
        "        int unusedVariable = 42;\n",
        "    }\n",
        "    private void methodTwo() {\n",
        "        // Another method\n",
        "    }\n",
        "}\n"
    ]))
    def test_extract_smart_context_with_variable_rule(self, mock_file):
        """
        Test context extraction for java:S1488 (Local variable could be final).
        It should extract 2 lines above and 3 lines below the issue.
        """
        issue = {
            'ruleId': 'java:S1488',
            'startLine': 3,  # Line number for "int unusedVariable = 42;"
            'endLine': 3,
        }
    
        # Extract context
        context = self.extractor.extract_smart_context(self.file_path, issue)
    
        # Expected context: 2 lines above and 3 lines below the variable issue
        expected_context = (
            "public class ExampleClass {\n"
            "    private void methodOne() {\n"
            "        int unusedVariable = 42;\n"
            "    }\n"
            "    private void methodTwo() {\n"
            "        // Another method\n"         
        )
    
        self.assertEqual(context, expected_context)

    @patch("builtins.open", new_callable=mock_open, read_data="".join([
        "public class ExampleClass {\n",
        "    private void methodOne() {\n",
        "        int unusedVariable = 42;\n",
        "    }\n",
        "    private void methodTwo() {\n",
        "        // Another method\n",
        "    }\n",
        "}\n"
    ]))
    def test_extract_smart_context_with_class_rule(self, mock_file):
        """
        Test context extraction for java:S1989 (God Class).
        It should extract the entire class.
        """
        issue = {
            'ruleId': 'java:S1989',
            'startLine': 1,
            'endLine': 8,
        }
    
        # Extract context for God Class
        context = self.extractor.extract_smart_context(self.file_path, issue)
    
        # Expected context: the entire class should be extracted
        expected_context = (
            "public class ExampleClass {\n"
            "    private void methodOne() {\n"
            "        int unusedVariable = 42;\n"
            "    }\n"
            "    private void methodTwo() {\n"
            "        // Another method\n"
            "    }\n"
            "}\n"
        )
    
        self.assertEqual(context, expected_context)

    # TODO: Add more test cases for different code smells


if __name__ == '__main__':
    unittest.main()

