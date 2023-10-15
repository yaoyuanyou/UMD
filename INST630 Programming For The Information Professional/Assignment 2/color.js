const changeButton = document.querySelector(".btn");

function changeButtonColor(){
  console.log("changeButtonColor");
  const titleColor = document.querySelector("h1");
  titleColor.classList.toggle("newcolor");
}

changeButton.addEventListener("click", () => changeButtonColor());