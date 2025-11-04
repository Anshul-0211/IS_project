// Monitor address bar changes for preemptive detection
let lastUrl = '';
let urlCheckInterval;

// Start monitoring URL changes
function startUrlMonitoring() {
  urlCheckInterval = setInterval(() => {
    const currentUrl = window.location.href;
    
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
