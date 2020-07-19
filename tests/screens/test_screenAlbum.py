from unittest import TestCase
from testUtils.TesterApp import TesterApp
from kivy.tests.common import GraphicUnitTest, UnitTestTouch
from kivy.base import EventLoop
from window.PhotoManager import PhotoManager

def displayMsg(value):
    print("displayMsg", value)

class TestScreenAlbum(GraphicUnitTest):

    print(11)

    # def setUp(self):
    #     self.root = PhotoManager()
    #     self.root.parent = None
    #     self.root.canvas = None
    #     self.root.load_config()
    #     # self.root.build()
    #     # self.root.load_config()
    #
    #
    #     self.app = TesterApp()
    #     # app.text_scale = 10
    #     # app.padding = 10
    #
    #     EventLoop.ensure_window()
    #     self._win = EventLoop.window
    #     self.clean_garbage()
    #
    #
    #     super(TestScreenAlbum, self).setUp()

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
        from screens.screenAlbum import ScreenAlbum
        screen_album = ScreenAlbum()
        screen_album.refresh_photolist()
        self.fail()

    def test_sort_photos(self):
        self.fail()

