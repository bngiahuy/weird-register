document
	.getElementById('registerForm')
	.addEventListener('submit', function (e) {
		e.preventDefault();
		const email = document.getElementById('email').value.trim();
		const password = document.getElementById('password').value;
		const errorDiv = document.getElementById('error-message');
		let error = '';

		// Kiểm tra định dạng email
		const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
		if (!emailRegex.test(email)) {
			error = 'Email không hợp lệ.';
		} else if (password.length < 6) {
			error = 'Mật khẩu phải có ít nhất 6 ký tự.';
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
					errorDiv.textContent = data.message || 'Không có dữ liệu trả về.';
					errorDiv.style.display = 'block';
				})
				.catch((err) => {
                    console.error('Error:', err);
					errorDiv.textContent = 'Đã xảy ra lỗi kết nối.';
					errorDiv.style.display = 'block';
				});
		}
	});
