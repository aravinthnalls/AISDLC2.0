// QR Code Generator Frontend JavaScript

class QRGenerator {
    constructor() {
        this.apiBaseUrl = 'http://localhost:8000';
        this.debounceTimer = null;
        this.currentQRBlob = null;
        
        this.initializeElements();
        this.bindEvents();
        this.updateHelperText();
    }

    initializeElements() {
        this.dataTypeSelect = document.getElementById('dataType');
        this.inputData = document.getElementById('inputData');
        this.qrContainer = document.getElementById('qrContainer');
        this.downloadBtn = document.getElementById('downloadBtn');
        this.loading = document.getElementById('loading');
        this.errorMessage = document.getElementById('errorMessage');
        this.errorText = document.getElementById('errorText');
        this.helperText = document.getElementById('helperText');
    }

    bindEvents() {
        // Real-time input handling with debounce
        this.inputData.addEventListener('input', () => {
            this.debounceGeneration();
        });

        // Data type change handler
        this.dataTypeSelect.addEventListener('change', () => {
            this.updateHelperText();
            this.updatePlaceholder();
            this.debounceGeneration();
        });

        // Download button handler
        this.downloadBtn.addEventListener('click', () => {
            this.downloadQRCode();
        });

        // Clear error on input
        this.inputData.addEventListener('focus', () => {
            this.hideError();
        });
    }

    debounceGeneration() {
        clearTimeout(this.debounceTimer);
        this.debounceTimer = setTimeout(() => {
            this.generateQRCode();
        }, 300); // 300ms debounce
    }

    updateHelperText() {
        const dataType = this.dataTypeSelect.value;
        const helperTexts = {
            text: 'Enter any text to generate a QR code',
            url: 'Enter a website URL (e.g., google.com or https://example.com)',
            email: 'Enter an email address (e.g., user@example.com)',
            phone: 'Enter a phone number (e.g., +1234567890)',
            wifi: 'Format: SSID,Password,Security (e.g., MyWiFi,password123,WPA)'
        };

        this.helperText.textContent = helperTexts[dataType] || helperTexts.text;
    }

    updatePlaceholder() {
        const dataType = this.dataTypeSelect.value;
        const placeholders = {
            text: 'Enter any text...',
            url: 'https://example.com',
            email: 'user@example.com',
            phone: '+1 (555) 123-4567',
            wifi: 'MyWiFi,password123,WPA'
        };

        this.inputData.placeholder = placeholders[dataType] || placeholders.text;
    }

    async generateQRCode() {
        const data = this.inputData.value.trim();
        
        // Clear previous QR code if input is empty
        if (!data) {
            this.clearQRCode();
            return;
        }

        try {
            this.showLoading();
            this.hideError();

            const response = await fetch(`${this.apiBaseUrl}/generate-qr`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    data: data,
                    data_type: this.dataTypeSelect.value
                })
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Failed to generate QR code');
            }

            const blob = await response.blob();
            this.currentQRBlob = blob;
            
            // Display QR code
            const imageUrl = URL.createObjectURL(blob);
            this.displayQRCode(imageUrl);
            
            this.enableDownload();

        } catch (error) {
            console.error('Error generating QR code:', error);
            this.showError(error.message);
            this.clearQRCode();
        } finally {
            this.hideLoading();
        }
    }

    displayQRCode(imageUrl) {
        this.qrContainer.innerHTML = `<img src="${imageUrl}" alt="Generated QR Code">`;
        this.qrContainer.classList.add('has-qr');
    }

    clearQRCode() {
        this.qrContainer.innerHTML = `
            <div class="placeholder">
                <div class="placeholder-icon">📱</div>
                <p>Your QR code will appear here</p>
            </div>
        `;
        this.qrContainer.classList.remove('has-qr');
        this.disableDownload();
        this.currentQRBlob = null;
    }

    enableDownload() {
        this.downloadBtn.disabled = false;
    }

    disableDownload() {
        this.downloadBtn.disabled = true;
    }

    downloadQRCode() {
        if (!this.currentQRBlob) {
            this.showError('No QR code to download');
            return;
        }

        try {
            const url = URL.createObjectURL(this.currentQRBlob);
            const link = document.createElement('a');
            link.href = url;
            
            // Generate filename based on data type and timestamp
            const dataType = this.dataTypeSelect.value;
            const timestamp = new Date().toISOString().slice(0, 19).replace(/:/g, '-');
            link.download = `qrcode-${dataType}-${timestamp}.png`;
            
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            
            // Clean up the URL object
            URL.revokeObjectURL(url);

        } catch (error) {
            console.error('Error downloading QR code:', error);
            this.showError('Failed to download QR code');
        }
    }

    showLoading() {
        this.loading.classList.add('show');
    }

    hideLoading() {
        this.loading.classList.remove('show');
    }

    showError(message) {
        this.errorText.textContent = message;
        this.errorMessage.classList.add('show');
        
        // Auto-hide error after 5 seconds
        setTimeout(() => {
            this.hideError();
        }, 5000);
    }

    hideError() {
        this.errorMessage.classList.remove('show');
    }

    // Check if API is available
    async checkAPIHealth() {
        try {
            const response = await fetch(`${this.apiBaseUrl}/health`);
            if (!response.ok) {
                throw new Error('API health check failed');
            }
            return true;
        } catch (error) {
            console.warn('API not available:', error);
            this.showError('Backend API is not available. Please make sure the server is running on http://localhost:8000');
            return false;
        }
    }
}

// Utility functions
function validateInput(data, dataType) {
    switch (dataType) {
        case 'email':
            return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(data);
        case 'url':
            try {
                new URL(data.startsWith('http') ? data : `https://${data}`);
                return true;
            } catch {
                return false;
            }
        case 'phone':
            return /^[\+]?[1-9][\d]{6,14}$/.test(data.replace(/\s/g, ''));
        case 'wifi':
            return data.split(',').length >= 2;
        default:
            return data.trim().length > 0;
    }
}

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    const qrGenerator = new QRGenerator();
    
    // Check API health on startup
    qrGenerator.checkAPIHealth();
    
    // Add some visual feedback for better UX
    console.log('🚀 QR Code Generator initialized successfully!');
    console.log('💡 Start typing in the input field to generate QR codes in real-time');
});

// Handle online/offline status
window.addEventListener('online', () => {
    console.log('📶 Connection restored');
});

window.addEventListener('offline', () => {
    console.log('📵 Connection lost');
});

// Export for potential testing or external use
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { QRGenerator, validateInput };
}
