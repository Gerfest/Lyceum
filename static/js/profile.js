'use strict'

window.onload = function () {
    console.log("JS loaded")

    let profile_data = document.getElementById("profile_data")
    let profile_change = document.getElementById("profile_change")
    let buttons = document.querySelectorAll('.change_toggle')

    let swap = function () {
        profile_data.classList.toggle("hidden");
        profile_change.classList.toggle("hidden");
    }

    buttons.forEach(btn => btn.addEventListener('click', swap))
}