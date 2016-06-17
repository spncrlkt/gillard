import json

import gillard
import test_utils
from utils import eprint


class LoadScheduleTestCase(test_utils.GillardBaseTestCase):

    def test_load_schedule_route_not_404(self):
        rv = self.app.post('/loadSchedule')
        assert rv.status_code != 404

    def test_load_schedule_route_200(self):
        rv = self.app.post('/loadSchedule')
        assert rv.status_code == 200
