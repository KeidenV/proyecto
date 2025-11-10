/**
 * Gestor de Cookies para el Club Deportivo
 */

class CookieManager {
    constructor() {
        this.apiBase = '/admin/cookies';
        this.preferences = {};
        this.init();
    }

    async init() {
        // Cargar preferencias existentes
        await this.loadPreferences();
        
        // Aplicar preferencias cargadas
        this.applyPreferences();
        
        // Configurar event listeners
        this.setupEventListeners();
    }

    async loadPreferences() {
        try {
            const response = await fetch(`${this.apiBase}/preferences`);
            const data = await response.json();
            
            if (data.success) {
                this.preferences = data.preferences;
                console.log('Preferencias cargadas:', this.preferences);
            }
        } catch (error) {
            console.error('Error al cargar preferencias:', error);
        }
    }

    async savePreferences(preferences) {
        try {
            const response = await fetch(`${this.apiBase}/preferences`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(preferences)
            });
            
            const data = await response.json();
            if (data.success) {
                this.preferences = { ...this.preferences, ...preferences };
                this.applyPreferences();
                console.log('Preferencias guardadas:', preferences);
            }
        } catch (error) {
            console.error('Error al guardar preferencias:', error);
        }
    }

    async logAction(action, data = {}) {
        try {
            await fetch(`${this.apiBase}/action`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ action, data })
            });
        } catch (error) {
            console.error('Error al registrar acción:', error);
        }
    }

    applyPreferences() {
        // Aplicar tema
        this.applyTheme();
        
        // Aplicar preferencias de tablas
        this.applyTablePreferences();
        
        // Aplicar preferencias de dashboard
        this.applyDashboardPreferences();
        
        // Aplicar preferencias de notificaciones
        this.applyNotificationPreferences();
    }

    applyTheme() {
        const theme = this.preferences.theme || 'dark';
        document.body.setAttribute('data-theme', theme);
        
        // Actualizar selector de tema si existe
        const themeSelector = document.getElementById('theme-selector');
        if (themeSelector) {
            themeSelector.value = theme;
        }
    }

    applyTablePreferences() {
        const tablePrefs = this.preferences.table_preferences || {};
        
        // Aplicar preferencias a cada tabla
        Object.keys(tablePrefs).forEach(tableName => {
            const prefs = tablePrefs[tableName];
            const table = document.getElementById(`${tableName}-table`);
            
            if (table && prefs) {
                // Aplicar orden de columnas
                if (prefs.column_order) {
                    this.reorderTableColumns(table, prefs.column_order);
                }
                
                // Aplicar filtros
                if (prefs.filters) {
                    this.applyTableFilters(table, prefs.filters);
                }
            }
        });
    }

    applyDashboardPreferences() {
        const dashboardPrefs = this.preferences.dashboard_preferences || {};
        
        // Aplicar vista por defecto
        if (dashboardPrefs.default_view) {
            const viewToggle = document.getElementById('view-toggle');
            if (viewToggle) {
                viewToggle.value = dashboardPrefs.default_view;
            }
        }
        
        // Aplicar elementos por página
        if (dashboardPrefs.items_per_page) {
            const itemsPerPage = document.getElementById('items-per-page');
            if (itemsPerPage) {
                itemsPerPage.value = dashboardPrefs.items_per_page;
            }
        }
        
        // Aplicar auto-refresh
        if (dashboardPrefs.auto_refresh !== undefined) {
            const autoRefresh = document.getElementById('auto-refresh');
            if (autoRefresh) {
                autoRefresh.checked = dashboardPrefs.auto_refresh;
            }
        }
    }

    applyNotificationPreferences() {
        const notificationPrefs = this.preferences.notification_preferences || {};
        
        // Configurar notificaciones del navegador
        if (notificationPrefs.browser_notifications) {
            this.requestNotificationPermission();
        }
        
        // Configurar sonidos
        if (notificationPrefs.sound_notifications) {
            this.enableSoundNotifications();
        }
    }

    setupEventListeners() {
        // Selector de tema
        const themeSelector = document.getElementById('theme-selector');
        if (themeSelector) {
            themeSelector.addEventListener('change', (e) => {
                this.savePreferences({ theme: e.target.value });
            });
        }

        // Selector de idioma
        const languageSelector = document.getElementById('language-selector');
        if (languageSelector) {
            languageSelector.addEventListener('change', (e) => {
                this.savePreferences({ language: e.target.value });
            });
        }

        // Preferencias de tabla
        document.addEventListener('table-preference-changed', (e) => {
            const { tableName, preference, value } = e.detail;
            this.updateTablePreference(tableName, preference, value);
        });

        // Preferencias de dashboard
        document.addEventListener('dashboard-preference-changed', (e) => {
            const { preference, value } = e.detail;
            this.updateDashboardPreference(preference, value);
        });

        // Preferencias de notificaciones
        document.addEventListener('notification-preference-changed', (e) => {
            const { preference, value } = e.detail;
            this.updateNotificationPreference(preference, value);
        });
    }

    async updateTablePreference(tableName, preference, value) {
        const currentPrefs = this.preferences.table_preferences || {};
        const tablePrefs = currentPrefs[tableName] || {};
        tablePrefs[preference] = value;
        
        await this.savePreferences({
            table_preferences: {
                ...currentPrefs,
                [tableName]: tablePrefs
            }
        });
    }

    async updateDashboardPreference(preference, value) {
        const currentPrefs = this.preferences.dashboard_preferences || {};
        currentPrefs[preference] = value;
        
        await this.savePreferences({
            dashboard_preferences: currentPrefs
        });
    }

    async updateNotificationPreference(preference, value) {
        const currentPrefs = this.preferences.notification_preferences || {};
        currentPrefs[preference] = value;
        
        await this.savePreferences({
            notification_preferences: currentPrefs
        });
    }

    reorderTableColumns(table, columnOrder) {
        // Implementar reordenamiento de columnas
        const headerRow = table.querySelector('thead tr');
        if (headerRow && columnOrder) {
            const cells = Array.from(headerRow.children);
            const reorderedCells = columnOrder.map(index => cells[index]).filter(Boolean);
            
            reorderedCells.forEach(cell => {
                headerRow.appendChild(cell);
            });
        }
    }

    applyTableFilters(table, filters) {
        // Implementar aplicación de filtros
        Object.keys(filters).forEach(filterName => {
            const filterElement = document.getElementById(`${filterName}-filter`);
            if (filterElement) {
                filterElement.value = filters[filterName];
            }
        });
    }

    async requestNotificationPermission() {
        if ('Notification' in window && Notification.permission === 'default') {
            await Notification.requestPermission();
        }
    }

    enableSoundNotifications() {
        // Implementar notificaciones de sonido
        this.soundEnabled = true;
    }

    showNotification(title, message, type = 'info') {
        const notificationPrefs = this.preferences.notification_preferences || {};
        
        // Notificación del navegador
        if (notificationPrefs.browser_notifications && Notification.permission === 'granted') {
            new Notification(title, {
                body: message,
                icon: '/static/images/icon.png'
            });
        }
        
        // Notificación visual
        this.showVisualNotification(title, message, type);
        
        // Sonido
        if (notificationPrefs.sound_notifications && this.soundEnabled) {
            this.playNotificationSound();
        }
    }

    showVisualNotification(title, message, type) {
        // Crear notificación visual
        const notification = document.createElement('div');
        notification.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
        notification.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
        
        notification.innerHTML = `
            <strong>${title}</strong><br>
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        document.body.appendChild(notification);
        
        // Auto-remove después de 5 segundos
        setTimeout(() => {
            if (notification.parentNode) {
                notification.remove();
            }
        }, 5000);
    }

    playNotificationSound() {
        // Crear y reproducir sonido de notificación
        const audio = new Audio('/static/sounds/notification.mp3');
        audio.volume = 0.3;
        audio.play().catch(e => console.log('No se pudo reproducir sonido:', e));
    }

    // Métodos de utilidad
    getPreference(category, key, defaultValue = null) {
        return this.preferences[category]?.[key] ?? defaultValue;
    }

    setPreference(category, key, value) {
        if (!this.preferences[category]) {
            this.preferences[category] = {};
        }
        this.preferences[category][key] = value;
    }

    async clearAllCookies() {
        try {
            await fetch(`${this.apiBase}/clear`, { method: 'POST' });
            this.preferences = {};
            location.reload();
        } catch (error) {
            console.error('Error al limpiar cookies:', error);
        }
    }
}

// Inicializar gestor de cookies
const cookieManager = new CookieManager();

// Exportar para uso global
window.cookieManager = cookieManager;
