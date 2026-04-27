// Dynamic API Base - works on localhost and HF Spaces
const API_BASE = window.location.origin + '/api';

console.log('[ResearchMind] Initializing app...');
console.log('[ResearchMind] API_BASE:', API_BASE);

// DOM Elements - with error handling
let queryInput, runBtn, tryBtns, pipelineContainer, resultsSection, reportContainer, reportTitle, reportContent, sourcesContainer, feedbackText, copyBtn, alertContainer;

function initializeDOMElements() {
    try {
        queryInput = document.getElementById('query-input');
        runBtn = document.getElementById('run-btn');
        tryBtns = document.querySelectorAll('.try-btn');
        pipelineContainer = document.getElementById('pipeline-container');
        resultsSection = document.getElementById('results-section');
        reportContainer = document.getElementById('report-container');
        reportTitle = document.getElementById('report-title');
        reportContent = document.getElementById('report-content');
        sourcesContainer = document.getElementById('sources-container');
        feedbackText = document.getElementById('feedback-text');
        copyBtn = document.getElementById('copy-btn');
        alertContainer = document.getElementById('alert-container');
        
        // Check if all required elements exist
        const requiredElements = {
            queryInput, runBtn, pipelineContainer, resultsSection, reportContainer,
            reportTitle, reportContent, sourcesContainer, feedbackText, copyBtn, alertContainer
        };
        
        const missing = Object.entries(requiredElements)
            .filter(([_, el]) => !el)
            .map(([name, _]) => name);
        
        if (missing.length > 0) {
            console.error('[ResearchMind] Missing DOM elements:', missing);
            throw new Error(`Missing DOM elements: ${missing.join(', ')}`);
        }
        
        console.log('[ResearchMind] ✅ All DOM elements found');
        return true;
    } catch (error) {
        console.error('[ResearchMind] Failed to initialize DOM elements:', error);
        return false;
    }
}

// Event Listeners
function attachEventListeners() {
    try {
        runBtn.addEventListener('click', runResearch);
        copyBtn.addEventListener('click', copyReportToClipboard);

        // Try These button listeners
        tryBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                queryInput.value = btn.textContent.trim();
                runResearch();
            });
        });
        
        console.log('[ResearchMind] ✅ Event listeners attached');
    } catch (error) {
        console.error('[ResearchMind] Failed to attach event listeners:', error);
    }
}

// Initialize on document ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        console.log('[ResearchMind] DOMContentLoaded fired');
        if (initializeDOMElements()) {
            attachEventListeners();
        }
    });
} else {
    console.log('[ResearchMind] Document already loaded');
    if (initializeDOMElements()) {
        attachEventListeners();
    }
}

async function runResearch() {
    const query = queryInput.value.trim();
    
    if (!query) {
        showAlert('Please enter a research topic', 'error');
        return;
    }

    // Reset agent cards to pending
    resetUI();
    showLoading(true);
    runBtn.disabled = true;

    try {
        console.log('[ResearchMind] Starting research for:', query);
        console.log('[ResearchMind] API Base URL:', API_BASE);
        
        const requestBody = {
            query: query,
            use_gemini: false
        };
        
        console.log('[ResearchMind] Request payload:', requestBody);
        
        // Create AbortController for timeout
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 120000); // 120 second timeout
        
        const response = await fetch(`${API_BASE}/run`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
            },
            body: JSON.stringify(requestBody),
            signal: controller.signal
        });

        clearTimeout(timeoutId);

        console.log('[ResearchMind] Response status:', response.status);
        console.log('[ResearchMind] Response headers:', {
            contentType: response.headers.get('content-type'),
            cacheControl: response.headers.get('cache-control')
        });

        if (!response.ok) {
            const errorText = await response.text();
            console.error('[ResearchMind] HTTP Error Response:', errorText);
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }

        let result;
        const contentType = response.headers.get('content-type');
        
        if (contentType && contentType.includes('application/json')) {
            result = await response.json();
        } else {
            const text = await response.text();
            console.warn('[ResearchMind] Unexpected content type:', contentType);
            console.warn('[ResearchMind] Response text:', text.substring(0, 200));
            try {
                result = JSON.parse(text);
            } catch (e) {
                throw new Error(`Invalid JSON response: ${text.substring(0, 100)}`);
            }
        }
        
        console.log('[ResearchMind] Parsed result:', result);
        
        // Validate result has required fields
        if (!result || typeof result !== 'object') {
            throw new Error('Invalid response format: expected an object');
        }
        
        const requiredFields = ['query', 'steps', 'report', 'sources', 'feedback'];
        const missingFields = requiredFields.filter(field => !(field in result));
        
        if (missingFields.length > 0) {
            console.warn('[ResearchMind] Missing fields:', missingFields);
        }
        
        // Show results section before animation
        resultsSection.classList.remove('hidden');
        reportContainer.classList.add('visible');
        
        displayResults(result);
        animateAgentCards();
        showAlert('✅ Research completed successfully!', 'success');
        console.log('[ResearchMind] Research completed successfully');
        
    } catch (error) {
        console.error('[ResearchMind] Full error object:', error);
        console.error('[ResearchMind] Error message:', error.message);
        console.error('[ResearchMind] Error name:', error.name);
        console.error('[ResearchMind] Error stack:', error.stack);
        
        let errorMsg = error.message || 'Unknown error occurred';
        
        // Handle specific error types
        if (error.name === 'AbortError') {
            errorMsg = 'Request timed out (took more than 2 minutes). Please try a simpler query.';
        } else if (error instanceof TypeError) {
            if (error.message.includes('fetch')) {
                errorMsg = 'Network error: Failed to connect to server. Check your connection.';
            } else if (error.message.includes('Cannot read')) {
                errorMsg = 'Frontend error: Application not properly initialized. Try refreshing the page.';
            } else {
                errorMsg = `Network/connection error: ${error.message}`;
            }
        } else if (error.message.includes('HTTP')) {
            errorMsg = `Server error: ${error.message}. The API may be temporarily unavailable.`;
        } else if (error.message.includes('Invalid')) {
            errorMsg = `Data error: ${error.message}. Try a different query.`;
        }
        
        showAlert(`❌ ${errorMsg}`, 'error');
        console.log('[ResearchMind] Error handled:', errorMsg);
        
    } finally {
        showLoading(false);
        runBtn.disabled = false;
    }
}

function animateAgentCards() {
    const cards = pipelineContainer.querySelectorAll('.agent-card');
    cards.forEach((card, index) => {
        setTimeout(() => {
            card.classList.add('done');
            card.querySelector('.checkmark').classList.remove('hidden');
            const status = card.querySelector('.text-xs.font-medium');
            if (status) {
                status.textContent = 'DONE';
                status.style.color = '#10b981';
            }
        }, (index + 1) * 1000);
    });
}

function displayResults(result) {
    try {
        // Update report title
        reportTitle.textContent = `Research Report: ${result.query || 'Research'}`;

        // Display report content
        if (result.report) {
            const formatted = formatReport(result.report);
            reportContent.innerHTML = formatted;
        } else {
            reportContent.innerHTML = '<p>No report generated</p>';
        }

        // Display sources
        if (result.sources && result.sources.length > 0) {
            sourcesContainer.innerHTML = '';
            result.sources.forEach((source, index) => {
                const sourceCard = document.createElement('div');
                sourceCard.className = 'glass-card rounded-lg p-4 hover:bg-gray-800 transition-all cursor-pointer';
                
                const title = source.title || 'Untitled';
                const snippet = source.snippet || '';
                const url = source.url || '';
                
                sourceCard.innerHTML = `
                    <div class="flex items-start gap-3">
                        <div class="flex-shrink-0 text-orange-500 font-semibold text-sm">
                            [${index + 1}]
                        </div>
                        <div class="flex-1 min-w-0">
                            <h4 class="font-semibold text-white truncate">${title}</h4>
                            <p class="text-sm text-gray-400 line-clamp-2 mt-1">${snippet}</p>
                            ${url ? `<a href="${url}" target="_blank" class="text-orange-500 text-xs mt-2 inline-block hover:underline">Read more →</a>` : ''}
                        </div>
                    </div>
                `;
                sourcesContainer.appendChild(sourceCard);
            });
        } else {
            sourcesContainer.innerHTML = '<p class="text-gray-400">No sources found</p>';
        }

        // Display feedback
        if (result.feedback) {
            feedbackText.textContent = result.feedback;
        } else {
            feedbackText.textContent = 'No feedback available';
        }

        // Show results section with animation
        resultsSection.classList.remove('hidden');
        setTimeout(() => {
            reportContainer.classList.add('visible');
        }, 100);
    } catch (error) {
        console.error('Error in displayResults:', error);
        showAlert(`Error displaying results: ${error.message}`, 'error');
        reportContent.innerHTML = `<p class="text-red-500">Error: ${error.message}</p>`;
    }
}

function formatReport(text) {
    // Convert markdown-like formatting to HTML
    let html = text
        .replace(/^# (.*?)$/gm, '<h2 class="text-2xl font-bold mt-6 mb-3 text-white">$1</h2>')
        .replace(/^## (.*?)$/gm, '<h3 class="text-xl font-semibold mt-4 mb-2 text-white">$1</h3>')
        .replace(/^### (.*?)$/gm, '<h4 class="text-lg font-semibold mt-3 mb-2 text-white">$1</h4>')
        .replace(/\*\*(.*?)\*\*/g, '<strong class="font-semibold">$1</strong>')
        .replace(/\*(.*?)\*/g, '<em class="italic">$1</em>')
        .replace(/^- (.*?)$/gm, '<li class="ml-4">$1</li>')
        .split('\n\n')
        .map(para => {
            if (para.includes('<h') || para.includes('<li')) {
                return para;
            }
            return para.trim() ? `<p class="mb-4 leading-relaxed">${para}</p>` : '';
        })
        .join('');

    return html;
}

function copyReportToClipboard() {
    const reportText = reportContent.innerText;
    navigator.clipboard.writeText(reportText).then(() => {
        showAlert('Report copied to clipboard!', 'success');
    }).catch(() => {
        showAlert('Failed to copy report', 'error');
    });
}

function showLoading(show) {
    if (show) {
        runBtn.innerHTML = '<i class="fas fa-spinner spinner"></i> <span>Running...</span>';
    } else {
        runBtn.innerHTML = '<i class="fas fa-bolt"></i> <span>Run Research Pipeline</span>';
    }
}

function resetUI() {
    // Reset agent cards to pending state but keep them visible
    const cards = pipelineContainer.querySelectorAll('.agent-card');
    cards.forEach(card => {
        card.classList.remove('done');
        card.style.opacity = '1';
        card.style.display = 'block';
        const checkmark = card.querySelector('.checkmark');
        if (checkmark) {
            checkmark.classList.add('hidden');
        }
        const status = card.querySelector('.text-xs.font-medium');
        if (status) {
            status.textContent = 'PENDING';
            status.style.color = '#6b7280';
        }
    });

    // Show pipeline section but keep it visible for new results
    pipelineContainer.style.display = 'block';
    pipelineContainer.style.opacity = '1';
}

function showAlert(message, type = 'info') {
    const alert = document.createElement('div');
    alert.className = `alert ${type}`;
    alert.textContent = message;
    alert.style.maxWidth = '500px';
    alert.style.wordWrap = 'break-word';
    alert.style.whiteSpace = 'normal';
    alert.style.overflowWrap = 'break-word';
    
    console.log(`[Alert - ${type}]`, message);
    
    alertContainer.appendChild(alert);

    // Auto-remove after 4 seconds
    const timeout = setTimeout(() => {
        alert.remove();
    }, 4000);
    
    // Allow manual close on click
    alert.addEventListener('click', () => {
        clearTimeout(timeout);
        alert.remove();
    });
}
