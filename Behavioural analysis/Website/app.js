const audioNumber = document.querySelector(".audio-number")
const audioFile = document.querySelector(".audio-files")
const melodyFile = document.querySelector(".melody-file")
const originalAudio=document.querySelector(".original-audio")
const ratingContainer = document.querySelector(".rating-container")
const homeBox = document.querySelector(".home-box")
const analysisBox = document.querySelector(".analysis-box")
const submissionBox = document.querySelector(".submission-box")
let audioCounter = 0
let currentAudio;
let availableAudios =[]
let dataDictionary =[]

const startButton = document.getElementById("start")


// console.log(getName)

// let url = "https://dissertationanalysis-default-rtdb.firebaseio.com/" +getName+'.json'
// let xhr = new XMLHttpRequest()
// xhr.open("POST",url)
// let iterationsAudios=[]

function setAvailableAudios(){
    const totalAudio = audioFiles.length
    for(let i=0;i<totalAudio; i++){
        availableAudios.push(audioFiles[i])
    }
    // console.log(availableAudios)


}

// Gets the audio 
function getNewAudio(){
    // document.getElementById('myrating').value=""
    audioNumber.innerHTML="Audio "+ (audioCounter+1)+" of "+audioFiles.length

    const audioIndex = availableAudios[Math.floor(Math.random()*availableAudios.length)]

    currentAudio = audioIndex.audios
    var keys = Object.keys(currentAudio)
    shuffleIterations = currentAudio[keys[ keys.length * Math.random() << 0]]
    console.log(shuffleIterations)
    // iterations = currentAudio.iterations

    // shuffleIterations = iterations[Math.floor(Math.random()*iterations.length)]
    document.getElementById('audio').src =shuffleIterations.audio 
    document.getElementById('melody').src =shuffleIterations.iteration
    // console.log(iterations.audio )
    // console.log(iterations.iteration)

    const index1 = availableAudios.indexOf(audioIndex)
    availableAudios.splice(index1,1)

    audioName = getAudioName(shuffleIterations.audio )
    console.log(audioName)
    iterationName = getAudioName(shuffleIterations.iteration)
    console.log(iterationName)

    ratingName = audioName + " rating for: " + iterationName
    audioCounter++

}




function getAudioName(audioName){
    var removePath= audioName.replace('static/music/','')
    var theAudioName =removePath.substring(0, removePath.lastIndexOf('.')) || removePath;
    // var f = theAudioName.substring(0, theAudioName.lastIndexOf('.')) 
    return theAudioName    

}
// The next page
function next(){
    console.log(validateScore())
    if(audioCounter==audioFiles.length){
        console.log("Finished analysis")
        const getRating = document.getElementById('myrating').value
        // console.log(document.getElementById('myrating').value)
        const getName = document.getElementById("myname").value
        // console.log(getName)

        dataDictionary.push({
            'Name':getName,
            'OriginalAudio':audioName,
            'iteration':iterationName,
            'Rating':getRating 
        });
        analysisOver()
    }else{
        const getRating = document.getElementById('myrating').value
        // console.log(document.getElementById('myrating').value)
        const getName = document.getElementById("myname").value
        // console.log(getName)

        dataDictionary.push({
            'Name':getName,
            'OriginalAudio':audioName,
            'iteration':iterationName,
            'Rating':getRating 
        });
        
        document.getElementById('myrating').value=""
        getNewAudio()
    }
}

// Once the analysis is over, the results are submitted to  firebase
function analysisOver(){
    const getName = document.getElementById("myname").value

    let url = "https://analysis-280bb-default-rtdb.firebaseio.com/" +getName+'.json'

    // console.log(JSON.stringify(dataDictionary))
    fetch(url, { method: "POST", body: JSON.stringify(dataDictionary) })
    analysisBox.classList.add("hide")
    submissionBox.classList.remove("hide")
}

function getStarted(){
    validate()  
  
    homeBox.classList.add("hide")

    analysisBox.classList.remove("hide")


}

// Validation incase the participant forgets to enter name 

function validate(){
    const nameField = document.getElementById("myname").value;

    let valid=true
    if(nameField === ""){
        const nameError = document.getElementById("nameError")
        nameError.classList.add("visible");
        nameField.classList.add("invalid");
        nameError.setAttribute("aria-hidden", false);
        nameError.setAttribute("aria-invalid", true);
    }
    return valid


}
// Validation incase the participant forgets to enter rating/ if the rating is any other number than 1,3,5 

function validateScore(){
    const scoreField = document.getElementById("myrating").value;
    scoreError.setAttribute("aria-hidden", true);

    let valid=true
    if(scoreField === ""){
        const scoreError = document.getElementById("scoreError")
        scoreError.classList.add("visible");
        scoreField.classList.add("invalid");
        scoreError.setAttribute("aria-hidden", false);
        scoreError.setAttribute("aria-invalid", true);
    }else if ((scoreField!='3') && (scoreField!='1')&&(scoreField!='5')){
        const scoreError = document.getElementById("scoreError")
        scoreError.classList.add("visible");
        scoreField.classList.add("invalid");
        scoreError.setAttribute("aria-hidden", false);
        scoreError.setAttribute("aria-invalid", true);
    }

    return valid

}

window.onload = function(){
  
    setAvailableAudios()

    getNewAudio()
}
