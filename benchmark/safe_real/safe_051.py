# source: SentrySafe / src/sentry/runner/commands/presenters/consolepresenter.py
# function: flush

class ConsolePresenter:
    def flush(self) -> None:
        import logging

        logger = logging.getLogger("sentry.options_automator")

        for key, db_value in self.drifted_options:
            click.echo(self.DRIFT_MSG % key)
            logger.error(self.DRIFT_MSG % key)
            if db_value != "":
                click.echo(self.DB_VALUE % key)
                # This is yaml instead of the python representation as the
                # expected flow, in this case, is to use the output of this
                # line to copy paste it in the config map.
                click.echo(safe_dump(db_value))

        for key in self.channel_updated_options:
            click.echo(self.CHANNEL_UPDATE_MSG % key)

        for key, db_value, value in self.updated_options:
            click.echo(self.UPDATE_MSG % (key, db_value, value))

        for key, value in self.set_options:
            click.echo(self.SET_MSG % (key, value))

        for key in self.unset_options:
            click.echo(self.UNSET_MSG % key)

        for key, reason in self.not_writable_options:
            click.echo(self.ERROR_MSG % (key, reason))

        for key in self.unregistered_options:
            click.echo(self.UNREGISTERED_OPTION_ERROR % key)
            logger.error(self.UNREGISTERED_OPTION_ERROR, key)

        for key, got_type, expected_type in self.invalid_type_options:
            click.echo(self.INVALID_TYPE_ERROR % (key, got_type, expected_type))
            logger.error(self.INVALID_TYPE_ERROR, key, got_type, expected_type)