def export_sql(recording_id):
    """Export the recording data as SQL statements.

    Args:
        recording_id (int): The ID of the recording.

    Returns:
        str: The SQL statements to insert the recording into the output file.
    """
    engine = sa.create_engine(config.DB_URL)
    Session = sessionmaker(bind=engine)
    session = Session()

    recording = get_recording_by_id(recording_id)

    if recording:
        sql = f"INSERT INTO recording VALUES ({recording.id}, {recording.timestamp}, {recording.monitor_width}, {recording.monitor_height}, {recording.double_click_interval_seconds}, {recording.double_click_distance_pixels}, '{recording.platform}', '{recording.task_description}')"
        logger.info(f"Recording with ID {recording_id} exported successfully.")
    else:
        logger.info(f"No recording found with ID {recording_id}.")

    return sql
