// Function to send URL to Flask backend for classification
async function classifyUrl(url) {
  try {
    console.log(`[Preemptive Check] Analyzing URL: ${url}`);
    
    const response = await fetch('http://localhost:5000/classify_url', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ url: url }),
    });

    if (response.status === 403) {
      // Phishing detected - show warning and block navigation
      console.log(`[PHISHING DETECTED] URL: ${url}`);
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
    message: `This website (${url}) may be malicious. Continue at your own risk.`,
    buttons: [
      { title: 'Continue Anyway' },
      { title: 'Go Back' }
    ]
  });
}

// Store pending URL checks to avoid duplicate requests
let pendingChecks = new Map();

// Preemptive URL detection - intercept navigation before page loads
chrome.webNavigation.onBeforeNavigate.addListener(async (details) => {
  // Only check main frame navigation (not iframes)
  if (details.frameId === 0) {
    const url = details.url;
    
    // Skip chrome:// and extension URLs
    if (url.startsWith('chrome://') || url.startsWith('chrome-extension://')) {
      return;
    }
    
    // Skip if already checking this URL
    if (pendingChecks.has(url)) {
      return;
    }
    
    console.log(`[Preemptive] Checking URL before navigation: ${url}`);
    pendingChecks.set(url, true);
    
    try {
      const result = await classifyUrl(url);
      
      if (result.isPhishing) {
        // Block navigation to phishing site
        console.log(`[BLOCKED] Preventing navigation to phishing site: ${url}`);
        
        // Redirect to warning page
        chrome.tabs.update(details.tabId, {
          url: chrome.runtime.getURL('warning.html')
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

// Listen for messages from content script
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'preVisitCheck') {
    classifyUrl(request.url).then(sendResponse);
    return true; // Keep message channel open for async response
  }
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
