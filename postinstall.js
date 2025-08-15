#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const os = require('os');
const { execSync } = require('child_process');

console.log('\n🎮 Setting up Zelda Claude Code...\n');

// Determine the installation directory
const packageDir = __dirname;
const homeDir = os.homedir();
const claudeDir = path.join(homeDir, '.claude');
const settingsFile = path.join(claudeDir, 'settings.json');
const zeldaDataDir = path.join(homeDir, '.zelda');

// Create necessary directories
if (!fs.existsSync(claudeDir)) {
    fs.mkdirSync(claudeDir, { recursive: true });
    console.log('✅ Created ~/.claude directory');
}

if (!fs.existsSync(zeldaDataDir)) {
    fs.mkdirSync(path.join(zeldaDataDir, 'sessions'), { recursive: true });
    console.log('✅ Created ~/.zelda directory for stats');
}

// Get the correct Python command
function getPythonCommand() {
    const commands = ['python3', 'python'];
    for (const cmd of commands) {
        try {
            const result = execSync(`${cmd} --version`, { encoding: 'utf8', stdio: 'pipe' });
            if (result.includes('Python 3.')) {
                return cmd;
            }
        } catch (e) {
            continue;
        }
    }
    return 'python3'; // Default fallback
}

// Configure Claude Code hooks with spec-compliant format
function configureHooks() {
    let settings = {};
    
    // Backup existing settings if they exist
    if (fs.existsSync(settingsFile)) {
        try {
            const content = fs.readFileSync(settingsFile, 'utf8');
            settings = JSON.parse(content);
            
            // Create backup
            const backupFile = settingsFile + '.backup.' + Date.now();
            fs.writeFileSync(backupFile, content);
            console.log(`✅ Backed up existing settings to ${path.basename(backupFile)}`);
        } catch (e) {
            console.log('⚠️  Could not parse existing settings.json, creating new one');
        }
    }
    
    // Get Python command and hook path
    const pythonCmd = getPythonCommand();
    const hookPath = path.join(packageDir, 'hooks', 'zelda_hook.py');
    const hookCommand = `${pythonCmd} "${hookPath}"`;
    
    // Create spec-compliant hooks configuration
    const hooksConfig = {
        "PostToolUse": [
            {
                "matcher": "*",
                "hooks": [
                    {
                        "type": "command",
                        "command": hookCommand,
                        "timeout": 5
                    }
                ]
            }
        ],
        "UserPromptSubmit": [
            {
                "hooks": [
                    {
                        "type": "command",
                        "command": hookCommand,
                        "timeout": 5
                    }
                ]
            }
        ],
        "SessionStart": [
            {
                "hooks": [
                    {
                        "type": "command",
                        "command": hookCommand,
                        "timeout": 5
                    }
                ]
            }
        ],
        "Stop": [
            {
                "hooks": [
                    {
                        "type": "command",
                        "command": hookCommand,
                        "timeout": 5
                    }
                ]
            }
        ],
        "Notification": [
            {
                "hooks": [
                    {
                        "type": "command",
                        "command": hookCommand,
                        "timeout": 5
                    }
                ]
            }
        ]
    };
    
    // Add schema if not present
    if (!settings.$schema) {
        settings.$schema = "https://json.schemastore.org/claude-code-settings.json";
    }
    
    // Update hooks with spec-compliant format
    settings.hooks = hooksConfig;
    
    // Write updated settings
    fs.writeFileSync(settingsFile, JSON.stringify(settings, null, 2));
    console.log('✅ Configured Claude Code hooks (spec-compliant)');
}

// Check Python availability
function checkPython() {
    const pythonCmd = getPythonCommand();
    try {
        const result = execSync(`${pythonCmd} --version`, { encoding: 'utf8' });
        if (result.includes('Python 3.')) {
            console.log(`✅ ${pythonCmd} is available`);
            return true;
        }
    } catch (e) {
        // Continue to error message
    }
    
    console.error('❌ Python3 is required but not found');
    console.error('   Please install Python 3.6+ from https://python.org');
    return false;
}

// Test sound playback
function testSoundPlayback() {
    console.log('\n🔊 Testing sound playback...');
    try {
        const pythonCmd = getPythonCommand();
        const testScript = path.join(packageDir, 'scripts', 'play_sound.py');
        execSync(`${pythonCmd} "${testScript}" success`, { stdio: 'ignore', timeout: 3000 });
        console.log('✅ Sound playback works!');
        return true;
    } catch (e) {
        console.log('⚠️  Sound test timed out or failed - sounds may not work on this system');
        return false;
    }
}

// Run universal installer if available
function runUniversalInstaller() {
    const installerPath = path.join(packageDir, 'universal_installer.py');
    if (fs.existsSync(installerPath)) {
        console.log('\n🚀 Running universal installer for comprehensive setup...');
        try {
            const pythonCmd = getPythonCommand();
            execSync(`${pythonCmd} "${installerPath}"`, { stdio: 'inherit' });
            return true;
        } catch (e) {
            console.log('⚠️  Universal installer encountered issues, continuing with basic setup');
        }
    }
    return false;
}

// Main installation
async function install() {
    console.log('📦 Installing Zelda Claude Code from npm package...\n');
    console.log('Version: 3.0.0 - Fully Claude Code Spec Compliant\n');
    
    // Check prerequisites
    if (!checkPython()) {
        process.exit(1);
    }
    
    // Try universal installer first
    const universalSuccess = runUniversalInstaller();
    
    // If universal installer didn't run or failed, do basic setup
    if (!universalSuccess) {
        // Configure hooks with spec-compliant format
        configureHooks();
        
        // Test sound playback
        testSoundPlayback();
    }
    
    console.log('\n' + '='.repeat(50));
    console.log('🎉 Zelda Claude Code installed successfully!');
    console.log('='.repeat(50));
    console.log('\n📋 Installation Summary:');
    console.log('  • Version: 3.0.0');
    console.log('  • Hooks: Spec-compliant configuration');
    console.log('  • Settings: ~/.claude/settings.json');
    console.log('  • Data: ~/.zelda/');
    console.log('\n⚠️  IMPORTANT: Restart Claude Code for changes to take effect');
    console.log('\nAfter restarting:');
    console.log('  • Sounds will play automatically as you code');
    console.log('  • Type @zelda help for available commands');
    console.log('\nVerify installation:');
    console.log('  • npm run test');
    console.log('  • npm run demo');
    console.log('\n🗡️  May the Triforce guide your code! ✨\n');
}

// Run installation
install().catch(console.error);