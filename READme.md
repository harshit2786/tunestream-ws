### Installation

To get started with the project, follow these steps:

1. Clone the repository:

```bash
git clone <repository_url>
cd project-directory
```

2. Create a virtual environment and activate it:

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

Install the dependencies:
```bash
pip install fastapi uvicorn
```

### Getting Started

To run the development server, use the following command:

```bash
uvicorn main:app --reload
```

This will start the server on http://localhost:8000.