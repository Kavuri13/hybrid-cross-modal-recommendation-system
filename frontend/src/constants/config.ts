// AI Search Configuration - Fixed parameters for production use
export const AI_SEARCH_CONFIG = {
  // Fixed search parameters
  topK: 12,
  imageWeight: 0.7,
  textWeight: 0.3,
  fusionMethod: 'weighted_avg' as const,
  enableReranking: true,
  rerankingMethod: 'cross_attention' as const,
  diversityWeight: 0.1,
} as const;

// E-commerce categories
export const PRODUCT_CATEGORIES = [
  'Electronics',
  'Fashion', 
  'Home & Kitchen',
  'Books',
  'Sports & Outdoors',
  'Beauty & Personal Care',
  'Automotive',
  'Toys & Games',
  'Health & Wellness',
  'Garden & Outdoor'
] as const;

// Popular brands
export const POPULAR_BRANDS = [
  'Apple', 'Samsung', 'Nike', 'Adidas', 'Sony', 'Dell', 'HP', 'Canon',
  'Nikon', 'LG', 'Panasonic', 'Microsoft', 'Google', 'Amazon', 'Philips'
] as const;

// Shipping options
export const SHIPPING_OPTIONS = {
  FREE_SHIPPING_THRESHOLD: 50,
  EXPRESS_DELIVERY_DAYS: 1,
  STANDARD_DELIVERY_DAYS: 3,
  INTERNATIONAL_DELIVERY_DAYS: 7
} as const;

// Price ranges for filtering
export const PRICE_RANGES = [
  { label: 'Under $25', min: 0, max: 25 },
  { label: '$25 - $50', min: 25, max: 50 },
  { label: '$50 - $100', min: 50, max: 100 },
  { label: '$100 - $250', min: 100, max: 250 },
  { label: '$250 - $500', min: 250, max: 500 },
  { label: 'Over $500', min: 500, max: null }
] as const;

// App configuration
export const APP_CONFIG = {
  APP_NAME: 'SmartShop',
  APP_TAGLINE: 'AI-Powered Shopping',
  COMPANY_NAME: 'SmartShop Inc.',
  SUPPORT_EMAIL: 'support@smartshop.com',
  RETURN_POLICY_DAYS: 30,
  WARRANTY_PERIOD_MONTHS: 12
} as const;