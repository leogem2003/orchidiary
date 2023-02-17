const modalClose = document.querySelector(".modal-exit")
const accountBtn = document.querySelector(".account-btn")
const loginLink = document.querySelector(".login-link")
const modal = document.querySelector(".modal")

const toggleModal = (event) => {
    modal.classList.toggle("invisible")
}

modalClose.addEventListener('click', toggleModal)
accountBtn.addEventListener('click', toggleModal)
try {
    loginLink.addEventListener('click', toggleModal)
} catch (e) {
    null
}