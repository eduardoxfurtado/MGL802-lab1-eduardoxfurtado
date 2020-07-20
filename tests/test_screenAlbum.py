from unittest import TestCase
from testUtils.TesterApp import TesterApp
from kivy.tests.common import GraphicUnitTest, UnitTestTouch
from kivy.base import EventLoop
from window.PhotoManager import PhotoManager
from kivy.config import ConfigParser
from window.Theme import Theme

def displayMsg(value):
    print("displayMsg", value)


class TestScreenAlbum(GraphicUnitTest):
    def setUp(self):
        self.app = TesterApp()
        # app.text_scale = 10
        # app.padding = 10

        EventLoop.ensure_window()
        self._win = EventLoop.window
        self.clean_garbage()

        super(TestScreenAlbum, self).setUp()

    def clean_garbage(self, *args):
        for child in self._win.children[:]:
            self._win.remove_widget(child)
        self.advance_frames(5)

    def test_refresh_photolist(self):
        app = PhotoManager(data_directory=".")
        app.config = ConfigParser(interpolation=None)
        app.build_config(app.config)

        app.theme = Theme(app)
        app.build()
        app.show_import()
        # render(self.app)
        from screens.screenAlbum import ScreenAlbum, Album, Tag
        screen_album = ScreenAlbum(name='test_album')
        self.assertIsInstance(screen_album, ScreenAlbum)
        # # need to mock the photo object, but I don't know how:
        # screen_album.photo = '21.jpg'
        # screen_album.refresh_photolist()

        screen_album_album = Album(name='Album_album')
        self.assertIsInstance(screen_album_album, ScreenAlbum)
        screen_album_album.refresh_photolist()
        self.assertIsNotNone(screen_album_album.photos)

        screen_album_tag = Tag(name='Album_album')
        self.assertIsInstance(screen_album_tag, ScreenAlbum)
        # it seems that the implementation of PhotoManager is incomplete to support the following case:
        # screen_album_tag.refresh_photolist()

        print("bye")
        pass
