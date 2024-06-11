import allure
import pytest
from selene import browser
from appium import webdriver
from utils import attach
from dotenv import load_dotenv


def pytest_addoption(parser):
    parser.addoption(
        "--context",
        default="bstack",
        help="Specify the test context"
    )


def pytest_configure(config):
    context = config.getoption('--context')
    env_file = f'.env.{context}'
    load_dotenv(dotenv_path=env_file)


@pytest.fixture
def context(request):
    return request.config.getoption('--context')


@pytest.fixture(scope='function', autouse=True)
def android_mobile_management(context):
    from config import config
    options = config.to_driver_options(context=context)

    with allure.step('setup app session'):
        browser.config.driver = webdriver.Remote(
            options.get_capability('remote_url'),
            options=options
        )

    browser.config.timeout = 10.0

    yield

    attach.attach_screenshot_and_dump(browser)

    session_id = browser.driver.session_id

    with allure.step('tear down app session with id' + session_id):
        browser.quit()

    if context == 'bstack':
        attach.attach_bstack_video(session_id)
