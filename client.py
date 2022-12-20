import os

from datetime import datetime

# TODO(asmacdo) blackify
from nio import AsyncClient, LoginResponse, SyncResponse, MatrixRoom, RoomMessageText, Event

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
      # self.add_event_callback(self.write_simple_messages, RoomMessageText)
      # self._messages_written = 0

      # Write all events
      self.add_event_callback(self.write_all_events, Event)
      self._events_written = 0

   async def authenticate(self, config):
      resp = await self.login(config["password"], device_name=config.get("sync-bot"))
      if isinstance(resp, LoginResponse):
         print("password login success")
      else:
         # TODO(asmacdo) better exception
         raise Exception("pass login failed")

   # TODO(asmacdo) not used
   async def write_simple_messages(self, room: MatrixRoom, event: RoomMessageText):
      """Callback to write a received message to disk.

      Arguments:
          room {MatrixRoom} -- Provided by nio
          event {RoomMessageText} -- Provided by nio
      """
      self._messages_written += 1
      event_dt = datetime.fromtimestamp(event.server_timestamp/ 1000)
      with open(os.path.join(self.store_path, event_dt.date().isoformat()), "a") as log:
         log.write(f"{event_dt.strftime('%H:%M:%S')} | {event.sender}: {event.body}\n")

   # TODO(asmacdo) not used
   async def write_all_events(self, room: MatrixRoom, event: Event):
      """Callback to write a received message to disk.

      Arguments:
          room {MatrixRoom} -- Provided by nio
          event {RoomMessageText} -- Provided by nio
      """
      self._events_written += 1
      event_dt = datetime.fromtimestamp(event.server_timestamp/ 1000)
      with open(os.path.join(self.store_path, event_dt.date().isoformat()), "a") as log:
         log.write("---------------------\n")
         try:
            log.write(f"{event_dt.strftime('%H:%M:%S')} | {event.sender}: {event.body}\n")
         except Exception as e:
            log.write(f"EXCEPTION {e}")
