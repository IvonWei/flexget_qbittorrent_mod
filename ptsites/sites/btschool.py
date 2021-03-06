from ..schema.nexusphp import NexusPHP
from ..schema.site_base import SignState, Work


class MainClass(NexusPHP):
    URL = 'https://pt.btschool.club/'
    USER_CLASSES = {
        'downloaded': [1099511627776, 10995116277760],
        'share_ratio': [3.05, 4.55],
        'days': [280, 700]
    }

    @classmethod
    def build_workflow(cls):
        return [
            Work(
                url='/index.php?action=addbonus',
                method='get',
                succeed_regex='欢迎回来',
                fail_regex=None,
                check_state=('final', SignState.SUCCEED),
                is_base_content=True
            )
        ]
