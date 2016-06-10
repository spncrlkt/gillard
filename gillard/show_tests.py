import gillard
import test_utils

from models import Show, Playlist

class ShowTestCase(test_utils.GillardBaseTestCase):

    def test_mk_new_show(self):
        with gillard.app.app_context():
            show = Show()

            show = test_utils.save_and_refresh(gillard.db.session, show)

            assert show.id is not None

    def test_show_attrs(self):
        with gillard.app.app_context():
            show = Show()
            show.startDay = 0
            show.startHour = 0
            show.endDay = 0
            show.endHour = 2

            show = test_utils.save_and_refresh(gillard.db.session, show)

            assert show.startDay == 0
            assert show.startHour == 0
            assert show.endDay == 0
            assert show.endHour == 2

    def test_new_show_has_no_playlists(self):
        with gillard.app.app_context():
            show = Show()

            show = test_utils.save_and_refresh(gillard.db.session, show)

            assert len(show.playlists) == 0

    def test_add_playlist_to_show(self):
        with gillard.app.app_context():
            playlist = Playlist()
            show = Show()

            show.playlists = [playlist]

            show = test_utils.save_and_refresh(gillard.db.session, show)

            assert len(show.playlists) == 1

            # cascading add
            assert show.playlists[0].id is not None
