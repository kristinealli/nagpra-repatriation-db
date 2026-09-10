"""Repatriation Database Management System - CS-205 Final Project

A GUI application for tracking and managing repatriation requests and transfers.
Provides filtering, statistics, and export capabilities for repatriation data.
"""

import csv
import datetime
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

# -----------------------
# Globals / dictionaries
# -----------------------
ROWS = []
NOTES = {}
STATUS_STYLE = {
    "confirmed": {"foreground": "green"},
    "potential": {"foreground": "orange"},
    "pending":   {"foreground": "blue"},
}

def load_data(filepath):
    """Read in data from a CSV file (requirement: read from file)."""
    rows = []
    with open(filepath, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["_status_lc"] = (row.get("status") or "").lower().strip()
            row["_title_lc"] = (row.get("item_title") or "").lower().strip()
            row["_req_dt"] = parse_date(row.get("request_date"))
            row["_xfer_dt"] = parse_date(row.get("transfer_date"))
            rows.append(row)
    return rows


def compute_stats(rows):
    """Calculate summary stats (requirement: calculation)."""
    total = len(rows)
    repatriated = sum(1 for r in rows if r["_xfer_dt"] is not None)
    pct = (repatriated / total * 100) if total else 0.0

    by_comm = {}
    for r in rows:  # loop requirement
        comm = r.get("community", "Unknown")
        by_comm[comm] = by_comm.get(comm, 0) + 1

    # Optional: average days request->transfer
    deltas = []
    for r in rows:
        if r["_req_dt"] and r["_xfer_dt"]:
            deltas.append((r["_xfer_dt"] - r["_req_dt"]).days)
    avg_days = sum(deltas)/len(deltas) if deltas else None

    return {"total": total, "repatriated": repatriated, "pct": pct, "by_comm": by_comm, "avg_days": avg_days}


def apply_filters():
    """Filter based on GUI inputs (logic + string manipulation)."""
    q = search_var.get().strip().lower()
    comm = community_var.get().strip()
    inst = institution_var.get().strip()
    status = status_var.get().strip().lower()

    filtered = []
    for r in ROWS:
        if q and q not in r["_title_lc"]:
            continue
        if comm and comm != r.get("community", ""):
            continue
        if inst and inst != r.get("holding_institution", ""):
            continue
        if status and status != r["_status_lc"]:
            continue
        filtered.append(r)

    populate_table(filtered)
    stats = compute_stats(filtered)
    stats_var.set(f"Total: {stats['total']} | Repatriated: {stats['repatriated']} "
                f"({stats['pct']:.1f}%) | Avg days: {stats['avg_days'] or '-'}")


def populate_table(rows):
    tree.delete(*tree.get_children())
    for r in rows:
        iid = r.get("item_id")
        st = r["_status_lc"]
        style = STATUS_STYLE.get(st, {})
        tags = []
        if st in STATUS_STYLE:
            tags.append(st)
        tree.insert("", "end", iid=iid,
                    values=(r.get("item_id"), r.get("item_title"),
                            r.get("community"), r.get("holding_institution"),
                            r.get("status"), NOTES.get(str(iid), "")),
                    tags=tags)


def export_results():
    """Write filtered rows + summary to files (requirement: output to file)."""
    # Get filtered rows from the current table display
    ids = [tree.item(i, "values")[0] for i in tree.get_children()]
    filtered = [r for r in ROWS if r.get("item_id") in ids]

    # Save CSV
    out_csv = f"filtered_{safe_slug(search_var.get() or 'all')}.csv"
    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "item_id", "item_title", "community", "holding_institution", "status", "request_date", "transfer_date"
        ])
        writer.writeheader()
        for r in filtered:
            writer.writerow({k: r.get(k, "") for k in writer.fieldnames})

    # Save summary (txt)
    stats = compute_stats(filtered)
    out_txt = f"summary_{safe_slug(search_var.get() or 'all')}.txt"
    with open(out_txt, "w", encoding="utf-8") as f:
        f.write(f"Total items: {stats['total']}\n")
        f.write(f"Repatriated: {stats['repatriated']} ({stats['pct']:.1f}%)\n")
        f.write(f"Average days request->transfer: {stats['avg_days']}\n")
        f.write("Items by community:\n")
        for comm, ct in sorted(stats["by_comm"].items(), key=lambda x: (-x[1], x[0])):
            f.write(f"  - {comm}: {ct}\n")

    messagebox.showinfo("Export", f"Saved:\n{out_csv}\n{out_txt}")


def add_note():
    """Read keyboard input and store in a dict (dictionary + input)."""
    sel = tree.selection()
    if not sel:
        messagebox.showwarning(
            "No selection", "Please select an item in the table.")
        return
    iid = tree.item(sel[0], "values")[0]
    note = note_var.get().strip()
    if note:
        NOTES[str(iid)] = note
        apply_filters()  # refresh display


def open_file():
    path = filedialog.askopenfilename(
        filetypes=[("CSV files", "*.csv"), ("All", "*.*")])
    if not path:
        return
    if not path.lower().endswith(".csv"):
        messagebox.showerror(
            "File error", "Please choose a CSV exported from your MySQL view.")
        return
    global ROWS
    ROWS = load_data(path)
    # Populate filter dropdowns
    communities = sorted({r.get("community", "")
                        for r in ROWS if r.get("community")})
    institutions = sorted({r.get("holding_institution", "")
                        for r in ROWS if r.get("holding_institution")})
    community_combo["values"] = [""] + communities
    institution_combo["values"] = [""] + institutions
    apply_filters()


# -----------------------
# GUI
# -----------------------
root = tk.Tk()
root.title("Repatriation Tracker")

top = ttk.Frame(root)
top.pack(fill="x", padx=8, pady=8)

ttk.Button(top, text="Open CSV", command=open_file).pack(side="left")

search_var = tk.StringVar()
ttk.Label(top, text="Search Title").pack(side="left", padx=(8, 2))
ttk.Entry(top, textvariable=search_var, width=30).pack(side="left")
ttk.Button(top, text="Apply Filters",
        command=apply_filters).pack(side="left", padx=6)

community_var = tk.StringVar()
institution_var = tk.StringVar()
status_var = tk.StringVar()

ttk.Label(top, text="Community").pack(side="left", padx=(12, 2))
community_combo = ttk.Combobox(top, textvariable=community_var, width=28)
community_combo.pack(side="left")

ttk.Label(top, text="Institution").pack(side="left", padx=(12, 2))
institution_combo = ttk.Combobox(top, textvariable=institution_var, width=28)
institution_combo.pack(side="left")

ttk.Label(top, text="Status").pack(side="left", padx=(12, 2))
status_combo = ttk.Combobox(top, textvariable=status_var, values=[
                            "", "Confirmed", "Potential", "Pending"], width=12)
status_combo.pack(side="left")

# Table
tree = ttk.Treeview(root, columns=("id", "title", "community",
                    "institution", "status", "note"), show="headings")
for c, w in [("id", 60), ("title", 260), ("community", 220), ("institution", 220), ("status", 80), ("note", 220)]:
    tree.heading(c, text=c.title())
    tree.column(c, width=w, anchor="w")
tree.pack(fill="both", expand=True, padx=8, pady=8)

# Tag styles for status
style = ttk.Style()
# (Tkinter ttk has limited per-row color; tags mainly used here just to mark rows.)

bottom = ttk.Frame(root)
bottom.pack(fill="x", padx=8, pady=8)
stats_var = tk.StringVar(value="Load a CSV to begin.")
ttk.Label(bottom, textvariable=stats_var).pack(side="left")

ttk.Button(bottom, text="Export Results",
        command=export_results).pack(side="right")

note_var = tk.StringVar()
ttk.Entry(bottom, textvariable=note_var, width=40).pack(
    side="right", padx=(0, 6))
ttk.Button(bottom, text="Add Note to Selected",
        command=add_note).pack(side="right", padx=(0, 6))

root.mainloop()
