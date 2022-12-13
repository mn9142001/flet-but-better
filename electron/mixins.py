from flet import View

class AppMixin:

    @property
    def all_views(self) -> list[View]:
        return self.page.views    

    @property
    def current_view(self):
        view = self.all_views[-1]
        return view

    @property
    def controls(self):
        return self.current_view.controls

    def add_controls(self, *controls):
        self.controls.extend(controls)
        self.page.update()

    @property
    def route(self):
        self.page.route
