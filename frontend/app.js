const API = "http://127.0.0.1:8000";

console.log("APP JS LOADED");


// ASK AI

async function askAI(){

    const prompt = document.getElementById("prompt").value;

    const response = await fetch(
        `${API}/chat`, // nosemgrep: typescript.react.security.react-insecure-request
        {
            method:"POST",

            headers:{
                "Content-Type":"application/json"
            },

            body:JSON.stringify({

                provider:"Ollama",

                prompt:prompt

            })

        }
    );


    const data = await response.json();


    document.getElementById("response").innerHTML =
    data.response;

}




// UPLOAD PDF

window.onload = function(){

    const button = document.getElementById("uploadBtn");


    button.onclick = async function(e){

        e.preventDefault();

        e.stopPropagation();


        console.log("UPLOAD BUTTON CLICKED");


        const file =
        document.getElementById("pdfFile").files[0];


        if(!file){

            alert("Select a PDF first");

            return;

        }


        console.log("Selected:", file.name);


        const formData = new FormData();


        formData.append(
            "file",
            file
        );



        try{


            const response = await fetch(
                `${API}/upload-pdf`, // nosemgrep: typescript.react.security.react-insecure-request
                {

                    method:"POST",

                    body:formData

                }
            );



            const data = await response.json();



            console.log(data);



            document.getElementById("uploadResult").innerHTML =

            "✅ " + data.message;



        }

        catch(error){


            console.log(error);


            document.getElementById("uploadResult").innerHTML =

            "❌ Upload failed";


        }


    };


};






// ASK DOCUMENT

async function askDocument(){


    const question =
    document.getElementById("documentQuestion").value;



    const response = await fetch(
        `${API}/ask-document`, // nosemgrep: typescript.react.security.react-insecure-request
        {

            method:"POST",

            headers:{

                "Content-Type":"application/json"

            },


            body:JSON.stringify({

                question:question

            })

        }
    );



    const data = await response.json();



    document.getElementById("documentResponse").innerHTML =

    data.answer;


}







// QUIZ

async function generateQuiz(){


    const topic =
    document.getElementById("quizTopic").value;



    const response = await fetch(
        `${API}/generate-quiz`, // nosemgrep: typescript.react.security.react-insecure-request
        {

            method:"POST",

            headers:{

                "Content-Type":"application/json"

            },


            body:JSON.stringify({

                topic:topic

            })

        }
    );



    const data = await response.json();



    document.getElementById("quizResult").innerHTML =

    data.quiz;


}
