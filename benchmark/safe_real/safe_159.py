# source: PyPikaSafe / pypika/terms.py
# function: get_frame_sql

class WindowFrameAnalyticFunction:
    def get_frame_sql(self) -> str:
        if not isinstance(self.bound, tuple):
            return "{frame} {bound}".format(frame=self.frame, bound=self.bound)

        lower, upper = self.bound
        return "{frame} BETWEEN {lower} AND {upper}".format(
            frame=self.frame,
            lower=lower,
            upper=upper,
        )