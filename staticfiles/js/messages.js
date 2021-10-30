window.onload = function () {
    let messages = document.getElementsByClassName("alert")
    let i = 0
    let cycle = setInterval(function () {
        if(i < messages.length) {
            setTimeout(function () {
                console.log(i)
                messages[i].classList.add('hidden'); // скрываем
                i++
            }, 2000); // задержка перед скрытием в миллисекундах
            console.log(`Message ${i} closed`)
        }
        else {
            clearInterval(cycle);
            console.log("Stopped")
        }
    }, 5000);
}