async function uploadfile() {
    const fileInput = document.getElementById('file-upload1');
    const file = fileInput.files[0];

    if (!file) {
        document.getElementById('uploadfile_result').textContent = 'Please select a file first.';
        return;
    }

    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch('http://127.0.0.1:5000/api/upload', {
        method: 'POST',
        body: formData
    });

    data = await response.text()
    let str = data.replace(/['"]/g, '');
    let cleanStr = str.trim()

    if (response.ok) {
        document.getElementById('uploadfile_result').textContent = cleanStr;
        } else {
        document.getElementById('uploadfile_result').textContent = Error + cleanStr;
        }
    }
