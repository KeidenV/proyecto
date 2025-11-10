// Sistema de búsqueda avanzada
class AdvancedSearch {
    constructor() {
        this.searchIndex = [];
        this.searchResults = [];
        this.currentQuery = '';
        this.filters = {};
        this.init();
    }

    init() {
        this.createSearchInterface();
        this.setupEventListeners();
        this.buildSearchIndex();
    }

    createSearchInterface() {
        if (document.getElementById('advanced-search')) return;

        const searchContainer = document.createElement('div');
        searchContainer.id = 'advanced-search';
        searchContainer.className = 'advanced-search-container';
        searchContainer.innerHTML = `
            <div class="search-overlay" id="search-overlay"></div>
            <div class="search-modal" id="search-modal">
                <div class="search-header">
                    <div class="search-input-container">
                        <i class="fas fa-search search-icon"></i>
                        <input type="text" id="search-input" placeholder="Buscar usuarios, entrenamientos, competiciones..." autocomplete="off">
                        <button class="search-clear" id="search-clear" style="display: none;">
                            <i class="fas fa-times"></i>
                        </button>
                    </div>
                    <button class="search-close" id="search-close">
                        <i class="fas fa-times"></i>
                    </button>
                </div>
                <div class="search-filters">
                    <div class="filter-group">
                        <label>Tipo:</label>
                        <select id="search-type">
                            <option value="">Todos</option>
                            <option value="usuario">Usuarios</option>
                            <option value="entrenamiento">Entrenamientos</option>
                            <option value="competicion">Competiciones</option>
                            <option value="actividad">Actividades</option>
                        </select>
                    </div>
                    <div class="filter-group">
                        <label>Rol:</label>
                        <select id="search-role">
                            <option value="">Todos</option>
                            <option value="Administrador">Administrador</option>
                            <option value="Entrenador">Entrenador</option>
                            <option value="Miembro">Miembro</option>
                        </select>
                    </div>
                    <div class="filter-group">
                        <label>Fecha:</label>
                        <input type="date" id="search-date">
                    </div>
                </div>
                <div class="search-results" id="search-results">
                    <div class="search-placeholder">
                        <i class="fas fa-search"></i>
                        <p>Escribe para buscar...</p>
                    </div>
                </div>
                <div class="search-shortcuts">
                    <span>Atajos:</span>
                    <kbd>Ctrl</kbd> + <kbd>K</kbd> para buscar
                    <kbd>Esc</kbd> para cerrar
                </div>
            </div>
        `;

        document.body.appendChild(searchContainer);
    }

    setupEventListeners() {
        // Atajo de teclado Ctrl+K
        document.addEventListener('keydown', (e) => {
            if (e.ctrlKey && e.key === 'k') {
                e.preventDefault();
                this.openSearch();
            }
            if (e.key === 'Escape') {
                this.closeSearch();
            }
        });

        // Eventos del modal de búsqueda
        document.getElementById('search-close').addEventListener('click', () => this.closeSearch());
        document.getElementById('search-clear').addEventListener('click', () => this.clearSearch());
        
        // Debounce para la búsqueda (esperar 300ms después de que el usuario deje de escribir)
        const debouncedSearch = this.debounce((value) => this.handleSearch(value), 300);
        document.getElementById('search-input').addEventListener('input', (e) => debouncedSearch(e.target.value));
        
        // Filtros
        ['search-type', 'search-role', 'search-date'].forEach(id => {
            document.getElementById(id).addEventListener('change', () => this.applyFilters());
        });

        // Cerrar al hacer clic en overlay
        document.getElementById('search-overlay').addEventListener('click', () => this.closeSearch());
    }

    buildSearchIndex() {
        // Los datos ahora se obtienen dinámicamente del servidor
        this.searchIndex = [];
    }

    openSearch() {
        document.getElementById('advanced-search').classList.add('active');
        document.getElementById('search-input').focus();
        document.body.style.overflow = 'hidden';
    }

    closeSearch() {
        document.getElementById('advanced-search').classList.remove('active');
        document.body.style.overflow = '';
        this.clearSearch();
    }

    clearSearch() {
        document.getElementById('search-input').value = '';
        document.getElementById('search-clear').style.display = 'none';
        this.currentQuery = '';
        this.showPlaceholder();
    }

    handleSearch(query) {
        this.currentQuery = query.toLowerCase();
        
        if (query.length === 0) {
            document.getElementById('search-clear').style.display = 'none';
            this.showPlaceholder();
            return;
        }

        document.getElementById('search-clear').style.display = 'block';
        this.performSearch();
    }

    async performSearch() {
        // Mostrar indicador de carga
        this.showLoading();
        
        // Mostrar spinner en el input
        const inputContainer = document.querySelector('.search-input-container');
        inputContainer.classList.add('searching');
        
        try {
            // Construir parámetros de búsqueda
            const params = new URLSearchParams({
                q: this.currentQuery,
                type: this.filters.type || '',
                role: this.filters.role || '',
                date: this.filters.date || ''
            });
            
            // Realizar búsqueda en el servidor
            const response = await fetch(`/api/search?${params}`);
            if (!response.ok) {
                throw new Error('Error en la búsqueda');
            }
            
            const results = await response.json();
            this.displayResults(results);
            
        } catch (error) {
            console.error('Error en búsqueda:', error);
            this.showError('Error al realizar la búsqueda. Inténtalo de nuevo.');
        } finally {
            // Ocultar spinner
            inputContainer.classList.remove('searching');
        }
    }

    showLoading() {
        const resultsContainer = document.getElementById('search-results');
        resultsContainer.innerHTML = `
            <div class="search-loading text-center py-4">
                <div class="spinner-border text-primary" role="status">
                    <span class="visually-hidden">Buscando...</span>
                </div>
                <p class="mt-2 text-muted">Buscando resultados...</p>
            </div>
        `;
    }

    showError(message) {
        const resultsContainer = document.getElementById('search-results');
        resultsContainer.innerHTML = `
            <div class="search-error text-center py-4">
                <i class="fas fa-exclamation-triangle fa-3x text-warning mb-3"></i>
                <p class="text-muted">${message}</p>
                <button class="btn btn-outline-primary btn-sm" onclick="advancedSearch.performSearch()">
                    <i class="fas fa-redo me-2"></i>Reintentar
                </button>
            </div>
        `;
    }

    applyFilters() {
        this.filters = {
            type: document.getElementById('search-type').value,
            role: document.getElementById('search-role').value,
            date: document.getElementById('search-date').value
        };
        
        if (this.currentQuery) {
            this.performSearch();
        }
    }

    displayResults(results) {
        const resultsContainer = document.getElementById('search-results');
        
        if (results.length === 0) {
            const safeQuery = this.escapeHtml(this.currentQuery);
            resultsContainer.innerHTML = `
                <div class="search-no-results">
                    <i class="fas fa-search"></i>
                    <p>No se encontraron resultados para "${safeQuery}"</p>
                </div>
            `;
            return;
        }

        resultsContainer.innerHTML = results.map(item => `
            <div class="search-result-item" data-url="${item.url}">
                <div class="result-icon">
                    <i class="fas ${this.getIconForType(item.type)}"></i>
                </div>
                <div class="result-content">
                    <h6 class="result-title">${this.highlightQuery(item.title)}</h6>
                    <p class="result-description">${this.highlightQuery(item.description)}</p>
                </div>
                <div class="result-arrow">
                    <i class="fas fa-arrow-right"></i>
                </div>
            </div>
        `).join('');

        // Agregar event listeners a los resultados
        resultsContainer.querySelectorAll('.search-result-item').forEach(item => {
            item.addEventListener('click', () => {
                window.location.href = item.dataset.url;
            });
        });
    }

    getIconForType(type) {
        const icons = {
            usuario: 'fa-user',
            entrenamiento: 'fa-running',
            competicion: 'fa-trophy',
            actividad: 'fa-dumbbell'
        };
        return icons[type] || 'fa-file';
    }

    // Debounce para evitar demasiadas búsquedas
    debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }

    highlightQuery(text) {
        if (!this.currentQuery) return this.escapeHtml(text);

        // Escapar caracteres especiales para la expresión regular
        const escapedQuery = this.currentQuery.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
        const regex = new RegExp(`(${escapedQuery})`, 'gi');

        // Escapar el texto antes de insertar HTML de resaltado
        const escapedText = this.escapeHtml(text);
        return escapedText.replace(regex, '<mark>$1</mark>');
    }

    escapeHtml(unsafe) {
        if (unsafe == null) return '';
        return String(unsafe)
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
            .replace(/'/g, '&#039;');
    }

    showPlaceholder() {
        document.getElementById('search-results').innerHTML = `
            <div class="search-placeholder">
                <i class="fas fa-search"></i>
                <p>Escribe para buscar...</p>
            </div>
        `;
    }
}

// Inicializar sistema de búsqueda
document.addEventListener('DOMContentLoaded', function() {
    window.advancedSearch = new AdvancedSearch();
});
