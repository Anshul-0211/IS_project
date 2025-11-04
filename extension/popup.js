// Load current state when popup opens
document.addEventListener('DOMContentLoaded', () => {
  loadExtensionState();
  loadStats();
  setupEventListeners();
});

// Setup event listeners
function setupEventListeners() {
  const toggleSwitch = document.getElementById('toggleSwitch');
  
  toggleSwitch.addEventListener('change', (e) => {
    const isEnabled = e.target.checked;
    saveExtensionState(isEnabled);
    updateUI(isEnabled);
    
    // Notify background script of state change
    chrome.runtime.sendMessage({
      action: 'toggleProtection',
      enabled: isEnabled
    });
  });
}

// Load extension state from storage
function loadExtensionState() {
  chrome.storage.local.get(['protectionEnabled'], (result) => {
    // Default to enabled if not set
    const isEnabled = result.protectionEnabled !== undefined ? result.protectionEnabled : true;
    
    document.getElementById('toggleSwitch').checked = isEnabled;
    updateUI(isEnabled);
  });
}

// Save extension state to storage
function saveExtensionState(isEnabled) {
  chrome.storage.local.set({ protectionEnabled: isEnabled }, () => {
    console.log(`Protection ${isEnabled ? 'enabled' : 'disabled'}`);
  });
}

// Update UI based on protection state
function updateUI(isEnabled) {
  const statusIcon = document.getElementById('statusIcon');
  const statusText = document.getElementById('statusText');
  const statusSection = document.querySelector('.status-section');
  
  if (isEnabled) {
    statusIcon.textContent = '🛡️';
    statusText.textContent = 'Protection Active';
    statusText.className = 'status-text status-enabled';
    statusSection.style.background = '#d4edda';
  } else {
    statusIcon.textContent = '⚠️';
    statusText.textContent = 'Protection Disabled';
    statusText.className = 'status-text status-disabled';
    statusSection.style.background = '#f8d7da';
  }
}

// Load statistics
function loadStats() {
  chrome.storage.local.get(['blockedCount', 'checkedCount'], (result) => {
    const blockedCount = result.blockedCount || 0;
    const checkedCount = result.checkedCount || 0;
    
    document.getElementById('blockedCount').textContent = blockedCount;
    document.getElementById('checkedCount').textContent = checkedCount;
  });
}

// Listen for stats updates
chrome.storage.onChanged.addListener((changes, namespace) => {
  if (namespace === 'local') {
    if (changes.blockedCount) {
      document.getElementById('blockedCount').textContent = changes.blockedCount.newValue || 0;
    }
    if (changes.checkedCount) {
      document.getElementById('checkedCount').textContent = changes.checkedCount.newValue || 0;
    }
  }
});
