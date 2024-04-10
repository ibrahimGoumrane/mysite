// Selecting necessary elements
const hamb = document.querySelector(".bx-menu-alt-left"); // Menu icon
const closes = document.querySelector(".bx-x"); // Close icon
const menu = document.querySelector(".menu"); // Menu container
const header = document.querySelector(".header"); // Header container
const w = window.innerWidth;
const navLink = document.querySelector(".nav");

// Responsive menu

if (w <= 655) {
    header.classList.add("none");
    hamb.classList.remove("none");
}
const toggler = function (e) {
    console.log(e.target);
    if (!e.target.closest(this)) return;
    console.log(this);
    header.classList.toggle("none");
    hamb.classList.toggle("none");
    closes.classList.toggle("none");
};
menu.addEventListener("click", toggler.bind(".bx"));
navLink.addEventListener('click', toggler.bind(".nav-link"));