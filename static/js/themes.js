// Sistema de temas y personalización
class ThemeManager {
    constructor() {
        this.currentTheme = 'light';
        this.availableThemes = [
            { id: 'light', name: 'Claro', icon: 'fas fa-sun' },
            { id: 'dark', name: 'Oscuro', icon: 'fas fa-moon' },
            { id: 'blue', name: 'Azul', icon: 'fas fa-palette' },
            { id: 'green', name: 'Verde', icon: 'fas fa-leaf' },
            { id: 'purple', name: 'Púrpura', icon: 'fas fa-gem' },
            { id: 'high-contrast', name: 'Alto Contraste', icon: 'fas fa-adjust' }
        ];
        this.init();
    }

    init() {
        this.loadTheme();
        this.createThemeSelector();
        this.setupEventListeners();
        this.applyTheme(this.currentTheme);
    }

    createThemeSelector() {
        if (document.getElementById('theme-selector')) return;

        const themeSelector = document.createElement('div');
        themeSelector.id = 'theme-selector';
        themeSelector.className = 'theme-selector';
        themeSelector.innerHTML = `
            <button class="theme-toggle" id="theme-toggle" title="Cambiar tema">
                <i class="fas fa-palette"></i>
            </button>
            <div class="theme-menu" id="theme-menu">
                <div class="theme-header">
                    <h6><i class="fas fa-palette me-2"></i>Temas</h6>
                </div>
                ${this.availableThemes.map(theme => `
                    <div class="theme-option ${theme.id === this.currentTheme ? 'active' : ''}" 
                         data-theme="${theme.id}">
                        <div class="theme-color ${theme.id}"></div>
                        <span class="theme-name">${theme.name}</span>
                        <i class="fas fa-check theme-check" style="display: ${theme.id === this.currentTheme ? 'block' : 'none'};"></i>
                    </div>
                `).join('')}
            </div>
        `;

        document.body.appendChild(themeSelector);
    }

    setupEventListeners() {
        // Toggle del menú de temas
        document.getElementById('theme-toggle').addEventListener('click', (e) => {
            e.stopPropagation();
            this.toggleThemeMenu();
        });

        // Selección de tema
        document.querySelectorAll('.theme-option').forEach(option => {
            option.addEventListener('click', (e) => {
                const themeId = e.currentTarget.dataset.theme;
                this.setTheme(themeId);
                this.closeThemeMenu();
            });
        });

        // Cerrar menú al hacer clic fuera
        document.addEventListener('click', (e) => {
            if (!e.target.closest('#theme-selector')) {
                this.closeThemeMenu();
            }
        });

        // Atajo de teclado para cambiar tema
        document.addEventListener('keydown', (e) => {
            if (e.ctrlKey && e.shiftKey && e.key === 'T') {
                e.preventDefault();
                this.cycleTheme();
            }
        });
    }

    toggleThemeMenu() {
        const menu = document.getElementById('theme-menu');
        menu.classList.toggle('show');
    }

    closeThemeMenu() {
        const menu = document.getElementById('theme-menu');
        menu.classList.remove('show');
    }

    setTheme(themeId) {
        if (!this.availableThemes.find(t => t.id === themeId)) return;

        this.currentTheme = themeId;
        this.applyTheme(themeId);
        this.saveTheme(themeId);
        this.updateThemeSelector();
    }

    applyTheme(themeId) {
        document.documentElement.setAttribute('data-theme', themeId);
        
        // Actualizar meta theme-color para móviles
        let metaThemeColor = document.querySelector('meta[name="theme-color"]');
        if (!metaThemeColor) {
            metaThemeColor = document.createElement('meta');
            metaThemeColor.name = 'theme-color';
            document.head.appendChild(metaThemeColor);
        }
        
        const themeColors = {
            'light': '#007bff',
            'dark': '#1a1a1a',
            'blue': '#0d6efd',
            'green': '#198754',
            'purple': '#6f42c1',
            'high-contrast': '#000000'
        };
        
        metaThemeColor.content = themeColors[themeId] || '#007bff';
    }

    updateThemeSelector() {
        // Actualizar opciones activas
        document.querySelectorAll('.theme-option').forEach(option => {
            const isActive = option.dataset.theme === this.currentTheme;
            option.classList.toggle('active', isActive);
            
            const checkIcon = option.querySelector('.theme-check');
            if (checkIcon) {
                checkIcon.style.display = isActive ? 'block' : 'none';
            }
        });

        // Actualizar icono del botón
        const currentThemeData = this.availableThemes.find(t => t.id === this.currentTheme);
        const toggleIcon = document.querySelector('#theme-toggle i');
        if (toggleIcon && currentThemeData) {
            toggleIcon.className = currentThemeData.icon;
        }
    }

    cycleTheme() {
        const currentIndex = this.availableThemes.findIndex(t => t.id === this.currentTheme);
        const nextIndex = (currentIndex + 1) % this.availableThemes.length;
        this.setTheme(this.availableThemes[nextIndex].id);
    }

    saveTheme(themeId) {
        localStorage.setItem('club_theme', themeId);
    }

    loadTheme() {
        const savedTheme = localStorage.getItem('club_theme');
        if (savedTheme && this.availableThemes.find(t => t.id === savedTheme)) {
            this.currentTheme = savedTheme;
        } else {
            // Detectar preferencia del sistema
            if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
                this.currentTheme = 'dark';
            }
        }
    }

    // Métodos para personalización adicional
    setCustomColor(colorType, color) {
        document.documentElement.style.setProperty(`--${colorType}-color`, color);
    }

    resetToDefault() {
        this.setTheme('light');
    }

    // Obtener tema actual
    getCurrentTheme() {
        return this.currentTheme;
    }

    // Obtener información del tema actual
    getCurrentThemeInfo() {
        return this.availableThemes.find(t => t.id === this.currentTheme);
    }

    // Aplicar tema basado en hora del día
    applyTimeBasedTheme() {
        const hour = new Date().getHours();
        if (hour >= 18 || hour <= 6) {
            this.setTheme('dark');
        } else {
            this.setTheme('light');
        }
    }

    // Auto-cambio de tema basado en hora
    enableAutoTheme() {
        this.applyTimeBasedTheme();
        
        // Cambiar cada hora
        setInterval(() => {
            this.applyTimeBasedTheme();
        }, 3600000); // 1 hora
    }
}

// Inicializar gestor de temas
document.addEventListener('DOMContentLoaded', function() {
    window.themeManager = new ThemeManager();
    
    // Opcional: Habilitar auto-cambio de tema
    // window.themeManager.enableAutoTheme();
});
