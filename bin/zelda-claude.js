#!/usr/bin/env node

const { program } = require('commander');
const path = require('path');
const { execSync } = require('child_process');
const fs = require('fs');
const chalk = require('chalk');
const ora = require('ora');

const packageDir = path.join(__dirname, '..');
const version = require('../package.json').version;

// Helper to run Python scripts
function runPythonScript(scriptPath, args = '') {
    try {
        const fullPath = path.join(packageDir, scriptPath);
        const result = execSync(`python3 "${fullPath}" ${args}`, { 
            stdio: 'inherit',
            cwd: packageDir 
        });
        return true;
    } catch (error) {
        console.error(chalk.red(`Error running ${scriptPath}: ${error.message}`));
        return false;
    }
}

// Helper to run shell scripts
function runShellScript(scriptPath) {
    try {
        const fullPath = path.join(packageDir, scriptPath);
        execSync(`bash "${fullPath}"`, { 
            stdio: 'inherit',
            cwd: packageDir 
        });
        return true;
    } catch (error) {
        console.error(chalk.red(`Error running ${scriptPath}: ${error.message}`));
        return false;
    }
}

program
    .name('zelda-claude')
    .description('Zelda Claude Code - Transform your coding into an epic adventure!')
    .version(version);

// Install command
program
    .command('install')
    .description('Install or reinstall Zelda Claude Code hooks')
    .action(() => {
        console.log(chalk.cyan('\n🎮 Installing Zelda Claude Code...\n'));
        const spinner = ora('Running installation...').start();
        
        // Run the install script
        const installScript = path.join(packageDir, 'install.sh');
        if (fs.existsSync(installScript)) {
            try {
                execSync(`bash "${installScript}"`, { 
                    stdio: 'inherit',
                    cwd: packageDir 
                });
                spinner.succeed('Installation complete!');
                console.log(chalk.green('\n✅ Zelda Claude Code installed successfully!'));
                console.log(chalk.yellow('⚠️  Remember to restart Claude Code'));
            } catch (error) {
                spinner.fail('Installation failed');
                console.error(chalk.red(error.message));
            }
        } else {
            // Fallback to Node.js installation
            require('../postinstall.js');
        }
    });

// Demo command
program
    .command('demo')
    .description('Play all Zelda sounds in sequence')
    .action(() => {
        console.log(chalk.cyan('\n🎵 Playing Zelda sound demo...\n'));
        runShellScript('demo_sounds.sh');
    });

// Test command
program
    .command('test')
    .description('Run comprehensive test suite')
    .option('-i, --integration', 'Run integration tests')
    .option('-p, --performance', 'Run performance tests')
    .action((options) => {
        console.log(chalk.cyan('\n🧪 Running tests...\n'));
        
        if (options.integration) {
            runPythonScript('test_integration.py');
        } else if (options.performance) {
            runPythonScript('test_performance.py');
        } else {
            runPythonScript('test_zelda_system.py');
        }
    });

// Play command
program
    .command('play <sound>')
    .description('Play a specific sound (success, error, achievement, etc.)')
    .action((sound) => {
        console.log(chalk.cyan(`\n🔊 Playing ${sound} sound...\n`));
        runPythonScript('scripts/play_sound.py', sound);
    });

// Stats command
program
    .command('stats')
    .description('View your Zelda coding statistics')
    .action(() => {
        const statsFile = path.join(process.env.HOME, '.zelda', 'stats.json');
        if (fs.existsSync(statsFile)) {
            try {
                const stats = JSON.parse(fs.readFileSync(statsFile, 'utf8'));
                console.log(chalk.cyan('\n📊 Your Zelda Coding Stats:\n'));
                console.log(chalk.white('Session Stats:'));
                console.log(`  Commands: ${stats.session?.total_commands || 0}`);
                console.log(`  Success Rate: ${stats.session?.success_rate || 0}%`);
                console.log(`  Current Combo: ${stats.session?.current_combo || 0}`);
                console.log(chalk.white('\nAll-Time Stats:'));
                console.log(`  Total Commands: ${stats.all_time?.total_commands || 0}`);
                console.log(`  Best Combo: ${stats.all_time?.best_combo || 0}`);
                console.log(`  Achievements: ${stats.achievements?.unlocked?.length || 0}/11`);
            } catch (e) {
                console.log(chalk.yellow('No stats available yet. Start coding!'));
            }
        } else {
            console.log(chalk.yellow('No stats file found. Start using Claude Code!'));
        }
    });

// Config command
program
    .command('config [key] [value]')
    .description('View or update configuration')
    .action((key, value) => {
        const configFile = path.join(process.env.HOME, '.zelda', 'config.json');
        let config = {};
        
        if (fs.existsSync(configFile)) {
            config = JSON.parse(fs.readFileSync(configFile, 'utf8'));
        }
        
        if (!key) {
            // Show all config
            console.log(chalk.cyan('\n⚙️  Current Configuration:\n'));
            console.log(JSON.stringify(config, null, 2));
        } else if (!value) {
            // Show specific config
            console.log(chalk.cyan(`\n${key}: ${JSON.stringify(config[key])}\n`));
        } else {
            // Set config
            // Handle nested keys like "sounds.enabled"
            const keys = key.split('.');
            let current = config;
            for (let i = 0; i < keys.length - 1; i++) {
                if (!current[keys[i]]) current[keys[i]] = {};
                current = current[keys[i]];
            }
            
            // Parse value
            let parsedValue = value;
            if (value === 'true') parsedValue = true;
            else if (value === 'false') parsedValue = false;
            else if (!isNaN(value)) parsedValue = Number(value);
            
            current[keys[keys.length - 1]] = parsedValue;
            
            // Save config
            if (!fs.existsSync(path.dirname(configFile))) {
                fs.mkdirSync(path.dirname(configFile), { recursive: true });
            }
            fs.writeFileSync(configFile, JSON.stringify(config, null, 2));
            console.log(chalk.green(`✅ Set ${key} = ${parsedValue}`));
        }
    });

// Uninstall command
program
    .command('uninstall')
    .description('Remove Zelda Claude Code hooks')
    .action(() => {
        console.log(chalk.cyan('\n🗑️  Uninstalling Zelda Claude Code...\n'));
        
        const settingsFile = path.join(process.env.HOME, '.claude', 'settings.json');
        if (fs.existsSync(settingsFile)) {
            try {
                const settings = JSON.parse(fs.readFileSync(settingsFile, 'utf8'));
                if (settings.hooks && settings.hooks.PostToolUse) {
                    delete settings.hooks.PostToolUse;
                    fs.writeFileSync(settingsFile, JSON.stringify(settings, null, 2));
                    console.log(chalk.green('✅ Removed Claude Code hooks'));
                }
            } catch (e) {
                console.error(chalk.red('Error updating settings.json'));
            }
        }
        
        console.log(chalk.yellow('Note: ~/.zelda directory preserved for stats'));
        console.log(chalk.green('\n✅ Uninstall complete'));
    });

// Help info
program.on('--help', () => {
    console.log('');
    console.log('Examples:');
    console.log('  $ zelda-claude install        # Install hooks');
    console.log('  $ zelda-claude demo           # Play all sounds');
    console.log('  $ zelda-claude play success   # Play specific sound');
    console.log('  $ zelda-claude test           # Run tests');
    console.log('  $ zelda-claude stats          # View your stats');
    console.log('  $ zelda-claude config         # View configuration');
    console.log('');
    console.log('After installation, use @zelda commands in Claude Code!');
});

program.parse(process.argv);