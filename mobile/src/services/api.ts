/**
 * API client for Pokemon Card Scanner backend
 */
import axios from 'axios';
import { PricingResult, ErrorResponse } from '../types';

// Backend URL - change this to your backend URL
// For local testing: http://localhost:8000
// For Cloud Run: https://your-service.run.app
const BACKEND_URL = 'http://localhost:8000';

export class CardScannerAPI {
  private baseUrl: string;

  constructor(baseUrl: string = BACKEND_URL) {
    this.baseUrl = baseUrl;
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

      // Append to form data
      formData.append('image', blob, 'card.jpg');

      // Send to backend
      const result = await axios.post<PricingResult>(
        `${this.baseUrl}/api/v1/scan`,
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
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
