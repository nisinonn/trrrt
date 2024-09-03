import rebootpy
import json
import os
import asyncio
import random

filename = 'device_auths.json'

class MyClient(rebootpy.Client):
    def __init__(self, device_auth_details):
        super().__init__(
            auth=rebootpy.DeviceAuth(
                device_id=device_auth_details['device_id'],
                account_id=device_auth_details['account_id'],
                secret=device_auth_details['secret']
            )
        )

    async def event_ready(self):
        print(f'クライアントが準備完了: {self.user.display_name}')
        await self.party.set_privacy(rebootpy.PartyPrivacy.PRIVATE)
        self.set_status('ランクバトルロイヤル - ソロ - 残り100人')
        asyncio.create_task(self.decrease_status_count())

    async def event_friend_request(self, request):
        await request.accept()
        print(f'フレンドリクエストを承認しました: {request.display_name}')

    async def event_friend_add(self, friend):
        print(f'フレンド追加: {friend.display_name}')

    async def event_friend_remove(self, friend):
        print(f'フレンド削除: {friend.display_name}')

    async def event_party_message(self, message):
        print(f'パーティーメッセージ: {message.author.display_name}: {message.content}')

    async def event_whisper(self, whisper):
        print(f'ささやき: {whisper.author.display_name}: {whisper.content}')

    async def decrease_status_count(self):
        while True:
            count = 100
            while count > 1:
                await asyncio.sleep(random.randint(1, 20))  # 1秒から30秒の間隔で実行
                count -= random.randint(1, 7)  # ランダムに数字を減らす（1から5）
                self.set_status(f'ランクバトルロイヤル - ソロ - 残り{count}人')
            await asyncio.sleep(5)  # 1人になった後30秒待機
            self.set_status('ランクバトルロイヤル - ソロ - 残り100人')

    def set_status(self, status):
        self.set_presence(status)

async def run_client(account):
    client = MyClient(account)
    await client.start()

async def main():
    if os.path.isfile(filename):
        with open(filename, 'r') as fp:
            data = json.load(fp)
            tasks = []
            for key, account in data.items():
                tasks.append(run_client(account))
            await asyncio.gather(*tasks)

asyncio.run(main())
