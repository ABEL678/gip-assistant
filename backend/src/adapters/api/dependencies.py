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
    SqlAlchemyCrossTaskRepository,
    SqlAlchemyDocumentLinkRepository,
    SqlAlchemyDocumentRepository,
    SqlAlchemyDocumentTypeRepository,
    SqlAlchemyDocumentVersionRepository,
    SqlAlchemyEntityRepository,
    SqlAlchemyEntityTypeRepository,
    SqlAlchemyGoalRepository,
    SqlAlchemyImportLogRepository,
    SqlAlchemyPremiseRepository,
    SqlAlchemyProjectRepository,
    SqlAlchemyProjectStandardRepository,
    SqlAlchemyResultRepository,
    SqlAlchemyTaskRepository,
)
from backend.src.adapters.db.session import AsyncSessionLocal
from backend.src.domain.ports.goal_validator import GoalValidatorService
from backend.src.domain.ports.repositories import (
    CrossTaskRepository,
    DocumentLinkRepository,
    DocumentRepository,
    DocumentTypeRepository,
    DocumentVersionRepository,
    EntityRepository,
    EntityTypeRepository,
    GoalRepository,
    ImportLogRepository,
    PremiseRepository,
    ProjectRepository,
    ProjectStandardRepository,
    ResultRepository,
    TaskRepository,
)
from backend.src.domain.services import (
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
    PremiseService,
    ProposalProtocolService,
    RuleBasedGoalValidator,
    SimilarityMatrixService,
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


def get_result_repo(session: DbSession) -> ResultRepository:
    return SqlAlchemyResultRepository(session)


def get_project_standard_repo(session: DbSession) -> ProjectStandardRepository:
    return SqlAlchemyProjectStandardRepository(session)


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
ResultRepoDep = Annotated[ResultRepository, Depends(get_result_repo)]
ProjectStandardRepoDep = Annotated[
    ProjectStandardRepository, Depends(get_project_standard_repo)
]


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
) -> DocumentService:
    return DocumentService(
        repo=document_repo,
        document_type_repo=document_type_repo,
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
