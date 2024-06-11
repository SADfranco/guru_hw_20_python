import os
from appium.options.android import UiAutomator2Options
import utils
from pydantic import BaseModel


class Config(BaseModel):
    context: str
    bs_login: str = os.getenv('BS_LOGIN')
    bs_password: str = os.getenv('BS_PASS')
    remote_url: str = os.getenv('REMOTE_URL')
    device_name: str = os.getenv('DEVICE_NAME')
    app_bstack: str = os.getenv('APP')
    platformName: str = os.getenv('PLATFORM_NAME')
    platformVersion: str = os.getenv('PLATFORM_VERSION')
    appWaitActivity: str = os.getenv('APP_WAIT_ACTIVITY')
    app_local: str = utils.file.abs_path_from_project(os.getenv('APP'))
    udid: str = os.getenv('UDID')

    def to_driver_options(self, context):
        options = UiAutomator2Options()

        if context == 'local_emulator':
            options.set_capability('remote_url', self.remote_url)
            options.set_capability('udid', self.udid)
            options.set_capability('appWaitActivity', self.appWaitActivity)
            options.set_capability('app', self.app_local)

        if context == 'bstack':
            options.set_capability('remote_url', self.remote_url)
            options.set_capability('deviceName', self.device_name)
            options.set_capability('platformName', self.platformName)
            options.set_capability('platformVersion', self.platformVersion)
            options.set_capability('appWaitActivity', self.appWaitActivity)
            options.set_capability('app', self.app_bstack)
            options.set_capability(
                'bstack:options', {
                    'projectName': 'BS_Test',
                    'buildName': 'BS_Test',
                    'sessionName': 'BS_Test',
                    'userName': self.bs_login,
                    'accessKey': self.bs_password,
                },
            )

        return options


config = Config(context="local_emulator")
