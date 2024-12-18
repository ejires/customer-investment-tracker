document.addEventListener("DOMContentLoaded", () => {
    const loginSection = document.getElementById('login-section');
    const customerSection = document.getElementById('customer-list-section');
    const loginForm = document.getElementById('login-form');
    const loginUsername = document.getElementById('login-username');
    const loginPassword = document.getElementById('login-password');
    const responseMessage = document.getElementById('responseMessage');
    const searchButton = document.getElementById('search-button');
    const searchInput = document.getElementById('search-input');
    const customerList = document.getElementById('customer-list'); // Table where customers will be displayed

    // Check Token on Page Load
    if (localStorage.getItem('token')) {
        loginSection.style.display = 'none';
        customerSection.style.display = 'block';
    } else {
        loginSection.style.display = 'block';
        customerSection.style.display = 'none';
    }

    // Handle Login Form Submission
    loginForm.addEventListener('submit', async (event) => {
        event.preventDefault();

        const username = loginUsername.value;
        const password = loginPassword.value;

        try {
            const response = await fetch('http://127.0.0.1:5000/auth/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, password })
            });

            const result = await response.json();

            if (response.ok) {
                // Save token to localStorage
                localStorage.setItem('token', result.access_token);

                // Update UI
                loginSection.style.display = 'none';
                customerSection.style.display = 'block';
                responseMessage.innerText = "Login successful!";
            } else {
                // Show error message
                responseMessage.innerText = result.msg;
            }
        } catch (error) {
            responseMessage.innerText = "An error occurred. Please try again.";
        }
    });

    // Search customers when search button is clicked
    searchButton.addEventListener('click', async () => {
        const query = searchInput.value.trim();
        if (!query) {
            alert('Please enter a search query.');
            return;
        }

        try {
            const response = await fetch(`http://127.0.0.1:5000/customers/search?q=${encodeURIComponent(query)}`);
            if (!response.ok) {
                throw new Error('Failed to search customers');
            }

            const customers = await response.json();
            displaySearchResults(customers);
        } catch (error) {
            console.error('Error during search:', error);
            alert('Failed to search customers.');
        }
    });

    // Display search results in the table
    function displaySearchResults(customers) {
        customerList.innerHTML = ''; // Clear existing customer rows

        if (customers.length === 0) {
            customerList.innerHTML = '<tr><td colspan="5">No customers found.</td></tr>';
            return;
        }

        customers.forEach((customer) => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${customer.id}</td>
                <td>${customer.name}</td>
                <td>${customer.email}</td>
                <td>${customer.phone}</td>
                <td></td> <!-- Placeholder for future actions -->
            `;
            customerList.appendChild(row);
        });
    }
});

