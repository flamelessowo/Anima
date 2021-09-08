let cards = document.querySelectorAll(".set-bg")

cards.forEach(el => {
    let oldimage = el.dataset.setbg;
    el.addEventListener("mouseenter", () => {
        el.style.backgroundImage = "url(/media/black.jpg)"
        el.style.transition = "0.3s"
    })
    el.addEventListener("mouseleave", () => {
        el.style.backgroundImage = `url(${oldimage})`
    })
})