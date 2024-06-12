import allure
import os


def attach_bstack_video(session_id):
    import requests
    bstack_session = requests.get(
        f'{os.getenv("BS_API_SESSIONS")}/{session_id}.json',
        auth=(os.getenv("BS_LOGIN"), os.getenv("BS_PASS")),
    ).json()
    print(bstack_session)
    video_url = bstack_session['automation_session']['video_url']

    allure.attach(
        '<html><body>'
        '<video width="100%" height="100%" controls autoplay>'
        f'<source src="{video_url}" type="video/mp4">'
        '</video>'
        '</body></html>',
        name='video recording',
        attachment_type=allure.attachment_type.HTML,
    )


def attach_screenshot_and_dump(browser):
    allure.attach(
        browser.driver.get_screenshot_as_png(),
        name='screenshot',
        attachment_type=allure.attachment_type.PNG,
    )

    allure.attach(
        browser.driver.page_source,
        name='screen xml dump',
        attachment_type=allure.attachment_type.XML,
    )
