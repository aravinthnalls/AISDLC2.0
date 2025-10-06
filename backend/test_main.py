"""
Unit tests for QR Code Generator API
"""

import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

class TestHealthEndpoint:
    """Test health check endpoint."""
    
    def test_health_check(self):
        """Test health endpoint returns 200."""
        response = client.get("/health")
        assert response.status_code == 200
        
        data = response.json()
        assert data["status"] == "healthy"
        assert "timestamp" in data
        assert "version" in data

class TestQRGeneration:
    """Test QR code generation functionality."""
    
    def test_generate_text_qr(self):
        """Test generating QR code from plain text."""
        response = client.post("/generate", json={
            "data": "Hello World",
            "data_type": "text"
        })
        assert response.status_code == 200
        assert response.headers["content-type"] == "image/png"
    
    def test_generate_url_qr(self):
        """Test generating QR code from URL."""
        response = client.post("/generate", json={
            "data": "https://example.com",
            "data_type": "url"
        })
        assert response.status_code == 200
        assert response.headers["content-type"] == "image/png"
    
    def test_generate_email_qr(self):
        """Test generating QR code from email."""
        response = client.post("/generate", json={
            "data": "test@example.com",
            "data_type": "email"
        })
        assert response.status_code == 200
        assert response.headers["content-type"] == "image/png"
    
    def test_invalid_email(self):
        """Test invalid email format."""
        response = client.post("/generate", json={
            "data": "invalid-email",
            "data_type": "email"
        })
        assert response.status_code == 400
    
    def test_invalid_phone(self):
        """Test invalid phone format."""
        response = client.post("/generate", json={
            "data": "123",
            "data_type": "phone"
        })
        assert response.status_code == 400
    
    def test_empty_data(self):
        """Test empty data input."""
        response = client.post("/generate", json={
            "data": "",
            "data_type": "text"
        })
        assert response.status_code == 400