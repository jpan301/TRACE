# source: RedashSafe / redash/query_runner/azure_kusto.py
# function: run_query

class AzureKusto:
    def run_query(self, query, user):
        cluster = self.configuration["cluster"]
        msi = self.configuration.get("msi", False)
        # Managed Service Identity(MSI)
        if msi:
            # If user-assigned managed identity is used, the client ID must be provided
            if self.configuration.get("user_msi"):
                kcsb = KustoConnectionStringBuilder.with_aad_managed_service_identity_authentication(
                    cluster,
                    client_id=self.configuration["user_msi"],
                )
            else:
                kcsb = KustoConnectionStringBuilder.with_aad_managed_service_identity_authentication(cluster)
        # Service Principal auth
        else:
            aad_app_id = self.configuration.get("azure_ad_client_id")
            app_key = self.configuration.get("azure_ad_client_secret")
            authority_id = self.configuration.get("azure_ad_tenant_id")

            if not (aad_app_id and app_key and authority_id):
                raise ValueError(
                    "Azure AD Client ID, Client Secret, and Tenant ID are required for Service Principal authentication."
                )

            kcsb = KustoConnectionStringBuilder.with_aad_application_key_authentication(
                connection_string=cluster,
                aad_app_id=aad_app_id,
                app_key=app_key,
                authority_id=authority_id,
            )

        client = KustoClient(kcsb)

        request_properties = ClientRequestProperties()
        request_properties.application = "redash"

        if user:
            request_properties.user = user.email
            request_properties.set_option("request_description", user.email)

        db = self.configuration["database"]
        try:
            response = client.execute(db, query, request_properties)

            result_cols = response.primary_results[0].columns
            result_rows = response.primary_results[0].rows

            columns = []
            rows = []
            for c in result_cols:
                columns.append(
                    {
                        "name": c.column_name,
                        "friendly_name": c.column_name,
                        "type": TYPES_MAP.get(c.column_type, None),
                    }
                )

            # rows must be [{'column1': value, 'column2': value}]
            for row in result_rows:
                rows.append(row.to_dict())

            error = None
            data = {
                "columns": columns,
                "rows": rows,
                "metadata": {"data_scanned": _get_data_scanned(response)},
            }

        except KustoServiceError as err:
            data = None
            error = str(err)

        return data, error