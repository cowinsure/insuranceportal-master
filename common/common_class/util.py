'''
 # @ Author: Tanmay Anthony Gomes
 # @ Create Time: 2025-06-12 15:13:41
 # @ Modified by: Tanmay Anthony Gomes
 # @ Modified time: 2025-06-12 17:49:03
 # @ Description: response function for returning result. will be called from DAL classes
 '''
def _response(status, message, data=None):
    return {
        "status": status,
        "message": message,
        "data": data or []
    }

'''
 # @ Author: Tanmay Anthony Gomes
 # @ Create Time: 2025-06-12 15:13:41
 # @ Modified by: Tanmay Anthony Gomes
 # @ Modified time: 2025-06-12 17:49:03
 # @ Description: function for getting user id from the request and injecting that into by_user_id property
 '''
def build_request_with_user(model_class, request, method='GET'):
    data = request.query_params.dict() if method == 'GET' else request.data
    print(data)
    payload = {**data, "by_user_id": request.user.id}
    return model_class(**payload)
