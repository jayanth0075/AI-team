import logging
from typing import Dict, Any, List
from sqlalchemy.orm import Session

from app.models.technology import TechnologyProfile
from app.services.llm_service import llm_service

logger = logging.getLogger(__name__)


DISCOVERY_PROMPT = """Based on the following technology and requirement match data, provide a match analysis.

Technology: {tech_name}
Match Score: {score:.1f}/100
TRL Level: {trl_level}
Patent Status: {patent_status}
Manufacturing Readiness: {manufacturing_readiness}

Requirement Domain: {domain}
Requirement Sub-domain: {sub_domain}
Required TRL: {required_trl}

Generate a brief 1-2 sentence match reason explaining why this technology fits the requirement.
Return JSON with field: "reason" (string)."""


class TechnologyDiscoveryAgent:
    async def search(
        self,
        db: Session,
        domain: str,
        sub_domain: str,
        keywords: List[str],
        required_trl: int,
    ) -> List[Dict[str, Any]]:
        try:
            technologies = db.query(TechnologyProfile).filter(
                TechnologyProfile.domain == domain,
                TechnologyProfile.sub_domain == sub_domain,
            ).all()

            results = []
            for tech in technologies:
                score = self._calculate_match_score(tech, required_trl, keywords)

                match_reason = ""
                if score > 0:
                    try:
                        prompt = DISCOVERY_PROMPT.format(
                            tech_name=tech.technology_name,
                            score=score,
                            trl_level=tech.trl_level,
                            patent_status=tech.patent_status,
                            manufacturing_readiness=tech.manufacturing_readiness,
                            domain=domain,
                            sub_domain=sub_domain,
                            required_trl=required_trl,
                        )
                        analysis = await llm_service.generate_json(prompt)
                        match_reason = analysis.get("reason", "")
                    except Exception:
                        pass

                results.append({
                    "id": tech.id,
                    "technology_name": tech.technology_name,
                    "match_score": round(score, 1),
                    "trl_level": tech.trl_level,
                    "patent_status": tech.patent_status,
                    "manufacturing_readiness": tech.manufacturing_readiness,
                    "match_reason": match_reason,
                })

            results.sort(key=lambda x: x["match_score"], reverse=True)
            return results
        except Exception as e:
            logger.error(f"Error searching technologies: {str(e)}")
            raise

    @staticmethod
    def _calculate_match_score(
        tech: TechnologyProfile,
        required_trl: int,
        keywords: List[str],
    ) -> float:
        score = 0.0
        if tech.trl_level >= required_trl:
            score += 25
        else:
            score += 25 * (tech.trl_level / required_trl)

        if tech.patent_status == "Granted":
            score += 25
        elif tech.patent_status == "Pending":
            score += 15

        if tech.manufacturing_readiness == "Ready":
            score += 20
        elif tech.manufacturing_readiness == "Scaling":
            score += 15

        if tech.license_available:
            score += 15

        if keywords and tech.keywords:
            keyword_matches = sum(
                1 for kw in keywords
                if kw.lower() in tech.keywords.lower()
            )
            score += 15 * (keyword_matches / len(keywords))

        return min(score, 100.0)
