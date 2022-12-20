import asyncio

from config import load_config_from_env
from client import VersationsClient

from nio import AsyncClient, LoginResponse, SyncResponse, AsyncClientConfig

async def main():

   config = load_config_from_env()

   client_config = AsyncClientConfig(
      max_limit_exceeded=0,
      max_timeouts=0,
      store_sync_tokens=True,
      encryption_enabled=True,
    )
   # TODO: if possible add filters for
   #  - the room
   #  - we care only about messages (not who left / joined etc)
   client = VersationsClient(
      config["homeserver"],
      config["user_id"],
      config["device_id"],
      config["store_path"],
      client_config,
      ssl=True,
   )
   await client.authenticate(config)

   # Sync callback `write_versations` produces files
   since = None
   missing_sessions = None
   # TODO: figure out how/when to stop
   # may be whenever timestamp is "recent enough" i.e. after
   # we entered the loop
   for i in range(1):  # do some and see what happens
       print(f"Syncing for since={since}")
       response = await client.sync(since=since)
       if missing_sessions is None:
           missing_sessions = client.get_missing_sessions(room_id=config["room_id"])
           print(f"Got {missing_sessions!r} missing sessions")
       since = response.next_batch
       if not since:
           break

   await client.close()
   print(f"Sync complete! Exported {client._events_written} events to disk")
if __name__ == "__main__":
   # TODO(asmacdo) whats the diff for run vs eventloop run until complete
   # asyncio.run(main())
   asyncio.get_event_loop().run_until_complete(main())
