/**
 * ChmodHero Game JavaScript
 * Handles frontend interactions and game logic
 */

// Game state
let gameState = {
    currentLevel: 1,
    score: 0,
    lives: 3,
    startTime: Date.now()
};

// Initialize game when page loads
document.addEventListener('DOMContentLoaded', function() {
    initializeGame();
});

function initializeGame() {
    // Focus on command input if it exists
    const commandInput = document.getElementById('command-input');
    if (commandInput) {
        commandInput.focus();
        
        // Add Enter key listener
        commandInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                submitCommand();
            }
        });
        
        // Add command history (up/down arrows)
        addCommandHistory(commandInput);
    }
    
    // Initialize tooltips if Bootstrap is available
    if (typeof bootstrap !== 'undefined') {
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }
    
    // Add smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });
}

function addCommandHistory(input) {
    let commandHistory = JSON.parse(localStorage.getItem('chmodHeroHistory') || '[]');
    let historyIndex = -1;
    
    input.addEventListener('keydown', function(e) {
        if (e.key === 'ArrowUp') {
            e.preventDefault();
            if (historyIndex < commandHistory.length - 1) {
                historyIndex++;
                input.value = commandHistory[commandHistory.length - 1 - historyIndex] || '';
            }
        } else if (e.key === 'ArrowDown') {
            e.preventDefault();
            if (historyIndex > 0) {
                historyIndex--;
                input.value = commandHistory[commandHistory.length - 1 - historyIndex] || '';
            } else if (historyIndex === 0) {
                historyIndex = -1;
                input.value = '';
            }
        }
    });
    
    // Save command to history when submitted
    window.saveToHistory = function(command) {
        if (command && !commandHistory.includes(command)) {
            commandHistory.push(command);
            if (commandHistory.length > 20) { // Keep only last 20 commands
                commandHistory.shift();
            }
            localStorage.setItem('chmodHeroHistory', JSON.stringify(commandHistory));
        }
    };
}

function submitCommand() {
    const commandInput = document.getElementById('command-input');
    const command = commandInput.value.trim();
    
    if (!command) {
        showNotification('Please enter a command!', 'warning');
        return;
    }
    
    // Save to history
    if (window.saveToHistory) {
        window.saveToHistory(command);
    }
    
    // Show loading state
    const submitButton = document.querySelector('button[onclick="submitCommand()"]');
    if (submitButton) {
        const originalText = submitButton.innerHTML;
        submitButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Executing...';
        submitButton.disabled = true;
        
        // Submit to server
        fetch('/submit_command', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                command: command,
                level: gameState.currentLevel,
                start_time: gameState.startTime
            })
        })
        .then(response => response.json())
        .then(data => {
            // Restore button
            submitButton.innerHTML = originalText;
            submitButton.disabled = false;
            
            handleCommandResponse(data);
        })
        .catch(error => {
            submitButton.innerHTML = originalText;
            submitButton.disabled = false;
            showNotification('Error submitting command. Please try again.', 'error');
            console.error('Error:', error);
        });
    }
}

function handleCommandResponse(data) {
    const commandInput = document.getElementById('command-input');
    
    if (data.success) {
        // Success!
        gameState.score = data.new_score;
        updateScoreDisplay(data.new_score);
        
        // Show success animation
        showSuccessAnimation();
        
        // Clear input
        commandInput.value = '';
        
        // Show success modal or message
        if (data.game_complete) {
            showGameCompleteModal(data);
        } else {
            showLevelCompleteModal(data);
        }
        
    } else {
        if (data.game_over) {
            showGameOverModal(data);
        } else {
            // Wrong answer, show feedback
            gameState.lives = data.lives_remaining;
            updateLivesDisplay(data.lives_remaining);
            
            showNotification(data.message, 'error');
            
            if (data.hint) {
                showHint(data.hint);
            }
            
            // Add shake animation to input
            commandInput.classList.add('animate__animated', 'animate__shakeX');
            setTimeout(() => {
                commandInput.classList.remove('animate__animated', 'animate__shakeX');
            }, 1000);
        }
    }
}

function showNotification(message, type = 'info') {
    // Create or update notification element
    let notification = document.getElementById('notification');
    if (!notification) {
        notification = document.createElement('div');
        notification.id = 'notification';
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 9999;
            max-width: 400px;
            border-radius: 8px;
            padding: 15px;
            font-weight: bold;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            transition: all 0.3s ease;
        `;
        document.body.appendChild(notification);
    }
    
    // Set notification style based on type
    const styles = {
        success: 'background: #d4edda; border: 1px solid #c3e6cb; color: #155724;',
        error: 'background: #f8d7da; border: 1px solid #f5c6cb; color: #721c24;',
        warning: 'background: #fff3cd; border: 1px solid #ffeaa7; color: #856404;',
        info: 'background: #d1ecf1; border: 1px solid #bee5eb; color: #0c5460;'
    };
    
    notification.style.cssText += styles[type] || styles.info;
    notification.innerHTML = `
        <div style="display: flex; align-items: center; justify-content: space-between;">
            <span>${message}</span>
            <button onclick="this.parentElement.parentElement.style.display='none'" style="background: none; border: none; font-size: 18px; cursor: pointer;">&times;</button>
        </div>
    `;
    
    notification.style.display = 'block';
    
    // Auto-hide after 5 seconds
    setTimeout(() => {
        if (notification.style.display !== 'none') {
            notification.style.display = 'none';
        }
    }, 5000);
}

function showSuccessAnimation() {
    // Create floating points animation
    const points = document.createElement('div');
    points.innerHTML = '+100';
    points.style.cssText = `
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        font-size: 48px;
        font-weight: bold;
        color: #28a745;
        z-index: 9999;
        pointer-events: none;
        animation: floatUp 2s ease-out forwards;
    `;
    
    // Add CSS animation if not exists
    if (!document.getElementById('float-animation')) {
        const style = document.createElement('style');
        style.id = 'float-animation';
        style.textContent = `
            @keyframes floatUp {
                0% { transform: translate(-50%, -50%) scale(0.5); opacity: 0; }
                20% { transform: translate(-50%, -50%) scale(1.2); opacity: 1; }
                100% { transform: translate(-50%, -200px) scale(1); opacity: 0; }
            }
        `;
        document.head.appendChild(style);
    }
    
    document.body.appendChild(points);
    
    setTimeout(() => {
        points.remove();
    }, 2000);
}

function updateScoreDisplay(newScore) {
    const scoreElement = document.getElementById('current-score');
    if (scoreElement) {
        // Animate score change
        const currentScore = parseInt(scoreElement.textContent) || 0;
        animateNumber(scoreElement, currentScore, newScore, 1000);
    }
}

function updateLivesDisplay(newLives) {
    const livesElement = document.getElementById('lives-count');
    if (livesElement) {
        livesElement.textContent = newLives;
        
        // Add pulse animation for life lost
        livesElement.classList.add('animate__animated', 'animate__pulse');
        setTimeout(() => {
            livesElement.classList.remove('animate__animated', 'animate__pulse');
        }, 1000);
    }
}

function animateNumber(element, start, end, duration) {
    const startTime = Date.now();
    const difference = end - start;
    
    function updateNumber() {
        const elapsed = Date.now() - startTime;
        const progress = Math.min(elapsed / duration, 1);
        
        const current = Math.floor(start + (difference * progress));
        element.textContent = current.toLocaleString();
        
        if (progress < 1) {
            requestAnimationFrame(updateNumber);
        }
    }
    
    updateNumber();
}

function showHint(hintText) {
    const hintBox = document.getElementById('hint-box');
    const hintTextElement = document.getElementById('hint-text');
    
    if (hintBox && hintTextElement) {
        hintTextElement.textContent = hintText;
        hintBox.style.display = 'block';
        
        // Scroll hint into view
        hintBox.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }
}

function showLevelCompleteModal(data) {
    const modal = document.getElementById('successModal');
    if (modal) {
        const messageElement = document.getElementById('success-message');
        const pointsElement = document.getElementById('points-earned');
        
        if (messageElement) messageElement.textContent = data.message;
        if (pointsElement) pointsElement.textContent = data.points;
        
        // Show modal using Bootstrap
        if (typeof bootstrap !== 'undefined') {
            const bsModal = new bootstrap.Modal(modal);
            bsModal.show();
        } else {
            modal.style.display = 'block';
        }
    }
}

function showGameOverModal(data) {
    const modal = document.getElementById('gameOverModal');
    if (modal) {
        const finalScoreElement = document.getElementById('final-score');
        const levelsCompletedElement = document.getElementById('levels-completed');
        
        if (finalScoreElement) finalScoreElement.textContent = data.final_score;
        if (levelsCompletedElement) levelsCompletedElement.textContent = gameState.currentLevel - 1;
        
        // Show modal
        if (typeof bootstrap !== 'undefined') {
            const bsModal = new bootstrap.Modal(modal);
            bsModal.show();
        } else {
            modal.style.display = 'block';
        }
    }
}

function nextLevel() {
    window.location.href = '/game';
}

function resetGame() {
    if (confirm('Are you sure you want to reset your progress?')) {
        fetch('/reset_game', {
            method: 'POST'
        })
        .then(() => {
            window.location.href = '/game';
        })
        .catch(error => {
            console.error('Error resetting game:', error);
            showNotification('Error resetting game. Please refresh the page.', 'error');
        });
    }
}

function playAgain() {
    resetGame();
}

function saveScore() {
    const playerName = document.getElementById('player-name').value.trim();
    if (!playerName) {
        showNotification('Please enter your name!', 'warning');
        return;
    }
    
    // Note: In a real implementation, you'd save this to the server
    showNotification('Score saved successfully!', 'success');
    setTimeout(() => {
        window.location.href = '/leaderboard';
    }, 1500);
}

// Utility functions
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        showNotification('Copied to clipboard!', 'success');
    }).catch(() => {
        showNotification('Failed to copy to clipboard', 'error');
    });
}

function shareScore(score, level) {
    const text = `I just scored ${score} points on level ${level} in ChmodHero! 🎮 Master Linux permissions through fun DevOps scenarios. Try it yourself!`;
    
    if (navigator.share) {
        navigator.share({
            title: 'ChmodHero Score',
            text: text,
            url: window.location.origin
        });
    } else {
        copyToClipboard(text);
    }
}

// Export functions for global use
window.submitCommand = submitCommand;
window.showHint = showHint;
window.nextLevel = nextLevel;
window.resetGame = resetGame;
window.playAgain = playAgain;
window.saveScore = saveScore;