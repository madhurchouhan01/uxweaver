const steps = document.querySelectorAll('.step');
let index = 0;

function highlightNextStep() {
    steps.forEach(step => step.classList.remove('blink'));
    steps[index].classList.add('blink');
    index = (index + 1) % steps.length;
}

setInterval(highlightNextStep, 1000);
