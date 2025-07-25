class ScenarioManager:
    """Manages different game scenarios and levels"""
    
    def __init__(self):
        self.scenarios = {
            1: {
                'title': 'Welcome to the Server Room!',
                'description': 'A new developer just joined your team and needs to run the deployment script. The script exists but isn\'t executable! This is super common in DevOps - files get the wrong permissions during git checkout or file transfers.',
                'context': 'DevOps Onboarding',
                'files': [
                    {'name': 'deploy.sh', 'current_permissions': 'rw-r--r--', 'octal': '644'},
                ],
                'task': 'Make the deploy.sh script executable for everyone',
                'expected_command': 'chmod +x deploy.sh',
                'alternative_commands': ['chmod 755 deploy.sh', 'chmod a+x deploy.sh', 'chmod u+x,g+x,o+x deploy.sh'],
                'explanation': 'Scripts need execute permission to run. The +x flag adds execute permission for all users (owner, group, others). Alternative: 755 gives full permissions to owner (rwx=7) and read+execute to group and others (rx=5).',
                'detailed_explanation': 'In DevOps, this happens constantly! Git doesn\'t preserve execute permissions across different filesystems, so freshly cloned deployment scripts often need chmod +x. Always check script permissions in your CI/CD pipelines!',
                'real_world_tip': 'Pro tip: Add "chmod +x *.sh" to your deployment scripts to automatically fix permissions for all shell scripts.',
                'difficulty': 'easy',
                'points': 100
            },
            
            2: {
                'title': 'SSH Key Security Alert!',
                'description': 'Security audit found that SSH private keys have wrong permissions. This is a CRITICAL security risk! Other users on the system can read your private key, potentially giving them access to any servers you can SSH into.',
                'context': 'Security Incident',
                'files': [
                    {'name': 'id_rsa', 'current_permissions': 'rw-r--r--', 'octal': '644'},
                ],
                'task': 'Secure the SSH private key so only the owner can read/write it',
                'expected_command': 'chmod 600 id_rsa',
                'alternative_commands': ['chmod u=rw,go= id_rsa', 'chmod u=rw,g-r,o-r id_rsa', 'chmod 600 ~/.ssh/id_rsa'],
                'explanation': 'SSH private keys should only be readable by the owner (600). This prevents other users from accessing your private key and impersonating you on remote servers.',
                'detailed_explanation': 'SSH will actually REFUSE to use private keys that have overly permissive permissions! You\'ll get a "WARNING: UNPROTECTED PRIVATE KEY FILE!" error. This is a security feature to prevent accidental key exposure.',
                'real_world_tip': 'Security tip: Always set SSH private keys to 600, public keys to 644. Many security audits specifically check for this!',
                'difficulty': 'easy',
                'points': 150
            },
            
            3: {
                'title': 'Configuration Chaos!',
                'description': 'Production is down! The web server can\'t read its config file because permissions got messed up during deployment. This is a P1 incident - every minute costs money!',
                'context': 'Production Incident',
                'files': [
                    {'name': 'nginx.conf', 'current_permissions': 'rw-------', 'octal': '600'},
                    {'name': 'app.conf', 'current_permissions': 'rwx------', 'octal': '700'},
                ],
                'task': 'Fix both config files so they\'re readable by all but only writable by owner',
                'expected_command': 'chmod 644 nginx.conf app.conf',
                'alternative_commands': ['chmod 644 *.conf', 'chmod u=rw,go=r nginx.conf app.conf', 'chmod u=rw,g=r,o=r nginx.conf app.conf'],
                'explanation': 'Config files should be readable by services (644) but only writable by admins. Services run as different users and need read access to configuration.',
                'detailed_explanation': 'Web servers, databases, and applications often run as dedicated service users (www-data, nginx, etc.). These processes need to read config files but shouldn\'t be able to modify them.',
                'real_world_tip': 'Always use 644 for config files unless they contain secrets (then use 600). Never make config files executable unless they\'re actually scripts!',
                'difficulty': 'medium',
                'points': 200
            },
            
            4: {
                'title': 'Container Build Failure!',
                'description': 'Your Docker build is failing because the build script doesn\'t have the right permissions inside the container. The CI/CD pipeline is blocked and the team is waiting!',
                'context': 'CI/CD Pipeline',
                'files': [
                    {'name': 'build.sh', 'current_permissions': 'rw-rw-rw-', 'octal': '666'},
                    {'name': 'test.sh', 'current_permissions': 'rw-rw-rw-', 'octal': '666'},
                ],
                'task': 'Make both scripts executable while keeping them secure (owner: rwx, group: r-x, others: r--)',
                'expected_command': 'chmod 754 build.sh test.sh',
                'alternative_commands': ['chmod u=rwx,g=rx,o=r build.sh test.sh', 'chmod 754 *.sh', 'chmod u+x,g+x build.sh test.sh'],
                'explanation': 'Build scripts need execute permission but should be more restrictive than 755 for security. 754 gives full access to owner, read+execute to group, and read-only to others.',
                'detailed_explanation': 'In containerized environments, you want to follow the principle of least privilege. 754 is more secure than 755 because it prevents "others" from executing the script, while still allowing group members to run it.',
                'real_world_tip': 'In Dockerfiles, use "RUN chmod 754 *.sh" after copying scripts. Many security scanners flag 755 permissions as potentially risky.',
                'difficulty': 'medium',
                'points': 250
            },
            
            5: {
                'title': 'Database Backup Emergency!',
                'description': 'The automated backup script failed because it can\'t access the database dump file. The DBA set overly restrictive permissions and now backups are failing silently!',
                'context': 'Database Operations',
                'files': [
                    {'name': 'backup.sql', 'current_permissions': 'rw-------', 'octal': '600'},
                    {'name': 'backup.sh', 'current_permissions': 'rw-r-----', 'octal': '640'},
                ],
                'task': 'Allow the backup script to run (executable) and the backup group to read the SQL file',
                'expected_command': 'chmod 750 backup.sh && chmod 640 backup.sql',
                'alternative_commands': ['chmod u+x backup.sh', 'chmod 750 backup.sh; chmod 640 backup.sql', 'chmod u=rwx,g=rx,o= backup.sh && chmod u=rw,g=r,o= backup.sql'],
                'explanation': 'Scripts need execute permission (750), and backup files should be accessible to the backup group (640). This allows automated backup systems to function while maintaining security.',
                'detailed_explanation': 'Database backups often involve multiple users: the DBA who creates dumps, the backup service that transfers them, and monitoring that checks file sizes. Group permissions (640/750) enable this collaboration securely.',
                'real_world_tip': 'Use groups for shared access! Create a "backup" group, add relevant users/services to it, and use 640/750 permissions instead of making files world-readable.',
                'difficulty': 'hard',
                'points': 300
            },
            
            6: {
                'title': 'Kubernetes Secret Leak!',
                'description': 'A security scan found that Kubernetes secret files are readable by all users on the node. This could expose API keys, database passwords, and certificates to any process on the system!',
                'context': 'Kubernetes Security',
                'files': [
                    {'name': 'db-password.txt', 'current_permissions': 'rw-r--r--', 'octal': '644'},
                    {'name': 'api-key.txt', 'current_permissions': 'rw-r--r--', 'octal': '644'},
                    {'name': 'tls.key', 'current_permissions': 'rw-r--r--', 'octal': '644'},
                ],
                'task': 'Secure all secret files so only the owner can access them',
                'expected_command': 'chmod 600 db-password.txt api-key.txt tls.key',
                'alternative_commands': ['chmod 600 *.txt *.key', 'chmod u=rw,go= db-password.txt api-key.txt tls.key', 'chmod 600 *'],
                'explanation': 'Secret files should never be readable by other users (600). This prevents credential theft and unauthorized access to sensitive systems.',
                'detailed_explanation': 'In Kubernetes, secrets are mounted as files in pods. Default permissions can be too permissive, allowing any process in the pod to read secrets. Use securityContext.fsGroup and defaultMode: 0600 in volume specs.',
                'real_world_tip': 'Always audit mounted secrets in K8s! Use "kubectl describe pod" to check volume mounts and set defaultMode: 0600 in your deployment manifests.',
                'difficulty': 'hard',
                'points': 350
            },
            
            7: {
                'title': 'Git Hook Nightmare!',
                'description': 'Your team\'s git hooks aren\'t running because they lost execute permissions during a repository migration. Code quality checks are being skipped and bugs are slipping through!',
                'context': 'Version Control',
                'files': [
                    {'name': 'pre-commit', 'current_permissions': 'rw-r--r--', 'octal': '644'},
                    {'name': 'pre-push', 'current_permissions': 'rw-r--r--', 'octal': '644'},
                    {'name': 'commit-msg', 'current_permissions': 'rw-r--r--', 'octal': '644'},
                ],
                'task': 'Make all git hooks executable while keeping them secure',
                'expected_command': 'chmod 755 pre-commit pre-push commit-msg',
                'alternative_commands': ['chmod +x pre-commit pre-push commit-msg', 'chmod 755 *', 'chmod a+x pre-commit pre-push commit-msg'],
                'explanation': 'Git hooks must be executable to run automatically. 755 permissions allow the git process to execute them while keeping them readable for debugging.',
                'detailed_explanation': 'Git hooks are scripts that run at specific points in the git workflow. They\'re crucial for code quality, running tests, and enforcing policies. Without execute permissions, they\'re silently ignored!',
                'real_world_tip': 'Add "chmod +x .git/hooks/*" to your repository setup scripts. Consider using tools like pre-commit or husky to manage hook permissions automatically.',
                'difficulty': 'medium',
                'points': 275
            }
        }
    
    def get_scenario(self, level):
        """Get scenario by level number"""
        return self.scenarios.get(level, self.scenarios[1])  # Default to level 1 if level doesn't exist
    
    def get_max_level(self):
        """Get the maximum level available"""
        return max(self.scenarios.keys())
    
    def get_scenario_count(self):
        """Get total number of scenarios"""
        return len(self.scenarios)
    
    def get_scenarios_by_difficulty(self, difficulty):
        """Get all scenarios of a specific difficulty"""
        return {level: scenario for level, scenario in self.scenarios.items() 
                if scenario['difficulty'] == difficulty}