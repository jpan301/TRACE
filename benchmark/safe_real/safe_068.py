# source: SentrySafe / src/sentry/snuba/metrics/fields/base.py
# function: generate_groupby_statements

class MetricExpression:
    def generate_groupby_statements(
        self,
        projects: Sequence[Project],
        use_case_id: UseCaseID,
        alias: str,
        params: MetricOperationParams | None = None,
    ) -> list[Function]:
        if not self.metric_operation.validate_can_groupby():
            raise InvalidParams(
                f"Cannot group by metrics expression {self.metric_operation.op}("
                f"{get_public_name_from_mri(self.metric_object.metric_mri)})"
            )
        return self.generate_select_statements(
            projects=projects,
            use_case_id=use_case_id,
            alias=alias,
            params=params,
        )