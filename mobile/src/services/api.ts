/**
 * API client for Pokemon Card Scanner backend
 */
import axios from 'axios';
import { PricingResult, ErrorResponse } from '../types';

// Backend URL - using WSL2 IP address for Windows browser access
// For local testing from Windows: http://192.168.50.229:8000
// For Cloud Run: https://your-service.run.app
const BACKEND_URL = 'http://192.168.50.229:8000';

export class CardScannerAPI {
  private baseUrl: string;

  constructor(baseUrl: string = BACKEND_URL) {
    this.baseUrl = baseUrl;
    console.log('[API] CardScannerAPI initialized - VERSION: 2025-11-10-v4');
  }

  /**
   * Scan a Pokemon card and get pricing information
   */
  async scanCard(imageUri: string): Promise<PricingResult> {
    try {
      // Create form data
      const formData = new FormData();

      // For web, we need to fetch the blob first
      const response = await fetch(imageUri);
      const blob = await response.blob();

      console.log('[API] Blob type:', blob.type);
      console.log('[API] Blob size:', blob.size);

      // Convert Blob to File - File objects preserve content-type better with axios
      // Axios has issues with Blob serialization in browsers, losing the content-type
      const file = new File([blob], 'card.jpg', { type: blob.type || 'image/jpeg' });

      console.log('[API] File object type:', file.type);
      console.log('[API] File object name:', file.name);
      console.log('[API] File object size:', file.size);

      // Append to form data
      formData.append('image', file);

      console.log('[API] FormData contents:', formData.get('image'));

      // Send to backend
      // Note: Don't set Content-Type header - let axios handle it automatically
      // Axios will set the proper multipart/form-data boundary
      const result = await axios.post<PricingResult>(
        `${this.baseUrl}/api/v1/scan`,
        formData,
        {
          timeout: 10000, // 10 second timeout
        }
      );

      return result.data;
    } catch (error: any) {
      if (error.response) {
        // Server responded with error
        const errorData = error.response.data as ErrorResponse;
        throw new Error(errorData.error.message || 'Failed to scan card');
      } else if (error.request) {
        // Request made but no response
        throw new Error('Could not connect to server. Please check your internet connection.');
      } else {
        // Something else went wrong
        throw new Error(error.message || 'An unexpected error occurred');
      }
    }
  }

  /**
   * Check backend health
   */
  async checkHealth(): Promise<boolean> {
    try {
      const response = await axios.get(`${this.baseUrl}/api/v1/health`, {
        timeout: 5000,
      });
      return response.data.status === 'healthy';
    } catch {
      return false;
    }
  }
}

// Export singleton instance
export const apiClient = new CardScannerAPI();
