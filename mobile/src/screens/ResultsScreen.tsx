/**
 * Results Screen - Display card pricing information
 */
import React from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  Image,
} from 'react-native';
import { PricingResult } from '../types';

interface ResultsScreenProps {
  route: {
    params: {
      result: PricingResult;
      imageUri?: string;
    };
  };
  navigation: any;
}

export default function ResultsScreen({ route, navigation }: ResultsScreenProps) {
  const { result, imageUri } = route.params;
  const { card, pricing, metadata } = result;

  const formatPrice = (price: number) => {
    return `$${price.toFixed(2)}`;
  };

  const formatTime = (ms: number) => {
    if (ms < 1000) return `${ms}ms`;
    return `${(ms / 1000).toFixed(2)}s`;
  };

  return (
    <ScrollView style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>Scan Results</Text>
        <Text style={styles.scanTime}>
          ⚡ Scanned in {formatTime(metadata.scan_time_ms)}
        </Text>
      </View>

      {/* Scanned Image */}
      {imageUri && (
        <View style={styles.imageContainer}>
          <Image
            source={{ uri: imageUri }}
            style={styles.cardImage}
            resizeMode="contain"
          />
        </View>
      )}

      {/* Card Info */}
      <View style={styles.card}>
        <Text style={styles.cardName}>{card.name}</Text>
        {card.set && <Text style={styles.cardDetail}>Set: {card.set}</Text>}
        {card.number && <Text style={styles.cardDetail}>Number: {card.number}</Text>}
        {card.rarity && <Text style={styles.cardDetail}>Rarity: {card.rarity}</Text>}
      </View>

      {/* Recommended Price */}
      {pricing.statistics.count > 0 && (
        <View style={styles.recommendedCard}>
          <Text style={styles.recommendedLabel}>Recommended Price</Text>
          <Text style={styles.recommendedPrice}>
            {formatPrice(pricing.statistics.median)}
          </Text>
          <Text style={styles.recommendedSubtext}>
            Median of {pricing.statistics.count} source{pricing.statistics.count !== 1 ? 's' : ''}
          </Text>
        </View>
      )}

      {/* Price Sources */}
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Price Breakdown</Text>

        {pricing.sources.length === 0 ? (
          <View style={styles.noPricing}>
            <Text style={styles.noPricingText}>
              No pricing data available for this card.
            </Text>
          </View>
        ) : (
          pricing.sources.map((source, index) => (
            <View key={index} style={styles.priceSource}>
              <View style={styles.sourceHeader}>
                <Text style={styles.sourceName}>{source.name}</Text>
                <Text style={styles.sourcePrice}>
                  {formatPrice(source.price_usd)}
                </Text>
              </View>
              <Text style={styles.sourceCondition}>
                Condition: {source.condition}
              </Text>
            </View>
          ))
        )}
      </View>

      {/* Statistics */}
      {pricing.statistics.count > 0 && (
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Statistics</Text>
          <View style={styles.statsRow}>
            <View style={styles.stat}>
              <Text style={styles.statLabel}>Median</Text>
              <Text style={styles.statValue}>
                {formatPrice(pricing.statistics.median)}
              </Text>
            </View>
            <View style={styles.stat}>
              <Text style={styles.statLabel}>Average</Text>
              <Text style={styles.statValue}>
                {formatPrice(pricing.statistics.average)}
              </Text>
            </View>
            <View style={styles.stat}>
              <Text style={styles.statLabel}>Sources</Text>
              <Text style={styles.statValue}>
                {pricing.statistics.count}
              </Text>
            </View>
          </View>
        </View>
      )}

      {/* Scan Again Button */}
      <TouchableOpacity
        style={styles.scanAgainButton}
        onPress={() => navigation.goBack()}
      >
        <Text style={styles.scanAgainText}>📷 Scan Another Card</Text>
      </TouchableOpacity>

      <View style={styles.bottomPadding} />
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  header: {
    backgroundColor: '#4CAF50',
    padding: 24,
    paddingTop: 48,
  },
  title: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#fff',
    marginBottom: 4,
  },
  scanTime: {
    fontSize: 14,
    color: '#fff',
    opacity: 0.9,
  },
  imageContainer: {
    alignItems: 'center',
    padding: 16,
    backgroundColor: '#fff',
    marginHorizontal: 16,
    marginTop: 16,
    borderRadius: 12,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  cardImage: {
    width: 250,
    height: 350,
    borderRadius: 8,
  },
  card: {
    backgroundColor: '#fff',
    margin: 16,
    padding: 20,
    borderRadius: 12,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  cardName: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 12,
  },
  cardDetail: {
    fontSize: 16,
    color: '#666',
    marginBottom: 4,
  },
  recommendedCard: {
    backgroundColor: '#4CAF50',
    marginHorizontal: 16,
    marginBottom: 16,
    padding: 24,
    borderRadius: 12,
    alignItems: 'center',
  },
  recommendedLabel: {
    fontSize: 14,
    color: '#fff',
    opacity: 0.9,
    marginBottom: 8,
  },
  recommendedPrice: {
    fontSize: 48,
    fontWeight: 'bold',
    color: '#fff',
    marginBottom: 4,
  },
  recommendedSubtext: {
    fontSize: 14,
    color: '#fff',
    opacity: 0.9,
  },
  section: {
    marginHorizontal: 16,
    marginBottom: 16,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 12,
  },
  priceSource: {
    backgroundColor: '#fff',
    padding: 16,
    borderRadius: 8,
    marginBottom: 8,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.05,
    shadowRadius: 2,
    elevation: 1,
  },
  sourceHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 4,
  },
  sourceName: {
    fontSize: 16,
    fontWeight: '600',
    color: '#333',
  },
  sourcePrice: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#4CAF50',
  },
  sourceCondition: {
    fontSize: 14,
    color: '#666',
  },
  noPricing: {
    backgroundColor: '#fff',
    padding: 24,
    borderRadius: 8,
    alignItems: 'center',
  },
  noPricingText: {
    fontSize: 16,
    color: '#666',
    textAlign: 'center',
  },
  statsRow: {
    flexDirection: 'row',
    gap: 12,
  },
  stat: {
    flex: 1,
    backgroundColor: '#fff',
    padding: 16,
    borderRadius: 8,
    alignItems: 'center',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.05,
    shadowRadius: 2,
    elevation: 1,
  },
  statLabel: {
    fontSize: 12,
    color: '#666',
    marginBottom: 4,
  },
  statValue: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#333',
  },
  scanAgainButton: {
    backgroundColor: '#2196F3',
    marginHorizontal: 16,
    marginTop: 8,
    paddingVertical: 16,
    borderRadius: 12,
    alignItems: 'center',
  },
  scanAgainText: {
    color: '#fff',
    fontSize: 18,
    fontWeight: 'bold',
  },
  bottomPadding: {
    height: 32,
  },
});
