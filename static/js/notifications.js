// Sistema de notificaciones en tiempo real
class NotificationSystem {
    constructor() {
        this.notifications = [];
        this.maxNotifications = 5;
        this.init();
    }

    init() {
        this.createNotificationContainer();
        this.loadStoredNotifications();
        this.setupEventListeners();
    }

    createNotificationContainer() {
        if (document.getElementById('notification-container')) return;

        const container = document.createElement('div');
        container.id = 'notification-container';
        container.className = 'notification-container';
        container.innerHTML = `
            <div class="notification-header">
                <h6><i class="fas fa-bell me-2"></i>Notificaciones</h6>
                <div class="notification-actions">
                    <button class="btn btn-sm btn-outline-secondary me-2" onclick="notificationSystem.markAllAsRead()">
                        <i class="fas fa-check-double"></i>
                    </button>
                    <button class="btn btn-sm btn-outline-danger" onclick="notificationSystem.clearAll()">
                        <i class="fas fa-trash"></i>
                    </button>
                </div>
            </div>
            <div class="notification-list" id="notification-list">
                <!-- Notificaciones se insertan aquí -->
            </div>
        `;

        document.body.appendChild(container);
    }

    setupEventListeners() {
        // Simular notificaciones cada 30 segundos (en producción sería WebSocket)
        setInterval(() => {
            this.simulateNotification();
        }, 30000);
    }

    addNotification(type, title, message, duration = 5000) {
        const notification = {
            id: Date.now(),
            type: type, // 'success', 'warning', 'error', 'info'
            title: title,
            message: message,
            timestamp: new Date(),
            read: false
        };

        this.notifications.unshift(notification);
        this.renderNotifications();
        this.storeNotifications();

        // Auto-remove después de la duración especificada
        if (duration > 0) {
            setTimeout(() => {
                this.removeNotification(notification.id);
            }, duration);
        }
    }

    renderNotifications() {
        const container = document.getElementById('notification-list');
        if (!container) return;

        const recentNotifications = this.notifications.slice(0, this.maxNotifications);
        
        container.innerHTML = recentNotifications.map(notification => `
            <div class="notification-item ${notification.type} ${notification.read ? 'read' : 'unread'}" 
                 data-id="${notification.id}">
                <div class="notification-icon">
                    <i class="fas ${this.getIconForType(notification.type)}"></i>
                </div>
                <div class="notification-content">
                    <h6 class="notification-title">${notification.title}</h6>
                    <p class="notification-message">${notification.message}</p>
                    <small class="notification-time">${this.formatTime(notification.timestamp)}</small>
                </div>
                <button class="notification-close" onclick="notificationSystem.removeNotification(${notification.id})">
                    <i class="fas fa-times"></i>
                </button>
            </div>
        `).join('');

        // Agregar event listeners para marcar como leído
        container.querySelectorAll('.notification-item').forEach(item => {
            item.addEventListener('click', (e) => {
                if (!e.target.closest('.notification-close')) {
                    this.markAsRead(parseInt(item.dataset.id));
                }
            });
        });

        // Actualizar badge de notificaciones
        this.updateNotificationBadge();
    }

    updateNotificationBadge() {
        const badge = document.getElementById('notification-badge');
        if (!badge) return;

        const unreadCount = this.notifications.filter(n => !n.read).length;
        if (unreadCount > 0) {
            badge.textContent = unreadCount > 99 ? '99+' : unreadCount;
            badge.style.display = 'block';
        } else {
            badge.style.display = 'none';
        }
    }

    getIconForType(type) {
        const icons = {
            success: 'fa-check-circle',
            warning: 'fa-exclamation-triangle',
            error: 'fa-times-circle',
            info: 'fa-info-circle'
        };
        return icons[type] || 'fa-bell';
    }

    formatTime(timestamp) {
        const now = new Date();
        const diff = now - timestamp;
        const minutes = Math.floor(diff / 60000);
        const hours = Math.floor(diff / 3600000);
        const days = Math.floor(diff / 86400000);

        if (minutes < 1) return 'Ahora';
        if (minutes < 60) return `${minutes}m`;
        if (hours < 24) return `${hours}h`;
        return `${days}d`;
    }

    removeNotification(id) {
        this.notifications = this.notifications.filter(n => n.id !== id);
        this.renderNotifications();
        this.storeNotifications();
    }

    markAsRead(id) {
        const notification = this.notifications.find(n => n.id === id);
        if (notification) {
            notification.read = true;
            this.renderNotifications();
            this.storeNotifications();
        }
    }

    clearAll() {
        this.notifications = [];
        this.renderNotifications();
        this.storeNotifications();
    }

    markAllAsRead() {
        this.notifications.forEach(notification => {
            notification.read = true;
        });
        this.renderNotifications();
        this.storeNotifications();
    }

    toggleContainer() {
        const container = document.getElementById('notification-container');
        container.classList.toggle('show');
    }

    simulateNotification() {
        const notifications = [
            {
                type: 'info',
                title: 'Nuevo Entrenamiento',
                message: 'Se ha programado un nuevo entrenamiento de fútbol para mañana a las 6:00 PM'
            },
            {
                type: 'success',
                title: 'Asistencia Registrada',
                message: 'Tu asistencia al entrenamiento de natación ha sido confirmada'
            },
            {
                type: 'warning',
                title: 'Recordatorio',
                message: 'Tienes un entrenamiento en 30 minutos'
            },
            {
                type: 'info',
                title: 'Nueva Competición',
                message: 'Se ha abierto la inscripción para el torneo de baloncesto'
            }
        ];

        const randomNotification = notifications[Math.floor(Math.random() * notifications.length)];
        this.addNotification(randomNotification.type, randomNotification.title, randomNotification.message);
    }

    storeNotifications() {
        localStorage.setItem('club_notifications', JSON.stringify(this.notifications));
    }

    loadStoredNotifications() {
        const stored = localStorage.getItem('club_notifications');
        if (stored) {
            this.notifications = JSON.parse(stored);
            this.renderNotifications();
        }
    }

    // Métodos para notificaciones específicas del sistema
    notifyNewTraining(training) {
        this.addNotification('info', 'Nuevo Entrenamiento', 
            `Se ha programado ${training.actividad} para ${training.fecha}`, 10000);
    }

    notifyAttendanceRecorded(attendance) {
        this.addNotification('success', 'Asistencia Registrada', 
            'Tu asistencia ha sido confirmada correctamente', 5000);
    }

    notifyUpcomingTraining(training) {
        this.addNotification('warning', 'Recordatorio de Entrenamiento', 
            `Tienes un entrenamiento de ${training.actividad} en 1 hora`, 15000);
    }

    notifyNewCompetition(competition) {
        this.addNotification('info', 'Nueva Competición', 
            `Se ha abierto la inscripción para ${competition.nombre}`, 10000);
    }
}

// Inicializar sistema de notificaciones
document.addEventListener('DOMContentLoaded', function() {
    window.notificationSystem = new NotificationSystem();
});
