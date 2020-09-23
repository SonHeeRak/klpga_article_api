from report.common_lib.db.db_record import DbRecord


class Hole(object):
    def __init__(self, tour_id):
        self.tour_id = tour_id
        self.hole_df = DbRecord().tour_course_hole_info(tour_id=self.tour_id)

    def get_hole_par_no(self):
        """
        파정보
        :return:
        """
        return self.hole_df[['hole_no', 'par']]
