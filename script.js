document
	.getElementById('registerForm')
	.addEventListener('submit', function (e) {
		e.preventDefault();
		const email = document.getElementById('email').value.trim();
		const password = document.getElementById('password').value;
		const errorDiv = document.getElementById('error-message');
		let error = '';

		// Check if email and password are provided
		const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
		if (!emailRegex.test(email)) {
			error = 'Invalid email format.';
		} else if (password.length < 6) {
			error = 'Password must be at least 6 characters long.';
		}

		if (error) {
			errorDiv.textContent = error;
			errorDiv.style.display = 'block';
		} else {
			errorDiv.style.display = 'none';
			fetch('http://localhost:8000/register', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
				},
				body: JSON.stringify({ email, password }),
			})
				.then((response) => response.json())
				.then((data) => {
					errorDiv.textContent = data.message || 'No response data.';
					errorDiv.style.display = 'block';
				})
				.catch((err) => {
                    console.error('Error:', err);
					errorDiv.textContent = 'Connection error occurred.';
					errorDiv.style.display = 'block';
				});
		}
	});
