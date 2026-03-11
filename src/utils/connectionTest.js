// Connection Test Utility
// Use this to verify backend connectivity

import api from '../services/api';

export const testBackendConnection = async () => {
  const results = {
    backend: false,
    health: false,
    auth: false,
    timestamp: new Date().toISOString(),
    errors: []
  };

  try {
    // Test 1: Basic backend connection
    console.log('🔍 Testing backend connection...');
    const response = await fetch('http://localhost:8000/health');
    
    if (response.ok) {
      results.backend = true;
      results.health = await response.json();
      console.log('✅ Backend is running:', results.health);
    } else {
      results.errors.push(`Backend returned status: ${response.status}`);
      console.error('❌ Backend health check failed');
    }
  } catch (error) {
    results.errors.push(`Backend connection failed: ${error.message}`);
    console.error('❌ Cannot connect to backend:', error.message);
  }

  try {
    // Test 2: API instance connection
    console.log('🔍 Testing API instance...');
    const apiResponse = await api.get('/health');
    
    if (apiResponse.status === 200) {
      results.auth = true;
      console.log('✅ API instance working correctly');
    }
  } catch (error) {
    results.errors.push(`API instance failed: ${error.message}`);
    console.error('❌ API instance test failed:', error.message);
  }

  // Summary
  console.log('\n📊 Connection Test Summary:');
  console.log('Backend Running:', results.backend ? '✅' : '❌');
  console.log('Health Check:', results.health ? '✅' : '❌');
  console.log('API Instance:', results.auth ? '✅' : '❌');
  
  if (results.errors.length > 0) {
    console.log('\n⚠️ Errors:');
    results.errors.forEach(err => console.log('  -', err));
  }

  if (results.backend && results.auth) {
    console.log('\n🎉 All systems operational!');
  } else {
    console.log('\n❌ Connection issues detected. Please check:');
    console.log('  1. Is backend running? (cd backend && python main.py)');
    console.log('  2. Is backend on port 8000?');
    console.log('  3. Check backend logs for errors');
  }

  return results;
};

// Auto-run in development mode
if (import.meta.env.DEV) {
  console.log('🚀 VidyaMitra - Development Mode');
  console.log('Running connection test...\n');
  
  // Run test after a short delay to allow app to initialize
  setTimeout(() => {
    testBackendConnection();
  }, 1000);
}

export default testBackendConnection;
