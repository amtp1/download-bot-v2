from .start import router_start
from .download import router_download
from .statistic import router_statistic
from .mailing import router_mailing

routers_basic = (router_start, router_statistic, router_mailing, router_download,)
