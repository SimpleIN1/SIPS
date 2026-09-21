from asgiref.sync import sync_to_async
from django_auth_ldap.backend import LDAPBackend


class AsyncLDAPBackend(LDAPBackend):
  async def aauthenticate(self, request, **credentials):
    return await sync_to_async(self.authenticate)(request, **credentials)

  async def aget_user(self, user_id):
    return await sync_to_async(self.get_user)(user_id)
