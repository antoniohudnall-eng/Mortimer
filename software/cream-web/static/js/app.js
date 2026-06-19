// CREAM App JavaScript

const API_BASE = '/api';
let currentPage = 'dashboard';

// Toast notification
function showToast(message, type = '') {
    const toast = document.getElementById('toast');
    toast.textContent = message;
    toast.className = 'toast ' + type;
    toast.classList.add('show');
    
    setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
}

// Toggle sidebar
function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    sidebar.classList.toggle('open');
}

// Show page
function showPage(page) {
    // Hide all pages
    document.querySelectorAll('.page').forEach(p => {
        p.classList.remove('active');
    });
    
    // Show selected page
    const pageEl = document.getElementById(`page-${page}`);
    if (pageEl) {
        pageEl.classList.add('active');
    }
    
    // Update nav items
    document.querySelectorAll('.nav-item').forEach(item => {
        item.classList.remove('active');
    });
    event?.target?.classList.add('active');
    
    // Update page title
    const titles = {
        dashboard: 'Dashboard',
        plan: 'Plan Business',
        leads: 'Leads',
        appointments: 'Appointments',
        farming: 'Community Farming',
        revenue: 'Revenue',
        transactions: 'Transactions',
        letters: 'Letter Generator',
        premium: 'Premium Tools'
    };
    document.querySelector('.page-title').textContent = titles[page] || page;
    
    // Close sidebar on mobile
    document.getElementById('sidebar').classList.remove('open');
    
    // Load page data
    if (page === 'dashboard') {
        loadDashboard();
    } else if (page === 'leads') {
        loadLeads();
    }
}

// Load dashboard data
async function loadDashboard() {
    try {
        const response = await fetch(`${API_BASE}/dashboard`);
        if (!response.ok) throw new Error('Failed to load');
        
        const data = await response.json();
        
        // Update stats
        document.getElementById('stat-leads').textContent = data.leads;
        document.getElementById('stat-appointments').textContent = data.appointments;
        document.getElementById('stat-revenue').textContent = '$' + data.revenue.toLocaleString();
        document.getElementById('stat-conversion').textContent = data.conversion_rate + '%';
        document.getElementById('task-count').textContent = data.tasks.length;
        
        // Update tasks
        const taskList = document.getElementById('task-list');
        if (data.tasks.length === 0) {
            taskList.innerHTML = '<div class="card"><p class="card-meta">No tasks for today!</p></div>';
        } else {
            taskList.innerHTML = data.tasks.map(task => `
                <div class="card">
                    <div class="card-title">${task}</div>
                    <div class="card-meta">Tap to complete</div>
                </div>
            `).join('');
        }
    } catch (err) {
        console.error('Failed to load dashboard:', err);
    }
}

// Load leads
async function loadLeads() {
    const container = document.getElementById('leads-list');
    container.innerHTML = '<div class="loading">Loading leads...</div>';
    
    try {
        const response = await fetch(`${API_BASE}/leads`);
        if (!response.ok) throw new Error('Failed to load');
        
        const data = await response.json();
        
        if (data.leads.length === 0) {
            container.innerHTML = `
                <div class="coming-soon">
                    <div class="coming-soon-icon">📭</div>
                    <h2>No leads yet</h2>
                    <p>Add your first lead to get started</p>
                </div>
            `;
        } else {
            container.innerHTML = data.leads.map(lead => `
                <div class="card">
                    <div class="card-title">${lead.name}</div>
                    <div class="card-meta">
                        ${lead.city || 'Unknown location'} • 
                        <span class="badge badge-${lead.temperature || 'cold'}">${lead.temperature || 'cold'}</span>
                        ${lead.ai_score ? `• AI Score: ${lead.ai_score}` : ''}
                    </div>
                </div>
            `).join('');
        }
    } catch (err) {
        container.innerHTML = '<div class="loading">Failed to load leads</div>';
    }
}

// Quick actions
function quickAddLead() {
    showPage('leads');
    setTimeout(() => showAddLead(), 100);
}

function quickSchedule() {
    showPage('appointments');
    showToast('Schedule appointment coming soon', 'success');
}

function quickLetter() {
    showPage('letters');
}

function quickRevenue() {
    showPage('revenue');
}

function addTask() {
    showToast('Add task coming soon', 'success');
}

function showNotifications() {
    showToast('No new notifications', 'success');
}

function showSettings() {
    showToast('Settings coming soon', 'success');
}

// Add lead modal
function showAddLead() {
    document.getElementById('add-lead-modal').style.display = 'flex';
}

function closeAddLead() {
    document.getElementById('add-lead-modal').style.display = 'none';
}

async function submitLead(event) {
    event.preventDefault();
    const form = event.target;
    const btn = form.querySelector('.btn-primary');
    
    btn.disabled = true;
    btn.textContent = 'Saving...';
    
    const data = Object.fromEntries(new FormData(form));
    
    try {
        const response = await fetch(`${API_BASE}/leads`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        
        if (response.ok) {
            showToast('Lead added successfully!', 'success');
            closeAddLead();
            form.reset();
            loadLeads();
            loadDashboard(); // Refresh stats
        } else {
            const error = await response.json();
            showToast(error.detail || 'Failed to add lead', 'error');
        }
    } catch (err) {
        showToast('Network error', 'error');
    } finally {
        btn.disabled = false;
        btn.textContent = 'Save Lead';
    }
}

// Logout
async function logout() {
    try {
        await fetch(`${API_BASE}/auth/logout`, { method: 'POST' });
        window.location.href = '/';
    } catch (err) {
        window.location.href = '/';
    }
}

// Initialize
async function init() {
    // Load dashboard on startup
    await loadDashboard();
}

document.addEventListener('DOMContentLoaded', init);
