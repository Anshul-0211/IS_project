// Initialize stats on install
chrome.runtime.onInstalled.addListener(() => {
  chrome.storage.local.get(['protectionEnabled', 'blockedCount', 'checkedCount'], (result) => {
    if (result.protectionEnabled === undefined) {
      chrome.storage.local.set({ protectionEnabled: true });
    }
    if (result.blockedCount === undefined) {
      chrome.storage.local.set({ blockedCount: 0 });
    }
    if (result.checkedCount === undefined) {
      chrome.storage.local.set({ checkedCount: 0 });
    }
  });
});

// Function to check if protection is enabled
async function isProtectionEnabled() {
  return new Promise((resolve) => {
    chrome.storage.local.get(['protectionEnabled'], (result) => {
      resolve(result.protectionEnabled !== false); // Default to true
    });
  });
}

// Function to increment stats
function incrementStats(blocked = false) {
  chrome.storage.local.get(['blockedCount', 'checkedCount'], (result) => {
    const checkedCount = (result.checkedCount || 0) + 1;
    const updates = { checkedCount };
    
    if (blocked) {
      updates.blockedCount = (result.blockedCount || 0) + 1;
    }
    
    chrome.storage.local.set(updates);
  });
}

// Function to check if URL should bypass warning (user clicked "Continue Anyway")
async function shouldBypassWarning(url) {
  return new Promise((resolve) => {
    chrome.storage.local.get(['bypassWarning', 'bypassTimestamp'], (result) => {
      if (result.bypassWarning === url && result.bypassTimestamp) {
        // Check if bypass is still valid (within 5 minutes)
        const timeDiff = Date.now() - result.bypassTimestamp;
        if (timeDiff < 5 * 60 * 1000) { // 5 minutes
          console.log(`[Bypass] Allowing previously bypassed URL: ${url}`);
          resolve(true);
        } else {
          // Expired, clear the bypass
          chrome.storage.local.remove(['bypassWarning', 'bypassTimestamp']);
          resolve(false);
        }
      } else {
        resolve(false);
      }
    });
  });
}

// Function to send URL to Flask backend for classification
async function classifyUrl(url) {
  try {
    // Check if protection is enabled
    const enabled = await isProtectionEnabled();
    if (!enabled) {
      console.log(`[Protection Disabled] Skipping check for: ${url}`);
      return { isPhishing: false, disabled: true };
    }

    // Check if user recently bypassed this URL
    const shouldBypass = await shouldBypassWarning(url);
    if (shouldBypass) {
      // Clear the bypass after using it once
      chrome.storage.local.remove(['bypassWarning', 'bypassTimestamp']);
      return { isPhishing: false, bypassed: true };
    }

    console.log(`[Preemptive Check] Analyzing URL: ${url}`);
    
    const response = await fetch('http://localhost:5000/classify_url', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ url: url }),
    });

    incrementStats(false); // Increment checked count

    if (response.status === 403) {
      // Phishing detected - show warning and block navigation
      console.log(`[PHISHING DETECTED] URL: ${url}`);
      incrementStats(true); // Increment blocked count
      showPhishingWarning(url);
      return { isPhishing: true };
    } else {
      const data = await response.json();
      console.log(`[SAFE] URL: ${url}, Probability: ${data.probability || 'N/A'}`);
      return { isPhishing: false, data: data };
    }
  } catch (error) {
    console.error('Error classifying URL:', error);
    return { isPhishing: false, error: error };
  }
}

// Show phishing warning popup
function showPhishingWarning(url) {
  chrome.notifications.create({
    type: 'basic',
    iconUrl: 'icon.png',
    title: '⚠️ PHISHING DETECTED!',
    message: `This website (${url}) may be malicious. Blocking access for your safety.`,
    priority: 2
  });
}

// Store pending URL checks to avoid duplicate requests
let pendingChecks = new Map();

// Function to normalize URL for comparison (remove trailing slashes, www, etc)
function normalizeUrl(url) {
  try {
    const urlObj = new URL(url);
    // Remove www. prefix
    let hostname = urlObj.hostname.replace(/^www\./, '');
    // Remove trailing slash from pathname
    let pathname = urlObj.pathname.replace(/\/$/, '') || '/';
    // Normalize to base domain + path (ignore protocol differences)
    return `${hostname}${pathname}${urlObj.search}`;
  } catch (e) {
    return url;
  }
}

// Function to check if URL or its normalized version is pending
function isPendingCheck(url) {
  const normalized = normalizeUrl(url);
  
  // Check exact URL
  if (pendingChecks.has(url)) {
    return true;
  }
  
  // Check normalized version
  for (let [pendingUrl, timestamp] of pendingChecks.entries()) {
    if (normalizeUrl(pendingUrl) === normalized) {
      // Check if it's still recent (within 2 seconds)
      if (Date.now() - timestamp < 2000) {
        return true;
      }
    }
  }
  
  return false;
}

// Preemptive URL detection - intercept navigation before page loads
chrome.webNavigation.onBeforeNavigate.addListener(async (details) => {
  // Only check main frame navigation (not iframes)
  if (details.frameId === 0) {
    const url = details.url;
    
    // Skip chrome:// and extension URLs
    if (url.startsWith('chrome://') || url.startsWith('chrome-extension://')) {
      return;
    }
    
    // Skip if already checking this URL or its normalized version
    if (isPendingCheck(url)) {
      console.log(`[Duplicate Check Prevented] Skipping: ${url}`);
      return;
    }
    
    console.log(`[Preemptive] Checking URL before navigation: ${url}`);
    pendingChecks.set(url, Date.now());
    
    try {
      const result = await classifyUrl(url);
      
      if (result.isPhishing) {
        // Block navigation to phishing site
        console.log(`[BLOCKED] Preventing navigation to phishing site: ${url}`);
        
        // Store the blocked URL for the warning page
        chrome.storage.local.set({ blockedUrl: url });
        
        // Redirect to warning page with URL parameter
        const warningUrl = chrome.runtime.getURL('warning.html') + '?url=' + encodeURIComponent(url);
        chrome.tabs.update(details.tabId, {
          url: warningUrl
        });
      }
    } catch (error) {
      console.error('Error in preemptive check:', error);
    } finally {
      // Remove from pending checks after a delay
      setTimeout(() => {
        pendingChecks.delete(url);
      }, 5000);
    }
  }
});

// Listen for messages from content script and popup
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'preVisitCheck') {
    classifyUrl(request.url).then(sendResponse);
    return true; // Keep message channel open for async response
  } else if (request.action === 'toggleProtection') {
    // Handle protection toggle from popup
    const enabled = request.enabled;
    console.log(`[Protection ${enabled ? 'ENABLED' : 'DISABLED'}]`);
    
    // Update badge to show status
    if (enabled) {
      chrome.action.setBadgeText({ text: '' });
      chrome.action.setBadgeBackgroundColor({ color: '#2ecc71' });
    } else {
      chrome.action.setBadgeText({ text: 'OFF' });
      chrome.action.setBadgeBackgroundColor({ color: '#e74c3c' });
    }
    
    sendResponse({ success: true });
  }
  return true;
});

// Monitor address bar changes for real-time detection
chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
  // Check when URL changes but before page loads
  if (changeInfo.url && changeInfo.status === 'loading') {
    console.log(`[URL Change] Detected URL change: ${changeInfo.url}`);
    // The onBeforeNavigate listener will handle the actual check
  }
});

// chrome.downloads.onChanged.addListener((delta) => {
//   if (delta.state && delta.state.current === 'complete') {
//     console.log('dekhliya')
//     chrome.downloads.search({ id: delta.id }, (results) => {
//       if (results && results.length && results[0].filename.endsWith('.txt')) {
//         fetchFileContents(results[0].filename)
//       }
//     })
//   }
// })

// function fetchFileContents(filename) {
//   fetch(`file://${filename}`)
//     .then((response) => response.text())
//     .then((text) => {
//       checkForRansomware(text)
//     })
//     .catch((error) => console.error('Error reading file:', error))
// }

// function checkForRansomware(fileContent) {
//   fetch('http://127.0.0.1:5000/check', {
//     method: 'POST',
//     headers: {
//       'Content-Type': 'application/json',
//     },
//     body: JSON.stringify({ content: fileContent }),
//   })
//     .then((response) => response.json())
//     .then((data) => {
//       if (data.is_ransomware) {
//         alert('Warning: This file is marked as ransomware.')
//       } else {
//         alert('File is safe.')
//       }
//     })
//     .catch((error) => console.error('Error checking for ransomware:', error))
// }
