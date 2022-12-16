import os

from datetime import datetime

# TODO(asmacdo) blackify
from nio import AsyncClient, LoginResponse, SyncResponse, MatrixRoom, RoomMessageText

class VersationsClient(AsyncClient):
   def __init__(self, homeserver, user="", device_id="", store_path="",
                config=None, ssl=None, proxy=None):
      super().__init__(homeserver, user=user, device_id=device_id,
                       store_path=store_path, config=config, ssl=ssl,
                       proxy=proxy)

      # if the store location doesn't exist, we'll make it
      if store_path and not os.path.isdir(store_path):
         os.mkdir(store_path)

      # TODO(asmacdo)auto-join room invites?
      # self.add_event_callback(self.cb_autojoin_room, InviteEvent)

      # Write each message to appropriate date-file
      self.add_event_callback(self.write_versation, RoomMessageText)
      self._versations_saved = 0


   async def authenticate(self, config):
      resp = await self.login(config["password"], device_name=config.get("sync-bot"))
      if isinstance(resp, LoginResponse):
         print("password login success")
      else:
         # TODO(asmacdo) better exception
         raise Exception("pass login failed")

   async def write_versation(self, room: MatrixRoom, event: RoomMessageText):
      """Callback to write a received message to disk.

      Arguments:
          room {MatrixRoom} -- Provided by nio
          event {RoomMessageText} -- Provided by nio
      """
      self._versations_saved += 1

      # TODO(asmacdo) encrpytion
      # if event.decrypted:
      #    encrypted_symbol = "🛡 "
      # else:
      #    encrypted_symbol = "⚠️ "

      event_dt = datetime.fromtimestamp(event.server_timestamp/ 1000)
      with open(os.path.join(self.store_path, event_dt.date().isoformat()), "a") as log:
         log.write(f"{event_dt.strftime('%H:%M:%S')} | {event.sender}: {event.body}\n")
