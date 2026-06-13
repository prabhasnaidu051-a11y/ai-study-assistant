const API_URL = "http://127.0.0.1:8000";


// =====================================
// AI CHAT
// =====================================
async function askAI() {

    const provider =
        document.getElementById("provider").value;

    const apiKey =
        document.getElementById("apiKey").value;

    const prompt =
        document.getElementById("prompt").value;

    if (!prompt.trim()) {
        alert("Enter a question.");
        return;
    }

    document.getElementById("response").innerHTML =
        "Thinking...";

    try {

        const response = await fetch(
            `${API_URL}/chat`,
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    provider: provider,
                    api_key: apiKey,
                    prompt: prompt
                })
            }
        );

        const data =
            await response.json();

        document.getElementById("response").innerHTML =
            `<p>${data.response}</p>`;

    } catch (error) {

        document.getElementById("response").innerHTML =
            `Error: ${error.message}`;
    }
}


// =====================================
// PDF UPLOAD
// =====================================
async function uploadPDF() {

    const file =
        document.getElementById("pdfFile").files[0];

    if (!file) {
        alert("Please select a PDF file.");
        return;
    }

    document.getElementById("uploadResult").innerHTML =
        "Uploading and indexing PDF...";

    const formData =
        new FormData();

    formData.append(
        "file",
        file
    );

    try {

        const response = await fetch(
            `${API_URL}/upload-pdf`,
            {
                method: "POST",
                body: formData
            }
        );

        const data =
            await response.json();

        document.getElementById("uploadResult").innerHTML =
            `<strong>${data.message}</strong>`;

    } catch (error) {

        document.getElementById("uploadResult").innerHTML =
            `Upload Failed: ${error.message}`;
    }
}
// =====================================
// ASK DOCUMENT
// =====================================
async function askDocument() {

    const question =
        document.getElementById(
            "documentQuestion"
        ).value;

    if (!question.trim()) {
        alert("Enter a question.");
        return;
    }

    document.getElementById(
        "documentResponse"
    ).innerHTML = "Searching document...";

    try {

        const response = await fetch(
            `${API_URL}/ask-document`,
            {
                method: "POST",
                headers: {
                    "Content-Type":
                    "application/json"
                },
                body: JSON.stringify({
                    question: question
                })
            }
        );

        const data =
            await response.json();

        document.getElementById(
            "documentResponse"
        ).innerHTML = `
            <h3>Answer</h3>
            <p>${data.answer}</p>
        `;

    } catch (error) {

        document.getElementById(
            "documentResponse"
        ).innerHTML =
            `Error: ${error.message}`;
    }
}


// =====================================
// GENERATE QUIZ
// =====================================
async function generateQuiz() {

    document.getElementById(
        "quizResult"
    ).innerHTML = "Generating quiz...";

    try {

        const response = await fetch(
            `${API_URL}/generate-quiz`,
            {
                method: "POST",
                headers: {
                    "Content-Type":
                    "application/json"
                },
                body: JSON.stringify({
                    topic: "document"
                })
            }
        );

        const data =
            await response.json();

        document.getElementById(
            "quizResult"
        ).innerHTML = `
            <h3>Quiz</h3>
            <div style="white-space: pre-wrap; line-height: 1.8;">
                ${data.quiz}
            </div>
        `;

    } catch (error) {

        document.getElementById(
            "quizResult"
        ).innerHTML =
            `Error: ${error.message}`;
    }
}