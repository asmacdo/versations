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
   client = VersationsClient(
      config["homeserver"],
      config["user_id"],
      config["device_id"],
      config["store_path"],
      client_config,
      ssl=False
   )
   await client.authenticate(config)

   # Sync callback `write_versations` produces files
   response = await client.sync()

   await client.close()
   print(f"Sync complete! Exported {client._versations_saved} messages to disk")
if __name__ == "__main__":
   # TODO(asmacdo) whats the diff for run vs eventloop run until complete
   # asyncio.run(main())
   asyncio.get_event_loop().run_until_complete(main())
