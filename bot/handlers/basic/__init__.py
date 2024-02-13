from .download import router_download
from .mailing import router_mailing
from .start import router_start
from .statistic import router_statistic

routers_basic = (
    router_start,
    router_statistic,
    router_mailing,
    router_download,
)
