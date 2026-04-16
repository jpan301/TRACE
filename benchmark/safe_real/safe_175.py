# source: PyPikaSafe / pypika/terms.py
# function: get_sql

class Interval:
    def get_sql(self, **kwargs: Any) -> str:
        dialect = self.dialect or kwargs.get("dialect")

        if self.largest == "MICROSECOND":
            expr = getattr(self, "microseconds")
            unit = "MICROSECOND"

        elif hasattr(self, "quarters"):
            expr = getattr(self, "quarters")
            unit = "QUARTER"

        elif hasattr(self, "weeks"):
            expr = getattr(self, "weeks")
            unit = "WEEK"

        else:
            # Create the whole expression but trim out the unnecessary fields
            expr = "{years}-{months}-{days} {hours}:{minutes}:{seconds}.{microseconds}".format(
                years=getattr(self, "years", 0),
                months=getattr(self, "months", 0),
                days=getattr(self, "days", 0),
                hours=getattr(self, "hours", 0),
                minutes=getattr(self, "minutes", 0),
                seconds=getattr(self, "seconds", 0),
                microseconds=getattr(self, "microseconds", 0),
            )
            expr = self.trim_pattern.sub("", expr)
            if self.is_negative:
                expr = "-" + expr

            unit = (
                "{largest}_{smallest}".format(
                    largest=self.largest,
                    smallest=self.smallest,
                )
                if self.largest != self.smallest
                else self.largest
            )

            # Set default unit with DAY
            if unit is None:
                unit = "DAY"

        return self.templates.get(dialect, "INTERVAL '{expr} {unit}'").format(expr=expr, unit=unit)