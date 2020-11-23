from http import HTTPStatus
def user_not_found():
    return {"message":"user not found"}, HTTPStatus.BAD_REQUEST
def item_not_found():
    return {"message":"item not found"}, HTTPStatus.BAD_REQUEST
