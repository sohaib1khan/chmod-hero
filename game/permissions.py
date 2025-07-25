import re
import time

class PermissionValidator:
    """Validates chmod commands and provides feedback"""
    
    def __init__(self):
        self.start_time = time.time()
    
    def validate_command(self, command, scenario):
        """
        Validate a chmod command against the expected solution
        
        Args:
            command (str): The command entered by the user
            scenario (dict): The current scenario data
            
        Returns:
            dict: Validation result with success, message, and hints
        """
        # Reset timer for this validation
        self.start_time = time.time()
        
        # Clean up the command
        command = command.strip().lower()
        
        # Check if it's a chmod command
        if not command.startswith('chmod'):
            return {
                'correct': False,
                'message': '❌ Command must start with "chmod"',
                'hint': 'Try: chmod [permissions] [filename]',
                'time_taken': self._get_time_taken()
            }
        
        # Check against expected command
        expected = scenario['expected_command'].lower()
        alternatives = [alt.lower() for alt in scenario.get('alternative_commands', [])]
        
        if command == expected or command in alternatives:
            return {
                'correct': True,
                'message': f'✅ Perfect! {scenario["explanation"]}',
                'time_taken': self._get_time_taken()
            }
        
        # Parse the command to give specific feedback
        feedback = self._analyze_command(command, scenario)
        return feedback
    
    def _analyze_command(self, command, scenario):
        """Analyze the command and provide specific feedback"""
        
        # Split command into parts
        parts = command.split()
        
        if len(parts) < 3:
            return {
                'correct': False,
                'message': '❌ Incomplete command. You need: chmod [permissions] [filename]',
                'hint': f'Try: chmod [permissions] {scenario["files"][0]["name"]}',
                'time_taken': self._get_time_taken()
            }
        
        chmod_part = parts[0]  # Should be 'chmod'
        permission_part = parts[1]
        file_part = ' '.join(parts[2:])  # Handle multiple files
        
        # Check specific issues
        
        # Check if using wrong files
        expected_files = [f['name'] for f in scenario['files']]
        mentioned_files = self._extract_files_from_command(file_part)
        
        if not any(f in expected_files for f in mentioned_files):
            return {
                'correct': False,
                'message': f'❌ Wrong file(s). You need to modify: {", ".join(expected_files)}',
                'hint': f'Include the correct filename(s) in your command',
                'time_taken': self._get_time_taken()
            }
        
        # Check permission format
        if self._is_octal_permission(permission_part):
            return self._check_octal_permission(permission_part, scenario)
        elif self._is_symbolic_permission(permission_part):
            return self._check_symbolic_permission(permission_part, scenario)
        else:
            return {
                'correct': False,
                'message': '❌ Invalid permission format',
                'hint': 'Use either octal (e.g., 755) or symbolic (e.g., +x, u+rwx) format',
                'time_taken': self._get_time_taken()
            }
    
    def _is_octal_permission(self, perm):
        """Check if permission is in octal format (e.g., 755)"""
        return re.match(r'^[0-7]{3,4}$', perm) is not None
    
    def _is_symbolic_permission(self, perm):
        """Check if permission is in symbolic format (e.g., +x, u+rwx)"""
        return re.match(r'^[ugoa]*[+-=][rwx]+$', perm) is not None
    
    def _check_octal_permission(self, perm, scenario):
        """Check octal permission against expected result"""
        
        # This is a simplified check - in a real implementation, 
        # you'd want to calculate the actual resulting permissions
        
        common_mistakes = {
            '777': 'Too permissive! This gives everyone full access.',
            '666': 'Files shouldn\'t be executable by default.',
            '700': 'Too restrictive - others might need read access.',
        }
        
        if perm in common_mistakes:
            return {
                'correct': False,
                'message': f'❌ {common_mistakes[perm]}',
                'hint': 'Think about what permissions each user type (owner/group/others) actually needs.',
                'time_taken': self._get_time_taken()
            }
        
        return {
            'correct': False,
            'message': f'❌ {perm} is not the right permission for this scenario.',
            'hint': f'Hint: {scenario.get("explanation", "Check the task description again.")}',
            'time_taken': self._get_time_taken()
        }
    
    def _check_symbolic_permission(self, perm, scenario):
        """Check symbolic permission against expected result"""
        
        if '+x' in perm and 'executable' in scenario['task'].lower():
            if perm == '+x':
                return {
                    'correct': True,
                    'message': f'✅ Good! {scenario["explanation"]}',
                    'time_taken': self._get_time_taken()
                }
        
        return {
            'correct': False,
            'message': f'❌ {perm} doesn\'t achieve the goal for this scenario.',
            'hint': 'Read the task description carefully and think about what permissions are needed.',
            'time_taken': self._get_time_taken()
        }
    
    def _extract_files_from_command(self, file_part):
        """Extract filenames from the command"""
        # Simple extraction - could be improved
        return file_part.split()
    
    def _get_time_taken(self):
        """Get time taken since validation started"""
        return round(time.time() - self.start_time, 2)
    
    def get_permission_hint(self, scenario):
        """Get a helpful hint for the current scenario"""
        
        hints = {
            'executable': 'Files need +x to be executable',
            'script': 'Scripts usually need 755 or 754 permissions',
            'config': 'Config files typically use 644 permissions',
            'secret': 'Secret files should use 600 permissions (owner only)',
            'ssh': 'SSH keys must be 600 for security',
        }
        
        task_lower = scenario['task'].lower()
        
        for keyword, hint in hints.items():
            if keyword in task_lower:
                return hint
        
        return 'Think about who needs what type of access to these files.'