const API_BASE_URL = "http://127.0.0.1:8000/api"; // Replace with your backend URL

let token = ""; // Token for authenticated requests

// Handle Registration
document.getElementById("register-form").addEventListener("submit", async (e) => {
    e.preventDefault();
    const username = document.getElementById("register-username").value;
    const email = document.getElementById("register-email").value;
    const password = document.getElementById("register-password").value;

    const response = await fetch(`${API_BASE_URL}/register/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ username, email, password }),
    });

    const data = await response.json();
    alert(data.token ? "Registration Successful!" : JSON.stringify(data));
});

// Handle Login
document.getElementById("login-form").addEventListener("submit", async (e) => {
    e.preventDefault();
    const username = document.getElementById("login-username").value;
    const password = document.getElementById("login-password").value;

    const response = await fetch(`${API_BASE_URL}/login/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ username, password }),
    });

    const data = await response.json();
    if (data.token) {
        token = data.token;
        alert("Login Successful!");
    } else {
        alert("Login Failed: " + JSON.stringify(data));
    }
});

// Handle Get Preferences
document.getElementById("get-preferences").addEventListener("click", async () => {
    if (!token) {
        alert("Please log in first!");
        return;
    }

    const response = await fetch(`${API_BASE_URL}/preferences/`, {
        method: "GET",
        headers: {
            "Authorization": `Bearer ${token}`,
        },
    });

    const data = await response.json();
    const preferencesResponse = document.getElementById("preferences-response");
    if (response.ok) {
        preferencesResponse.innerText = JSON.stringify(data, null, 2);
    } else {
        preferencesResponse.innerText = `Error: ${JSON.stringify(data)}`;
    }
});
