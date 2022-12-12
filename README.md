# flet-but-better

> It's a flet influenced app, it just flet framework but it's more simple in use with more utilities like refresh page.



## Example:
```
import flet as ft
from main import app
from views import View
import random

@app.register("/store/:id")
def store_page(page : ft.Page, id):
    return [
            ft.AppBar(title=ft.Text("store title")),
            ft.Text(
                f"cool text from store number {id}"
            )
    ]

@app.register("/")
class HomePage(View):
    def render(self, page : ft.Page):
        return [
            ft.AppBar(title=ft.Text(f"random title {random.randint(1, 1000000)}")),
            ft.ElevatedButton(text="go to store", on_click=lambda x : app.navigate_to("/store/asdf")),
            ft.ElevatedButton(text="refresh page", on_click=lambda x : app.refresh_page()),
        ]
        
```

## Pretty cool, right? now we can use both function based views and class based views :"D
