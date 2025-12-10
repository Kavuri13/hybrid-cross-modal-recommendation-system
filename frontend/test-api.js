// Test script to verify CLIP API
console.log('Testing CLIP API...');

fetch('http://localhost:8000/api/v1/search/workflow', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    text: "blue colour tshirt",
    top_k: 6,
    image_weight: 0.0,
    text_weight: 1.0,
    fusion_method: "weighted_avg",
    enable_reranking: true,
    reranking_method: "cross_attention",
    category_filter: "fashion"
  })
})
.then(response => {
  console.log('Response status:', response.status);
  return response.json();
})
.then(data => {
  console.log('API Response:', data);
})
.catch(error => {
  console.error('API Error:', error);
});