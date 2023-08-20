import os.path

import kivy

kivy.require('1.0.5')

from kivy.uix.floatlayout import FloatLayout
from kivy.app import App
from kivy.properties import ObjectProperty, StringProperty
from kivy.core.audio import SoundLoader
from kivy.network.urlrequest import UrlRequest

from kivy.utils import platform

if platform == "android":
    from android.permissions import request_permissions, Permission

    request_permissions([Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE])

SERVER_HOST_NAME = 'localhost'
SERVER_PORT = 8080

BASE_URL = f'http://{SERVER_HOST_NAME}:{SERVER_PORT}/'


class PlayerManager:
    sound = None

    def play_music(self, file_id: int, file_path=None):
        self.stop_music()
        if not file_path:
            file_path = f'cache/file{file_id}.mp3'

        self.sound = SoundLoader.load(file_path)
        if self.sound:
            print("Sound found at %s" % self.sound.source)
            print("Sound is %.3f seconds" % self.sound.length)
            self.sound.play()

    def stop_music(self):
        if self.sound:
            self.sound.stop()
            self.sound.unload()


player_manager = PlayerManager()


class Controller(FloatLayout):

    @classmethod
    def success(req, result):
        player_manager.play_music(0, file_path=result.file_path)

    def do_play(self, file_id: str):
        if not file_id:
            file_id = '1'
        file_id = int(file_id)
        if not os.path.exists(f'cache/file{file_id}.mp3'):
            req = UrlRequest(
                url=f'{BASE_URL}play/track/{file_id}',
                file_path=f'cache/file{file_id}.mp3',
                on_finish=self.success
            )
        else:
            player_manager.play_music(file_id)

    def do_stop(self):
        player_manager.stop_music()


class ControllerApp(App):

    def build(self):
        return Controller()


if __name__ == '__main__':
    ControllerApp().run()
