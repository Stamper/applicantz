from ninja import NinjaAPI

from users.auth import AuthBearer

api = NinjaAPI(auth=AuthBearer)
api.add_router("/users/", "users.api.router",)
api.add_router("/applicants/", "applicants.api.router")
