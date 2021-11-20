'use strict'

window.addEventListener('DOMContentLoaded', function () {
    let buttons = document.querySelectorAll('.change_toggle')
    let sections = document.querySelectorAll('.section-toggle')
    let size = Math.min(buttons.length, sections.length)

    let disable_inactive_buttons = function () {
        if (buttons.length > sections.length) {
            for (let i = sections.length; i < buttons.length; i++) {
                buttons[i].classList.add("disabled")
            }
        }
    }

    let swap = function (btn) {
        let index = btn.currentTarget.number
        sections.forEach(section => section.classList.add("hidden"))
        buttons.forEach(btn => btn.classList.remove("active"))
        buttons[index].classList.add("active")
        for (let i = 0; i < size; i++) {
            if (sections[i].number === index) {
                sections[i].classList.remove("hidden")
            }
        }
    }
    let main = function () {
        disable_inactive_buttons()
        for (let i = 0; i < size; i++) {
            buttons[i].addEventListener('click', swap, true)
            buttons[i].number = i
            sections[i].number = i
        }
    }
    main()
});