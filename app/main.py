import flet as ft
import sqlite3
import os

PRICE_PER_SHIRT = 15

def get_db_path():
    db_name = 'inventory.db'
    paths = [
        os.environ.get("HOME"),
        os.path.dirname(os.path.abspath(__file__)),
        os.getcwd()
    ]
    for p in paths:
        if p:
            try:
                test_file = os.path.join(p, "test.tmp")
                with open(test_file, 'w') as f:
                    f.write("1")
                os.remove(test_file)
                return os.path.join(p, db_name)
            except Exception:
                continue
    return db_name


DB_PATH = get_db_path()


def initialize_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='shirts'")
    table_exists = cursor.fetchone()

    if not table_exists:
        cursor.execute('''
                       CREATE TABLE shirts
                       (
                           id          INTEGER PRIMARY KEY AUTOINCREMENT,
                           color       TEXT,
                           size        TEXT,
                           initial_qty INTEGER,
                           sold_qty    INTEGER
                       )
                       ''')

        thanasis_data = [
            ("ΜΠΟΡΝΤΟ", "2XL", 2, 1), ("ΜΠΟΡΝΤΟ", "XL", 3, 3), ("ΜΠΟΡΝΤΟ", "L", 3, 1),
            ("ΜΠΟΡΝΤΟ", "M", 3, 3), ("ΜΠΟΡΝΤΟ", "S", 1, 1),
            ("ΜΠΕΖ", "XL", 2, 0), ("ΜΠΕΖ", "L", 2, 0), ("ΜΠΕΖ", "M", 2, 1), ("ΜΠΕΖ", "S", 1, 0),
            ("ΛΕΥΚΑ", "XL", 3, 2), ("ΛΕΥΚΑ", "L", 3, 1), ("ΛΕΥΚΑ", "M", 3, 1),
            ("ΛΕΥΚΑ", "S", 3, 0), ("ΛΕΥΚΑ", "9-10", 3, 0),
            ("ΜΑΥΡΑ", "2XL", 3, 0), ("ΜΑΥΡΑ", "XL", 7, 3), ("ΜΑΥΡΑ", "L", 3, 2),
            ("ΜΑΥΡΑ", "M", 3, 2), ("ΜΑΥΡΑ", "S", 3, 2), ("ΜΑΥΡΑ", "9-10", 3, 0), ("ΜΑΥΡΑ", "3XL", 2, 1)
        ]

        cursor.executemany('INSERT INTO shirts (color, size, initial_qty, sold_qty) VALUES (?, ?, ?, ?)', thanasis_data)
        conn.commit()

    conn.close()


def get_inventory():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, color, size, initial_qty, sold_qty FROM shirts ORDER BY color, size")
    rows = cursor.fetchall()
    conn.close()
    return rows


def update_sold_quantity(item_id, new_sold_qty):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE shirts SET sold_qty = ? WHERE id = ?", (new_sold_qty, item_id))
    conn.commit()
    conn.close()


def main(page: ft.Page):
    page.title = "Απόθεμα Μπλουζάκια"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.scroll = "adaptive"
    page.window_width = 400

    initialize_db()

    inventory_list = ft.Column(spacing=10)

    revenue_text = ft.Text("0 €", size=32, weight="bold", color=ft.Colors.GREEN_700)
    revenue_card = ft.Container(
        content=ft.Column([
            ft.Text("Συνολικά Έσοδα", size=14, color=ft.Colors.GREY_700, weight="bold"),
            revenue_text
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        padding=15,
        bgcolor=ft.Colors.GREEN_50,
        border_radius=15,
        border=ft.Border.all(2, ft.Colors.GREEN_200)
    )

    def load_ui():
        inventory_list.controls.clear()
        items = get_inventory()

        total_revenue = 0

        for item in items:
            item_id, color, size, initial_qty, sold_qty = item
            available = initial_qty - sold_qty

            total_revenue += sold_qty * PRICE_PER_SHIRT

            is_out_of_stock = available == 0
            card_color = ft.Colors.RED_50 if is_out_of_stock else ft.Colors.WHITE

            def minus_click(e, i=item_id, s=sold_qty):
                if s > 0:
                    update_sold_quantity(i, s - 1)
                    load_ui()

            def plus_click(e, i=item_id, s=sold_qty, init=initial_qty):
                if s < init:
                    update_sold_quantity(i, s + 1)
                    load_ui()

            row = ft.Container(
                content=ft.Row([
                    ft.Column([
                        ft.Text(f"{color} - {size}", size=18, weight="bold"),
                        ft.Text(f"Αρχικά: {initial_qty} | Πουλήθηκαν: {sold_qty}", size=12, color=ft.Colors.GREY_700),
                    ], expand=True),

                    ft.IconButton(ft.Icons.REMOVE_CIRCLE_OUTLINE, on_click=minus_click, icon_color="red"),
                    ft.Column([
                        ft.Text(str(available), size=22, weight="bold", color=ft.Colors.BLUE_900),
                        ft.Text("Διαθέσιμα", size=10)
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    ft.IconButton(ft.Icons.ADD_CIRCLE, on_click=plus_click, icon_color="green", icon_size=30),
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                padding=15,
                bgcolor=card_color,
                border=ft.Border.all(1, ft.Colors.OUTLINE_VARIANT),
                border_radius=12
            )
            inventory_list.controls.append(row)

        revenue_text.value = f"{total_revenue} €"
        page.update()

    main_layout = ft.SafeArea(
        content=ft.Column([
            ft.Text("Διαχείριση Πωλήσεων", size=26, weight="bold", color=ft.Colors.BLUE_800),
            revenue_card,
            ft.Divider(),
            inventory_list
        ])
    )

    page.add(main_layout)
    load_ui()


ft.run(main)