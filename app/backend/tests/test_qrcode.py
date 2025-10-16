from backend.services.qrcode_utils import make_qr_png


def test_make_qr_png_returns_image():
    img = make_qr_png("http://example.com")
    assert img.mode == "RGB"
    assert img.size[0] == img.size[1]
