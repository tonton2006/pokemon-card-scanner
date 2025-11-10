/**
 * TypeScript type definitions for Pokemon Card Scanner
 */

export interface CardInfo {
  name: string;
  set: string | null;
  number: string | null;
  rarity: string | null;
}

export interface PriceSource {
  name: string;
  price_usd: number;
  condition: string;
  url: string | null;
  last_updated: string;
}

export interface PricingStatistics {
  median: number;
  average: number;
  count: number;
  recommendation: string;
}

export interface PricingData {
  sources: PriceSource[];
  statistics: PricingStatistics;
}

export interface ScanMetadata {
  scan_time_ms: number;
  confidence_score: number;
}

export interface PricingResult {
  card: CardInfo;
  pricing: PricingData;
  metadata: ScanMetadata;
}

export interface ErrorResponse {
  error: {
    code: string;
    message: string;
    details?: any;
  };
}
