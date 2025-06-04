
# 🌐 **Custom Python Web Server** 

A custom Python web server that supports HTTP, HTTPS, and multiple request types (GET, POST, HEAD, and others). It also includes a PHP integration for testing input parameters and serves HTML pages with appropriate headers, all built from scratch without using external parsing libraries. This project is Dockerized for easy deployment and scalability.

---

## 🚀 Features

- **HTTP & HTTPS Support**: Handles HTTP and HTTPS requests.
- **Multiple Request Types**: Supports GET, POST, HEAD, and other HTTP methods.
- **PHP Integration**: Supports PHP script execution and input parameter testing.
- **Custom Header Handling**: All HTTP headers are custom-programmed.
- **Dockerized**: Easy to deploy via Docker.

---

## 📥 Installation

### Clone the repository:

```bash
git clone https://github.com/tanishqborse/PythonWebServer.git
cd PythonWebServer
```

### Build the Docker image:

```bash
docker build -t python-web-server .
```

This will build the Docker image with the tag `python-web-server`.

---

## ⚡ Usage

### Run the Docker container:

```bash
docker run -d -p 80:80 -p 443:443 python-web-server
```

This will start the Python web server inside a Docker container, mapping port 80 (HTTP) and port 443 (HTTPS) on your local machine to the corresponding ports in the container.

### Access the server:

- For HTTP: Open a web browser and navigate to `http://localhost`.
- For HTTPS: Use `https://localhost` (note: this may show a security warning due to self-signed certificates).

---

## 🔧 Customization

- **PHP Integration**: Place PHP scripts in the `php` directory to execute server-side logic.
- **Static Content**: Place HTML, CSS, JavaScript, and other static files in the `static` directory to serve them via the web server. If the directory does not exist, create it with `mkdir static`.
- **Server Configuration**: Modify `server.py` to customize server behavior, add new endpoints, or handle additional request types.

---

## 📜 License

This project is licensed under the MIT License. See the LICENSE file for more details.

---

## 🤝 Contributing

🚀 Contributions are welcome! If you have ideas to improve the server or additional features to add, feel free to contribute.

To contribute:
1. Fork the repository.
2. Create a new branch.
3. Implement your changes.
4. Submit a pull request.

---

👨‍💻 Developed with ❤️ by Tanishq Borse

If you found this project useful, give it a ⭐ and feel free to reach out for any questions or feedback!
