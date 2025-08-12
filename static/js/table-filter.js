/**
 * Universal Table Filter - Real-time filtering for all tables
 * Features: Search, column filters, row counting, keyboard shortcuts
 */

class TableFilter {
    constructor(tableId, options = {}) {
        this.tableId = tableId;
        this.table = document.getElementById(tableId);
        this.options = {
            searchPlaceholder: 'Search...',
            showRowCount: true,
            keyboardShortcuts: true,
            filters: [],
            ...options
        };

        this.init();
    }

    init() {
        if (!this.table) {
            console.error(`Table with ID '${this.tableId}' not found`);
            return;
        }

        this.createFilterUI();
        this.bindEvents();
        this.updateRowCount();
    }

    createFilterUI() {
        // Create filter container
        const filterContainer = document.createElement('div');
        filterContainer.className = 'table-filter-container mb-3';
        filterContainer.innerHTML = this.getFilterHTML();

        // Insert before table
        this.table.parentNode.insertBefore(filterContainer, this.table);

        // Store references
        this.searchInput = filterContainer.querySelector('.table-search');
        this.clearButton = filterContainer.querySelector('.clear-filters');
        this.filterSelects = filterContainer.querySelectorAll('.filter-select');
        this.rowCountDisplay = filterContainer.querySelector('.row-count');
    }

    getFilterHTML() {
        let html = `
            <div class="row">
                <div class="col-md-6">
                    <div class="input-group">
                        <span class="input-group-text">
                            <i class="fas fa-search"></i>
                        </span>
                        <input type="text" class="table-search form-control" placeholder="${this.options.searchPlaceholder}">
                        <button class="clear-filters btn btn-outline-secondary" type="button">
                            <i class="fas fa-times"></i>
                        </button>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="d-flex gap-2">
        `;

        // Add custom filters
        this.options.filters.forEach(filter => {
            html += `
                <select class="filter-select form-select" data-filter="${filter.column}">
                    <option value="">All ${filter.label}</option>
                    ${filter.options.map(option =>
                `<option value="${option.value}">${option.label}</option>`
            ).join('')}
                </select>
            `;
        });

        html += `
                    </div>
                </div>
            </div>
            ${this.options.showRowCount ? '<div class="row-count text-muted small mt-2"></div>' : ''}
        `;

        return html;
    }

    bindEvents() {
        // Search input
        this.searchInput.addEventListener('input', () => this.filterTable());

        // Filter selects
        this.filterSelects.forEach(select => {
            select.addEventListener('change', () => this.filterTable());
        });

        // Clear button
        this.clearButton.addEventListener('click', () => this.clearFilters());

        // Keyboard shortcuts
        if (this.options.keyboardShortcuts) {
            this.setupKeyboardShortcuts();
        }
    }

    setupKeyboardShortcuts() {
        document.addEventListener('keydown', (e) => {
            // Ctrl/Cmd + F to focus search
            if ((e.ctrlKey || e.metaKey) && e.key === 'f') {
                e.preventDefault();
                this.searchInput.focus();
            }

            // Escape to clear search
            if (e.key === 'Escape') {
                this.searchInput.value = '';
                this.filterTable();
                this.searchInput.blur();
            }
        });
    }

    filterTable() {
        const searchTerm = this.searchInput.value.toLowerCase();
        const filterValues = {};

        // Get filter values
        this.filterSelects.forEach(select => {
            const filterName = select.dataset.filter;
            filterValues[filterName] = select.value.toLowerCase();
        });

        const rows = this.table.querySelectorAll('tbody tr');
        let visibleCount = 0;

        rows.forEach(row => {
            let showRow = true;
            const rowText = row.textContent.toLowerCase();

            // Search filter
            if (searchTerm && !rowText.includes(searchTerm)) {
                showRow = false;
            }

            // Column filters
            Object.entries(filterValues).forEach(([filterName, filterValue]) => {
                if (filterValue) {
                    const filterConfig = this.options.filters.find(f => f.column === filterName);
                    if (filterConfig) {
                        const cell = row.querySelector(`td:nth-child(${filterConfig.columnIndex})`);
                        if (cell && !cell.textContent.toLowerCase().includes(filterValue)) {
                            showRow = false;
                        }
                    }
                }
            });

            // Show/hide row
            row.style.display = showRow ? '' : 'none';
            if (showRow) visibleCount++;
        });

        this.updateRowCount(visibleCount, rows.length);
    }

    updateRowCount(visible = null, total = null) {
        if (!this.options.showRowCount || !this.rowCountDisplay) return;

        if (visible === null || total === null) {
            const rows = this.table.querySelectorAll('tbody tr');
            visible = Array.from(rows).filter(row => row.style.display !== 'none').length;
            total = rows.length;
        }

        this.rowCountDisplay.textContent = `Showing ${visible} of ${total} items`;
    }

    clearFilters() {
        this.searchInput.value = '';
        this.filterSelects.forEach(select => select.value = '');
        this.filterTable();
    }

    // Public method to refresh filters
    refresh() {
        this.filterTable();
    }

    // Public method to destroy
    destroy() {
        const filterContainer = this.table.parentNode.querySelector('.table-filter-container');
        if (filterContainer) {
            filterContainer.remove();
        }
    }
}

// Auto-initialize tables with data-table-filter attribute
document.addEventListener('DOMContentLoaded', function () {
    const tables = document.querySelectorAll('[data-table-filter]');
    tables.forEach(table => {
        const options = JSON.parse(table.dataset.tableFilter || '{}');
        new TableFilter(table.id, options);
    });
});

// Export for manual initialization
window.TableFilter = TableFilter;
