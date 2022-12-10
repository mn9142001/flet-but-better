import flet as ft

class App:
    views = {}

    def __init__(self) -> None:
        self.load_builtin_views()

    def __call__(self, page : ft.Page, title : str = "HomePage"):
        page.on_route_change = self.on_route_change
        page.on_view_pop = self.on_view_pop
        self.route = page.route
        self.page = page
        page.title = title
        return self.prefix_render(page)


    def on_route_change(self, event: ft.RouteChangeEvent):

        #condition to prevent duplicate screens when returning back
        if  not event.route == self.top_view.route:
            self.page.views.append(
                ft.View(
                    event.route,
                    self.views.get(event.route, self.views['/404'])(self.page)
                )
            )

        self.page.update()

        
    def on_view_pop(self, event : ft.ViewPopEvent):
        self.page.views.pop()
        self.page.go(self.top_view.route)


    def prefix_render(self, page : ft.Page):
        """method used to do some stuff before rendering the HomePage"""
        return page.go("/")

    def view_404(self, page : ft.Page):
        return [
                ft.AppBar(title=ft.Text("Flet app")),
                ft.ElevatedButton("Page is not found", on_click=lambda _: page.go(self.previous_route)),
            ]

    def load_builtin_views(self):
        views = [attr for attr in dir(self) if attr.startswith("view_")]

        for view in views:
            self.views[f"/{view.split('view_')[1]}"] = getattr(self, view)


    def register(self, route):
        def decorator(func):
            self.views[f"{route}"] = func
            def wrapper(*args, **kwargs):
                result = function(*args, **kwargs)
                return result
            return wrapper
        return decorator

    @property
    def top_view(self):
        return self.page.views[-1]

    @property
    def previous_route(self):
        if len(self.page.views) > 1:
            return self.page.views[-2].route
        return self.page.views[-1].route
