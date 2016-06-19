import json
import os

from io import BytesIO

import gillard
import test_utils
from utils import eprint


class LoadScheduleTestCase(test_utils.GillardBaseTestCase):

    def test_load_schedule_route_not_404(self):
        rv = self.app.post('/loadSchedule')
        assert rv.status_code != 404

    def test_load_schedule_route_200(self):
        rv = self.app.post(
            '/loadSchedule',
            buffered=True,
            content_type='multipart/form-data',
            data={
                'schedule' : (BytesIO(b'"{hello: world}"'), 'schedule.json')
            }
        )
        assert rv.status_code == 200

    def test_sched_upload_dir_exists(self):
        assert os.path.isdir(gillard.UPLOAD_FOLDER)

    def test_schedule_upload_no_file(self):
        rv = self.app.post(
            '/loadSchedule',
            buffered=True,
            content_type='multipart/form-data',
            data={}
        )

        res_json = json.loads(rv.data.decode("utf-8"))
        assert res_json['message'] == 'Schedule file not provided'

    def test_schedule_upload(self):
        rv = self.app.post(
            '/loadSchedule',
            buffered=True,
            content_type='multipart/form-data',
            data={
                'schedule' : (BytesIO(b'"{hello: world}"'), 'schedule.json')
            }
        )

        assert os.path.isfile("{}/schedule.json".format(gillard.UPLOAD_FOLDER))

    def test_schedule_upload_invalid_json(self):
        rv = self.app.post(
            '/loadSchedule',
            buffered=True,
            content_type='multipart/form-data',
            data={
                'schedule' : (BytesIO(b'invalid_json{}'), 'schedule.json')
            }
        )

        res_json = json.loads(rv.data.decode("utf-8"))
        assert res_json['message'] == 'Invalid JSON: Expecting value: line 1 column 1 (char 0)'

    def test_schedule_upload_single_song(self):
        show_list = [{
            'showID': '[KFFP59247]',
            'title': 'Based Goth Radio',
            'startDay': '3',
            'startHour': '12',
            'endDay': '3',
            'endHour': '14'
        }]
        rv = self.app.post(
            '/loadSchedule',
            buffered=True,
            content_type='multipart/form-data',
            data={
                'schedule' : (BytesIO(bytes(json.dumps(show_list), 'utf8')), 'schedule.json')
            }
        )

        assert rv.status_code == 200



