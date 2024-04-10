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


const sections = document.querySelectorAll('.intersect');
// const header_nav = document.querySelector('ul.nav');
const callback = function (entries, observer) {
    const [entry] = entries;
    // if (entry.target.closest('ul.nav')) {
    //     entry.target.classList.toggle("intersecting");
    //     [...entry.target.children].forEach((child, index) => {
    //         const closestNavItem = child.closest('.nav-item');
    //         const itera = closestNavItem && !closestNavItem.classList.contains('nav') ? index : 0;
    //         setTimeout(function () {
    //             closestNavItem.classList.toggle('nav');
    //         }
    //             , 400 * itera)
    //     });
    //     return;
    // };
    if (!entry.isIntersecting) return;
    entry.target.classList.remove("intersecting");
    observer.unobserve(entry.target);
}
const options = {
    root: null,
    rootMargin: "-20px",
    threshold: 0.3,
};

const observer = new IntersectionObserver(callback, options);
sections.forEach(section => {
    observer.observe(section);
})
// observer.observe(header_nav);
