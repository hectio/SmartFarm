/**
 * Parcelles JavaScript - Interactions et fonctionnalités pour l'application Parcelles
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialiser les tooltips Bootstrap
    initializeBootstrapTooltips();
    
    // Initialiser les filtres
    initializeFilters();
    
    // Initialiser les actions en masse
    initializeBulkActions();
});

/**
 * Initialiser les tooltips Bootstrap
 */
function initializeBootstrapTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

/**
 * Initialiser les filtres de parcelles
 */
function initializeFilters() {
    const filterForm = document.getElementById('parcelle-filter-form');
    const filterInputs = document.querySelectorAll('.parcelle-filter');
    
    if (filterForm) {
        filterInputs.forEach(input => {
            input.addEventListener('change', function() {
                filterForm.submit();
            });
        });
    }
}

/**
 * Initialiser les actions en masse
 */
function initializeBulkActions() {
    const selectAllCheckbox = document.getElementById('select-all-parcelles');
    const parcellCheckboxes = document.querySelectorAll('.parcelle-checkbox');
    
    if (selectAllCheckbox) {
        selectAllCheckbox.addEventListener('change', function() {
            parcellCheckboxes.forEach(checkbox => {
                checkbox.checked = this.checked;
            });
            updateBulkActionButtons();
        });
    }
    
    parcellCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('change', function() {
            updateBulkActionButtons();
        });
    });
}

/**
 * Mettre à jour l'état des boutons d'actions en masse
 */
function updateBulkActionButtons() {
    const parcellCheckboxes = document.querySelectorAll('.parcelle-checkbox:checked');
    const bulkActionButtons = document.querySelectorAll('.bulk-action-btn');
    
    if (parcellCheckboxes.length > 0) {
        bulkActionButtons.forEach(btn => {
            btn.disabled = false;
        });
    } else {
        bulkActionButtons.forEach(btn => {
            btn.disabled = true;
        });
    }
}

/**
 * Récupérer les IDs des parcelles sélectionnées
 */
function getSelectedParcellesIds() {
    const checkboxes = document.querySelectorAll('.parcelle-checkbox:checked');
    return Array.from(checkboxes).map(cb => cb.value);
}

/**
 * Afficher une confirmation avant suppression
 */
function confirmDelete(parcelleNom) {
    return confirm(`Êtes-vous sûr de vouloir supprimer la parcelle "${parcelleNom}"? Cette action est irréversible.`);
}

/**
 * Exporter les parcelles en CSV
 */
function exportToCSV() {
    const ids = getSelectedParcellesIds();
    if (ids.length === 0) {
        alert('Veuillez sélectionner au moins une parcelle.');
        return;
    }
    window.location.href = `/parcelles/export/?ids=${ids.join(',')}`;
}

/**
 * Imprimer la liste des parcelles
 */
function printParcelles() {
    window.print();
}

/**
 * Valider le formulaire avant envoi
 */
function validateParcelleForm(formElement) {
    const code = formElement.querySelector('[name="code"]').value.trim();
    const nom = formElement.querySelector('[name="nom"]').value.trim();
    const superficie = formElement.querySelector('[name="superficie"]').value;
    
    if (!code || !nom || !superficie) {
        alert('Veuillez remplir tous les champs obligatoires.');
        return false;
    }
    
    if (isNaN(superficie) || parseFloat(superficie) <= 0) {
        alert('La superficie doit être un nombre positif.');
        return false;
    }
    
    return true;
}

/**
 * Fonction pour réinitialiser les filtres
 */
function resetFilters() {
    document.getElementById('parcelle-filter-form').reset();
    document.getElementById('parcelle-filter-form').submit();
}

// Exporter les fonctions globales
window.parcellesApp = {
    confirmDelete,
    exportToCSV,
    printParcelles,
    validateParcelleForm,
    resetFilters,
    getSelectedParcellesIds
};
