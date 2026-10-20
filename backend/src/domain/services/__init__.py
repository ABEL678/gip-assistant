"""Доменные сервисы."""

from backend.src.domain.services.change_service import ChangeService
from backend.src.domain.services.document_link_service import DocumentLinkService
from backend.src.domain.services.document_service import DocumentService
from backend.src.domain.services.document_type_service import DocumentTypeService
from backend.src.domain.services.document_version_service import DocumentVersionService
from backend.src.domain.services.entity_service import EntityService
from backend.src.domain.services.entity_type_service import EntityTypeService
from backend.src.domain.services.goal_proposal_service import GoalProposalService
from backend.src.domain.services.goal_service import GoalService
from backend.src.domain.services.import_service import ImportService
from backend.src.domain.services.matrix_service import MatrixService
from backend.src.domain.services.premise_service import PremiseService
from backend.src.domain.services.project_standard_service import ProjectStandardService
from backend.src.domain.services.proposal_protocol_service import ProposalProtocolService
from backend.src.domain.services.result_service import ResultService
from backend.src.domain.services.revision_decision_service import RevisionDecisionService
from backend.src.domain.services.revision_service import RevisionService
from backend.src.domain.services.rule_based_goal_validator import RuleBasedGoalValidator
from backend.src.domain.services.similarity_matrix_service import SimilarityMatrixService
from backend.src.domain.services.stop_flag_service import StopFlagService

__all__ = [
    "ChangeService",
    "DocumentLinkService",
    "DocumentService",
    "DocumentTypeService",
    "DocumentVersionService",
    "EntityService",
    "EntityTypeService",
    "GoalProposalService",
    "GoalService",
    "ImportService",
    "MatrixService",
    "PremiseService",
    "ProjectStandardService",
    "ProposalProtocolService",
    "RevisionDecisionService",
    "RevisionService",
    "ResultService",
    "RuleBasedGoalValidator",
    "SimilarityMatrixService",
    "StopFlagService",
]
