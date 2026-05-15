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
            const todayName = today.toLocaleString('default', { day: 'numeric', month: 'long' });
            label = `Today (${todayName})`;
            break;
            
        case 'yesterday':
            const yesterday = new Date(today);
            yesterday.setDate(yesterday.getDate() - 1);
            startDate = endDate = formatDateForInput(yesterday);
            const yesterdayName = yesterday.toLocaleString('default', { day: 'numeric', month: 'long' });
            label = `Yesterday (${yesterdayName})`;
            break;
            
        case 'week':
            // Get start of week (Monday)
            const weekStart = new Date(today);
            const dayOfWeek = today.getDay();
            const diff = dayOfWeek === 0 ? 6 : dayOfWeek - 1; // 5 days ago to today
            const sevenDaysAgo = new Date(weekStart).getDate() - 8; // seven days ago
            weekStart.setDate(today.getDate() - sevenDaysAgo);
            startDate = formatDateForInput(weekStart);
            endDate = formatDateForInput(today);
            const weekName = weekStart.toLocaleString('default', { day: 'numeric', month: 'long' }) + ' - ' + today.toLocaleString('default', { day: 'numeric', month: 'long' });
            label = `This Week (${weekName})`;
            break;
            
        case 'month':
            const monthStart = new Date(today.getFullYear(), today.getMonth(), 1);
            const monthName = new Date(today.getFullYear(), today.getMonth(), 1).toLocaleString('default', { month: 'long' });
            startDate = formatDateForInput(monthStart);
            endDate = formatDateForInput(today);
            label = `This Month (${monthName})`;
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
    
    const startDateName = new Date(startDate).toLocaleString('default', { day: 'numeric', month: 'long' });
    const endDateName = new Date(endDate).toLocaleString('default', { day: 'numeric', month: 'long' });
    
    let label = `Custom Range (${startDateName} - ${endDateName})`;
    
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

async function updateTaskStatus(labelId, newStatus) {
    const response = await fetch(`/api/session-labels/${labelId}/status`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ status: newStatus })
    });

    if (response.ok) {
        const data = await response.json();
        
        if (newStatus === 'done') {
            await loadLabels();
            document.getElementById('active-label-chip').innerHTML = "General";
            document.querySelectorAll('.label-chip').forEach(el => el.classList.remove('active'));
        }
    } else {
        alert("Failed to update status.");
    }
}

function toggleSearchBar() {
    const searchInput = document.getElementById('task-search-input');
    if (searchInput.style.display === 'none') {
        searchInput.style.display = 'block';
        searchInput.focus();
    } else {
        searchInput.style.display = 'none';
        searchInput.value = "";
        executeSearch("");
    }
}

function executeSearch(query) {
    currentSearchQuery = query.toLowerCase();
    loadLabels();
}

function toggleDoneFilter() {
    hideDoneTasks = !hideDoneTasks;
    
    const filterBtn = document.getElementById('filter-done-btn');
    if (hideDoneTasks) {
        filterBtn.style.color = '#5b8def';
        filterBtn.title = "Show Done Tasks";
    } else {
        filterBtn.style.color = '#888';
        filterBtn.title = "Hide Done Tasks";
    }
    
    loadLabels();
}

let currentActiveLabelId = 0;
let currentSearchQuery = "";
let hideDoneTasks = false;

async function loadLabels() {
    const response = await fetch('/api/session-labels');
    const labels = await response.json();
    const container = document.getElementById('label-container');
    
    container.innerHTML = '';

    const taskContainerStyle = 'display: flex; align-items: center; justify-content: space-between; background: #1a1a1f; border-left: 4px solid transparent; padding: 8px 12px; border-radius: 12px; cursor: pointer; margin-bottom: 6px; transition: all 0.2s;';

    const modalActiveLabelRow = document.getElementById('modal-active-label-row');
    if (modalActiveLabelRow) {
        modalActiveLabelRow.style.borderColor = labels.find(label => label.id === currentActiveLabelId)?.color || '#5b8def';
        modalActiveLabelRow.style.filter = `drop-shadow(0 0 5px ${hexToRgba(labels.find(label => label.id === currentActiveLabelId)?.color || '#5b8def', 0.3)})`;
    }

    const activeLabelChip = document.getElementById('active-label-chip');
    if (activeLabelChip) {
        activeLabelChip.style.borderColor = labels.find(label => label.id === currentActiveLabelId)?.color;
        activeLabelChip.style.color = labels.find(label => label.id === currentActiveLabelId)?.color;
    }

    const activeLabelObj = labels.find(label => label.id === currentActiveLabelId);

    const modalActiveLabelName = document.getElementById('modal-active-label-name');
    if (modalActiveLabelName) {
        modalActiveLabelName.innerHTML = currentActiveLabelId === 0 || !activeLabelObj 
            ? "General" 
            : activeLabelObj.name;
    }

    const modalActiveLabelStatus = document.getElementById('modal-active-label-status');
    if (modalActiveLabelStatus) {
        if (currentActiveLabelId === 0 || !activeLabelObj) {
            // General Task Infinity Icon
            modalActiveLabelStatus.innerHTML = `<label style="padding: 3px 8px; color: #e0e0e0; display: flex; align-items: center;">
                <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 14 14"><path fill="currentColor" fill-rule="evenodd" d="M3.564 4.884a1.91 1.91 0 0 0-1.523.542a1.9 1.9 0 0 0-.442.691a2.5 2.5 0 0 0-.08.511c-.02.255-.02.49 0 .744c.02.241.052.434.08.51A1.87 1.87 0 0 0 2.74 9.015c.263.094.545.129.824.102l.07-.003c.373 0 .78-.2 1.271-.68c.392-.384.77-.879 1.172-1.433c-.401-.554-.78-1.049-1.172-1.432c-.491-.482-.898-.681-1.27-.681zM7 8.277a11 11 0 0 1-1.045 1.227c-.598.585-1.352 1.096-2.284 1.109a3.41 3.41 0 0 1-2.687-.974a3.4 3.4 0 0 1-.796-1.246c-.104-.287-.144-.664-.163-.9A6 6 0 0 1 0 7q.001-.247.024-.493c.02-.236.06-.613.163-.9a3.37 3.37 0 0 1 2.048-2.034c.46-.164.95-.227 1.435-.186c.932.013 1.686.524 2.284 1.109c.368.36.716.789 1.045 1.227a11 11 0 0 1 1.045-1.227c.598-.585 1.352-1.096 2.284-1.109a3.41 3.41 0 0 1 2.687.974c.354.352.626.777.796 1.246c.104.287.144.664.163.9q.022.246.025.493q-.002.247-.025.493c-.02.236-.06.613-.163.9a3.37 3.37 0 0 1-2.048 2.034c-.46.164-.95.227-1.435.186c-.932-.013-1.686-.524-2.284-1.109a11 11 0 0 1-1.045-1.227m5.48-.905c-.02.241-.051.434-.079.51a1.87 1.87 0 0 1-1.141 1.132a1.9 1.9 0 0 1-.824.102l-.07-.003c-.373 0-.78-.2-1.271-.68c-.392-.384-.77-.879-1.172-1.433c.401-.554.78-1.049 1.172-1.432c.491-.482.898-.681 1.27-.681l.071-.003a1.91 1.91 0 0 1 1.523.542c.197.196.348.432.442.691c.028.077.06.27.08.511c.02.255.02.49 0 .744" clip-rule="evenodd"/></svg>
            </label>`;
        } else {
            // Status Toggle Button
            modalActiveLabelStatus.innerHTML = `<button id="current-status-toggle-btn" style="padding: 0 8px;" class="status-toggle-btn active status-${activeLabelObj.status}" 
                onclick="event.stopPropagation(); cycleTaskStatus(${activeLabelObj.id}, '${activeLabelObj.status}')" 
                title="Current Status: ${activeLabelObj.status}">
                <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 1024 1024">
                    <path fill="currentColor" d="M512 0C229.232 0 0 229.232 0 512c0 282.784 229.232 512 512 512c282.784 0 512-229.216 512-512C1024 229.232 794.784 0 512 0m0 961.008c-247.024 0-448-201.984-448-449.01c0-247.024 200.976-448 448-448s448 200.977 448 448s-200.976 449.01-448 449.01m204.336-636.352L415.935 626.944l-135.28-135.28c-12.496-12.496-32.752-12.496-45.264 0c-12.496 12.496-12.496 32.752 0 45.248l158.384 158.4c12.496 12.48 32.752 12.48 45.264 0c1.44-1.44 2.673-3.009 3.793-4.64l318.784-320.753c12.48-12.496 12.48-32.752 0-45.263c-12.512-12.496-32.768-12.496-45.28 0"/>
                </svg>
            </button>`;
        }
    }

    const modalActiveLabelDate = document.getElementById('modal-active-label-date');
    if (modalActiveLabelDate) {
        if (currentActiveLabelId === 0 || !activeLabelObj) {
            modalActiveLabelDate.innerHTML = `<label style="color: #fff; width: 20px;">-</label>`;
        } else {
        modalActiveLabelDate.innerHTML = `<button onclick="event.stopPropagation(); openEditModal(${activeLabelObj.id}, '${activeLabelObj.name}', '${activeLabelObj.color}')" 
                    style="background: transparent; border: none; color: inherit;  cursor: pointer;" title="Edit Task">
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10" fill="none" stroke="currentColor" stroke-width="1.5"/><path fill="currentColor" d="m7 14.94l6.06-6.06l2.06 2.06L9.06 17H7zM16.7 9.35l-1 1l-2.05-2.05l1-1c.21-.22.56-.22.77 0l1.28 1.28c.22.21.22.56 0 .77"/></svg>
                </button>
                
                <button onclick="event.stopPropagation(); deleteTask(${activeLabelObj.id})" 
                    style="background: transparent; border: none; color: inherit; cursor: pointer;" title="Delete Task">
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9.172 14.828L12.001 12m2.828-2.828L12.001 12m0 0L9.172 9.172M12.001 12l2.828 2.828M12 22c5.523 0 10-4.477 10-10S17.523 2 12 2S2 6.477 2 12s4.477 10 10 10"/></svg>
                </button>`;

        // FUTURE REFERENCE: when want to show the date of the task, we can use this.
        // if (currentActiveLabelId === 0 || !activeLabelObj || !activeLabelObj.created_at) {
        //     modalActiveLabelDate.innerHTML = "-";
        // } else {
        //     // Format the date properly for the header
        //     const d = new Date(activeLabelObj.created_at + 'Z'); 
        //     modalActiveLabelDate.innerHTML = d.toLocaleDateString(undefined, { month: 'short', day: 'numeric' });
        // }
        }
    }


    // Render 'General' ONLY if it is NOT currently active
    if (currentActiveLabelId !== 0) {
        container.innerHTML += `
            <div class="task-row hoverable-row" 
                onclick="switchLabel(0, 'General', 'todo', '-')"
                style="${taskContainerStyle} padding: 6px 10px;">
                
                <label style="margin: 6px; color: #888; display: flex; align-items: center;">
                    <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 14 14"><path fill="currentColor" fill-rule="evenodd" d="M3.564 4.884a1.91 1.91 0 0 0-1.523.542a1.9 1.9 0 0 0-.442.691a2.5 2.5 0 0 0-.08.511c-.02.255-.02.49 0 .744c.02.241.052.434.08.51A1.87 1.87 0 0 0 2.74 9.015c.263.094.545.129.824.102l.07-.003c.373 0 .78-.2 1.271-.68c.392-.384.77-.879 1.172-1.433c-.401-.554-.78-1.049-1.172-1.432c-.491-.482-.898-.681-1.27-.681zM7 8.277a11 11 0 0 1-1.045 1.227c-.598.585-1.352 1.096-2.284 1.109a3.41 3.41 0 0 1-2.687-.974a3.4 3.4 0 0 1-.796-1.246c-.104-.287-.144-.664-.163-.9A6 6 0 0 1 0 7q.001-.247.024-.493c.02-.236.06-.613.163-.9a3.37 3.37 0 0 1 2.048-2.034c.46-.164.95-.227 1.435-.186c.932.013 1.686.524 2.284 1.109c.368.36.716.789 1.045 1.227a11 11 0 0 1 1.045-1.227c.598-.585 1.352-1.096 2.284-1.109a3.41 3.41 0 0 1 2.687.974c.354.352.626.777.796 1.246c.104.287.144.664.163.9q.022.246.025.493q-.002.247-.025.493c-.02.236-.06.613-.163.9a3.37 3.37 0 0 1-2.048 2.034c-.46.164-.95.227-1.435.186c-.932-.013-1.686-.524-2.284-1.109a11 11 0 0 1-1.045-1.227m5.48-.905c-.02.241-.051.434-.079.51a1.87 1.87 0 0 1-1.141 1.132a1.9 1.9 0 0 1-.824.102l-.07-.003c-.373 0-.78-.2-1.271-.68c-.392-.384-.77-.879-1.172-1.433c.401-.554.78-1.049 1.172-1.432c.491-.482.898-.681 1.27-.681l.071-.003a1.91 1.91 0 0 1 1.523.542c.197.196.348.432.442.691c.028.077.06.27.08.511c.02.255.02.49 0 .744" clip-rule="evenodd"/></svg>
                </label>
                <span id="row-name-0" style="flex-grow: 1; margin-left: 12px; font-size: 14px; color: #888; font-weight: normal;">
                    General
                </span>
                <label style="font-style: italic; font-size: 0.75rem; color: #888; margin-right: 10px; pointer-events: none;">-</label>
            </div>`;
    }

    //Render fetched labels
    labels.forEach(label => {
        if (label.id === currentActiveLabelId) {
            return; 
        }

        if (currentSearchQuery && !label.name.toLowerCase().includes(currentSearchQuery)) {
            return;
        }
        
        if (hideDoneTasks && label.status === 'done') {
            return;
        }

        // Format date
        let dateStr = "";
        if (label.created_at) {
            const d = new Date(label.created_at + 'Z'); 
            dateStr = d.toLocaleDateString(undefined, { month: 'short', day: 'numeric' });
        }

        container.innerHTML += `
        <div class="task-row hoverable-row" 
            onclick="switchLabel(${label.id}, '${label.name}', '${label.status}', '${dateStr}')"
            onmouseover="this.style.borderColor = '${label.color}'; this.style.backgroundColor = 'var(--bg-hover)';"
            onmouseout="this.style.borderColor = 'transparent'; this.style.backgroundColor = '#1a1a1f';"
            style="${taskContainerStyle}">
            
            <div style="display: flex; align-items: center; gap: 12px; flex-grow: 1;">
                <button class="status-toggle-btn status-${label.status}" 
                    onclick="event.stopPropagation(); cycleTaskStatus(${label.id}, '${label.status}')" 
                    title="Current Status: ${label.status}">
                    <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 1024 1024"><path fill="currentColor" d="M512 0C229.232 0 0 229.232 0 512c0 282.784 229.232 512 512 512c282.784 0 512-229.216 512-512C1024 229.232 794.784 0 512 0m0 961.008c-247.024 0-448-201.984-448-449.01c0-247.024 200.976-448 448-448s448 200.977 448 448s-200.976 449.01-448 449.01m204.336-636.352L415.935 626.944l-135.28-135.28c-12.496-12.496-32.752-12.496-45.264 0c-12.496 12.496-12.496 32.752 0 45.248l158.384 158.4c12.496 12.48 32.752 12.48 45.264 0c1.44-1.44 2.673-3.009 3.793-4.64l318.784-320.753c12.48-12.496 12.48-32.752 0-45.263c-12.512-12.496-32.768-12.496-45.28 0"/></svg>
                </button>

                <span id="row-name-${label.id}" style="flex-grow: 1; font-weight: normal; color: #888; font-size: 14px;">
                    ${label.name}
                </span>
                
                <div style="font-style: italic; font-size: 0.75rem; color: #444444; display: flex; align-items: end; gap: 0.3rem;">
                    
                <button onclick="event.stopPropagation(); openEditModal(${label.id}, '${label.name}', '${label.color}')" 
                    style="background: transparent; border: none; color: inherit;  cursor: pointer;" title="Edit Task">
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10" fill="none" stroke="currentColor" stroke-width="1.5"/><path fill="currentColor" d="m7 14.94l6.06-6.06l2.06 2.06L9.06 17H7zM16.7 9.35l-1 1l-2.05-2.05l1-1c.21-.22.56-.22.77 0l1.28 1.28c.22.21.22.56 0 .77"/></svg>
                </button>
                
                <button onclick="event.stopPropagation(); deleteTask(${label.id})" 
                    style="background: transparent; border: none; color: inherit; cursor: pointer;" title="Delete Task">
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9.172 14.828L12.001 12m2.828-2.828L12.001 12m0 0L9.172 9.172M12.001 12l2.828 2.828M12 22c5.523 0 10-4.477 10-10S17.523 2 12 2S2 6.477 2 12s4.477 10 10 10"/></svg>
                </button>
                </div>
            </div>

        
        </div>
        `;
    });
}

async function cycleTaskStatus(labelId, currentStatus) {
    let nextStatus = 'todo';
    if (currentStatus === 'todo') nextStatus = 'partial';
    else if (currentStatus === 'partial') nextStatus = 'done';
    else if (currentStatus === 'done') nextStatus = 'todo';

    const response = await fetch(`/api/session-labels/${labelId}/status`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ status: nextStatus })
    });

    if (response.ok) {
        await loadLabels();
        
        if (nextStatus === 'done') {
            const activeHeaderChip = document.getElementById('active-label-chip');
            if (activeHeaderChip && activeHeaderChip.innerHTML.includes(labelId)) {
                activeHeaderChip.innerHTML = "General";
                document.querySelectorAll('.label-chip').forEach(el => el.classList.remove('active'));
            }
        }
    } else {
        const errorData = await response.json();
        console.error("Backend Crash Details:", errorData);
        alert(`Server Crash: ${errorData.detail}`);
    }
}

async function switchLabel(labelId, labelName, labelStatus, labelDate) {
    const response = await fetch(`/api/monitor/set-session-label/${labelId}`, { method: 'POST' });
    if (response.ok) {
        const label = await response.json();

        currentActiveLabelId = labelId; 
        await loadLabels();
       
        closeNewLabelModal();
    }
}

function hexToRgba(hex, alpha = 1) {
    hex = hex.replace('#', '');

    const r = parseInt(hex.substring(0, 2), 16);
    const g = parseInt(hex.substring(2, 4), 16);
    const b = parseInt(hex.substring(4, 6), 16);

    return `rgba(${r}, ${g}, ${b}, ${alpha})`;
}

function openEditModal(id, name, color) {
    document.getElementById('edit-label-id').value = id;
    document.getElementById('edit-label-name').value = name;
    document.getElementById('edit-label-color').value = color;
    document.getElementById('edit-modal').style.display = 'flex';
}

async function submitEditLabel() {
    const id = document.getElementById('edit-label-id').value;
    const name = document.getElementById('edit-label-name').value;
    const color = document.getElementById('edit-label-color').value;

    if (!name) return alert("Task name cannot be empty.");

    const response = await fetch(`/api/session-labels/${id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, color })
    });

    if (response.ok) {
        document.getElementById('edit-modal').style.display = 'none';
        await loadLabels();
        
        if (parseInt(id) === currentActiveLabelId) {
            document.getElementById('active-label-chip').innerHTML = name;
        }
    } else {
        alert("Error updating task.");
    }
}

async function deleteTask(labelId) {
    if (!confirm("Are you sure you want to delete this task? This cannot be undone.")) return;

    const response = await fetch(`/api/session-labels/${labelId}`, { method: 'DELETE' });

    if (response.ok) {
        if (labelId === currentActiveLabelId) {
            currentActiveLabelId = 0;
            document.getElementById('active-label-chip').innerHTML = "General";
            
            const modalActiveLabelName = document.getElementById('modal-active-label-name');
            if (modalActiveLabelName) modalActiveLabelName.innerHTML = "General";
        }
        
        await loadLabels();
    } else {
        alert("Error deleting task.");
    }
}

function showNewLabelModal() {
    document.getElementById('label-modal').style.display = 'flex';
    document.getElementById('new-label-name').focus();
}

function closeNewLabelModal() {
    document.getElementById('label-modal').style.display = 'none';
    document.getElementById('new-label-name').value = '';
}

async function submitNewLabel() {
    const name = document.getElementById('new-label-name').value;
    const color = document.getElementById('new-label-color').value;

    if (!name) return alert("Please enter a label name");

    const response = await fetch('/api/session-labels', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, color })
    });

    if (response.ok) {
        const responseData = await response.json();
        
        document.getElementById('new-label-modal').style.display = 'none';
        closeNewLabelModal();

        await loadLabels(); 

        await switchLabel(responseData.id, name, 'todo', 'Just now');
    } else {
        alert("Error creating label. Name might be a duplicate.");
    }
}

// Close modal on Escape key
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        closeExportModal();
    }
});

// Start when DOM is ready
document.addEventListener("DOMContentLoaded", async () => {
    init();
    
    await loadLabels();

    showNewLabelModal();
});