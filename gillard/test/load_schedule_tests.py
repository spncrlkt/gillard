import json
import os

from io import BytesIO

import gillard
import test_utils
from utils import eprint

from models import Show


class LoadScheduleTestCase(test_utils.GillardBaseTestCase):

    def test_load_schedule_route_not_404(self):
        show_list = self.get_show_list_single()

        rv = self.app.post(
            '/loadSchedule',
            buffered=True,
            content_type='multipart/form-data',
            data={
                'schedule' : (BytesIO(bytes(json.dumps(show_list), 'utf8')), 'schedule.json')
            }
        )
        assert rv.status_code != 404

    def test_load_schedule_route_200(self):
        show_list = self.get_show_list_single()

        rv = self.app.post(
            '/loadSchedule',
            buffered=True,
            content_type='multipart/form-data',
            data={
                'schedule' : (BytesIO(bytes(json.dumps(show_list), 'utf8')), 'schedule.json')
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
        show_list = self.get_show_list_single()

        rv = self.app.post(
            '/loadSchedule',
            buffered=True,
            content_type='multipart/form-data',
            data={
                'schedule' : (BytesIO(bytes(json.dumps(show_list), 'utf8')), 'schedule.json')
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

    def test_schedule_upload_single_show(self):
        show_list = self.get_show_list_single()

        rv = self.app.post(
            '/loadSchedule',
            buffered=True,
            content_type='multipart/form-data',
            data={
                'schedule' : (BytesIO(bytes(json.dumps(show_list), 'utf8')), 'schedule.json')
            }
        )

        with gillard.app.app_context():
            show = gillard.db.session.query(Show).filter_by(id=1).one()
            assert show.display_id == show_list[0]['display_id']

    def test_schedule_upload_2_shows(self):
        show_list = self.get_show_list_double()

        rv = self.app.post(
            '/loadSchedule',
            buffered=True,
            content_type='multipart/form-data',
            data={
                'schedule' : (BytesIO(bytes(json.dumps(show_list), 'utf8')), 'schedule.json')
            }
        )

        with gillard.app.app_context():
            show = gillard.db.session.query(Show).filter_by(id=1).one()
            assert show.display_id == show_list[0]['display_id']
            show = gillard.db.session.query(Show).filter_by(id=2).one()
            assert show.display_id == show_list[1]['display_id']

    def test_schedule_upload_show_attrs(self):
        show_list = self.get_show_list_single()

        rv = self.app.post(
            '/loadSchedule',
            buffered=True,
            content_type='multipart/form-data',
            data={
                'schedule' : (BytesIO(bytes(json.dumps(show_list), 'utf8')), 'schedule.json')
            }
        )

        with gillard.app.app_context():
            show = gillard.db.session.query(Show).filter_by(id=1).one()
            assert show.display_id == show_list[0]['display_id']
            assert show.password == show_list[0]['password']
            assert show.title == show_list[0]['title']
            assert show.startDay == show_list[0]['startDay']
            assert show.startHour == show_list[0]['startHour']
            assert show.endDay == show_list[0]['endDay']
            assert show.endHour == show_list[0]['endHour']

    def test_schedule_upload_show_missing_attr(self):
        show_list = self.get_show_list_single()
        del show_list[0]['title']

        rv = self.app.post(
            '/loadSchedule',
            buffered=True,
            content_type='multipart/form-data',
            data={
                'schedule' : (BytesIO(bytes(json.dumps(show_list), 'utf8')), 'schedule.json')
            }
        )

        res_json = json.loads(rv.data.decode("utf-8"))
        assert res_json['message'] == "Missing `['title']` for schedule index 0"

    def test_schedule_upload_show_missing_attrs(self):
        show_list = self.get_show_list_single()
        del show_list[0]['title']
        del show_list[0]['startHour']

        rv = self.app.post(
            '/loadSchedule',
            buffered=True,
            content_type='multipart/form-data',
            data={
                'schedule' : (BytesIO(bytes(json.dumps(show_list), 'utf8')), 'schedule.json')
            }
        )

        res_json = json.loads(rv.data.decode("utf-8"))

        assert res_json['message'] == "Missing `['title', 'startHour']` for schedule index 0"

    def get_show_list_single(self):
        return [{
            'display_id': '[KFFP59247]',
            'password': 'TESTPASS',
            'title': 'Based Goth Radio',
            'startDay': 3,
            'startHour': 12,
            'endDay': 3,
            'endHour': 14
        }]

    def get_show_list_double(self):
        show_list = self.get_show_list_single()
        show_list.append({
            'display_id': '[KFFP59248]',
            'password': 'TESTPASSS',
            'title': 'Based Goth Radio 2',
            'startDay': '3',
            'startHour': '14',
            'endDay': '3',
            'endHour': '16'
        })
        return show_list

