// Sound map with GitHub Pages URLs
const SOUND_BASE_URL = 'https://raw.githubusercontent.com/linjiw/claude-code-but-zelda/main/sounds/';

const soundMap = {
    // Success sounds
    'success': 'success.wav',
    'puzzle_solved': 'puzzle_solved.wav',
    'test_pass': 'test_pass.wav',
    
    // Error sounds
    'error': 'error.wav',
    'damage': 'damage.wav',
    'game_over': 'game_over.wav',
    
    // Achievement sounds
    'achievement': 'achievement.wav',
    'item_get': 'item_get.wav',
    'secret': 'secret.wav',
    
    // Combo sounds
    'rupee': 'rupee.wav',
    'heart_get': 'heart_get.wav',
    'shrine_complete': 'shrine_complete.wav',
    
    // Task sounds
    'todo_complete': 'todo_complete.wav',
    'file_create': 'file_create.wav',
    'search_found': 'search_found.wav',
    
    // Session sounds
    'session_start': 'session_start.wav',
    'session_night': 'session_night.wav',
    'notification': 'notification.wav'
};

// Terminal simulation state
let terminalStats = {
    commands: 0,
    successes: 0,
    failures: 0,
    currentCombo: 0,
    bestCombo: 0,
    achievements: 0
};

// Initialize audio player
const audioPlayer = document.getElementById('audio-player');
let currentlyPlaying = null;

// Play sound function
function playSound(soundName) {
    const soundFile = soundMap[soundName];
    if (!soundFile) return;
    
    // Visual feedback
    const button = document.querySelector(`[data-sound="${soundName}"]`);
    if (button) {
        button.classList.add('playing');
        setTimeout(() => button.classList.remove('playing'), 500);
    }
    
    // Play audio
    audioPlayer.src = SOUND_BASE_URL + soundFile;
    audioPlayer.play().catch(err => {
        console.log('Audio play failed:', err);
        // Fallback: show visual effect only
    });
}

// Initialize sound buttons
document.addEventListener('DOMContentLoaded', () => {
    // Sound button clicks
    document.querySelectorAll('.sound-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            const sound = btn.dataset.sound;
            playSound(sound);
            
            // Add ripple effect
            const ripple = document.createElement('span');
            ripple.className = 'ripple';
            btn.appendChild(ripple);
            setTimeout(() => ripple.remove(), 600);
        });
    });
    
    // Terminal input handler
    const terminalInput = document.getElementById('terminal-command');
    const terminalOutput = document.getElementById('terminal-output');
    
    if (terminalInput) {
        terminalInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                const command = terminalInput.value.trim();
                if (command) {
                    processCommand(command);
                    terminalInput.value = '';
                }
            }
        });
    }
    
    // Smooth scroll for navigation
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({ behavior: 'smooth' });
            }
        });
    });
    
    // Add sparkle effects on mouse move
    let sparkleTimeout;
    document.addEventListener('mousemove', (e) => {
        clearTimeout(sparkleTimeout);
        sparkleTimeout = setTimeout(() => {
            createSparkle(e.clientX, e.clientY);
        }, 100);
    });
});

// Process terminal commands
function processCommand(command) {
    const output = document.getElementById('terminal-output');
    const lowerCmd = command.toLowerCase();
    
    // Add command to output
    addTerminalLine(`$ ${command}`);
    
    // Simulate different command responses
    let success = false;
    let soundToPlay = null;
    let response = '';
    
    if (lowerCmd.includes('test')) {
        success = Math.random() > 0.2;
        if (success) {
            response = '✅ All tests passed! (42/42)';
            soundToPlay = 'test_pass';
            terminalStats.successes++;
            terminalStats.currentCombo++;
        } else {
            response = '❌ Tests failed! (38/42)';
            soundToPlay = 'error';
            terminalStats.failures++;
            terminalStats.currentCombo = 0;
        }
    } else if (lowerCmd.includes('commit')) {
        success = true;
        response = '🎮 Changes committed successfully!';
        soundToPlay = 'success';
        terminalStats.successes++;
        terminalStats.currentCombo++;
    } else if (lowerCmd.includes('@zelda stats')) {
        success = true;
        response = `📊 Stats: ${terminalStats.commands} commands, ${Math.round((terminalStats.successes / Math.max(1, terminalStats.commands)) * 100)}% success rate, ${terminalStats.currentCombo}x combo`;
        soundToPlay = 'notification';
    } else if (lowerCmd.includes('@zelda')) {
        success = true;
        response = '🎮 Zelda Claude Code v2.1.0 - Ready!';
        soundToPlay = 'item_get';
    } else if (lowerCmd.includes('build')) {
        success = Math.random() > 0.3;
        if (success) {
            response = '🔨 Build completed successfully!';
            soundToPlay = 'puzzle_solved';
            terminalStats.successes++;
            terminalStats.currentCombo++;
        } else {
            response = '💥 Build failed with errors!';
            soundToPlay = 'damage';
            terminalStats.failures++;
            terminalStats.currentCombo = 0;
        }
    } else if (lowerCmd === 'help') {
        success = true;
        response = '💡 Available commands: npm test, git commit, @zelda stats, build, search';
        soundToPlay = 'menu_select';
    } else if (lowerCmd.includes('search')) {
        success = true;
        response = '🔍 Found 42 results!';
        soundToPlay = 'search_found';
        terminalStats.successes++;
        terminalStats.currentCombo++;
    } else {
        success = Math.random() > 0.4;
        if (success) {
            response = '✅ Command executed successfully!';
            soundToPlay = 'success';
            terminalStats.successes++;
            terminalStats.currentCombo++;
        } else {
            response = '❌ Command failed!';
            soundToPlay = 'error';
            terminalStats.failures++;
            terminalStats.currentCombo = 0;
        }
    }
    
    // Update stats
    terminalStats.commands++;
    if (terminalStats.currentCombo > terminalStats.bestCombo) {
        terminalStats.bestCombo = terminalStats.currentCombo;
    }
    
    // Check for combo sounds
    if (terminalStats.currentCombo === 3) {
        soundToPlay = 'rupee';
        response += ' 🔥 3x Combo!';
    } else if (terminalStats.currentCombo === 5) {
        soundToPlay = 'heart_get';
        response += ' 🔥 5x Combo!';
    } else if (terminalStats.currentCombo === 10) {
        soundToPlay = 'shrine_complete';
        response += ' 🔥 10x MEGA COMBO!';
        if (terminalStats.achievements === 0) {
            terminalStats.achievements++;
            setTimeout(() => {
                addTerminalLine('🏆 Achievement Unlocked: Combo Master!');
                playSound('achievement');
            }, 1000);
        }
    }
    
    // Add response
    addTerminalLine(response);
    
    // Play sound
    if (soundToPlay) {
        playSound(soundToPlay);
    }
    
    // Update display stats
    updateStatsDisplay();
}

// Add line to terminal
function addTerminalLine(text) {
    const output = document.getElementById('terminal-output');
    const line = document.createElement('div');
    line.className = 'terminal-line';
    line.textContent = text;
    output.appendChild(line);
    output.scrollTop = output.scrollHeight;
    
    // Remove old lines if too many
    while (output.children.length > 20) {
        output.removeChild(output.firstChild);
    }
}

// Update stats display
function updateStatsDisplay() {
    document.getElementById('stat-commands').textContent = terminalStats.commands;
    document.getElementById('stat-success').textContent = 
        Math.round((terminalStats.successes / Math.max(1, terminalStats.commands)) * 100) + '%';
    document.getElementById('stat-combo').textContent = terminalStats.currentCombo + 'x';
    document.getElementById('stat-achievements').textContent = terminalStats.achievements + '/11';
    
    // Add glow effect for high combos
    const comboDisplay = document.getElementById('stat-combo');
    if (terminalStats.currentCombo >= 5) {
        comboDisplay.style.color = '#f59e0b';
        comboDisplay.style.textShadow = '0 0 20px rgba(245, 158, 11, 0.8)';
    } else if (terminalStats.currentCombo >= 3) {
        comboDisplay.style.color = '#10b981';
        comboDisplay.style.textShadow = '0 0 10px rgba(16, 185, 129, 0.5)';
    } else {
        comboDisplay.style.color = '';
        comboDisplay.style.textShadow = '';
    }
}

// Copy to clipboard
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        // Show feedback
        event.target.textContent = '✅ Copied!';
        setTimeout(() => {
            event.target.textContent = '📋 Copy';
        }, 2000);
    });
}

// Scroll to section
function scrollToSection(sectionId) {
    const section = document.getElementById(sectionId);
    if (section) {
        section.scrollIntoView({ behavior: 'smooth' });
    }
}

// Create sparkle effect
function createSparkle(x, y) {
    const sparkle = document.createElement('div');
    sparkle.className = 'mouse-sparkle';
    sparkle.style.left = x + 'px';
    sparkle.style.top = y + 'px';
    sparkle.style.position = 'fixed';
    sparkle.style.width = '4px';
    sparkle.style.height = '4px';
    sparkle.style.background = 'rgba(74, 222, 128, 0.8)';
    sparkle.style.borderRadius = '50%';
    sparkle.style.pointerEvents = 'none';
    sparkle.style.animation = 'sparkleFade 1s ease-out forwards';
    document.body.appendChild(sparkle);
    setTimeout(() => sparkle.remove(), 1000);
}

// Add sparkle fade animation
const style = document.createElement('style');
style.textContent = `
    @keyframes sparkleFade {
        0% {
            transform: translate(0, 0) scale(1);
            opacity: 1;
        }
        100% {
            transform: translate(0, -20px) scale(0);
            opacity: 0;
        }
    }
    
    .ripple {
        position: absolute;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.5);
        transform: scale(0);
        animation: rippleEffect 0.6s ease-out;
        pointer-events: none;
    }
    
    @keyframes rippleEffect {
        to {
            transform: scale(4);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

// Initialize demo on load
window.addEventListener('load', () => {
    // Play welcome sound after a short delay
    setTimeout(() => {
        playSound('session_start');
        addTerminalLine('🎮 Welcome to Zelda Claude Code Demo!');
        addTerminalLine('Try typing commands like: npm test, git commit, @zelda stats');
    }, 500);
});