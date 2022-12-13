import flet as ft
from dataclasses import dataclass, field, fields
from .mixins import AppMixin


@dataclass
class ViewConfig:
    scroll : ft.ScrollMode =ft.ScrollMode.ADAPTIVE


@dataclass
class PageConfig:
    title : str = field(default="Not set yet")
    theme_mode : ft.ThemeMode = field(default=ft.ThemeMode.DARK)
    horizontal_alignment : ft.CrossAxisAlignment = field(default=ft.CrossAxisAlignment.CENTER)
    vertical_alignment : ft.MainAxisAlignment = field(default=ft.MainAxisAlignment.CENTER)

class BaseView(type):
    """it only exists so type(View) returns BaseView instead of type"""

class View(AppMixin, metaclass=BaseView):
    """Base class to be inherited from for all class based views"""

    view_config = ViewConfig
    page_config = PageConfig
    controls = []

    def __init__(self, page : ft.Page, *args, **kwargs) -> None:
        self.page = page
        self.load_page_config()

    def load_page_config(self):
        for field in fields(self.page_config):
            setattr(self.page, field.name, getattr(self.page_config, field.name))

    @classmethod
    def create_view(cls, page : ft.Page, *args, **kwargs) :
        view : View = cls(page, *args, **kwargs)
        view.controls = view.render(page, *args, **kwargs)
        return view

    def render(self, page, **kwargs):
        "to render your page"
        raise NotImplementedError("render method must be implemented")

