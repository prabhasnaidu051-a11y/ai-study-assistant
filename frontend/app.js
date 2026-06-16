const API = "http://127.0.0.1:8000";

async function sendChat() {

    const question =
        document.getElementById("question").value;

    const response = await fetch(
        `${API}/chat`,
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                message: question
            })
        }
    );

    const data = await response.json();

    document.getElementById("response").innerHTML =
        data.response;
}

async function uploadPDF() {

    const file =
        document.getElementById("pdfFile").files[0];

    const formData = new FormData();

    formData.append("file", file);

    const response = await fetch(
        `${API}/upload-pdf`,
        {
            method: "POST",
            body: formData
        }
    );

    const data = await response.json();

    alert(data.message);
}