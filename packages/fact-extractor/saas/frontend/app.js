// Global state
let currentJobId = null;
let allFacts = [];
let currentEditingFactId = null;

// API base URL
const API_BASE = '';

// Initialize app
document.addEventListener('DOMContentLoaded', () => {
    setupFileUpload();
});

// Setup file upload
function setupFileUpload() {
    const uploadArea = document.getElementById('uploadArea');
    const fileInput = document.getElementById('fileInput');

    // Click to upload
    uploadArea.addEventListener('click', () => {
        fileInput.click();
    });

    // Drag and drop
    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.classList.add('dragging');
    });

    uploadArea.addEventListener('dragleave', () => {
        uploadArea.classList.remove('dragging');
    });

    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.classList.remove('dragging');
        const file = e.dataTransfer.files[0];
        if (file) {
            handleFileUpload(file);
        }
    });

    // File input change
    fileInput.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (file) {
            handleFileUpload(file);
        }
    });
}

// Handle file upload
async function handleFileUpload(file) {
    // Validate file type
    const validTypes = ['application/pdf', 'text/markdown', 'text/plain'];
    const validExtensions = ['.pdf', '.md'];
    const fileExtension = file.name.substring(file.name.lastIndexOf('.')).toLowerCase();

    if (!validExtensions.includes(fileExtension)) {
        showError('Please upload a PDF or Markdown (.md) file');
        return;
    }

    // Show progress section
    document.getElementById('uploadSection').style.display = 'none';
    document.getElementById('progressSection').style.display = 'block';
    document.getElementById('errorSection').style.display = 'none';

    // Create form data
    const formData = new FormData();
    formData.append('file', file);

    try {
        // Upload file
        updateProgress(0, 'Uploading file...');
        const response = await fetch(`${API_BASE}/api/upload`, {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Upload failed');
        }

        const data = await response.json();
        currentJobId = data.job_id;

        // Start polling for progress
        pollJobStatus();

    } catch (error) {
        showError(`Upload failed: ${error.message}`);
    }
}

// Poll job status
async function pollJobStatus() {
    if (!currentJobId) return;

    try {
        const response = await fetch(`${API_BASE}/api/jobs/${currentJobId}`);
        if (!response.ok) throw new Error('Failed to get job status');

        const job = await response.json();

        // Update progress
        updateProgress(job.progress, job.status);

        if (job.status === 'completed') {
            // Load facts and show results
            await loadFacts();
        } else if (job.status === 'failed') {
            showError(`Processing failed: ${job.error_message || 'Unknown error'}`);
        } else {
            // Continue polling
            setTimeout(pollJobStatus, 1000);
        }

    } catch (error) {
        showError(`Error checking status: ${error.message}`);
    }
}

// Update progress bar
function updateProgress(percent, text) {
    document.getElementById('progressFill').style.width = `${percent}%`;
    document.getElementById('progressText').textContent = text;
}

// Load facts from API
async function loadFacts() {
    try {
        const response = await fetch(`${API_BASE}/api/jobs/${currentJobId}/facts`);
        if (!response.ok) throw new Error('Failed to load facts');

        allFacts = await response.json();

        // Show results section
        document.getElementById('progressSection').style.display = 'none';
        document.getElementById('resultsSection').style.display = 'block';

        // Update stats
        const conflicts = allFacts.filter(f => f.has_conflict).length;
        document.getElementById('statsText').textContent =
            `${allFacts.length} facts extracted • ${conflicts} conflicts detected`;

        // Display facts
        displayFacts(allFacts);

    } catch (error) {
        showError(`Error loading facts: ${error.message}`);
    }
}

// Display facts in table
function displayFacts(facts) {
    const tbody = document.getElementById('factsTableBody');
    tbody.innerHTML = '';

    if (facts.length === 0) {
        tbody.innerHTML = '<tr><td colspan="8" style="text-align: center; padding: 40px;">No facts found</td></tr>';
        return;
    }

    facts.forEach(fact => {
        const row = document.createElement('tr');

        // Highlight edited rows
        if (fact.user_edited) {
            row.style.background = '#e7f3ff';
        }

        row.innerHTML = `
            <td>
                ${escapeHtml(fact.name)}
                ${fact.user_edited ? '<span class="edited-badge">Edited</span>' : ''}
            </td>
            <td>${fact.value_normalized !== null ? fact.value_normalized.toFixed(2) : 'N/A'}</td>
            <td>${escapeHtml(fact.unit_normalized || '')}</td>
            <td>${fact.page || 'N/A'}</td>
            <td>${fact.occurrence_count || 1}</td>
            <td>
                <span class="conflict-badge ${fact.has_conflict ? 'conflict-yes' : 'conflict-no'}">
                    ${fact.has_conflict ? '⚠️ Yes' : '✓ No'}
                </span>
            </td>
            <td>
                <div style="max-width: 300px; overflow: hidden; text-overflow: ellipsis;">
                    ${fact.has_conflict ?
                        `<strong>Conflict:</strong> ${escapeHtml(fact.conflict_description || '')}<br>` :
                        ''}
                    ${fact.user_comment ?
                        `<strong>Comment:</strong> ${escapeHtml(fact.user_comment)}<br>` :
                        ''}
                    ${fact.evidence ?
                        `<em>${escapeHtml(fact.evidence.substring(0, 100))}...</em>` :
                        ''}
                </div>
            </td>
            <td>
                <button class="btn btn-edit" onclick="editFact(${fact.id})">✏️ Edit</button>
                <button class="btn btn-danger" onclick="deleteFact(${fact.id})">🗑️</button>
            </td>
        `;

        tbody.appendChild(row);
    });
}

// Filter facts
function filterFacts() {
    const searchTerm = document.getElementById('searchInput').value.toLowerCase();
    const conflictsOnly = document.getElementById('conflictsOnly').checked;

    let filtered = allFacts;

    // Filter by search term
    if (searchTerm) {
        filtered = filtered.filter(fact =>
            fact.name.toLowerCase().includes(searchTerm) ||
            (fact.evidence && fact.evidence.toLowerCase().includes(searchTerm)) ||
            (fact.unit_normalized && fact.unit_normalized.toLowerCase().includes(searchTerm))
        );
    }

    // Filter by conflicts
    if (conflictsOnly) {
        filtered = filtered.filter(fact => fact.has_conflict);
    }

    displayFacts(filtered);
}

// Edit fact
function editFact(factId) {
    const fact = allFacts.find(f => f.id === factId);
    if (!fact) return;

    currentEditingFactId = factId;

    // Populate modal
    document.getElementById('editName').value = fact.name;
    document.getElementById('editValue').value = fact.value_normalized || '';
    document.getElementById('editUnit').value = fact.unit_normalized || '';
    document.getElementById('editComment').value = fact.user_comment || '';

    // Show modal
    document.getElementById('editModal').style.display = 'flex';
}

// Close edit modal
function closeEditModal() {
    document.getElementById('editModal').style.display = 'none';
    currentEditingFactId = null;
}

// Save fact
async function saveFact() {
    if (!currentEditingFactId) return;

    const value = parseFloat(document.getElementById('editValue').value);
    const unit = document.getElementById('editUnit').value;
    const comment = document.getElementById('editComment').value;

    try {
        const response = await fetch(`${API_BASE}/api/facts/${currentEditingFactId}`, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                value_normalized: value,
                unit_normalized: unit,
                user_comment: comment,
                user_edited: true
            })
        });

        if (!response.ok) throw new Error('Failed to update fact');

        // Update local data
        const updatedFact = await response.json();
        const index = allFacts.findIndex(f => f.id === currentEditingFactId);
        if (index !== -1) {
            allFacts[index] = updatedFact;
            displayFacts(allFacts);
        }

        closeEditModal();

    } catch (error) {
        alert(`Error saving fact: ${error.message}`);
    }
}

// Delete fact
async function deleteFact(factId) {
    if (!confirm('Are you sure you want to delete this fact?')) return;

    try {
        const response = await fetch(`${API_BASE}/api/facts/${factId}`, {
            method: 'DELETE'
        });

        if (!response.ok) throw new Error('Failed to delete fact');

        // Remove from local data
        allFacts = allFacts.filter(f => f.id !== factId);
        displayFacts(allFacts);

        // Update stats
        const conflicts = allFacts.filter(f => f.has_conflict).length;
        document.getElementById('statsText').textContent =
            `${allFacts.length} facts extracted • ${conflicts} conflicts detected`;

    } catch (error) {
        alert(`Error deleting fact: ${error.message}`);
    }
}

// Export to CSV
function exportCSV() {
    if (!currentJobId) return;
    window.location.href = `${API_BASE}/api/jobs/${currentJobId}/export/csv`;
}

// Reset app
function resetApp() {
    currentJobId = null;
    allFacts = [];
    document.getElementById('uploadSection').style.display = 'block';
    document.getElementById('progressSection').style.display = 'none';
    document.getElementById('resultsSection').style.display = 'none';
    document.getElementById('errorSection').style.display = 'none';
    document.getElementById('fileInput').value = '';
}

// Show error
function showError(message) {
    document.getElementById('uploadSection').style.display = 'none';
    document.getElementById('progressSection').style.display = 'none';
    document.getElementById('resultsSection').style.display = 'none';
    document.getElementById('errorSection').style.display = 'block';
    document.getElementById('errorText').textContent = message;
}

// Escape HTML
function escapeHtml(text) {
    if (!text) return '';
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Close modal on outside click
window.onclick = function(event) {
    const modal = document.getElementById('editModal');
    if (event.target === modal) {
        closeEditModal();
    }
}
