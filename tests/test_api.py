from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root():
    """Test endpoint root untuk memastikan aplikasi berjalan dengan baik."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json().get("ok") is True


def test_upload_and_evaluate(monkeypatch):
    """
    Test proses upload file dan evaluasi.
    
    Args:
        monkeypatch: Fixture pytest untuk memodifikasi behavior selama testing
    """
    # Siapkan file PDF dummy (header minimal untuk menghindari parsing pypdf)
    fake_pdf_content = b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n1 0 obj\n<<>>\nendobj\ntrailer\n<<>>\n%%EOF"
    
    files = {
        "cv": ("cv.pdf", fake_pdf_content, "application/pdf"),
        "report": ("rep.pdf", fake_pdf_content, "application/pdf"),
    }
    
    # Test upload endpoint
    response = client.post("/upload", files=files)
    assert response.status_code == 200
    
    data = response.json()
    assert "cv_id" in data
    assert "report_id" in data
    
    # Monkeypatch celery task untuk menghindari dependency worker eksternal
    called_tracker = {}
    
    def fake_delay(job_id, payload):
        """Fake function untuk menggantikan celery task delay."""
        called_tracker["job_id"] = job_id
        called_tracker["payload"] = payload
    
    # Patch the celery task
    import app.tasks as tasks
    monkeypatch.setattr(tasks.evaluate_job, "delay", fake_delay)
    
    # Test evaluate endpoint
    evaluate_payload = {
        "job_title": "Backend Engineer",
        "cv_id": data["cv_id"],
        "report_id": data["report_id"]
    }
    
    response = client.post("/evaluate", json=evaluate_payload)
    assert response.status_code == 200
    assert response.json()["status"] == "queued"
    
    # Verifikasi bahwa fake task dipanggil dengan parameter yang benar
    assert "job_id" in called_tracker