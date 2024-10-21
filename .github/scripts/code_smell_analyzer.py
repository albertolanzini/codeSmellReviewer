from pathlib import Path
from typing import Dict, List, Tuple, Any
import subprocess
import javalang

from smell_context_rules import SMELL_CONTEXT_RULES
from context_extractor import SmartContextExtractor


class CodeChangeAnalyzer:
    def __init__(self, repo_path: Path):
        self.repo_path = repo_path
        
    def get_pr_changes(self, base_sha: str, head_sha: str) -> Dict[str, List[Tuple[int, int]]]:
        """Get changed line ranges for each modified file in PR"""
        cmd = f"git diff -U0 {base_sha} {head_sha}"
        diff_output = subprocess.check_output(cmd, shell=True, text=True)
        
        changes = {}
        current_file = None
        
        for line in diff_output.split('\n'):
            if line.startswith('+++'):
                current_file = line[6:]
                if current_file.startswith('b/'):
                    current_file = current_file[2:]
                if current_file.endswith('.java'):
                    changes[current_file] = []
            elif line.startswith('@@'):
                if current_file and current_file.endswith('.java'):
                    # Parse the @@ line to get changed line ranges
                    parts = line.split(' ')[2].split(',')
                    start = int(parts[0])
                    length = int(parts[1]) if len(parts) > 1 else 1
                    changes[current_file].append((start, start + length - 1))
                    
        return changes

class SmartAnalysisRunner:
    def __init__(self):
        self.context_extractor = SmartContextExtractor()  # Initialize SmartContextExtractor

    def analyze_pr_changes(self, 
                           repo_path: Path, 
                           code_smells: Dict[str, List[Dict[str, Any]]]) -> List[Dict]:
        """
        Analyze the code smells across multiple files.
        `code_smells` is a dictionary where keys are file paths and values are lists of code smells in each file.
        """
        issues = []
        
        for file_path, file_code_smells in code_smells.items():
            # Extract the line ranges from the code smells
            line_ranges = [(smell['startLine'], smell['endLine']) for smell in file_code_smells]

            # Merge the overlapping or adjacent ranges
            merged_ranges = self._merge_ranges(line_ranges)

            # Analyze the merged ranges in the file and get issues
            file_issues = self._analyze_file_ranges(repo_path / file_path, merged_ranges, file_code_smells)
            issues.extend(file_issues)
            
        return issues

    def _analyze_file_ranges(self, 
                             file_path: Path, 
                             merged_ranges: List[Tuple[int, int]], 
                             code_smells: List[Dict[str, Any]]) -> List[Dict]:
        """
        Analyze specific line ranges in a file based on merged ranges from code smells.
        """
        issues = []
        for i, (start, end) in enumerate(merged_ranges):
            code_smell = code_smells[i]
            rule_id = code_smell['ruleId']
            description = code_smell['description']
            
            # Prepare rule_info with all relevant information
            rule_info = {
                'startLine': start,
                'endLine': end,
                'ruleId': rule_id,
                'description': description
            }

            # Ensure at least 10 extra lines above and below for proper context
            adjusted_start = max(0, start - 10)
            adjusted_end = end + 10

            # Update rule_info with expanded line range
            rule_info['startLine'] = adjusted_start
            rule_info['endLine'] = adjusted_end

            # Use SmartContextExtractor to extract the relevant context
            issue_context = self.context_extractor.extract_smart_context(file_path, rule_info)

            # Collect the issue details including extracted context
            issues.append({
                'file': str(file_path),
                'ruleId': rule_id,
                'description': description,
                'context': issue_context
            })
        
        return issues

    @staticmethod
    def _merge_ranges(ranges: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
        """Merge overlapping line ranges"""
        if not ranges:
            return []

        ranges.sort(key=lambda x: x[0])
        merged = [ranges[0]]

        for current in ranges[1:]:
            previous = merged[-1]
            if current[0] <= previous[1]:
                merged[-1] = (previous[0], max(previous[1], current[1]))
            else:
                merged.append(current)

        return merged
