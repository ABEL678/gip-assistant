"""FastAPI dependencies (DI через Depends).

Здесь мы связываем:
- SQLAlchemy-сессию (adapter/db)
- Репозитории (adapter/db/repositories)
- Доменные сервисы (domain/services)

И передаём их в роуты через `Depends`.
"""

from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.adapters.db.repositories import (
    SqlAlchemyActionRepository,
    SqlAlchemyChangeRepository,
    SqlAlchemyCrossTaskRepository,
    SqlAlchemyDecisionLinkRepository,
    SqlAlchemyDecisionNormRepository,
    SqlAlchemyDecisionRepository,
    SqlAlchemyDocumentLinkRepository,
    SqlAlchemyDocumentRepository,
    SqlAlchemyDocumentTypeRepository,
    SqlAlchemyDocumentVersionRepository,
    SqlAlchemyEntityRepository,
    SqlAlchemyEntityTypeRepository,
    SqlAlchemyGoalRepository,
    SqlAlchemyImportLogRepository,
    SqlAlchemyNormRepository,
    SqlAlchemyPremiseRepository,
    SqlAlchemyProjectRepository,
    SqlAlchemyProjectStandardRepository,
    SqlAlchemyResultRepository,
    SqlAlchemyRevisionDecisionRepository,
    SqlAlchemyRevisionRepository,
    SqlAlchemyRfiRepository,
    SqlAlchemyStopFlagRepository,
    SqlAlchemyTaskRepository,
)
from backend.src.adapters.db.session import AsyncSessionLocal
from backend.src.domain.ports.goal_validator import GoalValidatorService
from backend.src.domain.ports.repositories import (
    ActionRepository,
    ChangeRepository,
    CrossTaskRepository,
    DecisionLinkRepository,
    DecisionNormRepository,
    DecisionRepository,
    DocumentLinkRepository,
    DocumentRepository,
    DocumentTypeRepository,
    DocumentVersionRepository,
    EntityRepository,
    EntityTypeRepository,
    GoalRepository,
    ImportLogRepository,
    NormRepository,
    PremiseRepository,
    ProjectRepository,
    ProjectStandardRepository,
    ResultRepository,
    RevisionDecisionRepository,
    RevisionRepository,
    RfiRepository,
    StopFlagRepository,
    TaskRepository,
)
from backend.src.domain.services import (
    ActionService,
    ChangeService,
    DecisionLinkService,
    DecisionNormService,
    DecisionProposalService,
    DecisionService,
    DocumentLinkService,
    DocumentService,
    DocumentTypeService,
    DocumentVersionService,
    EntityService,
    EntityTypeService,
    GoalProposalService,
    GoalService,
    ImportService,
    MatrixService,
    NormService,
    PremiseService,
    ProjectStandardService,
    ProposalProtocolService,
    ResultService,
    RevisionDecisionService,
    RevisionService,
    RfiProposalService,
    RfiService,
    RuleBasedGoalValidator,
    SimilarityMatrixService,
    StopFlagService,
)

# ---------- Session ----------


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """Открыть сессию БД на время запроса.

    После успешного запроса — commit.
    При ошибке — rollback.
    Сессия автоматически закроется (async with).
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


DbSession = Annotated[AsyncSession, Depends(get_db_session)]


# ---------- Repositories ----------


def get_project_repo(session: DbSession) -> ProjectRepository:
    return SqlAlchemyProjectRepository(session)


def get_task_repo(session: DbSession) -> TaskRepository:
    return SqlAlchemyTaskRepository(session)


def get_cross_task_repo(session: DbSession) -> CrossTaskRepository:
    return SqlAlchemyCrossTaskRepository(session)


def get_import_log_repo(session: DbSession) -> ImportLogRepository:
    return SqlAlchemyImportLogRepository(session)


def get_entity_type_repo(session: DbSession) -> EntityTypeRepository:
    return SqlAlchemyEntityTypeRepository(session)


def get_entity_repo(session: DbSession) -> EntityRepository:
    return SqlAlchemyEntityRepository(session)


def get_document_type_repo(session: DbSession) -> DocumentTypeRepository:
    return SqlAlchemyDocumentTypeRepository(session)


def get_document_repo(session: DbSession) -> DocumentRepository:
    return SqlAlchemyDocumentRepository(session)


def get_document_version_repo(session: DbSession) -> DocumentVersionRepository:
    return SqlAlchemyDocumentVersionRepository(session)


def get_document_link_repo(session: DbSession) -> DocumentLinkRepository:
    return SqlAlchemyDocumentLinkRepository(session)


def get_premise_repo(session: DbSession) -> PremiseRepository:
    return SqlAlchemyPremiseRepository(session)


def get_goal_repo(session: DbSession) -> GoalRepository:
    return SqlAlchemyGoalRepository(session)


def get_decision_repo(session: DbSession) -> DecisionRepository:
    return SqlAlchemyDecisionRepository(session)


def get_norm_repo(session: DbSession) -> NormRepository:
    return SqlAlchemyNormRepository(session)


def get_decision_link_repo(session: DbSession) -> DecisionLinkRepository:
    return SqlAlchemyDecisionLinkRepository(session)


def get_decision_norm_repo(session: DbSession) -> DecisionNormRepository:
    return SqlAlchemyDecisionNormRepository(session)


def get_result_repo(session: DbSession) -> ResultRepository:
    return SqlAlchemyResultRepository(session)


def get_project_standard_repo(session: DbSession) -> ProjectStandardRepository:
    return SqlAlchemyProjectStandardRepository(session)


def get_revision_repo(session: DbSession) -> RevisionRepository:
    return SqlAlchemyRevisionRepository(session)


def get_change_repo(session: DbSession) -> ChangeRepository:
    return SqlAlchemyChangeRepository(session)


def get_stop_flag_repo(session: DbSession) -> StopFlagRepository:
    return SqlAlchemyStopFlagRepository(session)


def get_revision_decision_repo(
    session: DbSession,
) -> RevisionDecisionRepository:
    return SqlAlchemyRevisionDecisionRepository(session)


def get_action_repo(session: DbSession) -> ActionRepository:
    return SqlAlchemyActionRepository(session)


def get_rfi_repo(session: DbSession) -> RfiRepository:
    return SqlAlchemyRfiRepository(
        session, SqlAlchemyTaskRepository(session)
    )


ProjectRepoDep = Annotated[ProjectRepository, Depends(get_project_repo)]
TaskRepoDep = Annotated[TaskRepository, Depends(get_task_repo)]
CrossTaskRepoDep = Annotated[CrossTaskRepository, Depends(get_cross_task_repo)]
ImportLogRepoDep = Annotated[ImportLogRepository, Depends(get_import_log_repo)]
EntityTypeRepoDep = Annotated[EntityTypeRepository, Depends(get_entity_type_repo)]
EntityRepoDep = Annotated[EntityRepository, Depends(get_entity_repo)]

DocumentTypeRepoDep = Annotated[DocumentTypeRepository, Depends(get_document_type_repo)]
DocumentRepoDep = Annotated[DocumentRepository, Depends(get_document_repo)]
DocumentVersionRepoDep = Annotated[DocumentVersionRepository, Depends(get_document_version_repo)]
DocumentLinkRepoDep = Annotated[DocumentLinkRepository, Depends(get_document_link_repo)]
PremiseRepoDep = Annotated[PremiseRepository, Depends(get_premise_repo)]
GoalRepoDep = Annotated[GoalRepository, Depends(get_goal_repo)]
DecisionRepoDep = Annotated[DecisionRepository, Depends(get_decision_repo)]
NormRepoDep = Annotated[NormRepository, Depends(get_norm_repo)]
DecisionLinkRepoDep = Annotated[DecisionLinkRepository, Depends(get_decision_link_repo)]
DecisionNormRepoDep = Annotated[DecisionNormRepository, Depends(get_decision_norm_repo)]
ResultRepoDep = Annotated[ResultRepository, Depends(get_result_repo)]
ProjectStandardRepoDep = Annotated[
    ProjectStandardRepository, Depends(get_project_standard_repo)
]
RevisionRepoDep = Annotated[RevisionRepository, Depends(get_revision_repo)]
ChangeRepoDep = Annotated[ChangeRepository, Depends(get_change_repo)]
StopFlagRepoDep = Annotated[StopFlagRepository, Depends(get_stop_flag_repo)]
RevisionDecisionRepoDep = Annotated[
    RevisionDecisionRepository, Depends(get_revision_decision_repo)
]
ActionRepoDep = Annotated[ActionRepository, Depends(get_action_repo)]
RfiRepoDep = Annotated[RfiRepository, Depends(get_rfi_repo)]


# ---------- Domain services ----------


def get_import_service(
    task_repo: TaskRepoDep,
    import_log_repo: ImportLogRepoDep,
) -> ImportService:
    return ImportService(
        task_repo=task_repo,
        import_log_repo=import_log_repo,
    )


def get_matrix_service(
    cross_task_repo: CrossTaskRepoDep,
    task_repo: TaskRepoDep,
) -> MatrixService:
    return MatrixService(
        cross_task_repo=cross_task_repo,
        task_repo=task_repo,
    )


def get_entity_type_service(
    entity_type_repo: EntityTypeRepoDep,
) -> EntityTypeService:
    return EntityTypeService(repo=entity_type_repo)


def get_entity_service(
    entity_repo: EntityRepoDep,
    entity_type_repo: EntityTypeRepoDep,
) -> EntityService:
    return EntityService(
        repo=entity_repo,
        entity_type_repo=entity_type_repo,
    )


def get_document_type_service(
    document_type_repo: DocumentTypeRepoDep,
) -> DocumentTypeService:
    return DocumentTypeService(repo=document_type_repo)


def get_document_service(
    document_repo: DocumentRepoDep,
    document_type_repo: DocumentTypeRepoDep,
    task_repo: TaskRepoDep,
) -> DocumentService:
    return DocumentService(
        repo=document_repo,
        document_type_repo=document_type_repo,
        task_repo=task_repo,
    )


def get_document_version_service(
    version_repo: DocumentVersionRepoDep,
    document_repo: DocumentRepoDep,
) -> DocumentVersionService:
    return DocumentVersionService(
        version_repo=version_repo,
        document_repo=document_repo,
    )


def get_document_link_service(
    document_link_repo: DocumentLinkRepoDep,
    document_repo: DocumentRepoDep,
) -> DocumentLinkService:
    return DocumentLinkService(
        repo=document_link_repo,
        document_repo=document_repo,
    )


def get_premise_service(
    premise_repo: PremiseRepoDep,
) -> PremiseService:
    return PremiseService(repo=premise_repo)


def get_goal_service(
    goal_repo: GoalRepoDep,
    premise_repo: PremiseRepoDep,
) -> GoalService:
    return GoalService(repo=goal_repo, premise_repo=premise_repo)


def get_goal_proposal_service(
    premise_repo: PremiseRepoDep,
) -> GoalProposalService:
    return GoalProposalService(premise_repo=premise_repo)


def get_decision_service(
    decision_repo: DecisionRepoDep,
    project_repo: ProjectRepoDep,
    premise_repo: PremiseRepoDep,
    goal_repo: GoalRepoDep,
) -> DecisionService:
    return DecisionService(
        repo=decision_repo,
        project_repo=project_repo,
        premise_repo=premise_repo,
        goal_repo=goal_repo,
    )


def get_norm_service(
    norm_repo: NormRepoDep,
) -> NormService:
    return NormService(repo=norm_repo)


def get_decision_link_service(
    link_repo: DecisionLinkRepoDep,
    decision_repo: DecisionRepoDep,
) -> DecisionLinkService:
    return DecisionLinkService(repo=link_repo, decision_repo=decision_repo)


def get_decision_norm_service(
    decision_norm_repo: DecisionNormRepoDep,
    decision_repo: DecisionRepoDep,
    norm_repo: NormRepoDep,
) -> DecisionNormService:
    return DecisionNormService(
        repo=decision_norm_repo,
        decision_repo=decision_repo,
        norm_repo=norm_repo,
    )


def get_decision_proposal_service(
    goal_repo: GoalRepoDep,
    decision_repo: DecisionRepoDep,
) -> DecisionProposalService:
    return DecisionProposalService(
        goal_repo=goal_repo,
        decision_repo=decision_repo,
    )


def get_goal_validator_service(
    goal_repo: GoalRepoDep,
    premise_repo: PremiseRepoDep,
    result_repo: ResultRepoDep,
    standard_repo: ProjectStandardRepoDep,
) -> RuleBasedGoalValidator:
    return RuleBasedGoalValidator(
        goal_repo=goal_repo,
        premise_repo=premise_repo,
        result_repo=result_repo,
        standard_repo=standard_repo,
    )


def get_similarity_matrix_service(
    premise_repo: PremiseRepoDep,
) -> SimilarityMatrixService:
    return SimilarityMatrixService(premise_repo=premise_repo)


def get_proposal_protocol_service(
    goal_repo: GoalRepoDep,
) -> ProposalProtocolService:
    return ProposalProtocolService(goal_repo=goal_repo)


def get_goal_validators(
    validator: "GoalValidatorServiceDep",
) -> list[GoalValidatorService]:
    """Список валидаторов для протокола. Сейчас — один, веха 6 — +LLM."""
    return [validator]


def get_result_service(
    result_repo: ResultRepoDep,
) -> ResultService:
    return ResultService(repo=result_repo)


def get_project_standard_service(
    standard_repo: ProjectStandardRepoDep,
) -> ProjectStandardService:
    return ProjectStandardService(repo=standard_repo)


def get_revision_service(
    revision_repo: RevisionRepoDep,
) -> RevisionService:
    return RevisionService(repo=revision_repo)


def get_action_service(
    action_repo: ActionRepoDep,
) -> ActionService:
    return ActionService(repo=action_repo)


def get_change_service(
    change_repo: ChangeRepoDep,
) -> ChangeService:
    return ChangeService(repo=change_repo)


def get_stop_flag_service(
    stop_flag_repo: StopFlagRepoDep,
) -> StopFlagService:
    return StopFlagService(repo=stop_flag_repo)


def get_revision_decision_service(
    decision_repo: RevisionDecisionRepoDep,
) -> RevisionDecisionService:
    return RevisionDecisionService(repo=decision_repo)


def get_rfi_service(
    rfi_repo: RfiRepoDep,
    task_repo: TaskRepoDep,
    project_repo: ProjectRepoDep,
    decision_repo: DecisionRepoDep,
    goal_repo: GoalRepoDep,
) -> RfiService:
    return RfiService(
        task_repo=task_repo,
        project_repo=project_repo,
        decision_repo=decision_repo,
        goal_repo=goal_repo,
        rfi_repo=rfi_repo,
    )


def get_rfi_proposal_service(
    decision_repo: DecisionRepoDep,
    rfi_repo: RfiRepoDep,
) -> RfiProposalService:
    return RfiProposalService(
        decision_repo=decision_repo,
        rfi_repo=rfi_repo,
    )


ImportServiceDep = Annotated[ImportService, Depends(get_import_service)]
MatrixServiceDep = Annotated[MatrixService, Depends(get_matrix_service)]
EntityTypeServiceDep = Annotated[EntityTypeService, Depends(get_entity_type_service)]
EntityServiceDep = Annotated[EntityService, Depends(get_entity_service)]

DocumentTypeServiceDep = Annotated[DocumentTypeService, Depends(get_document_type_service)]
DocumentServiceDep = Annotated[DocumentService, Depends(get_document_service)]
DocumentVersionServiceDep = Annotated[DocumentVersionService, Depends(get_document_version_service)]
DocumentLinkServiceDep = Annotated[DocumentLinkService, Depends(get_document_link_service)]
PremiseServiceDep = Annotated[PremiseService, Depends(get_premise_service)]
GoalServiceDep = Annotated[GoalService, Depends(get_goal_service)]
GoalProposalServiceDep = Annotated[GoalProposalService, Depends(get_goal_proposal_service)]
DecisionServiceDep = Annotated[DecisionService, Depends(get_decision_service)]
NormServiceDep = Annotated[NormService, Depends(get_norm_service)]
DecisionLinkServiceDep = Annotated[
    DecisionLinkService, Depends(get_decision_link_service)
]
DecisionNormServiceDep = Annotated[
    DecisionNormService, Depends(get_decision_norm_service)
]
DecisionProposalServiceDep = Annotated[
    DecisionProposalService, Depends(get_decision_proposal_service)
]
GoalValidatorServiceDep = Annotated[RuleBasedGoalValidator, Depends(get_goal_validator_service)]
SimilarityMatrixServiceDep = Annotated[
    SimilarityMatrixService, Depends(get_similarity_matrix_service)
]
ProposalProtocolServiceDep = Annotated[
    ProposalProtocolService, Depends(get_proposal_protocol_service)
]
GoalValidatorsDep = Annotated[
    list[GoalValidatorService],
    Depends(get_goal_validators),
]
ResultServiceDep = Annotated[ResultService, Depends(get_result_service)]
ProjectStandardServiceDep = Annotated[
    ProjectStandardService, Depends(get_project_standard_service)
]
RevisionServiceDep = Annotated[RevisionService, Depends(get_revision_service)]
ChangeServiceDep = Annotated[ChangeService, Depends(get_change_service)]
StopFlagServiceDep = Annotated[StopFlagService, Depends(get_stop_flag_service)]
RevisionDecisionServiceDep = Annotated[
    RevisionDecisionService, Depends(get_revision_decision_service)
]
ActionServiceDep = Annotated[ActionService, Depends(get_action_service)]
RfiServiceDep = Annotated[RfiService, Depends(get_rfi_service)]
RfiProposalServiceDep = Annotated[RfiProposalService, Depends(get_rfi_proposal_service)]
