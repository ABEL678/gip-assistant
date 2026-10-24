"""Smoke-тесты маппинга result_document_id и trigger_action_id (6.12a)."""

from uuid import uuid4

from backend.src.adapters.db.models.action import ActionModel
from backend.src.adapters.db.models.document import DocumentModel
from backend.src.adapters.db.repositories.action_repository import SqlAlchemyActionRepository
from backend.src.adapters.db.repositories.document_repository import SqlAlchemyDocumentRepository
from backend.src.domain.entities.action import Action
from backend.src.domain.entities.document import Document


def test_action_result_document_to_model():
    """result_document_id маппится корректно."""
    doc_id = uuid4()
    action = Action(
        project_id=uuid4(),
        formulation="test",
        result_document_id=doc_id,
    )
    model = SqlAlchemyActionRepository._to_model(action)
    assert model.result_document_id == doc_id


def test_action_result_document_to_domain():
    """result_document_id маппится из модели в домен."""
    doc_id = uuid4()
    model = ActionModel(
        id=uuid4(),
        project_id=uuid4(),
        formulation="test",
        result_document_id=doc_id,
        state="plan",
    )
    action = SqlAlchemyActionRepository._to_domain(model)
    assert action.result_document_id == doc_id


def test_document_trigger_action_to_model():
    """trigger_action_id маппится корректно."""
    action_id = uuid4()
    doc = Document(
        project_id=uuid4(),
        cipher="TEST",
        document_name="test",
        document_type_id=uuid4(),
        trigger_action_id=action_id,
    )
    model = SqlAlchemyDocumentRepository._to_model(doc)
    assert model.trigger_action_id == action_id


def test_document_trigger_action_to_domain():
    """trigger_action_id маппится из модели в домен."""
    action_id = uuid4()
    model = DocumentModel(
        id=uuid4(),
        guid=uuid4(),
        project_id=uuid4(),
        cipher="TEST",
        document_name="test",
        document_type_id=uuid4(),
        document_kind="ПД",
        lifecycle_status="DRAFT",
        trigger_action_id=action_id,
    )
    doc = SqlAlchemyDocumentRepository._to_domain(model)
    assert doc.trigger_action_id == action_id
