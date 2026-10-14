"""Smoke-тесты маппинга SQLAlchemy-моделей ↔ доменных сущностей документов."""

import uuid

from backend.src.adapters.db.models.document import DocumentModel
from backend.src.adapters.db.repositories.document_link_repository import (
    SqlAlchemyDocumentLinkRepository,
)
from backend.src.adapters.db.repositories.document_repository import (
    SqlAlchemyDocumentRepository,
)
from backend.src.adapters.db.repositories.document_type_repository import (
    SqlAlchemyDocumentTypeRepository,
)
from backend.src.adapters.db.repositories.document_version_repository import (
    SqlAlchemyDocumentVersionRepository,
)
from backend.src.domain.entities.document import Document
from backend.src.domain.entities.document_link import DocumentLink
from backend.src.domain.entities.document_type import DocumentType
from backend.src.domain.entities.document_version import DocumentVersion
from backend.src.domain.value_objects.document import (
    DocPartType,
    DocumentKind,
    DocumentLinkType,
    LifecycleStatus,
)

# ---------- Document — Enum-маппинг ----------


def test_document_to_model_enum_values():
    """Domain → model: Enum-поля становятся строками через .value."""
    doc = Document(
        project_id=uuid.uuid4(),
        document_type_id=uuid.uuid4(),
        document_kind=DocumentKind.PD,
        doc_part_type=DocPartType.TCH,
        lifecycle_status=LifecycleStatus.APPROVED,
        document_name="Test",
        cipher="АБЗ-001-XX ЭД",
    )
    model = SqlAlchemyDocumentRepository._to_model(doc)

    assert model.document_kind == "ПД"
    assert model.doc_part_type == "ТЧ"
    assert model.lifecycle_status == "APPROVED"
    assert str(model.document_kind) != "DocumentKind.PD"


def test_document_to_domain_enum_values():
    """Model → domain: строковые поля превращаются в Enum через конструктор."""
    model = DocumentModel(
        id=uuid.uuid4(),
        guid=uuid.uuid4(),
        project_id=uuid.uuid4(),
        document_type_id=uuid.uuid4(),
        document_kind="ПД",
        doc_part_type="ТЧ",
        lifecycle_status="APPROVED",
        cipher="АБЗ-001-XX ЭД",
        document_name="Test",
    )
    doc = SqlAlchemyDocumentRepository._to_domain(model)

    assert isinstance(doc.document_kind, DocumentKind)
    assert doc.document_kind == DocumentKind.PD
    assert isinstance(doc.doc_part_type, DocPartType)
    assert doc.doc_part_type == DocPartType.TCH
    assert isinstance(doc.lifecycle_status, LifecycleStatus)
    assert doc.lifecycle_status == LifecycleStatus.APPROVED


def test_document_roundtrip():
    """Domain → model → domain: поля не теряются."""
    project_id = uuid.uuid4()
    doc = Document(
        id=uuid.uuid4(),
        guid=uuid.uuid4(),
        project_id=project_id,
        document_type_id=uuid.uuid4(),
        cipher="АБЗ-001-XX ЭД",
        document_name="Технологический процесс",
        document_kind=DocumentKind.RD,
        doc_part_type=None,
        section_code="АИ",
        mark="А",
        lifecycle_status=LifecycleStatus.IN_REVIEW,
    )
    model = SqlAlchemyDocumentRepository._to_model(doc)
    doc2 = SqlAlchemyDocumentRepository._to_domain(model)

    assert doc2.id == doc.id
    assert doc2.project_id == project_id
    assert doc2.document_type_id == doc.document_type_id
    assert doc2.guid == doc.guid
    assert doc2.document_name == doc.document_name
    assert doc2.cipher == doc.cipher
    assert doc2.section_code == doc.section_code
    assert doc2.mark == doc.mark
    assert doc2.document_kind == DocumentKind.RD
    assert doc2.lifecycle_status == LifecycleStatus.IN_REVIEW
    assert doc2.doc_part_type is None


def test_document_to_model_no_timestamps():
    """Domain → model: created_at / updated_at НЕ передаются (их ставит БД)."""
    doc = Document(
        project_id=uuid.uuid4(),
        document_type_id=uuid.uuid4(),
        document_name="Test",
        cipher="X",
    )
    model = SqlAlchemyDocumentRepository._to_model(doc)

    assert model.__dict__.get("created_at") is None
    assert model.__dict__.get("updated_at") is None


# ---------- DocumentLink — Enum-маппинг ----------


def test_document_link_roundtrip():
    """Domain → model → domain для DocumentLink."""
    source = uuid.uuid4()
    target = uuid.uuid4()
    link = DocumentLink(
        source_document_id=source,
        target_document_id=target,
        link_type=DocumentLinkType.APPENDIX,
    )
    model = SqlAlchemyDocumentLinkRepository._to_model(link)
    link2 = SqlAlchemyDocumentLinkRepository._to_domain(model)

    assert link2.link_type == DocumentLinkType.APPENDIX
    assert link2.source_document_id == source
    assert link2.target_document_id == target


def test_document_link_to_model_enum_value():
    """Domain → model: link_type становится строкой 'appendix'."""
    link = DocumentLink(
        source_document_id=uuid.uuid4(),
        target_document_id=uuid.uuid4(),
        link_type=DocumentLinkType.APPENDIX,
    )
    model = SqlAlchemyDocumentLinkRepository._to_model(link)

    assert model.link_type == "appendix"
    assert isinstance(model.link_type, str)


# ---------- DocumentType и DocumentVersion — простые ----------


def test_document_type_roundtrip():
    """Domain → model → domain для DocumentType."""
    dt = DocumentType(
        code="drawing",
        name="Чертёж",
        gost_code=None,
    )
    model = SqlAlchemyDocumentTypeRepository._to_model(dt)
    dt2 = SqlAlchemyDocumentTypeRepository._to_domain(model)

    assert dt2.code == "drawing"
    assert dt2.name == "Чертёж"
    assert dt2.gost_code is None


def test_document_version_roundtrip():
    """Domain → model → domain для DocumentVersion."""
    document_id = uuid.uuid4()
    v = DocumentVersion(
        document_id=document_id,
        version="v1.0",
        file_path="/x/y.pdf",
        file_name="y.pdf",
        hash_sha256="a" * 64,
        format_original="pdf",
        size_bytes=1024,
        is_current=True,
    )
    model = SqlAlchemyDocumentVersionRepository._to_model(v)
    v2 = SqlAlchemyDocumentVersionRepository._to_domain(model)

    assert v2.is_current is True
    assert v2.size_bytes == 1024
    assert v2.hash_sha256 == "a" * 64
    assert v2.document_id == document_id
    assert v2.version == "v1.0"
