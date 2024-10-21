from pathlib import Path
from smell_context_rules import SMELL_CONTEXT_RULES
from typing import List

class SmartContextExtractor:
    def extract_smart_context(self, file_path: Path, issue: dict) -> str:
        """
        Extracts the relevant code context around the issue based on the rule's defined scope.
        """
        # Get the rule for this specific issue
        rule = SMELL_CONTEXT_RULES.get(issue['ruleId'], SMELL_CONTEXT_RULES['default'])
        extra_context = rule.get('extra_context', {'above': 3, 'below': 3})

        # Lines above and below the issue to extract
        lines_above = extra_context.get('above', 3)
        lines_below = extra_context.get('below', 3)

        # Since needs_class_context is False in your rule, we only extract lines around the variable
        with open(file_path, 'r') as file:
            lines = file.readlines()

            # Calculate the start and end line based on the rule's "above" and "below"
            start = max(0, issue['startLine'] - 1 - lines_above)  # Convert 1-based to 0-based indexing
            end = min(len(lines), issue['endLine'] + lines_below)

            # Return the range of lines around the issue
            return ''.join(lines[start:end])

    def _extract_class_context(self, lines: List[str], issue: dict) -> str:
        class_start, class_end = None, None
        for i, line in enumerate(lines):
            if 'class ' in line and class_start is None:
                class_start = i
            if '}' in line and class_start is not None:
                class_end = i
        if class_start is not None and class_end is not None:
            return ''.join(lines[class_start:class_end+1])
        return ''.join(lines)

    def _extract_method_context(self, lines: List[str], issue: dict) -> str:
        """
        Extracts the method context around the issue (used for variable-level rules).
        """
        method_start, method_end = None, None
        for i, line in enumerate(lines):
            if 'void ' in line or 'public ' in line or 'private ' in line:  # Detect method start
                method_start = i
            if '}' in line and method_start is not None:  # Detect method end
                method_end = i
                break
        if method_start is not None and method_end is not None:
            return ''.join(lines[method_start:method_end+1])
        return ''.join(lines)
