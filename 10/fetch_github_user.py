import asyncio
from aiohttp import ClientSession, TCPConnector, ClientError

# username = input("Input github username, please >> ")
async def get_github_user(username: str) -> dict | None:
    async with ClientSession(connector=TCPConnector(ssl=False)) as session:
        try:
            async with session.get(f"https://api.github.com/users/{username}") as response:
                if response.status == 200:
                    return await response.json()
                else:
                    print(f"Error with getting response: {response.status}")
                    return None
        except ClientError as err:
                    print(f"An error occurred: {err}")

# result = asyncio.run(get_github_user())
# if result:
#     for key, value in result.items():
#         print(f"{key} >> {value}")