// static/script.js
// Handles authentication and CRUD operations with the API.

const API_BASE = '';  // same origin, no prefix needed

// Store token in localStorage
let token = localStorage.getItem('token') || '';

// On page load, check if token exists and show items if valid
document.addEventListener('DOMContentLoaded', () => {
    if (token) {
        showItemsSection();
        fetchItems();
    }
});

// ----------------------------
// Helper: add Authorization header
// ----------------------------
function authHeaders() {
    return {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
    };
}

// ----------------------------
// UI toggles
// ----------------------------
function showItemsSection() {
    document.getElementById('auth-section').classList.add('hidden');
    document.getElementById('items-section').classList.remove('hidden');
}

function showAuthSection() {
    document.getElementById('auth-section').classList.remove('hidden');
    document.getElementById('items-section').classList.add('hidden');
}

// ----------------------------
// Authentication functions
// ----------------------------
async function login() {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    // FastAPI's OAuth2PasswordRequestForm expects form data
    const formData = new FormData();
    formData.append('username', username);
    formData.append('password', password);

    const response = await fetch(`${API_BASE}/login`, {
        method: 'POST',
        body: formData
    });

    if (response.ok) {
        const data = await response.json();
        token = data.access_token;
        localStorage.setItem('token', token);
        showItemsSection();
        fetchItems();
    } else {
        alert('Login failed');
    }
}

async function register() {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    const response = await fetch(`${API_BASE}/register`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
    });

    if (response.ok) {
        alert('Registration successful! Please login.');
    } else {
        alert('Registration failed');
    }
}

function logout() {
    token = '';
    localStorage.removeItem('token');
    showAuthSection();
    document.getElementById('username').value = '';
    document.getElementById('password').value = '';
    document.getElementById('items-list').innerHTML = '';
}

// ----------------------------
// CRUD functions for items
// ----------------------------
async function fetchItems() {
    const response = await fetch(`${API_BASE}/items/`, {
        headers: authHeaders()
    });
    if (response.status === 401) {
        // Token expired or invalid
        logout();
        return;
    }
    const items = await response.json();
    const list = document.getElementById('items-list');
    list.innerHTML = '';
    items.forEach(item => {
        const li = document.createElement('li');
        li.textContent = `${item.name} - $${item.price} (${item.description || ''})`;
        const deleteBtn = document.createElement('button');
        deleteBtn.textContent = 'Delete';
        deleteBtn.onclick = () => deleteItem(item.id);
        li.appendChild(deleteBtn);
        list.appendChild(li);
    });
}

document.getElementById('create-item-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const name = document.getElementById('item-name').value;
    const description = document.getElementById('item-description').value;
    const price = parseFloat(document.getElementById('item-price').value);

    const response = await fetch(`${API_BASE}/items/`, {
        method: 'POST',
        headers: authHeaders(),
        body: JSON.stringify({ name, description, price })
    });

    if (response.ok) {
        // Clear form and refresh list
        document.getElementById('item-name').value = '';
        document.getElementById('item-description').value = '';
        document.getElementById('item-price').value = '';
        fetchItems();
    } else {
        alert('Failed to create item');
    }
});

async function deleteItem(id) {
    const response = await fetch(`${API_BASE}/items/${id}`, {
        method: 'DELETE',
        headers: authHeaders()
    });
    if (response.ok) {
        fetchItems();
    } else {
        alert('Failed to delete item');
    }
}