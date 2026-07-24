import flet as ft
import sqlite3


def get_inventory():
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, color, size, initial_qty, sold_qty FROM shirts ORDER BY color, size")
    rows = cursor.fetchall()
    conn.close()
    return rows


def update_sold_quantity(item_id, new_sold_qty):
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE shirts SET sold_qty = ? WHERE id = ?", (new_sold_qty, item_id))
    conn.commit()
    conn.close()


def main(page: ft.Page):
    page.title = "Απόθεμα Μπλουζάκια"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.scroll = "adaptive"
    page.window_width = 400

    inventory_list = ft.Column(spacing=10)

    def load_ui():
        inventory_list.controls.clear()
        items = get_inventory()

        for item in items:
            item_id, color, size, initial_qty, sold_qty = item
            available = initial_qty - sold_qty

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
                    # Πληροφορίες Είδους
                    ft.Column([
                        ft.Text(f"{color} - {size}", size=18, weight="bold"),
                        ft.Text(f"Αρχικά: {initial_qty} | Πουλήθηκαν: {sold_qty}", size=12, color=ft.Colors.GREY_700),
                    ], expand=True),

                    # Κουμπιά & Διαθέσιμο απόθεμα
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
        page.update()

    page.add(
        ft.Text("Διαχείριση Πωλήσεων", size=26, weight="bold", color=ft.Colors.BLUE_800),
        ft.Divider(),
        inventory_list
    )
    load_ui()


ft.run(main)