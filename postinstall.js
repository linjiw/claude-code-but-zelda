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
    fs.mkdirSync(zeldaDataDir, { recursive: true });
    console.log('✅ Created ~/.zelda directory for stats');
}

// Configure Claude Code hooks
function configureHooks() {
    let settings = {};
    
    // Read existing settings if they exist
    if (fs.existsSync(settingsFile)) {
        try {
            const content = fs.readFileSync(settingsFile, 'utf8');
            settings = JSON.parse(content);
        } catch (e) {
            console.log('⚠️  Could not parse existing settings.json, creating new one');
        }
    }
    
    // Ensure hooks array exists
    if (!settings.hooks) {
        settings.hooks = {};
    }
    
    // Add Zelda hook configuration
    const hookPath = path.join(packageDir, 'hooks', 'zelda_hook.py');
    settings.hooks.PostToolUse = `python3 "${hookPath}"`;
    
    // Write updated settings
    fs.writeFileSync(settingsFile, JSON.stringify(settings, null, 2));
    console.log('✅ Configured Claude Code hooks');
}

// Check Python availability
function checkPython() {
    try {
        execSync('python3 --version', { stdio: 'ignore' });
        console.log('✅ Python3 is available');
        return true;
    } catch (e) {
        console.error('❌ Python3 is required but not found');
        console.error('   Please install Python 3.6+ from https://python.org');
        return false;
    }
}

// Main installation
async function install() {
    console.log('📦 Installing Zelda Claude Code from npm package...\n');
    
    // Check prerequisites
    if (!checkPython()) {
        process.exit(1);
    }
    
    // Configure hooks
    configureHooks();
    
    // Test sound playback
    console.log('\n🔊 Testing sound playback...');
    try {
        const testScript = path.join(packageDir, 'scripts', 'play_sound.py');
        execSync(`python3 "${testScript}" success`, { stdio: 'ignore' });
        console.log('✅ Sound playback works!');
    } catch (e) {
        console.log('⚠️  Sound test failed - sounds may not work on this system');
    }
    
    console.log('\n' + '='.repeat(50));
    console.log('🎉 Zelda Claude Code installed successfully!');
    console.log('='.repeat(50));
    console.log('\n⚠️  IMPORTANT: Restart Claude Code for changes to take effect');
    console.log('\nAfter restarting, type: @zelda help');
    console.log('\n🗡️  May the Triforce guide your code! ✨\n');
}

// Run installation
install().catch(console.error);