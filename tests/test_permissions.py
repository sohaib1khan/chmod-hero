"""
Unit tests for the permission validation system
"""

import unittest
import sys
import os

# Add the parent directory to the path so we can import game modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from game.permissions import PermissionValidator
from game.scenarios import ScenarioManager
from game.scoring import ScoreManager

class TestPermissionValidator(unittest.TestCase):
    """Test the permission validation logic"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.validator = PermissionValidator()
        self.scenario_manager = ScenarioManager()
    
    def test_valid_chmod_command(self):
        """Test that valid chmod commands are accepted"""
        scenario = self.scenario_manager.get_scenario(1)
        
        # Test the expected command
        result = self.validator.validate_command('chmod +x deploy.sh', scenario)
        self.assertTrue(result['correct'])
        self.assertIn('✅', result['message'])
    
    def test_invalid_command_format(self):
        """Test that invalid command formats are rejected"""
        scenario = self.scenario_manager.get_scenario(1)
        
        # Test non-chmod command
        result = self.validator.validate_command('ls -l', scenario)
        self.assertFalse(result['correct'])
        self.assertIn('chmod', result['message'])
    
    def test_incomplete_command(self):
        """Test that incomplete commands are rejected"""
        scenario = self.scenario_manager.get_scenario(1)
        
        # Test incomplete command
        result = self.validator.validate_command('chmod', scenario)
        self.assertFalse(result['correct'])
        self.assertIn('Incomplete', result['message'])
    
    def test_wrong_file(self):
        """Test that commands with wrong files are rejected"""
        scenario = self.scenario_manager.get_scenario(1)
        
        # Test wrong filename
        result = self.validator.validate_command('chmod +x wrongfile.sh', scenario)
        self.assertFalse(result['correct'])
        self.assertIn('Wrong file', result['message'])
    
    def test_octal_permission_detection(self):
        """Test octal permission format detection"""
        self.assertTrue(self.validator._is_octal_permission('755'))
        self.assertTrue(self.validator._is_octal_permission('644'))
        self.assertTrue(self.validator._is_octal_permission('600'))
        self.assertFalse(self.validator._is_octal_permission('+x'))
        self.assertFalse(self.validator._is_octal_permission('abc'))
    
    def test_symbolic_permission_detection(self):
        """Test symbolic permission format detection"""
        self.assertTrue(self.validator._is_symbolic_permission('+x'))
        self.assertTrue(self.validator._is_symbolic_permission('u+rwx'))
        self.assertTrue(self.validator._is_symbolic_permission('go-w'))
        self.assertFalse(self.validator._is_symbolic_permission('755'))
        self.assertFalse(self.validator._is_symbolic_permission('invalid'))

class TestScenarioManager(unittest.TestCase):
    """Test the scenario management system"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.scenario_manager = ScenarioManager()
    
    def test_get_scenario(self):
        """Test getting scenarios by level"""
        scenario1 = self.scenario_manager.get_scenario(1)
        self.assertIsNotNone(scenario1)
        self.assertIn('title', scenario1)
        self.assertIn('description', scenario1)
        self.assertIn('files', scenario1)
        self.assertIn('task', scenario1)
    
    def test_get_invalid_scenario(self):
        """Test getting non-existent scenario returns default"""
        scenario = self.scenario_manager.get_scenario(999)
        self.assertIsNotNone(scenario)
        # Should return level 1 as default
        self.assertEqual(scenario, self.scenario_manager.get_scenario(1))
    
    def test_scenario_structure(self):
        """Test that all scenarios have required fields"""
        required_fields = ['title', 'description', 'context', 'files', 'task', 
                          'expected_command', 'explanation', 'difficulty', 'points']
        
        for level in range(1, self.scenario_manager.get_max_level() + 1):
            scenario = self.scenario_manager.get_scenario(level)
            for field in required_fields:
                self.assertIn(field, scenario, f"Level {level} missing field: {field}")
    
    def test_file_structure(self):
        """Test that all scenario files have required fields"""
        required_file_fields = ['name', 'current_permissions', 'octal']
        
        for level in range(1, self.scenario_manager.get_max_level() + 1):
            scenario = self.scenario_manager.get_scenario(level)
            self.assertIsInstance(scenario['files'], list)
            self.assertGreater(len(scenario['files']), 0)
            
            for file_info in scenario['files']:
                for field in required_file_fields:
                    self.assertIn(field, file_info, 
                                f"Level {level} file missing field: {field}")

class TestScoreManager(unittest.TestCase):
    """Test the scoring system"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.score_manager = ScoreManager('test_scores.json')
        # Clean up any existing test file
        if os.path.exists('test_scores.json'):
            os.remove('test_scores.json')
    
    def tearDown(self):
        """Clean up after tests"""
        if os.path.exists('test_scores.json'):
            os.remove('test_scores.json')
    
    def test_calculate_points(self):
        """Test point calculation logic"""
        # Test fast completion (should get time bonus)
        points = self.score_manager.calculate_points(1, 5)
        self.assertGreater(points, 100)  # Should be more than base points
        
        # Test slow completion (should get no time bonus)
        points = self.score_manager.calculate_points(1, 60)
        self.assertEqual(points, 100)  # Should be just base points
        
        # Test higher level (should get difficulty multiplier)
        points = self.score_manager.calculate_points(5, 10)
        self.assertGreater(points, 200)  # Should be higher due to difficulty
    
    def test_save_and_retrieve_scores(self):
        """Test saving and retrieving scores"""
        # Save a test score
        self.score_manager.save_score('TestPlayer', 1500, 3)
        
        # Retrieve scores
        scores = self.score_manager.get_top_scores()
        self.assertEqual(len(scores), 1)
        self.assertEqual(scores[0]['player_name'], 'TestPlayer')
        self.assertEqual(scores[0]['score'], 1500)
        self.assertEqual(scores[0]['levels_completed'], 3)
    
    def test_leaderboard_sorting(self):
        """Test that leaderboard is properly sorted"""
        # Save multiple scores
        self.score_manager.save_score('Player1', 1000, 2)
        self.score_manager.save_score('Player2', 2000, 4)
        self.score_manager.save_score('Player3', 1500, 3)
        
        # Retrieve and check order
        scores = self.score_manager.get_top_scores()
        self.assertEqual(len(scores), 3)
        self.assertEqual(scores[0]['player_name'], 'Player2')  # Highest score
        self.assertEqual(scores[1]['player_name'], 'Player3')  # Middle score
        self.assertEqual(scores[2]['player_name'], 'Player1')  # Lowest score
    
    def test_achievements(self):
        """Test achievement system"""
        # Test speed achievement
        achievements = self.score_manager.award_achievement(1, 2, 100)
        self.assertIn('Lightning Fingers ⚡', achievements)
        
        # Test level achievement
        achievements = self.score_manager.award_achievement(1, 10, 100)
        self.assertIn('First Steps 👶', achievements)
        
        # Test score achievement
        achievements = self.score_manager.award_achievement(3, 15, 1200)
        self.assertIn('Point Collector 💎', achievements)

class TestGameIntegration(unittest.TestCase):
    """Integration tests for the complete game system"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.scenario_manager = ScenarioManager()
        self.validator = PermissionValidator()
        self.score_manager = ScoreManager('test_scores_integration.json')
        
        # Clean up any existing test file
        if os.path.exists('test_scores_integration.json'):
            os.remove('test_scores_integration.json')
    
    def tearDown(self):
        """Clean up after tests"""
        if os.path.exists('test_scores_integration.json'):
            os.remove('test_scores_integration.json')
    
    def test_complete_level_flow(self):
        """Test completing a level from start to finish"""
        # Get level 1 scenario
        scenario = self.scenario_manager.get_scenario(1)
        
        # Validate the correct command
        result = self.validator.validate_command(scenario['expected_command'], scenario)
        self.assertTrue(result['correct'])
        
        # Calculate points
        points = self.score_manager.calculate_points(1, result['time_taken'])
        self.assertGreater(points, 0)
        
        # Save score (simulation)
        self.score_manager.save_score('TestPlayer', points, 1)
        
        # Verify score was saved
        scores = self.score_manager.get_top_scores()
        self.assertEqual(len(scores), 1)
        self.assertEqual(scores[0]['score'], points)

if __name__ == '__main__':
    # Create a test suite
    test_suite = unittest.TestSuite()
    
    # Add all test classes
    test_classes = [TestPermissionValidator, TestScenarioManager, 
                   TestScoreManager, TestGameIntegration]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Run the tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Print summary
    print(f"\n{'='*50}")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    print(f"{'='*50}")