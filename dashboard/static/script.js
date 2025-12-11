/**
 * WorkShot Dashboard - Live Activity Tracker
 * Sci-Fi Futuristic Interface
 */

// ═══════════════════════════════════════════════════════════════
// State Management
// ═══════════════════════════════════════════════════════════════

const state = {
    currentActivity: null,
    todayData: null,
    monitorData: null,
    sessions: null,
    eventSource: null
};

// ═══════════════════════════════════════════════════════════════
// App Icons - Multi-Source Icon System  
// ═══════════════════════════════════════════════════════════════

// Primary icon mappings using Iconify API (more reliable than SimpleIcons CDN)
const appIconSources = {
    // Browsers
    'chrome': 'https://api.iconify.design/logos:chrome.svg',
    'firefox': 'https://api.iconify.design/logos:firefox.svg',
    'edge': 'https://api.iconify.design/logos:microsoft-edge.svg',
    'msedge': 'https://api.iconify.design/logos:microsoft-edge.svg',
    'opera': 'https://api.iconify.design/logos:opera.svg',
    'brave': 'https://api.iconify.design/logos:brave.svg',
    'safari': 'https://api.iconify.design/logos:safari.svg',
    'vivaldi': 'https://api.iconify.design/logos:vivaldi.svg',
    'arc': 'https://api.iconify.design/simple-icons:arc.svg',
    
    // Code Editors & IDEs
    'vs code': 'https://api.iconify.design/logos:visual-studio-code.svg',
    'cursor': 'https://api.iconify.design/simple-icons:cursor.svg',
    'visual studio': 'https://api.iconify.design/logos:visual-studio.svg',
    'sublime': 'https://api.iconify.design/logos:sublime-text-icon.svg',
    'atom': 'https://api.iconify.design/logos:atom-icon.svg',
    'notepad++': 'https://api.iconify.design/simple-icons:notepadplusplus.svg',
    'intellij': 'https://api.iconify.design/logos:intellij-idea.svg',
    'pycharm': 'https://api.iconify.design/logos:pycharm.svg',
    'webstorm': 'https://api.iconify.design/logos:webstorm.svg',
    'android studio': 'https://api.iconify.design/logos:android-icon.svg',
    'xcode': 'https://api.iconify.design/logos:xcode.svg',
    
    // Communication
    'discord': 'https://api.iconify.design/logos:discord-icon.svg',
    'slack': 'https://api.iconify.design/logos:slack-icon.svg',
    'teams': 'https://api.iconify.design/logos:microsoft-teams.svg',
    'zoom': 'https://api.iconify.design/logos:zoom-icon.svg',
    'skype': 'https://api.iconify.design/logos:skype.svg',
    'telegram': 'https://api.iconify.design/logos:telegram.svg',
    'whatsapp': 'https://api.iconify.design/logos:whatsapp-icon.svg',
    'messenger': 'https://api.iconify.design/logos:messenger.svg',
    'signal': 'https://api.iconify.design/simple-icons:signal.svg',
    
    // Entertainment & Media
    'spotify': 'https://api.iconify.design/logos:spotify-icon.svg',
    'youtube': 'https://api.iconify.design/logos:youtube-icon.svg',
    'netflix': 'https://api.iconify.design/logos:netflix-icon.svg',
    'twitch': 'https://api.iconify.design/logos:twitch.svg',
    'vlc': 'https://api.iconify.design/simple-icons:vlcmediaplayer.svg',
    
    // Gaming
    'steam': 'https://api.iconify.design/logos:steam-icon.svg',
    'valorant': 'https://api.iconify.design/simple-icons:valorant.svg',
    'epic': 'https://api.iconify.design/simple-icons:epicgames.svg',
    'riot': 'https://api.iconify.design/simple-icons:riotgames.svg',
    'blizzard': 'https://api.iconify.design/simple-icons:blizzard.svg',
    'ubisoft': 'https://api.iconify.design/simple-icons:ubisoft.svg',
    
    // Design & Creative
    'figma': 'https://api.iconify.design/logos:figma.svg',
    'adobe': 'https://api.iconify.design/logos:adobe.svg',
    'photoshop': 'https://api.iconify.design/logos:adobe-photoshop.svg',
    'illustrator': 'https://api.iconify.design/logos:adobe-illustrator.svg',
    'premiere': 'https://api.iconify.design/simple-icons:adobepremierepro.svg',
    'after effects': 'https://api.iconify.design/simple-icons:adobeaftereffects.svg',
    'blender': 'https://api.iconify.design/logos:blender.svg',
    'sketch': 'https://api.iconify.design/logos:sketch.svg',
    'canva': 'https://api.iconify.design/simple-icons:canva.svg',
    'gimp': 'https://api.iconify.design/simple-icons:gimp.svg',
    
    // Development Tools
    'github': 'https://api.iconify.design/logos:github-icon.svg',
    'gitlab': 'https://api.iconify.design/logos:gitlab.svg',
    'bitbucket': 'https://api.iconify.design/logos:bitbucket.svg',
    'git': 'https://api.iconify.design/logos:git-icon.svg',
    'docker': 'https://api.iconify.design/logos:docker-icon.svg',
    'postman': 'https://api.iconify.design/logos:postman-icon.svg',
    'insomnia': 'https://api.iconify.design/simple-icons:insomnia.svg',
    'powershell': 'https://api.iconify.design/devicon-plain:powershell.svg',
    'windowsterminal': 'https://api.iconify.design/simple-icons:windowsterminal.svg',
    'windows terminal': 'https://api.iconify.design/simple-icons:windowsterminal.svg',
    'warp': 'https://api.iconify.design/simple-icons:warp.svg',
    
    // Productivity & Office
    'notion': 'https://api.iconify.design/logos:notion-icon.svg',
    'obsidian': 'https://api.iconify.design/simple-icons:obsidian.svg',
    'evernote': 'https://api.iconify.design/logos:evernote.svg',
    'asana': 'https://api.iconify.design/logos:asana-icon.svg',
    'trello': 'https://api.iconify.design/logos:trello.svg',
    'jira': 'https://api.iconify.design/logos:jira.svg',
    'linear': 'https://api.iconify.design/simple-icons:linear.svg',
    'todoist': 'https://api.iconify.design/simple-icons:todoist.svg',
    'outlook': 'https://api.iconify.design/logos:microsoft-outlook.svg',
    'word': 'https://api.iconify.design/vscode-icons:file-type-word.svg',
    'excel': 'https://api.iconify.design/vscode-icons:file-type-excel.svg',
    'powerpoint': 'https://api.iconify.design/vscode-icons:file-type-powerpoint.svg',
    'onenote': 'https://api.iconify.design/simple-icons:microsoftonenote.svg',
    'onedrive': 'https://api.iconify.design/simple-icons:microsoftonedrive.svg',
    
    // Cloud & Storage
    'dropbox': 'https://api.iconify.design/logos:dropbox.svg',
    'google drive': 'https://api.iconify.design/logos:google-drive.svg',
    
    // Databases
    'mongodb': 'https://api.iconify.design/logos:mongodb-icon.svg',
    'mysql': 'https://api.iconify.design/logos:mysql-icon.svg',
    'postgresql': 'https://api.iconify.design/logos:postgresql.svg',
    'redis': 'https://api.iconify.design/logos:redis.svg',
    
    // 3D & Game Dev
    'unity': 'https://api.iconify.design/logos:unity.svg',
    'unreal': 'https://api.iconify.design/logos:unreal-engine.svg',
    'godot': 'https://api.iconify.design/simple-icons:godotengine.svg',
    
    // Languages
    'node': 'https://api.iconify.design/logos:nodejs-icon.svg',
    'python': 'https://api.iconify.design/logos:python.svg',
    'rust': 'https://api.iconify.design/logos:rust.svg',
    'go': 'https://api.iconify.design/logos:go.svg',
    
    // Security
    '1password': 'https://api.iconify.design/simple-icons:1password.svg',
    'bitwarden': 'https://api.iconify.design/simple-icons:bitwarden.svg',
    'lastpass': 'https://api.iconify.design/simple-icons:lastpass.svg',
    'norton': 'https://api.iconify.design/simple-icons:norton.svg',
    
    // Other
    'deepl': 'https://api.iconify.design/simple-icons:deepl.svg',
    'openvpn': 'https://api.iconify.design/simple-icons:openvpn.svg',
    
    // Windows System Apps (using fluent icons)
    'file explorer': 'https://api.iconify.design/fluent:folder-24-filled.svg',
    'explorer': 'https://api.iconify.design/fluent:folder-24-filled.svg',
    'notepad': 'https://api.iconify.design/fluent:notepad-24-regular.svg',
    'snipping': 'https://api.iconify.design/fluent:screenshot-24-regular.svg',
    'snippingtool': 'https://api.iconify.design/fluent:screenshot-24-regular.svg',
    'calculator': 'https://api.iconify.design/fluent:calculator-24-regular.svg',
    'photos': 'https://api.iconify.design/fluent:image-24-filled.svg',
    'paint': 'https://api.iconify.design/fluent:paint-brush-24-regular.svg',
    'settings': 'https://api.iconify.design/fluent:settings-24-filled.svg',
    'control panel': 'https://api.iconify.design/fluent:settings-24-regular.svg',
    'task manager': 'https://api.iconify.design/fluent:task-list-square-24-filled.svg',
    'taskmgr': 'https://api.iconify.design/fluent:task-list-square-24-filled.svg',
    'mail': 'https://api.iconify.design/fluent:mail-24-filled.svg',
    'calendar': 'https://api.iconify.design/fluent:calendar-24-filled.svg',
    'shellexperiencehost': 'https://api.iconify.design/fluent:window-24-filled.svg',
    'microsoft store': 'https://api.iconify.design/fluent:store-microsoft-24-filled.svg',
    'store': 'https://api.iconify.design/fluent:store-microsoft-24-filled.svg',
    
    // Special states
    'idle': 'https://api.iconify.design/icon-park-outline:sleep-one.svg',
};

// Generic fallback icons for unknown apps by category
const genericIcons = {
    // Terminal/Shell apps fallback
    'terminal': 'https://api.iconify.design/fluent:window-console-20-filled.svg',
    'shell': 'https://api.iconify.design/fluent:window-console-20-filled.svg',
    'cmd': 'https://api.iconify.design/fluent:window-console-20-filled.svg',
    'bash': 'https://api.iconify.design/fluent:window-console-20-filled.svg',
};

function getAppIconUrl(appName) {
    const lower = appName.toLowerCase();
    
    // Try specific app icons first
    for (const [key, url] of Object.entries(appIconSources)) {
        if (lower.includes(key)) {
            return url;
        }
    }
    
    // Try generic category icons
    for (const [key, url] of Object.entries(genericIcons)) {
        if (lower.includes(key)) {
            return url;
        }
    }
    
    // Final fallback: generic app icon
    return 'https://api.iconify.design/fluent:app-generic-24-filled.svg';
}

function getAppInitial(appName) {
    // Get first letter, handling special cases
    const cleaned = appName.replace(/[^a-zA-Z0-9]/g, '');
    return cleaned.charAt(0).toUpperCase() || '?';
}

function createAppIconHtml(appName, size = 'normal') {
    const iconUrl = getAppIconUrl(appName); // Always returns a URL (specific, category, or generic fallback)
    const sizeClass = size === 'large' ? 'app-icon-img-large' : 'app-icon-img';
    
    return `<img src="${iconUrl}" alt="${appName}" class="${sizeClass}">`;
}

// ═══════════════════════════════════════════════════════════════
// DOM Elements (initialized after DOM loads)
// ═══════════════════════════════════════════════════════════════

let elements = {};

function initElements() {
    elements = {
        currentAppIcon: document.getElementById('current-app-icon'),
        currentAppName: document.getElementById('current-app-name'),
        currentWindowTitle: document.getElementById('current-window-title'),
        currentTimer: document.getElementById('current-timer'),
        currentMonitor: document.getElementById('current-monitor'),
        totalTime: document.getElementById('total-time'),
        totalApps: document.getElementById('total-apps'),
        totalSessions: document.getElementById('total-sessions'),
        appList: document.getElementById('app-list'),
        monitor1Time: document.getElementById('monitor-1-time'),
        monitor2Time: document.getElementById('monitor-2-time'),
        sessionLog: document.getElementById('session-log')
    };
}

// ═══════════════════════════════════════════════════════════════
// API Functions
// ═══════════════════════════════════════════════════════════════

async function fetchTodayData() {
    try {
        const response = await fetch('/api/today');
        state.todayData = await response.json();
        renderTodayData();
    } catch (err) {
        console.error('Error fetching today data:', err);
    }
}

async function fetchMonitorData() {
    try {
        const response = await fetch('/api/monitors');
        state.monitorData = await response.json();
        renderMonitorData();
    } catch (err) {
        console.error('Error fetching monitor data:', err);
    }
}

async function fetchSessions() {
    try {
        const response = await fetch('/api/sessions?limit=10'); // Reduced from 15 for faster loading
        state.sessions = await response.json();
        renderSessions();
    } catch (err) {
        console.error('Error fetching sessions:', err);
    }
}

// ═══════════════════════════════════════════════════════════════
// SSE Live Updates
// ═══════════════════════════════════════════════════════════════

function connectSSE() {
    if (state.eventSource) {
        state.eventSource.close();
    }

    state.eventSource = new EventSource('/api/stream');

    state.eventSource.onmessage = (event) => {
        try {
            const data = JSON.parse(event.data);
            state.currentActivity = data;
            renderCurrentActivity();
        } catch (err) {
            console.error('SSE parse error:', err);
        }
    };

    state.eventSource.onerror = (err) => {
        console.error('SSE error:', err);
        // Reconnect after 5 seconds
        setTimeout(connectSSE, 5000);
    };
}

// ═══════════════════════════════════════════════════════════════
// Render Functions
// ═══════════════════════════════════════════════════════════════

function renderCurrentActivity() {
    const activity = state.currentActivity;

    if (!activity || activity.status === 'idle') {
        elements.currentAppIcon.innerHTML = createAppIconHtml('Idle', 'large');
        elements.currentAppName.textContent = activity?.is_idle ? 'Idle' : 'No Activity';
        elements.currentWindowTitle.textContent = activity?.is_idle ? 'User is idle - not tracking' : 'No active window detected';
        elements.currentTimer.textContent = activity?.idle_duration_formatted || '00:00';
        elements.currentMonitor.textContent = 'Monitor -';
        return;
    }

    const appName = activity.app_display || activity.app_name;
    elements.currentAppIcon.innerHTML = createAppIconHtml(appName, 'large');
    elements.currentAppName.textContent = appName;
    elements.currentWindowTitle.textContent = truncateText(activity.window_title, 80);
    elements.currentTimer.textContent = activity.elapsed_formatted || formatDuration(activity.elapsed_seconds);
    elements.currentMonitor.textContent = `Monitor ${activity.monitor}`;
}

function renderTodayData() {
    const data = state.todayData;
    if (!data) return;

    // Update stats
    elements.totalTime.textContent = data.total_formatted || '0s';
    elements.totalApps.textContent = data.summary?.length || 0;
    
    // Count total sessions
    const totalSessions = data.summary?.reduce((acc, item) => acc + (item.session_count || 0), 0) || 0;
    elements.totalSessions.textContent = totalSessions;

    // Render app list
    if (!data.summary || data.summary.length === 0) {
        elements.appList.innerHTML = `
            <div class="empty-state">
                <p>No activity recorded yet today</p>
            </div>
        `;
        return;
    }

    const maxTime = Math.max(...data.summary.map(item => item.total_seconds));

    elements.appList.innerHTML = data.summary.map(item => {
        const appName = item.app_display || item.app_name;
        const percentage = maxTime > 0 ? (item.total_seconds / maxTime) * 100 : 0;

        return `
            <div class="app-item">
                <div class="app-icon">${createAppIconHtml(appName)}</div>
                <div class="app-info">
                    <div class="app-name">${appName}</div>
                    <div class="app-sessions">${item.session_count} session${item.session_count !== 1 ? 's' : ''}</div>
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: ${percentage}%"></div>
                    </div>
                </div>
                <div class="app-time">${item.duration_formatted}</div>
            </div>
        `;
    }).join('');
}

function renderMonitorData() {
    const data = state.monitorData;
    if (!data || data.length === 0) {
        elements.monitor1Time.textContent = '0s';
        elements.monitor2Time.textContent = '0s';
        return;
    }

    const monitor1 = data.find(m => m.monitor === 1);
    const monitor2 = data.find(m => m.monitor === 2);

    elements.monitor1Time.textContent = monitor1?.duration_formatted || '0s';
    elements.monitor2Time.textContent = monitor2?.duration_formatted || '0s';
}

function renderSessions() {
    const sessions = state.sessions;

    if (!sessions || sessions.length === 0) {
        elements.sessionLog.innerHTML = `
            <div class="empty-state">
                <p>No sessions recorded yet</p>
            </div>
        `;
        return;
    }

    elements.sessionLog.innerHTML = sessions.map(session => {
        const isIdle = session.is_idle || session.app_name === 'Idle';
        const appName = session.app_display || session.app_name;
        //const itemClass = isIdle ? 'session-item session-idle' : 'session-item';
        
        return `
            <div class="session-item">
                <span class="session-time">${session.start_formatted || '--:--'}</span>
                <span class="session-app">${appName}</span>
                <span class="session-title">${isIdle ? 'User was idle' : truncateText(session.window_title, 40)}</span>
                <span class="session-duration">${session.duration_formatted}</span>
                <span class="session-monitor">${isIdle ? '-' : 'M' + session.monitor}</span>
            </div>
        `;
    }).join('');
}

// ═══════════════════════════════════════════════════════════════
// Utility Functions
// ═══════════════════════════════════════════════════════════════

function truncateText(text, maxLength) {
    if (!text) return '';
    if (text.length <= maxLength) return text;
    return text.substring(0, maxLength - 3) + '...';
}

function formatDuration(seconds) {
    if (!seconds || seconds < 0) return '0s';

    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const secs = seconds % 60;

    if (hours > 0) {
        return `${hours}h ${minutes}m`;
    } else if (minutes > 0) {
        return `${minutes}m ${secs}s`;
    }
    return `${secs}s`;
}

// ═══════════════════════════════════════════════════════════════
// Initialization
// ═══════════════════════════════════════════════════════════════

function init() {
    console.log('🚀 WorkShot Dashboard initializing...');

    // Initialize DOM element references
    initElements();

    // Show loading state
    if (elements.appList) {
        elements.appList.innerHTML = '<div class="empty-state"><p>Loading...</p></div>';
    }
    if (elements.sessionLog) {
        elements.sessionLog.innerHTML = '<div class="empty-state"><p>Loading...</p></div>';
    }

    // Initial data fetch - parallel requests
    Promise.all([
        fetchTodayData(),
        fetchMonitorData(),
        fetchSessions()
    ]).then(() => {
        console.log('✅ Initial data loaded');
    });

    // Connect to live updates
    connectSSE();

    // Refresh aggregated data every 30 seconds
    setInterval(() => {
        fetchTodayData();
        fetchMonitorData();
        fetchSessions();
    }, 30000);

    console.log('✅ Dashboard ready!');
}

// ═══════════════════════════════════════════════════════════════
// Export Modal Functions
// ═══════════════════════════════════════════════════════════════

let currentPreset = 'all';

function openExportModal() {
    const modal = document.getElementById('export-modal');
    modal.classList.add('active');
    
    // Set default dates
    const today = new Date().toISOString().split('T')[0];
    const startInput = document.getElementById('export-start-date');
    const endInput = document.getElementById('export-end-date');
    
    // Set max date to today (no future dates allowed)
    startInput.max = today;
    endInput.max = today;
    
    startInput.value = today;
    endInput.value = today;
    
    // Default to "all time"
    setPreset('all');
}

function closeExportModal(event) {
    // If event exists and target is not the overlay itself, don't close
    if (event && event.target !== event.currentTarget) return;
    
    const modal = document.getElementById('export-modal');
    modal.classList.remove('active');
}

function setPreset(preset) {
    currentPreset = preset;
    
    const today = new Date();
    let startDate, endDate;
    let label;
    
    switch (preset) {
        case 'today':
            startDate = endDate = formatDateForInput(today);
            label = 'Today';
            break;
            
        case 'yesterday':
            const yesterday = new Date(today);
            yesterday.setDate(yesterday.getDate() - 1);
            startDate = endDate = formatDateForInput(yesterday);
            label = 'Yesterday (Dec 10)';
            break;
            
        case 'week':
            // Get start of week (Monday)
            const weekStart = new Date(today);
            const dayOfWeek = today.getDay();
            const diff = dayOfWeek === 0 ? 6 : dayOfWeek - 1; // Adjust for Monday start
            weekStart.setDate(today.getDate() - diff);
            startDate = formatDateForInput(weekStart);
            endDate = formatDateForInput(today);
            label = 'This Week';
            break;
            
        case 'month':
            const monthStart = new Date(today.getFullYear(), today.getMonth(), 1);
            startDate = formatDateForInput(monthStart);
            endDate = formatDateForInput(today);
            label = 'This Month (December)';
            break;
            
        case 'all':
        default:
            startDate = '';
            endDate = '';
            label = 'All Time';
            break;
    }
    
    // Update date inputs
    document.getElementById('export-start-date').value = startDate;
    document.getElementById('export-end-date').value = endDate;
    
    // Update preset button states
    document.querySelectorAll('.preset-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    event?.target?.classList.add('active');
    
    // Update selected range display
    updateSelectedRangeDisplay(label, startDate, endDate);
}

function updatePresetSelection() {
    // When custom dates are selected, clear preset selection
    currentPreset = 'custom';
    document.querySelectorAll('.preset-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    
    const startDate = document.getElementById('export-start-date').value;
    const endDate = document.getElementById('export-end-date').value;
    
    let label = 'Custom Range';
    if (startDate && endDate) {
        if (startDate === endDate) {
            label = startDate;
        } else {
            label = `${startDate} to ${endDate}`;
        }
    }
    
    updateSelectedRangeDisplay(label, startDate, endDate);
}

function updateSelectedRangeDisplay(label, startDate, endDate) {
    const display = document.getElementById('selected-range');
    display.innerHTML = `Exporting: <strong>${label}</strong>`;
}

function formatDateForInput(date) {
    return date.toISOString().split('T')[0];
}

function exportWithDates(format) {
    const startDate = document.getElementById('export-start-date').value;
    const endDate = document.getElementById('export-end-date').value;
    
    // Build URL with date parameters
    let url = `/api/export/${format}`;
    const params = [];
    
    if (startDate) params.push(`start=${startDate}`);
    if (endDate) params.push(`end=${endDate}`);
    
    if (params.length > 0) {
        url += '?' + params.join('&');
    }
    
    // Get the clicked button
    const btn = event.target.closest('.format-btn');
    const originalHTML = btn.innerHTML;
    
    // Show loading state
    btn.innerHTML = '<span class="format-icon">⏳</span><span class="format-name">Exporting...</span><span class="format-desc">Please wait</span>';
    btn.disabled = true;
    
    // Trigger download
    fetch(url)
        .then(response => {
            if (!response.ok) throw new Error('Export failed');
            return response.blob();
        })
        .then(blob => {
            // Generate filename
            const timestamp = new Date().toISOString().slice(0, 19).replace(/[T:]/g, '-');
            const ext = format === 'html' ? 'html' : format;
            const dateRange = startDate ? `_${startDate}` + (endDate && endDate !== startDate ? `_to_${endDate}` : '') : '';
            const filename = format === 'html' ? `report${dateRange}_${timestamp}.${ext}` : `sessions${dateRange}_${timestamp}.${ext}`;
            
            // Create download link
            const downloadUrl = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = downloadUrl;
            a.download = filename;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(downloadUrl);
            a.remove();
            
            // Success feedback
            btn.innerHTML = '<span class="format-icon">✅</span><span class="format-name">Done!</span><span class="format-desc">Downloaded</span>';
            setTimeout(() => {
                btn.innerHTML = originalHTML;
                btn.disabled = false;
            }, 2000);
        })
        .catch(err => {
            console.error('Export error:', err);
            btn.innerHTML = '<span class="format-icon">❌</span><span class="format-name">Failed</span><span class="format-desc">Try again</span>';
            setTimeout(() => {
                btn.innerHTML = originalHTML;
                btn.disabled = false;
            }, 2000);
        });
}

// Close modal on Escape key
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        closeExportModal();
    }
});

// Start when DOM is ready
document.addEventListener('DOMContentLoaded', init);


