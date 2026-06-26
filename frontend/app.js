const API = "https://ai-study-assistant-ox51.onrender.com";

console.log("APP JS LOADED");


// -----------------------------
// ASK AI
// -----------------------------

async function askAI(){

    const prompt =
    document.getElementById("prompt").value;


    try {

        const response = await fetch(
            `${API}/chat`,
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
        data.response || "No response";


    }

    catch(error){

        console.log(error);

        document.getElementById("response").innerHTML =
        "❌ AI request failed";

    }

}




// -----------------------------
// UPLOAD PDF
// -----------------------------

window.onload = function(){


    const button =
    document.getElementById("uploadBtn");


    if(button){


        button.onclick = async function(e){


            e.preventDefault();


            const file =
            document.getElementById("pdfFile").files[0];



            if(!file){

                alert("Select a PDF first");

                return;

            }



            const formData =
            new FormData();


            formData.append(
                "file",
                file
            );



            try{


                const response = await fetch(
                    `${API}/upload-pdf`,
                    {

                        method:"POST",

                        body:formData

                    }
                );



                const data =
                await response.json();



                console.log(
                    "UPLOAD:",
                    data
                );



                document.getElementById("uploadResult").innerHTML =

                "✅ " + data.message;



            }


            catch(error){


                console.log(error);


                document.getElementById("uploadResult").innerHTML =

                "❌ Upload failed";


            }


        };


    }


};





// -----------------------------
// ASK DOCUMENT
// -----------------------------

async function askDocument(){


    const question =
    document.getElementById("documentQuestion").value;



    try{


        const response = await fetch(

            `${API}/ask-document`,

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



        const data =
        await response.json();



        console.log(
            "ANSWER:",
            data
        );



        document.getElementById("documentResponse").innerHTML =

        data.answer || "No answer found";



    }


    catch(error){


        console.log(error);


        document.getElementById("documentResponse").innerHTML =

        "❌ Question failed";


    }


}





// -----------------------------
// GENERATE QUIZ
// -----------------------------

async function generateQuiz(){


    const topic =
    document.getElementById("quizTopic").value;



    try{


        const response = await fetch(

            `${API}/generate-quiz`,

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



        const data =
        await response.json();



        document.getElementById("quizResult").textContent =

        data.quiz || "No quiz generated";


    }


    catch(error){


        console.log(error);


        document.getElementById("quizResult").textContent =

        "❌ Quiz failed";


    }


}