import re
from urllib.parse import urljoin

from ..schema.discuz import Discuz
from ..schema.site_base import Work, NetworkState, SignState


class MainClass(Discuz):
    URL = 'https://www.skyey2.com/'
    USER_CLASSES = {
        'points': [1000000]
    }

    @classmethod
    def build_workflow(cls):
        return [
            Work(
                url='/login.php',
                method='get',
                check_state=('network', NetworkState.SUCCEED),
            ),
            Work(
                url='/login.php',
                method='login',
                succeed_regex='欢迎您回来，.*?(?=，)',
                check_state=('final', SignState.SUCCEED),
                is_base_content=True,

                login_url_regex='(?<=action=").*?(?=")',
                formhash_regex='(?<="formhash" value=").*(?=")'

            )
        ]

    def sign_in_by_login(self, entry, config, work, last_content):
        login = entry['site_config'].get('login')
        if not login:
            entry.fail_with_prefix('Login data not found!')
            return

        login_url = urljoin(entry['url'], re.search(work.login_url_regex, last_content).group())
        work.response_urls = [login_url]
        formhash = re.search(work.formhash_regex, last_content).group()
        data = {
            'formhash': formhash,
            'referer': '/',
            'loginfield': 'username',
            'username': login['username'],
            'password': login['password'],
            'loginsubmit': 'true'
        }
        return self._request(entry, 'post', login_url, data=data, verify=False)
