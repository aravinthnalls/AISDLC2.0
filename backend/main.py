from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import qrcode
from io import BytesIO
import re

app = FastAPI(title="QR Code Generator API", version="1.0.0")

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QRRequest(BaseModel):
    data: str
    data_type: str

def format_data_for_qr(data: str, data_type: str) -> str:
    """Format data based on type for QR code generation."""
    if data_type == "email":
        # Basic email validation
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', data):
            raise HTTPException(status_code=400, detail="Invalid email format")
        return f"mailto:{data}"
    
    elif data_type == "phone":
        # Remove non-numeric characters and validate
        phone = re.sub(r'[^\d+]', '', data)
        if not phone or len(phone) < 7:
            raise HTTPException(status_code=400, detail="Invalid phone number")
        return f"tel:{phone}"
    
    elif data_type == "url":
        # Add protocol if missing
        if not data.startswith(('http://', 'https://')):
            data = f"https://{data}"
        # Basic URL validation
        if not re.match(r'^https?://[^\s/$.?#].[^\s]*$', data):
            raise HTTPException(status_code=400, detail="Invalid URL format")
        return data
    
    elif data_type == "wifi":
        # Expected format: SSID,Password,Security (WPA/WEP/nopass)
        parts = data.split(',')
        if len(parts) < 2:
            raise HTTPException(status_code=400, detail="WiFi format: SSID,Password,Security")
        ssid, password = parts[0].strip(), parts[1].strip()
        security = parts[2].strip().upper() if len(parts) > 2 else "WPA"
        
        if security not in ["WPA", "WEP", "NOPASS"]:
            security = "WPA"
        
        return f"WIFI:T:{security};S:{ssid};P:{password};;"
    
    else:  # text or default
        return data

@app.get("/")
async def root():
    return {"message": "QR Code Generator API is running"}

@app.post("/generate")
async def generate_qr(request: QRRequest):
    """Generate QR code from input data."""
    try:
        # Format data based on type
        formatted_data = format_data_for_qr(request.data, request.data_type)
        
        # Create QR code
        qr = qrcode.QRCode(
            version=1,  # Controls the size of the QR Code
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(formatted_data)
        qr.make(fit=True)
        
        # Create image
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Save to bytes buffer
        img_buffer = BytesIO()
        img.save(img_buffer, format='PNG')
        img_buffer.seek(0)
        
        return StreamingResponse(
            BytesIO(img_buffer.read()),
            media_type="image/png",
            headers={"Content-Disposition": "inline; filename=qr_code.png"}
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"QR generation failed: {str(e)}")

@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring."""
    return {
        "status": "healthy",
        "timestamp": "2024-01-01T00:00:00Z",
        "version": "1.0.0",
        "service": "QR Code Generator API"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "QR Code Generator"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
