# source: SentrySafe / src/sentry/preprod/size_analysis/grouptype.py
# function: _matches_query

class PreprodSizeAnalysisDetectorHandler:
    def _matches_query(self, data_packet: SizeAnalysisDataPacket) -> bool:
        query = self.detector.config.get("query", "")
        if not query or not query.strip():
            return True

        metadata = data_packet.packet.get("metadata")
        if not metadata:
            raise ValueError(
                f"Data packet is missing metadata required to evaluate query filter: {query}"
            )

        artifact = metadata["head_artifact"]
        organization = self.detector.project.organization

        try:
            return artifact_matches_query(artifact, query, organization)
        except InvalidSearchQuery:
            logger.exception(
                "preprod.size_analysis.invalid_detector_query",
                extra={"detector_id": self.detector.id, "query": query},
            )
            return False