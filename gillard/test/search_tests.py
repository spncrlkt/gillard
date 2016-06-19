import json
import os
import random

from io import BytesIO

import gillard
import test_utils
from utils import eprint


class SearchTestCase(test_utils.GillardBaseTestCase):

    def test_load_search_route_not_404(self):
        search_term = self.get_search_term()

        rv = self.app.post(
            '/search',
            buffered=True,
            data=json.dumps(dict(search_term=search_term)),
            content_type='application/json',
        )
        assert rv.status_code != 404

    def test_load_search_route_200(self):
        search_term = self.get_search_term()

        rv = self.app.post(
            '/search',
            buffered=True,
            data=json.dumps(dict(search_term=search_term)),
            content_type='application/json',
        )
        assert rv.status_code == 200

    def test_search_produces_results(self):
        search_term = self.get_search_term()

        rv = self.app.post(
            '/search',
            buffered=True,
            data=json.dumps(dict(search_term=search_term)),
            content_type='application/json',
        )

        res = json.loads(rv.data.decode("utf-8"))

        eprint(res['tracks'])

        assert len(res['tracks']) > 0

    def get_search_term(self):
        search_terms = [
                'new order temptation',
                'temptation',
                'echo & the bunnymen ocean rain',
                'gold star for robot boy',
                'guided by voices gold star',
                'rapture out of the races',
        ]
        return search_terms[random.randint(0,len(search_terms)-1)]

