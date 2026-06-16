const API = "http://127.0.0.1:8000";

// Ask AI
async function askAI() {

    const prompt =
        document.getElementById("prompt").value;


    const response = await fetch(
        `${API}/chat`,
        {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                provider: "Ollama",
                prompt: prompt
            })
        }
    );


    const data = await response.json();


    document.getElementById("response").innerHTML =
        JSON.stringify(data, null, 2);
}

// Upload PDF
async function uploadPDF() {

    const file =
        document.getElementById("pdfFile").files[0];

    if (!file) {
        alert("Select a PDF first");
        return;
    }

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

    document.getElementById("uploadResult").innerHTML =
        "✅ PDF uploaded successfully";
}


// Ask Uploaded Document
async function askDocument() {

    const question =
        document.getElementById("documentQuestion").value;

    const response = await fetch(
        `${API}/ask-document`,
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                question: question
            })
        }
    );

    const data = await response.json();

    document.getElementById("documentResponse").innerHTML =
        data.answer;
}


// Generate Quiz
async function generateQuiz() {

    const topic =
        document.getElementById("quizTopic").value;

    const response = await fetch(
        `${API}/generate-quiz`,
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                topic: topic
            })
        }
    );

    const data = await response.json();

    document.getElementById("quizResult").innerHTML =
        data.quiz;
}