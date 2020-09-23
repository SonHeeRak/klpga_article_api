class ParentControllers:
    def __init__(self):
        self.success_result = {
            'result_code': 100,
            'result_msg': '성공'
        }
        self.failure_result = {
            'result_code': 300,
            'result_msg': '실패'
        }
        self.no_data_result = {
            'result_code': 200,
            'result_msg': '데이터 없음'
        }

    def success_result(self):
        return self.success_result

    def failure_result(self):
        return self.failure_result

    def no_data_result(self):
        return self.no_data_result
