# Imports
import csv
import os
import flet as ft

# Input CSV filename
CSV_FILENAME = "repatriation_items.csv"

# Output summary filename
SUMMARY_FILENAME = "repatriation_summary.txt"

# CSV column headers 
ITEM_ID_HEADER = "Item ID"
ITEM_TITLE_HEADER = "Item Title"
CATEGORY_HEADER = "Category"
INSTITUTION_HEADER = "Institution Name"
COMMUNITIES_HEADER = "Communities"
STORAGE_LOCATION_HEADER = "Storage Location"
HOLDING_SINCE_HEADER = "Holding Since"

CSV_HEADERS = [
    ITEM_ID_HEADER,
    ITEM_TITLE_HEADER,
    CATEGORY_HEADER,
    INSTITUTION_HEADER,
    COMMUNITIES_HEADER,
    STORAGE_LOCATION_HEADER,
    HOLDING_SINCE_HEADER,
]

# Helper Functions
def get_current_directory():
    """Return the directory of the current file."""
    return os.path.dirname(os.path.abspath(__file__))

def get_csv_file_path():
    """Return the full path to the CSV file."""
    return os.path.join(get_current_directory(), CSV_FILENAME)

def get_summary_file_path():
    """Return the full path to the summary file."""
    return os.path.join(get_current_directory(), SUMMARY_FILENAME)
    
def load_repatriation_items(csv_file_path):
    """
    Read data from CSV into a dictionary keyed by Item ID.
    Raises FileNotFoundError if CSV does not exist.
    Raises ValueError if expected columns are missing.
    """
    if not os.path.exists(csv_file_path):
        raise FileNotFoundError(f"CSV not found: {csv_file_path}")
    repatriation_items = {}
    with open(csv_file_path, newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        # Check for missing headers
        missing_headers = [header for header in CSV_HEADERS if header not in reader.fieldnames]
        if missing_headers:
            raise ValueError(f"Missing expected columns: {missing_headers}")
        # Read each row and add to dictionary
        for row in reader:
            item_id = (row.get(ITEM_ID_HEADER) or "").strip()
            if not item_id:
                continue
            repatriation_items[item_id] = {
                ITEM_TITLE_HEADER: (row.get(ITEM_TITLE_HEADER) or "").strip(),
                CATEGORY_HEADER: (row.get(CATEGORY_HEADER) or "").strip(),
                INSTITUTION_HEADER: (row.get(INSTITUTION_HEADER) or "").strip(),
                COMMUNITIES_HEADER: (row.get(COMMUNITIES_HEADER) or "").strip(),
                STORAGE_LOCATION_HEADER: (row.get(STORAGE_LOCATION_HEADER) or "").strip(),
                HOLDING_SINCE_HEADER: (row.get(HOLDING_SINCE_HEADER) or "").strip(),
            }
    return repatriation_items

def save_repatriation_items(csv_file_path, repatriation_items_dict):
    """
    Write the dictionary back to CSV (output to file).
    """
    with open(csv_file_path, "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=CSV_HEADERS)
        writer.writeheader()
        # Write each item as a row
        for item_id, item_info in repatriation_items_dict.items():
            writer.writerow({
                ITEM_ID_HEADER: item_id,
                ITEM_TITLE_HEADER: item_info[ITEM_TITLE_HEADER],
                CATEGORY_HEADER: item_info[CATEGORY_HEADER],
                INSTITUTION_HEADER: item_info[INSTITUTION_HEADER],
                COMMUNITIES_HEADER: item_info[COMMUNITIES_HEADER],
                STORAGE_LOCATION_HEADER: item_info[STORAGE_LOCATION_HEADER],
                HOLDING_SINCE_HEADER: item_info[HOLDING_SINCE_HEADER],
            })

def save_repatriation_summary(summary_file_path, repatriation_items_dict):
    """
    Perform calculations and write a simple text summary.
    Returns the path to the summary file.
    """
    total_items = len(repatriation_items_dict)
    community_counts, category_counts = {}, {}
    # Count items by community and category
    for item_info in repatriation_items_dict.values():
        community = (item_info[COMMUNITIES_HEADER] or "Unaffiliated").strip()
        community_counts[community] = community_counts.get(community, 0) + 1
        category = (item_info[CATEGORY_HEADER] or "Unknown").strip()
        category_counts[category] = category_counts.get(category, 0) + 1

    # Build summary lines
    summary_lines = [f"Total items: {total_items}", "", "By Community:"]
    for community, count in sorted(community_counts.items()):
        summary_lines.append(f"  - {community}: {count}")
    summary_lines.append("")
    summary_lines.append("By Category:")
    for category, count in sorted(category_counts.items()):
        summary_lines.append(f"  - {category}: {count}")

    # Write summary to file
    with open(summary_file_path, "w", encoding="utf-8") as summary_file:
        summary_file.write("\n".join(summary_lines))
    return summary_file_path

# ---------- Flet UI ---------- 
def main(page: ft.Page):
    """
    Sets up the page, loads data, and defines UI controls and event handlers.
    """
    page.title = "Repatriation Items"
    page.theme_mode = ft.ThemeMode.DARK
    page.window_width = 900
    page.window_height = 620

    # Data model: dictionary keyed by Item ID
    try:
        repatriation_items = load_repatriation_items(get_csv_file_path())
        status_message = ft.Text("Loaded CSV.", selectable=True)
    except Exception as ex:
        # Show error if CSV cannot be loaded
        page.add(ft.Text(str(ex), color="red"))
        return

    # Controls (keyboard input)
    search_text_field = ft.TextField(label="Search (ID, Title, Community, Category, Institution)", expand=True, bgcolor="#0ABAB5")
    update_item_id_field = ft.TextField(label="Item ID to update", width=180, bgcolor="#0ABAB5")
    update_community_field = ft.TextField(label='New "Communities" value', expand=True, bgcolor="#0ABAB5")
    repatriation_list_view = ft.ListView(expand=True, spacing=6, auto_scroll=False)

    def refresh_repatriation_list(filtered_items_dict=None):
        """
        Render list from dictionary.
        If filtered_items_dict is provided, display only those items.
        Allows dynamic updates to list view.
        """
        repatriation_list_view.controls.clear()
        items_to_display = filtered_items_dict if filtered_items_dict is not None else repatriation_items
        # Sort and display items, lambda function to enable numerical sorting
        for item_id, item_info in sorted(items_to_display.items(), key=lambda kv: int(kv[0])):
            subtitle = (
                f'{item_info[CATEGORY_HEADER]} | {item_info[INSTITUTION_HEADER]} | '
                f'{item_info[COMMUNITIES_HEADER]} | {item_info[STORAGE_LOCATION_HEADER]} | '
                f'Since {item_info[HOLDING_SINCE_HEADER]}'
            )
            repatriation_list_view.controls.append(
                ft.ListTile(
                    leading=ft.Icon(name="inventory_2"),
                    title=ft.Text(f'{item_id} — {item_info[ITEM_TITLE_HEADER]}'),
                    subtitle=ft.Text(subtitle),
                    dense=True,
                )
            )
        repatriation_list_view.update()

    def handle_search(event):
        """
        Handle search button click.
        Filters items based on search query.
        """
        search_query = (search_text_field.value or "").strip().lower()
        if not search_query:
            status_message.value = "Showing all."
            refresh_repatriation_list()
        else:
            filtered_items = {}
            # Search in multiple fields
            for item_id, item_info in repatriation_items.items():
                searchable_text = " | ".join([
                    item_id.lower(),
                    item_info[ITEM_TITLE_HEADER].lower(),
                    item_info[COMMUNITIES_HEADER].lower(),
                    item_info[CATEGORY_HEADER].lower(),
                    item_info[INSTITUTION_HEADER].lower(),
                    item_info[STORAGE_LOCATION_HEADER].lower(),
                ])
                if search_query in searchable_text:
                    filtered_items[item_id] = item_info
            status_message.value = f"Matches: {len(filtered_items)}"
            refresh_repatriation_list(filtered_items)
        page.update()

    def handle_update_community(event):
        """
        Handle update community button click.
        Updates the 'Communities' field for the given Item ID.
        """
        item_id_to_update = (update_item_id_field.value or "").strip()
        new_community_value = (update_community_field.value or "").strip()
        
        if not item_id_to_update:
            status_message.value = "Enter an Item ID."
        elif item_id_to_update not in repatriation_items:
            status_message.value = f"Item ID {item_id_to_update} not found."
        else:
            # Update community value and save to CSV
            repatriation_items[item_id_to_update][COMMUNITIES_HEADER] = " ".join(new_community_value.split())
            save_repatriation_items(get_csv_file_path(), repatriation_items)
            refresh_repatriation_list()
            status_message.value = f'Updated Communities for {item_id_to_update}.'
        page.update()

    def handle_save_summary(event):
        """
        Handle save summary button click.
        Saves a summary file with item counts by community and category.
        """
        summary_file_path = save_repatriation_summary(get_summary_file_path(), repatriation_items)
        status_message.value = f"Saved summary -> {os.path.basename(summary_file_path)}"
        page.update()

    def handle_clear_search(event):
        """
        Handle clear search button click.
        Clears the search field and shows all items.
        """
        search_text_field.value = ""
        status_message.value = "Cleared."
        refresh_repatriation_list()
        page.update()

    # Layout: page controls
    page.add(
        ft.Text("Repatriation Items", size=20, weight="bold"),
        ft.Row([
            search_text_field,
            ft.CupertinoFilledButton("Search", on_click=handle_search),
            ft.CupertinoFilledButton("Clear", on_click=handle_clear_search)
        ]),
        ft.Row([
            update_item_id_field,
            update_community_field,
            ft.CupertinoFilledButton(
                "Update Community", on_click=handle_update_community),
            ft.CupertinoFilledButton(
                "Save Summary", on_click=handle_save_summary)
        ]),
        ft.Divider(),
        repatriation_list_view,
        ft.Divider(),
        status_message,
    )

    refresh_repatriation_list()

if __name__ == "__main__":
    ft.app(target=main)
