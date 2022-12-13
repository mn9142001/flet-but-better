import flet as ft
from views import BaseView
from mixins import AppMixin
import os
from functools import cached_property

class BaseApp:
    
    def __init__(self) -> None:
        self.load_builtin_views()

    def __call__(self, page : ft.Page):
        page.on_route_change = self.on_route_change
        page.on_view_pop = self.on_view_pop
        self.page = page

        self.clear_page()
        return self.navigate_to(self.route)

    def clear_page(self):
        self.page.views.clear()

    def load_builtin_views(self):
        raise NotImplementedError("load_builtin_views must be implemented")

    def on_route_change(self, event : ft.RouteChangeEvent):
        raise NotImplementedError("on_route_change must be implemented")

    def on_view_pop(self, event : ft.ViewPopEvent):
        return self.page.views.pop()

    def pre_render(self):
        """method used to do some stuff before rendering the HomePage"""

    def update_page(self):
        """we used it to update the page so we can override to do things before every upload"""
        self.page.update()

    def post_render(self):
        """method used if needed to do some stuff after adding the controls to the homepage"""

class App(BaseApp, AppMixin):
    """Main app with benefitial utilities"""
    
    views = {}

    def get_view(self, route=None):
        if not route:
            route = "/"

        troute = ft.TemplateRoute(route)
        route_kwargs = {}
        for _route in self.app_view.keys():
            if troute.match(_route):
                route_kwargs = troute._TemplateRoute__last_params
                route = _route
                view = self.views[_route]
                view = view.create_view if type(view) == BaseView else view 
                break
        else:
            if not view:
                view = self.views['/404']
        
        return ft.View(
                route,
                view(self.page, **route_kwargs)
            )

    def on_route_change(self, event: ft.RouteChangeEvent):
        self.page.views.append(
            self.get_view(route = event.route)
        )
        self.pre_render()
        self.update_page()
        self.post_render()
 
    def on_view_pop(self, event : ft.ViewPopEvent):
        super().on_view_pop(event)        
        self.update_page()
        
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
    def previous_route(self):
        if len(self.page.views) > 1:
            return self.page.views[-2].route
        return None

    def refresh_page(self):
        if getattr(self, 'refreshing', False):
            return

        self.refreshing = True
        view = self.all_views.pop()
        self.navigate_to(view.route)
        self.refreshing = False

    def navigate_to(self, route : str):
        route_event = ft.RouteChangeEvent(route=route)
        self.on_route_change(route_event)

    @cached_property
    def app_view(self):
        return self.views

app = App()

