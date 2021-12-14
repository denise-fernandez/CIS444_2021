var jwt = null

        function clearAll() {
           const meme = document.querySelector(".meme-content");
           const joke = document.querySelector(".joke-content");

           meme.innerHTML = "";
           joke.innerHTML = "";
        }

        function showMeme() {
           // Value should be a string representing image URL
           const randomMemeUrl = getRandomData("memes");

           const memeContainer = document.querySelector(".meme-content");
           const newMeme = document.createElement("img");
           newMeme.setAttribute("src", randomMemeUrl);

           clearAll();

           // Add the new img to the document
           memeContainer.appendChild(newMeme);
        }

        function showJoke() {
           // Value should be a string representing the joke
           const randomJokeText = getRandomData("jokes");

           const jokeContainer = document.querySelector(".joke-content");
           const newJoke = document.createElement("p");
           newJoke.textContent = randomJokeText;

           clearAll();

           // Add the new img to the document
           jokeContainer.appendChild(newJoke);
        }

        //This function is used to get random data
        function getRandomData(type) {
           return data[type][rn(data[type].length)];
        }


function secure_get_with_token(endpoint, on_success_callback, on_fail_callback){
	xhr = new XMLHttpRequest();
	function setHeader(xhr) {
		xhr.setRequestHeader('Authorization', 'Bearer:'+jwt);
	}
	function get_and_set_new_jwt(data){
		console.log(data);
		jwt  = data.token
		on_success_callback(data)
	}
	$.ajax({
		url: endpoint,
		type: 'GET',
		datatype: 'json',
		success: on_success_callback,
		error: on_fail_callback,
		beforeSend: setHeader
	});
}

function secure_get_with_data(endpoint, data_to_send, on_success_callback, on_fail_callback){
        xhr = new XMLHttpRequest();
        function setHeader(xhr) {
                xhr.setRequestHeader('Authorization', 'Bearer:'+jwt);
        }
        function get_and_set_new_jwt(data){
                console.log(data);
                jwt  = data.token
                on_success_callback(data)
        }
        $.ajax({
            url: endpoint,
	    data: data_to_send,
            type: 'GET',
            datatype: 'json',
            success: on_success_callback,
            error: on_fail_callback,
            beforeSend: setHeader
        });
}


// Source for content:
//https://memes.com/search/?term=programming
//https://www.thecoderpedia.com/blog/programming-memes/, Reddit
const memes = [
  "https://cdn.memes.com/up/94544761585650888/i/1585651440780.jpg",
  "https://cdn.memes.com/up/95018491572030779/i/1572031000417.jpg",
  "https://i.chzbgr.com/full/9553638400/hC34DEFED/fast-paced-and-dynamic-software-engineering-job-first-day-on-actual-job-no-time-explain-grab-cactus",
  "https://i.chzbgr.com/full/9553638656/h7E3BB5DF/person-english-teacher-is-semicolon-will-hardly-use-computer-science-student",
  "https://i.chzbgr.com/full/9553639680/h63957ECE/person-randomly-realize-couldve-caused-bug-codehub",
  "https://i.chzbgr.com/full/9553641216/h6D578DDB/if-want-be-sure-line-error-is-on-openinc-mon-tue-thur-write-all-code-on-one-line-urwa-imgflipcom",
  "https://i.chzbgr.com/full/9553642496/hCFDF2F82/car-copy-snippet-stackoverflow-and-doesnt-works-aarr-those-bastards-lied",
  "https://miro.medium.com/max/1000/0*Ua695vjzFHV6VNOX.png",
  "https://pbs.twimg.com/media/EKkPagPXkAA__Qo.jpg",
  "https://www.thecoderpedia.com/wp-content/uploads/2020/06/Programming-Memes-Programmer-while-sleeping.jpg",
  "https://www.thecoderpedia.com/wp-content/uploads/2020/06/Internet-Explorer-Joke-915x1024.jpg",
];

// Sourced from: 
//https://devdojo.com/devdojo/10-awesome-programming-jokes
//http://www.devtopics.com/best-programming-jokes/
const jokes = [
  "This statement",
  "How many programmers does it take to change a light bulb? None, that's a hardware problem",
  "Why did the programmer quit his job? Because he didn't get arrays",
  "What did the Java code say to the C code? You've got no class.",
  "What is the most used language in programming? Profanity.",
  "Eight bytes walk into a bar.  The bartender asks, “Can I get you anything?” “Yeah,” reply the bytes.  “Make us a double.”",
  "There are only 10 kinds of people in this world: those who know binary and those who don’t.",
  "All programmers are playwrights, and all computers are lousy actors.",
  "Have you heard about the new Cray super computer?  It’s so fast, it executes an infinite loop in 6 seconds.",
  "The generation of random numbers is too important to be left to chance.",
  "Debugging: Removing the needles from the haystack.",
  "“Debugging” is like being the detective in a crime drama where you are also the murderer.",
  "There are two ways to write error-free programs; only the third one works.",
  "The best thing about a Boolean is even if you are wrong, you are only off by a bit.",
];

function rn(len) {
  return Math.floor(Math.random() * len);
}

const data = {
  memes,
  jokes,
};
