// ===================================
// MAIN.JS - FRUTOS DE ORO
// Sistema de Gestión de Cumplimiento Normativo
// ===================================

// Esperar a que el DOM esté listo
$(document).ready(function() {
    console.log('Sistema cargado correctamente');
    
    // Inicializar tooltips de Bootstrap
    initializeTooltips();
    
    // Inicializar popovers
    initializePopovers();
    
    // Configurar validación de formularios
    setupFormValidation();
    
    // NO llamar setupDeleteEvents() - cada página maneja sus propios eventos
});

/**
 * Inicializar tooltips de Bootstrap
 */
function initializeTooltips() {
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

/**
 * Inicializar popovers de Bootstrap
 */
function initializePopovers() {
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
}

/**
 * Configurar validación de formularios
 */
function setupFormValidation() {
    var forms = document.querySelectorAll('.needs-validation');
    
    Array.prototype.slice.call(forms).forEach(function (form) {
        form.addEventListener('submit', function (event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });
}

/**
 * NOTA: setupDeleteEvents() fue removido
 * Cada página debe manejar sus propios eventos de eliminación
 * para usar modales específicos en lugar de confirm() genérico
 */

/**
 * Mostrar alerta de éxito
 */
function showSuccessAlert(message, container = 'body') {
    showAlert(message, 'success', container);
}

/**
 * Mostrar alerta de error
 */
function showErrorAlert(message, container = 'body') {
    showAlert(message, 'danger', container);
}

/**
 * Mostrar alerta de advertencia
 */
function showWarningAlert(message, container = 'body') {
    showAlert(message, 'warning', container);
}

/**
 * Mostrar alerta de información
 */
function showInfoAlert(message, container = 'body') {
    showAlert(message, 'info', container);
}

/**
 * Función genérica para mostrar alertas
 */
function showAlert(message, type = 'info', container = 'body') {
    var alertHtml = `
        <div class="alert alert-${type} alert-dismissible fade show" role="alert">
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>
    `;
    
    if (container === 'body') {
        $(alertHtml).prependTo('main');
    } else {
        $(alertHtml).prependTo(container);
    }
    
    // Auto-descartar después de 5 segundos
    setTimeout(function() {
        $('.alert').fadeOut('slow', function() {
            $(this).remove();
        });
    }, 5000);
}

/**
 * Formatear fecha a formato DD/MM/YYYY
 */
function formatDate(date) {
    if (typeof date === 'string') {
        date = new Date(date);
    }
    
    var day = String(date.getDate()).padStart(2, '0');
    var month = String(date.getMonth() + 1).padStart(2, '0');
    var year = date.getFullYear();
    
    return `${day}/${month}/${year}`;
}

/**
 * Formatear fecha con hora
 */
function formatDateTime(date) {
    if (typeof date === 'string') {
        date = new Date(date);
    }
    
    var day = String(date.getDate()).padStart(2, '0');
    var month = String(date.getMonth() + 1).padStart(2, '0');
    var year = date.getFullYear();
    var hours = String(date.getHours()).padStart(2, '0');
    var minutes = String(date.getMinutes()).padStart(2, '0');
    
    return `${day}/${month}/${year} ${hours}:${minutes}`;
}

/**
 * Calcular días para vencimiento
 */
function daysUntilExpiration(expirationDate) {
    var today = new Date();
    today.setHours(0, 0, 0, 0);
    
    if (typeof expirationDate === 'string') {
        expirationDate = new Date(expirationDate);
    }
    expirationDate.setHours(0, 0, 0, 0);
    
    var diff = expirationDate.getTime() - today.getTime();
    var days = Math.ceil(diff / (1000 * 60 * 60 * 24));
    
    return days;
}

/**
 * Obtener color de estado según días faltantes
 */
function getStatusColor(days) {
    if (days < 0) {
        return 'danger'; // Rojo - Vencido
    } else if (days < 15) {
        return 'danger'; // Rojo - Crítico
    } else if (days < 30) {
        return 'warning'; // Amarillo - Próximo a vencer
    } else {
        return 'success'; // Verde - Vigente
    }
}

/**
 * Obtener badge de estado
 */
function getStatusBadge(status) {
    var badges = {
        'vigente': '<span class="badge bg-success">Vigente</span>',
        'proxima_vencer': '<span class="badge bg-warning">Próxima a Vencer</span>',
        'vencida': '<span class="badge bg-danger">Vencida</span>',
        'programada': '<span class="badge bg-info">Programada</span>',
        'en_ejecucion': '<span class="badge bg-warning">En Ejecución</span>',
        'completada': '<span class="badge bg-success">Completada</span>',
        'abierto': '<span class="badge bg-warning">Abierto</span>',
        'cerrado': '<span class="badge bg-success">Cerrado</span>'
    };
    
    return badges[status] || `<span class="badge bg-secondary">${status}</span>`;
}

/**
 * Marcar alertas como leídas vía AJAX
 */
function markAlertAsRead(alertId) {
    $.ajax({
        url: `/dashboard/alerts/mark-as-read/${alertId}`,
        type: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        success: function(response) {
            $(`#alert-${alertId}`).fadeOut('slow', function() {
                $(this).remove();
            });
        },
        error: function(xhr) {
            console.error('Error al marcar alerta como leída:', xhr);
        }
    });
}

/**
 * Descargar archivo
 */
function downloadFile(url, filename) {
    var link = document.createElement('a');
    link.href = url;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

/**
 * Validar email
 */
function isValidEmail(email) {
    var re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

/**
 * Limpiar formulario
 */
function clearForm(formId) {
    $(`#${formId}`)[0].reset();
    $(`#${formId}`).removeClass('was-validated');
}

/**
 * Mostrar spinner de carga
 */
function showSpinner(element) {
    $(element).html(`
        <div class="spinner-border spinner-border-sm" role="status">
            <span class="visually-hidden">Cargando...</span>
        </div>
    `);
}

/**
 * Exportar tabla a CSV
 */
function exportTableToCSV(filename) {
    var csv = [];
    var rows = document.querySelectorAll('table tr');
    
    rows.forEach(function(row) {
        var cells = Array.prototype.slice.call(row.querySelectorAll('th, td'));
        var rowData = cells.map(function(cell) {
            return '"' + cell.textContent.trim() + '"';
        }).join(',');
        csv.push(rowData);
    });
    
    downloadCSV(csv.join('\n'), filename);
}

/**
 * Descargar CSV
 */
function downloadCSV(csv, filename) {
    var csvFile;
    var downloadLink;
    
    csvFile = new Blob([csv], {type: "text/csv"});
    downloadLink = document.createElement('a');
    downloadLink.href = URL.createObjectURL(csvFile);
    downloadLink.download = filename || 'export.csv';
    document.body.appendChild(downloadLink);
    downloadLink.click();
    document.body.removeChild(downloadLink);
}

/**
 * Función para manejar carga de archivos con validación
 */
function setupFileUpload(inputSelector, maxSizeMB = 50) {
    $(inputSelector).on('change', function(e) {
        var file = this.files[0];
        
        if (!file) return;
        
        // Validar tamaño
        var fileSizeMB = file.size / (1024 * 1024);
        if (fileSizeMB > maxSizeMB) {
            showErrorAlert(`El archivo es demasiado grande. Tamaño máximo: ${maxSizeMB}MB`);
            $(this).val('');
            return;
        }
        
        // Validar tipo de archivo
        var allowedTypes = ['application/pdf', 'image/jpeg', 'image/png', 'application/msword', 
                          'application/vnd.openxmlformats-officedocument.wordprocessingml.document'];
        if (!allowedTypes.includes(file.type)) {
            showErrorAlert('Tipo de archivo no permitido. Use: PDF, JPG, PNG, DOC, DOCX');
            $(this).val('');
            return;
        }
        
        showSuccessAlert(`Archivo "${file.name}" seleccionado correctamente.`);
    });
}

/**
 * Debounce para búsquedas
 */
function debounce(func, wait) {
    var timeout;
    return function executedFunction(...args) {
        var later = function() {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

/**
 * Búsqueda en tiempo real
 */
function setupLiveSearch(inputSelector, tableSelector, columnIndexes = []) {
    $(inputSelector).on('keyup', debounce(function() {
        var searchTerm = $(this).val().toLowerCase();
        var rows = $(tableSelector + ' tbody tr');
        
        rows.each(function() {
            var rowText = $(this).text().toLowerCase();
            if (rowText.indexOf(searchTerm) > -1) {
                $(this).show();
            } else {
                $(this).hide();
            }
        });
    }, 300));
}

/**
 * Inicializar DataTables con configuración común
 */
function initDataTable(tableSelector, options = {}) {
    var defaultOptions = {
        language: {
            url: 'https://cdn.datatables.net/plug-ins/1.13.5/i18n/es-ES.json'
        },
        responsive: true,
        pageLength: 10,
        dom: '<"row"<"col-sm-12 col-md-6"l><"col-sm-12 col-md-6"f>><"row"<"col-sm-12"tr>><"row"<"col-sm-12 col-md-5"i><"col-sm-12 col-md-7"p>>'
    };
    
    var finalOptions = Object.assign(defaultOptions, options);
    return $(tableSelector).DataTable(finalOptions);
}

/**
 * Función para formatear moneda
 */
function formatCurrency(value, currency = '$') {
    return currency + parseFloat(value).toFixed(2).replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

/**
 * Obtener parámetro de URL
 */
function getURLParameter(name) {
    return decodeURIComponent((new RegExp('[?|&]' + name + '=' + '([^&;]+?)(&|#|;|$)').exec(location.search) || [, ""])[1].replace(/\+/g, '%20'));
}

/**
 * Mostrar notificación del navegador
 */
function showBrowserNotification(title, options = {}) {
    if ('Notification' in window && Notification.permission === 'granted') {
        new Notification(title, options);
    }
}

/**
 * Log en consola con timestamps
 */
function logDebug(message, data = null) {
    var timestamp = new Date().toLocaleTimeString();
    console.log(`[${timestamp}] ${message}`, data);
}

// ===================================
// INICIALIZACIONES
// ===================================

// Configurar CSRF token para AJAX
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!(/^http:/.test(settings.url) || /^https:/.test(settings.url))) {
            var token = $('meta[name="csrf-token"]').attr('content');
            if (token) {
                xhr.setRequestHeader('X-CSRFToken', token);
            }
        }
    }
});

// Log de inicio
console.log('%c=== FRUTOS DE ORO - Sistema de Gestión de Cumplimiento Normativo ===', 
            'color: #1a472a; font-size: 16px; font-weight: bold;');
console.log('%cSistema cargado correctamente', 'color: #2d7a4d; font-weight: bold;');
