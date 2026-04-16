# source: SentrySafe / src/sentry/backup/services/import_export/impl.py
# function: get_existing_import_chunk

def get_existing_import_chunk(
    model_name: NormalizedModelName,
    flags: ImportFlags,
    import_chunk_type: type[models.base.Model],
    min_ordinal: int,
) -> RpcImportOk | None:
    found_chunk = import_chunk_type.objects.filter(
        import_uuid=flags.import_uuid, model=model_name, min_ordinal=min_ordinal
    ).first()
    if found_chunk is None:
        return None

    found_data = model_to_dict(found_chunk)
    out_pk_map = PrimaryKeyMap()
    for old_pk, new_pk in found_data["inserted_map"].items():
        identifier = found_data["inserted_identifiers"].get(old_pk, None)
        out_pk_map.insert(model_name, int(old_pk), int(new_pk), ImportKind.Inserted, identifier)
    for old_pk, new_pk in found_data["existing_map"].items():
        out_pk_map.insert(model_name, int(old_pk), int(new_pk), ImportKind.Existing)
    for old_pk, new_pk in found_data["overwrite_map"].items():
        out_pk_map.insert(model_name, int(old_pk), int(new_pk), ImportKind.Overwrite)

    return RpcImportOk(
        mapped_pks=RpcPrimaryKeyMap.into_rpc(out_pk_map),
        min_ordinal=found_data["min_ordinal"],
        max_ordinal=found_data["max_ordinal"],
        min_source_pk=found_data["min_source_pk"],
        max_source_pk=found_data["max_source_pk"],
        min_inserted_pk=found_data["min_inserted_pk"],
        max_inserted_pk=found_data["max_inserted_pk"],
    )