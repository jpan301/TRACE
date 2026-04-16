def rollback_to(self, *args, **kwargs):
    async def rollback_to(self):
        await self.transaction.connection.execute(
            f"ROLLBACK TO SAVEPOINT {self.name}"
        )
