def release(self, *args, **kwargs):
    async def release(self):
        await self.transaction.connection.execute(
            f"RELEASE SAVEPOINT {self.name}"
        )
