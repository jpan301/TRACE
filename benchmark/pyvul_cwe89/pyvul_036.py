def savepoint(self, *args, **kwargs):
    async def savepoint(self, name: t.Optional[str] = None) -> Savepoint:
        name = name or f"savepoint_{self.get_savepoint_id()}"
        await self.connection.execute(f"SAVEPOINT {name}")
        return Savepoint(name=name, transaction=self)
