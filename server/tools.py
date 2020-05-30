

class HttpHelper():
    def BuildBadRequest(message):
        """(dict, status) Returns a default error dict with a specified message."""
        return {'success': False, 'message': message}, 400


    def BuildGoodRequest(data):
        """(dict, status) Returns a default success dict with a specified data."""
        return {'success': True, 'data': data}, 200
        
