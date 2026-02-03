const socket = io({autoconnect: true});


socket.on('connect', function () {
    socket.emit('my event', {data: 'I\'m connected!'});
});
const input = document.getElementById('guess_input');
const guesses = document.getElementById('guesses');
input.focus()
console.log(localStorage.getItem('guesses'));

const circle = document.getElementById('guess_circle');
if (localStorage.getItem('circle') === null) {
            circle.style.fill=localStorage.getItem('circle');
        } else {
            localStorage.setItem('circle', "#FFFFFF");
            circle.style.fill="#FFFFFF";
        }


// On reload
guesses.innerText = "";

socket.emit("reload_values", localStorage.getItem('guesses'));
socket.on("reloaded_values", data => {
    console.log(data)
    let array = Object.entries(data["reload_guesses"]);
    array = array.sort((a, b) => -a[1][0] + b[1][0]);
    for (let i = 0; i < array.length; i++) {
        let color = document.createElement("div");
        let value = document.createElement("div");
        color.id = "c" + String(i);
        color.className = "color_block";
        value.className = "value_block";
        value.id = "v" + String(i);
        color.innerHTML = array[i][0][0];
        value.innerHTML = String(Math.round((array[i][1][0] + Number.EPSILON) * 100) / 100) + "%";
        color.style.backgroundColor = array[i][1][1];
        value.style.backgroundColor = array[i][1][1];
        localStorage.setItem('circle', array[i][1][1]);
        circle.style.fill = array[i][1][1];
        guesses.appendChild(color);
        guesses.appendChild(value);
    }
})


function guess() {
    if (event.key === "Enter") {
        let text = input.value;

        if (localStorage.getItem('guesses') === null) {
            localStorage.setItem('guesses', JSON.stringify({"guesses": [text]}))
        } else {
            let guesses_json = JSON.parse(localStorage.getItem('guesses'));
            guesses_json.guesses.push(text);
            localStorage.setItem("guesses", JSON.stringify(guesses_json));
        }
        console.log(localStorage.getItem('guesses'));
        socket.emit("guess", {guess: text, "previous_guesses": JSON.parse(localStorage.getItem('guesses'))["guesses"]});
        input.value = "";

    }

}

function change_color(){
    socket.emit("change_color", {});
}

socket.on("accuracy", (data) => {

    guesses.innerText = "";
    let array = Object.entries(data["previous_guesses"]);
    array = array.sort((a, b) => -a[1][0] + b[1][0]);
    for (let i = 0; i < array.length; i++) {
        let color = document.createElement("div");
        let value = document.createElement("div");
        color.id = "c" + String(i);
        color.className = "color_block";
        value.className = "value_block";
        value.id = "v" + String(i);
        color.innerHTML = array[i][0][0];
        value.innerHTML = String(Math.round((array[i][1][0] + Number.EPSILON) * 100) / 100) + "%";
        color.style.backgroundColor = array[i][1][1];
        value.style.backgroundColor = array[i][1][1];
        localStorage.setItem('circle', array[i][1][1]);
        circle.style.fill = array[i][1][1];
        guesses.appendChild(color);
        guesses.appendChild(value);


    }
    console.log(array);


})
