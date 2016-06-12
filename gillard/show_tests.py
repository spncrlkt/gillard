import gillard
import test_utils

from models import Show, Playlist

class ShowTestCase(test_utils.GillardBaseTestCase):

    def test_mk_new_show(self):
        with gillard.app.app_context():
            show = Show('TESTID')

            show = test_utils.save_and_refresh(gillard.db.session, show)

            assert show.id is not None

    def test_show_attrs(self):
        with gillard.app.app_context():
            show = Show('TESTID')
            show.startDay = 2
            show.startHour = 4
            show.endDay = 6
            show.endHour = 8

            show = test_utils.save_and_refresh(gillard.db.session, show)

            assert show.display_id == 'TESTID'
            assert show.startDay == 2
            assert show.startHour == 4
            assert show.endDay == 6
            assert show.endHour == 8

    def test_new_show_has_no_playlists(self):
        with gillard.app.app_context():
            show = Show('TESTID')

            show = test_utils.save_and_refresh(gillard.db.session, show)

            assert len(show.playlists) == 0

    def test_add_playlist_to_show(self):
        with gillard.app.app_context():
            playlist = Playlist()
            show = Show('TESTID')

            show.playlists = [playlist]

            show = test_utils.save_and_refresh(gillard.db.session, show)

            assert len(show.playlists) == 1

            # cascading add
            assert show.playlists[0].id is not None
