let blue = 255;
let red = 0;
let gweiFee = data.blockPrices[0].estimatedPrices[0].maxPriorityFeePerGas + data.blockPrices[0].baseFeePerGas;

function adjustGradient() {
    if(gweiFee > 50) {
        blue = 0;
        red = 255;
    }
    else {
        blue = 255 - (gweiFee * 5.1);
        red = 0 + (gweiFee * 5.1);
    }
}


let heat = `rgba(${red}, 0, ${blue})`;

const gradient = document.querySelector('gradient');
let gradientColor = `linear-gradient(153deg, rgba(2, 0, 36, 1) 58%, ${heat} 100%)`;