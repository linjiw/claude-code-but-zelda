// Zelda Claude Code NPM Package
// Main library entry point

const path = require('path');
const fs = require('fs');
const { execSync } = require('child_process');

class ZeldaClaudeCode {
    constructor() {
        this.packageDir = path.join(__dirname, '..');
        this.homeDir = process.env.HOME || process.env.USERPROFILE;
        this.zeldaDir = path.join(this.homeDir, '.zelda');
        this.configFile = path.join(this.zeldaDir, 'config.json');
        this.statsFile = path.join(this.zeldaDir, 'stats.json');
    }

    // Play a sound
    playSound(soundName) {
        const scriptPath = path.join(this.packageDir, 'scripts', 'play_sound.py');
        try {
            execSync(`python3 "${scriptPath}" ${soundName}`, { stdio: 'ignore' });
            return true;
        } catch (e) {
            return false;
        }
    }

    // Get statistics
    getStats() {
        if (!fs.existsSync(this.statsFile)) {
            return null;
        }
        try {
            return JSON.parse(fs.readFileSync(this.statsFile, 'utf8'));
        } catch (e) {
            return null;
        }
    }

    // Get configuration
    getConfig() {
        if (!fs.existsSync(this.configFile)) {
            return {};
        }
        try {
            return JSON.parse(fs.readFileSync(this.configFile, 'utf8'));
        } catch (e) {
            return {};
        }
    }

    // Update configuration
    setConfig(key, value) {
        let config = this.getConfig();
        
        // Handle nested keys
        const keys = key.split('.');
        let current = config;
        for (let i = 0; i < keys.length - 1; i++) {
            if (!current[keys[i]]) current[keys[i]] = {};
            current = current[keys[i]];
        }
        current[keys[keys.length - 1]] = value;
        
        // Save config
        if (!fs.existsSync(this.zeldaDir)) {
            fs.mkdirSync(this.zeldaDir, { recursive: true });
        }
        fs.writeFileSync(this.configFile, JSON.stringify(config, null, 2));
        return true;
    }

    // Check if installed
    isInstalled() {
        const settingsFile = path.join(this.homeDir, '.claude', 'settings.json');
        if (!fs.existsSync(settingsFile)) {
            return false;
        }
        try {
            const settings = JSON.parse(fs.readFileSync(settingsFile, 'utf8'));
            return settings.hooks && settings.hooks.PostToolUse && 
                   settings.hooks.PostToolUse.includes('zelda_hook');
        } catch (e) {
            return false;
        }
    }

    // Run installation
    install() {
        const installScript = path.join(this.packageDir, 'install.sh');
        if (fs.existsSync(installScript)) {
            try {
                execSync(`bash "${installScript}"`, { stdio: 'inherit' });
                return true;
            } catch (e) {
                return false;
            }
        }
        return false;
    }
}

module.exports = ZeldaClaudeCode;