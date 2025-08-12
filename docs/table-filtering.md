# Universal Table Filter System

This document explains how to implement real-time JavaScript filtering for all tables in the GrantTracker system.

## Overview

The universal table filter system provides:
- **Real-time search** across all table content
- **Column-specific filters** (dropdowns for status, category, etc.)
- **Row counting** (showing X of Y items)
- **Keyboard shortcuts** (Ctrl+F to focus search, Escape to clear)
- **Clear filters** functionality
- **Responsive design** that works on all devices

## How to Use

### 1. Basic Implementation

Simply add the `data-table-filter` attribute to any table:

```html
<table id="myTable" data-table-filter='{"searchPlaceholder": "Search items..."}'>
    <!-- table content -->
</table>
```

### 2. Advanced Configuration

For tables with specific filters:

```html
<table id="proposalsTable" data-table-filter='{
    "searchPlaceholder": "Search proposals...",
    "filters": [
        {
            "column": "status",
            "label": "Statuses",
            "columnIndex": 6,
            "options": [
                {"value": "Draft", "label": "Draft"},
                {"value": "Approved", "label": "Approved"}
            ]
        },
        {
            "column": "category",
            "label": "Categories", 
            "columnIndex": 4,
            "options": [
                {"value": "Infrastructure", "label": "Infrastructure"},
                {"value": "Academic", "label": "Academic"}
            ]
        }
    ]
}'>
```

### 3. Configuration Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `searchPlaceholder` | string | "Search..." | Placeholder text for search input |
| `showRowCount` | boolean | true | Show/hide row count display |
| `keyboardShortcuts` | boolean | true | Enable/disable keyboard shortcuts |
| `filters` | array | [] | Array of filter configurations |

### 4. Filter Configuration

Each filter object should have:

```javascript
{
    "column": "unique_name",           // Unique identifier for the filter
    "label": "Human Readable Name",    // Display name for the filter
    "columnIndex": 4,                  // CSS nth-child index (1-based)
    "options": [                       // Array of filter options
        {"value": "option1", "label": "Option 1"},
        {"value": "option2", "label": "Option 2"}
    ]
}
```

## Examples

### User Management Table

```html
<table id="usersTable" data-table-filter='{
    "searchPlaceholder": "Search users...",
    "filters": [
        {
            "column": "role",
            "label": "Roles",
            "columnIndex": 3,
            "options": [
                {"value": "REB Officer", "label": "REB Officer"},
                {"value": "School Administrator", "label": "School Administrator"},
                {"value": "Teacher", "label": "Teacher"}
            ]
        },
        {
            "column": "status",
            "label": "Status",
            "columnIndex": 4,
            "options": [
                {"value": "Active", "label": "Active"},
                {"value": "Inactive", "label": "Inactive"},
                {"value": "Pending", "label": "Pending"}
            ]
        }
    ]
}'>
```

### Budget Table

```html
<table id="budgetTable" data-table-filter='{
    "searchPlaceholder": "Search budget items...",
    "filters": [
        {
            "column": "category",
            "label": "Budget Categories",
            "columnIndex": 2,
            "options": [
                {"value": "Personnel", "label": "Personnel"},
                {"value": "Equipment", "label": "Equipment"},
                {"value": "Infrastructure", "label": "Infrastructure"}
            ]
        },
        {
            "column": "period",
            "label": "Budget Periods",
            "columnIndex": 3,
            "options": [
                {"value": "2024-2025", "label": "2024-2025"},
                {"value": "2025-2026", "label": "2025-2026"}
            ]
        }
    ]
}'>
```

## Manual Initialization

If you need to initialize the filter manually:

```javascript
// Initialize with custom options
const tableFilter = new TableFilter('myTableId', {
    searchPlaceholder: 'Custom search...',
    filters: [
        // ... filter configurations
    ]
});

// Refresh filters
tableFilter.refresh();

// Destroy filter
tableFilter.destroy();
```

## Keyboard Shortcuts

- **Ctrl/Cmd + F**: Focus search input
- **Escape**: Clear search and blur input

## Browser Compatibility

- Chrome 60+
- Firefox 55+
- Safari 12+
- Edge 79+

## CSS Classes

The system automatically adds these CSS classes:

- `.table-filter-container`: Main filter container
- `.table-search`: Search input field
- `.filter-select`: Filter dropdown selects
- `.clear-filters`: Clear filters button
- `.row-count`: Row count display

## Troubleshooting

### Filter not working?
1. Check that the table has a unique ID
2. Verify the `data-table-filter` attribute is properly formatted JSON
3. Ensure the `table-filter.js` file is loaded
4. Check browser console for JavaScript errors

### Column index issues?
- Column indexing starts at 1 (not 0)
- Count from left to right including all visible columns
- Hidden columns still count toward the index

### Performance issues?
- The filter processes all rows in real-time
- For very large tables (>1000 rows), consider server-side filtering
- The system automatically debounces input events for better performance

## Best Practices

1. **Use descriptive placeholders**: "Search proposals..." vs "Search..."
2. **Limit filter options**: Keep dropdowns under 20 options for usability
3. **Consistent column indexing**: Use the same column structure across similar tables
4. **Meaningful filter labels**: Use human-readable names for filters
5. **Test on mobile**: Ensure filters work well on small screens
