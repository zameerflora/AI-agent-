function showSignup() {
    document.getElementById("welcome-screen").classList.add("hidden");
    document.getElementById("login-screen").classList.add("hidden");
    document.getElementById("signup-screen").classList.remove("hidden");
}

function showLogin() {
    document.getElementById("welcome-screen").classList.add("hidden");
    document.getElementById("signup-screen").classList.add("hidden");
    document.getElementById("login-screen").classList.remove("hidden");
}

