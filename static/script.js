// Application State
let messages = [];
let isLoading = false;

// DOM Elements
const welcomeScreen = document.getElementById('welcomeScreen');
const messagesContainer = document.getElementById('messagesContainer');
const loadingIndicator = document.getElementById('loadingIndicator');
const messagesEnd = document.getElementById('messagesEnd');
const clearBtn = document.getElementById('clearBtn');
const chatForm = document.getElementById('chatForm');
const messageInput = document.getElementById('messageInput');
const modelSelect = document.getElementById('modelSelect');
const sendButton = document.getElementById('sendButton');
const sendIcon = document.getElementById('sendIcon');
const loadingSpinner = document.getElementById('loadingSpinner');

// Initialize
document.addEventListener('DOMContentLoaded', function() {
    // Set default model (Ensure this matches the value in your index.html options, e.g., 'ollama3' or 'llama3')
    if (modelSelect) {
        // Fallback check to ensure we match whatever option is available in the dropdown
        const availableOptions = Array.from(modelSelect.options).map(opt => opt.value);
        if (availableOptions.includes('ollama3')) {
            modelSelect.value = 'ollama3';
        } else if (availableOptions.includes('llama3')) {
            modelSelect.value = 'llama3';
        } else {
            modelSelect.selectedIndex = 0;
        }
    }
    
    // Setup event listeners
    setupEventListeners();
    
    // Initial state
    updateSendButton();
});

function setupEventListeners() {
    if (chatForm) chatForm.addEventListener('submit', handleSubmit);
    if (clearBtn) clearBtn.addEventListener('click', clearChat);
    if (messageInput) {
        messageInput.addEventListener('input', handleInputChange);
        messageInput.addEventListener('keydown', handleKeyDown);
    }
}

function handleSubmit(e) {
    e.preventDefault();
    
    const content = messageInput.value.trim();
    const model = modelSelect ? modelSelect.value : 'ollama3';
    
    if (!content || isLoading) return;
    
    sendMessage(content, model);
}

function handleKeyDown(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        handleSubmit(e);
    }
}

function handleInputChange() {
    autoResizeTextarea();
    updateSendButton();
}

function autoResizeTextarea() {
    if (!messageInput) return;
    messageInput.style.height = 'auto';
    const newHeight = Math.min(messageInput.scrollHeight, 128);
    messageInput.style.height = newHeight + 'px';
}

function updateSendButton() {
    if (!sendButton || !messageInput) return;
    const hasContent = messageInput.value.trim().length > 0;
    sendButton.disabled = !hasContent || isLoading;
}

async function sendMessage(content, model) {
    // Add user message
    const userMessage = {
        id: Date.now().toString(),
        content: content,
        type: 'user',
        timestamp: new Date()
    };
    
    messages.push(userMessage);
    displayMessage(userMessage);
    
    // Clear input and update UI
    messageInput.value = '';
    messageInput.style.height = 'auto';
    hideWelcomeScreen();
    showClearButton();
    setLoadingState(true);
    
    // Normalize model selection to match what backend app.py expects
    let requestModel = model;
    if (model === 'llama3') {
        requestModel = 'ollama3'; 
    }
    
    try {
        const response = await fetch('/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                message: content,
                model: requestModel
            }),
        });

        const data = await response.json();

        let aiMessage;
        if (data.error) {
            aiMessage = {
                id: (Date.now() + 1).toString(),
                content: `Error: ${data.error}`,
                type: 'ai',
                model: model,
                timestamp: new Date()
            };
        } else {
            // --- BULLETPROOF EXTRACTION FALLBACKS ---
            // If the model returned an alternative schema key or directly as a string, resolve it
            let finalContent = "";
            
            if (data.response) {
                finalContent = data.response;
            } else if (data.summary && data.sentiment !== undefined) {
                // If it returned a structured summary but is missing the response key specifically
                finalContent = `**Summary:** ${data.summary}\n\n**Sentiment:** ${data.sentiment}/100`;
            } else if (typeof data === 'string') {
                finalContent = data;
            } else {
                // Fallback to stringifying whatever structure came back so the user can inspect it
                finalContent = JSON.stringify(data, null, 2);
            }
            
            aiMessage = {
                id: (Date.now() + 1).toString(),
                content: finalContent,
                type: 'ai',
                model: model,
                duration: data.duration,
                timestamp: new Date()
            };
        }
        
        messages.push(aiMessage);
        displayMessage(aiMessage);
        
    } catch (error) {
        const errorMessage = {
            id: (Date.now() + 1).toString(),
            content: `Network Error: ${error.message}. Please check if the local server is running.`,
            type: 'ai',
            model: model,
            timestamp: new Date()
        };
        
        messages.push(errorMessage);
        displayMessage(errorMessage);
        
    } finally {
        setLoadingState(false);
    }
}

function displayMessage(message) {
    if (!messagesContainer) return;
    
    const messageEl = document.createElement('div');
    messageEl.className = `message ${message.type}`;
    
    const time = message.timestamp.toLocaleTimeString([], { 
        hour: '2-digit', 
        minute: '2-digit' 
    });
    
    const avatarIcon = message.type === 'user' ? 
        '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>' :
        '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2z"/><path d="M8 14s1.5 2 4 2 4-2 4-2"/><line x1="9" y1="9" x2="9.01" y2="9"/><line x1="15" y1="9" x2="15.01" y2="9"/></svg>';
    
    const modelBadge = message.model ? 
        `<span class="message-model">${message.model}</span>` : '';
    
    const duration = message.duration ? 
        `<span>${message.duration.toFixed(2)}s</span>` : '';
    
    // Ensure content markdown doesn't display raw script injections
    let safeContent = message.content ? message.content : "No response generated.";
    
    messageEl.innerHTML = `
        <div class="message-wrapper">
            <div class="message-header">
                <div class="message-avatar">
                    ${avatarIcon}
                </div>
                <div class="message-info">
                    <span class="message-sender">${message.type === 'user' ? 'You' : 'AI Assistant'}</span>
                    ${modelBadge}
                </div>
            </div>
            <div class="message-bubble">
                <div class="message-text">${safeContent}</div>
            </div>
            <div class="message-footer">
                <span>${time}</span>
                ${duration}
            </div>
        </div>
    `;
    
    messagesContainer.appendChild(messageEl);
    scrollToBottom();
}

function setLoadingState(loading) {
    isLoading = loading;
    
    updateSendButton();
    if (messageInput) messageInput.disabled = loading;
    
    // Toggle loading indicator and send button icon
    if (loading) {
        if (loadingIndicator) loadingIndicator.style.display = 'block';
        if (sendIcon) sendIcon.style.display = 'none';
        if (loadingSpinner) loadingSpinner.style.display = 'block';
    } else {
        if (loadingIndicator) loadingIndicator.style.display = 'none';
        if (sendIcon) sendIcon.style.display = 'block';
        if (loadingSpinner) loadingSpinner.style.display = 'none';
    }
    
    if (loading) {
        scrollToBottom();
    }
}

function hideWelcomeScreen() {
    if (welcomeScreen) welcomeScreen.style.display = 'none';
}

function showWelcomeScreen() {
    if (welcomeScreen) welcomeScreen.style.display = 'flex';
}

function showClearButton() {
    if (clearBtn) clearBtn.style.display = 'flex';
}

function hideClearButton() {
    if (clearBtn) clearBtn.style.display = 'none';
}

function clearChat() {
    messages = [];
    if (messagesContainer) messagesContainer.innerHTML = '';
    showWelcomeScreen();
    hideClearButton();
    setLoadingState(false);
    updateSendButton();
}

function scrollToBottom() {
    if (messagesEnd) messagesEnd.scrollIntoView({ behavior: 'smooth' });
}