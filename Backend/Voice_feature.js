async function speak(text) {
  await fetch("http://127.0.0.1:5000/api/voice/speak", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text })
  });
}

async function listen() {
  const res = await fetch("http://127.0.0.1:5000/api/voice/listen");
  const data = await res.json();
  return data.result;
}

async function activateVoiceCommands() {
  const page = window.location.pathname.split("/").pop();

  await speak("Welcome. Say a command.");

  const command = await listen();

  if (page === "dashboard.html") {
    if (command.includes("course")) window.location.href = "course_registration.html";
    else if (command.includes("result")) window.location.href = "results.html";
    else if (command.includes("profile")) window.location.href = "profile.html";
    else if (command.includes("log out")) {
      localStorage.clear();
      await speak("Logging out now.");
      window.location.href = "login.html";
    } else {
      await speak("I didn't understand that. Try again.");
      activateVoiceCommands();
    }
  }

  if (page === "login.html" && command.includes("sign up")) {
    window.location.href = "signup.html";
  }

  if (page === "signup.html" && command.includes("register")) {
    document.querySelector("button[type=submit]").click();
  }

  if (page === "results.html" && command.includes("print")) {
    window.print();
  }
}
window.addEventListener("DOMContentLoaded", () => {
  setTimeout(() => {
    if (!window.voiceDisabled) activateVoiceCommands();
  }, 1000);
});