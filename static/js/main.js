// JavaScript para el Club Deportivo

document.addEventListener('DOMContentLoaded', function() {
    // Inicializar tooltips de Bootstrap
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Auto-dismiss alerts después de 5 segundos
    setTimeout(function() {
        var alerts = document.querySelectorAll('.alert');
        alerts.forEach(function(alert) {
            var bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);

    // Confirmación para acciones de eliminación
    document.querySelectorAll('.btn-danger[data-confirm]').forEach(function(button) {
        button.addEventListener('click', function(e) {
            if (!confirm('¿Estás seguro de que quieres eliminar este elemento?')) {
                e.preventDefault();
            }
        });
    });

    // Formatear números de teléfono
    document.querySelectorAll('input[type="tel"]').forEach(function(input) {
        input.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, '');
            if (value.length >= 10) {
                value = value.replace(/(\d{3})(\d{3})(\d{4})/, '($1) $2-$3');
            }
            e.target.value = value;
        });
    });

    // Validación de formularios en tiempo real
    document.querySelectorAll('form').forEach(function(form) {
        form.addEventListener('submit', function(e) {
            let isValid = true;
            let requiredFields = form.querySelectorAll('[required]');
            
            requiredFields.forEach(function(field) {
                if (!field.value.trim()) {
                    isValid = false;
                    field.classList.add('is-invalid');
                } else {
                    field.classList.remove('is-invalid');
                }
            });
            
            if (!isValid) {
                e.preventDefault();
                alert('Por favor, completa todos los campos requeridos.');
            }
        });
    });

    // Animación de contadores en dashboard
    function animateCounter(element, target) {
        let current = 0;
        let increment = target / 100;
        let timer = setInterval(function() {
            current += increment;
            if (current >= target) {
                current = target;
                clearInterval(timer);
            }
            element.textContent = Math.floor(current);
        }, 20);
    }

    // Inicializar contadores si existen
    document.querySelectorAll('.stats-number').forEach(function(counter) {
        let target = parseInt(counter.textContent);
        if (!isNaN(target)) {
            counter.textContent = '0';
            animateCounter(counter, target);
        }
    });

    // Filtro de búsqueda en tablas
    document.querySelectorAll('.search-input').forEach(function(input) {
        input.addEventListener('keyup', function(e) {
            let filter = e.target.value.toLowerCase();
            let table = e.target.closest('.card').querySelector('table');
            if (table) {
                let rows = table.querySelectorAll('tbody tr');
                rows.forEach(function(row) {
                    let text = row.textContent.toLowerCase();
                    if (text.includes(filter)) {
                        row.style.display = '';
                    } else {
                        row.style.display = 'none';
                    }
                });
            }
        });
    });

    // Calendario - mostrar detalles del evento al hacer clic
    document.querySelectorAll('.calendar-event').forEach(function(event) {
        event.addEventListener('click', function() {
            // Aquí podrías mostrar un modal con más detalles
            console.log('Evento clickeado:', this);
        });
    });

    // Validación de fechas
    document.querySelectorAll('input[type="date"]').forEach(function(input) {
        input.addEventListener('change', function(e) {
            let selectedDate = new Date(e.target.value);
            let today = new Date();
            
            if (selectedDate < today && !e.target.hasAttribute('data-allow-past')) {
                alert('La fecha no puede ser anterior a hoy.');
                e.target.value = '';
            }
        });
    });

    // Auto-save para formularios largos
    let autoSaveTimer;
    document.querySelectorAll('form[data-autosave]').forEach(function(form) {
        form.addEventListener('input', function() {
            clearTimeout(autoSaveTimer);
            autoSaveTimer = setTimeout(function() {
                // Aquí podrías implementar auto-save
                console.log('Auto-saving form...');
            }, 2000);
        });
    });

    // Smooth scroll para enlaces internos
    document.querySelectorAll('a[href^="#"]').forEach(function(link) {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            let target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Cargar más datos (paginación infinita)
    let loadingMore = false;
    window.loadMoreData = function(url, container) {
        if (loadingMore) return;
        
        loadingMore = true;
        let loadingIndicator = document.createElement('div');
        loadingIndicator.className = 'text-center py-3';
        loadingIndicator.innerHTML = '<div class="loading"></div>';
        container.appendChild(loadingIndicator);
        
        fetch(url)
            .then(response => response.json())
            .then(data => {
                loadingIndicator.remove();
                container.innerHTML += data.html;
                loadingMore = false;
            })
            .catch(error => {
                loadingIndicator.remove();
                loadingMore = false;
                console.error('Error loading more data:', error);
            });
    };

    // Exportar datos a CSV
    window.exportToCSV = function(tableId, filename) {
        let table = document.getElementById(tableId);
        if (!table) return;
        
        let csv = [];
        let rows = table.querySelectorAll('tr');
        
        rows.forEach(function(row) {
            let rowData = [];
            let cells = row.querySelectorAll('td, th');
            cells.forEach(function(cell) {
                rowData.push('"' + cell.textContent.replace(/"/g, '""') + '"');
            });
            csv.push(rowData.join(','));
        });
        
        let csvContent = csv.join('\n');
        let blob = new Blob([csvContent], { type: 'text/csv' });
        let url = window.URL.createObjectURL(blob);
        let a = document.createElement('a');
        a.href = url;
        a.download = filename || 'export.csv';
        a.click();
        window.URL.revokeObjectURL(url);
    };

    // Notificaciones push (si el navegador lo soporta)
    if ('Notification' in window && Notification.permission === 'default') {
        Notification.requestPermission();
    }

    // Modo oscuro (opcional)
    let darkModeToggle = document.getElementById('darkModeToggle');
    if (darkModeToggle) {
        darkModeToggle.addEventListener('click', function() {
            document.body.classList.toggle('dark-mode');
            localStorage.setItem('darkMode', document.body.classList.contains('dark-mode'));
        });
        
        // Cargar preferencia guardada
        if (localStorage.getItem('darkMode') === 'true') {
            document.body.classList.add('dark-mode');
        }
    }
});

// Funciones globales útiles
window.formatDate = function(dateString) {
    let date = new Date(dateString);
    return date.toLocaleDateString('es-ES', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
};

window.formatTime = function(timeString) {
    let time = new Date('2000-01-01 ' + timeString);
    return time.toLocaleTimeString('es-ES', {
        hour: '2-digit',
        minute: '2-digit'
    });
};

window.showLoading = function(element) {
    element.innerHTML = '<div class="loading"></div>';
};

window.hideLoading = function(element, originalContent) {
    element.innerHTML = originalContent;
};
