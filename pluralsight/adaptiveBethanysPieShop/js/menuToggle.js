function toggleMenu() {
    document.getElementById("primaryNav").classList.toggle("open");
}
let x = document.getElementById('hamburgerButton');
x.onclick = toggleMenu;