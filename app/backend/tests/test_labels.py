import uuid

from backend.models.item import Item
from backend.services import labels


def test_render_label_pdf(tmp_path):
    labels.settings.media_dir = tmp_path
    item = Item(
        id=uuid.uuid4(),
        short_id="abc1234",
        title="Test Item",
        description="This is a test description for a label.",
        tags=["test"],
        status="active",
    )
    pdf_path = labels.render_label_pdf(item)
    assert pdf_path.exists()
    assert pdf_path.suffix == ".pdf"
