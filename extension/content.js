// Monitor address bar changes for preemptive detection
let lastUrl = '';
let urlCheckInterval;

// Function to check if protection is enabled
async function isProtectionEnabled() {
  return new Promise((resolve) => {
    chrome.storage.local.get(['protectionEnabled'], (result) => {
      resolve(result.protectionEnabled !== false); // Default to true
    });
  });
}

// Start monitoring URL changes
// NOTE: This is currently disabled because background.js webNavigation.onBeforeNavigate
// already handles all URL checks BEFORE pages load, which is more efficient.
// Content script monitoring would create duplicate checks.
function startUrlMonitoring() {
  // DISABLED - webNavigation in background.js handles this better
  console.log('[Content Script] URL monitoring disabled - using background.js webNavigation instead');
  return;
  
  /* ORIGINAL CODE - COMMENTED OUT TO PREVENT DUPLICATES
  urlCheckInterval = setInterval(async () => {
    const currentUrl = window.location.href;
    
    // Check if protection is enabled
    const enabled = await isProtectionEnabled();
    if (!enabled) {
      return; // Skip monitoring if disabled
    }
    
    // Check if URL has changed
    if (currentUrl !== lastUrl && currentUrl !== 'about:blank') {
      lastUrl = currentUrl;
      
      // Send URL to background script for preemptive check
      chrome.runtime.sendMessage({ 
        url: currentUrl,
        action: 'preVisitCheck' 
      }, (response) => {
        if (response && response.isPhishing) {
          console.log(`[Content Script] Phishing detected: ${currentUrl}`);
          // The background script will handle the blocking
        }
      });
    }
  }, 100); // Check every 100ms
  */
}

// Stop monitoring
function stopUrlMonitoring() {
  if (urlCheckInterval) {
    clearInterval(urlCheckInterval);
    urlCheckInterval = null;
  }
}

// Listen for messages from background script
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.action === 'checkURL') {
    // Legacy support - send current URL
    chrome.runtime.sendMessage({ url: window.location.href });
  } else if (message.action === 'startMonitoring') {
    startUrlMonitoring();
  } else if (message.action === 'stopMonitoring') {
    stopUrlMonitoring();
  }
});

// Start monitoring when content script loads
startUrlMonitoring();
