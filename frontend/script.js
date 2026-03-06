// QR Code Generator Frontend JavaScript

class QRGenerator {
    constructor() {
        const runtimeApiBase = typeof window !== 'undefined' && window.__API_BASE_URL__;
        this.apiBaseUrl = runtimeApiBase || 'http://localhost:8000';
        this.debounceTimer = null;
        this.currentQRBlob = null;
        this.currentQRImageUrl = null;
        this.activeRequestController = null;
        this.errorTimeout = null;
        
        this.initializeElements();
        this.bindEvents();
        this.updateHelperText();
        this.updatePlaceholder();
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

        // Cleanup object URLs and pending network requests
        window.addEventListener('beforeunload', () => {
            this.cleanupResources();
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
        const rawData = this.inputData.value.trim();
        const dataType = this.dataTypeSelect.value;
        
        // Clear previous QR code if input is empty
        if (!rawData) {
            this.clearQRCode();
            return;
        }

        const data = normalizeInput(rawData, dataType);
        const validationError = getValidationErrorMessage(data, dataType);

        if (validationError) {
            this.showError(validationError);
            this.clearQRCode();
            return;
        }

        try {
            // Cancel in-flight request to avoid stale preview updates
            if (this.activeRequestController) {
                this.activeRequestController.abort();
            }

            this.activeRequestController = new AbortController();
            this.showLoading();
            this.hideError();

            const response = await fetch(`${this.apiBaseUrl}/generate-qr`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                signal: this.activeRequestController.signal,
                body: JSON.stringify({
                    data: data,
                    data_type: dataType
                })
            });

            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                throw new Error(errorData.detail || 'Failed to generate QR code');
            }

            const blob = await response.blob();
            this.currentQRBlob = blob;
            
            // Display QR code
            const imageUrl = URL.createObjectURL(blob);
            this.displayQRCode(imageUrl);
            
            this.enableDownload();

        } catch (error) {
            if (error.name === 'AbortError') {
                return;
            }

            console.error('Error generating QR code:', error);
            this.showError(error.message);
            this.clearQRCode();
        } finally {
            this.activeRequestController = null;
            this.hideLoading();
        }
    }

    displayQRCode(imageUrl) {
        if (this.currentQRImageUrl) {
            URL.revokeObjectURL(this.currentQRImageUrl);
        }

        this.currentQRImageUrl = imageUrl;
        this.qrContainer.innerHTML = `<img src="${imageUrl}" alt="Generated QR Code">`;
        this.qrContainer.classList.add('has-qr');
    }

    clearQRCode() {
        if (this.currentQRImageUrl) {
            URL.revokeObjectURL(this.currentQRImageUrl);
            this.currentQRImageUrl = null;
        }

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

        if (this.errorTimeout) {
            clearTimeout(this.errorTimeout);
        }
        
        // Auto-hide error after 5 seconds
        this.errorTimeout = setTimeout(() => {
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

    cleanupResources() {
        if (this.activeRequestController) {
            this.activeRequestController.abort();
            this.activeRequestController = null;
        }

        if (this.currentQRImageUrl) {
            URL.revokeObjectURL(this.currentQRImageUrl);
            this.currentQRImageUrl = null;
        }

        if (this.errorTimeout) {
            clearTimeout(this.errorTimeout);
            this.errorTimeout = null;
        }
    }
}

// Utility functions
function normalizeInput(data, dataType) {
    if (!data) {
        return data;
    }

    if (dataType === 'url' && !/^https?:\/\//i.test(data)) {
        return `https://${data}`;
    }

    return data;
}

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
            return /\d/.test(data) && data.replace(/[^\d]/g, '').length >= 7;
        case 'wifi': {
            const parts = data.split(',').map((part) => part.trim());
            return parts.length >= 2 && parts[0].length > 0;
        }
        default:
            return data.trim().length > 0;
    }
}

function getValidationErrorMessage(data, dataType) {
    if (data.length > 1000) {
        return 'Input is too long. Please keep it under 1000 characters.';
    }

    if (validateInput(data, dataType)) {
        return '';
    }

    const validationMessages = {
        text: 'Please enter text to generate a QR code.',
        url: 'Please enter a valid URL (e.g., https://example.com).',
        email: 'Please enter a valid email address.',
        phone: 'Please enter a valid phone number with at least 7 digits.',
        wifi: 'Please use WiFi format: SSID,Password,Security (security is optional).'
    };

    return validationMessages[dataType] || 'Please enter valid input.';
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
    const errorMessage = document.getElementById('errorMessage');
    const errorText = document.getElementById('errorText');
    if (errorMessage && errorText) {
        errorText.textContent = 'You appear to be offline. QR generation requires backend connectivity.';
        errorMessage.classList.add('show');
    }
});

// Export for potential testing or external use
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { QRGenerator, validateInput, normalizeInput, getValidationErrorMessage };
}
