//############################################################//
// Progress Bar Function
//############################################################//
function onLoad() {
    var line = new ProgressBar.Line('#line', {
        color: 'rgba(255, 255, 255, 0.1)',
        duration: 10000,
        easing: 'easeInOut',
    });

    line.animate(1);
};

function remove() {
    document.querySelector("svg").remove()
}

//############################################################//
// Fetch Function
//############################################################//
var test = async () => {
    var element = document.getElementById("data-card")

    var response = await fetch('https://api.blocknative.com/gasprices/blockprices')
    var data = await response.json()

    element.innerHTML = createCard(data)
    changeContent(data);

    let gweiFee = data.blockPrices[0].estimatedPrices[0].maxPriorityFeePerGas + data.blockPrices[0].baseFeePerGas

    let lowGas = false

    if(gweiFee <= 8) {
        lowGas = true;
    }
    else {
        lowGas = false;
    }

    function httpGet(theUrl) {
        var xmlHttp = new XMLHttpRequest()
        xmlHttp.open( "GET", theUrl, false);
        xmlHttp.send( null );
        return xmlHttp.responseText;
    }

    if(lowGas) {
        httpGet("http://localhost:5000/send/email");
    }

    const colors = adjustGradient(data);
    let heat = `rgba(${colors.red}, 0, ${colors.blue})`;
    let gradientColor = `linear-gradient(153deg, rgba(2, 0, 36, 1) 58%, ${heat} 100%)`;
    document.body.style.background = gradientColor;

    onLoad();

}

test()
setInterval(test, 10000)
setInterval(remove, 10000)

//############################################################//
// Adjust Color Gradient Function
//############################################################//
function adjustGradient(data) {
    let blue = 255;
    let red = 0;
    let gweiFee = data.blockPrices[0].estimatedPrices[0].maxPriorityFeePerGas + data.blockPrices[0].baseFeePerGas;
    console.log(gweiFee);
    if(gweiFee > 30) {
        blue = 0;
        red = 255;
    }
    else {
        // blue = 0;
        // red = 255;
        blue = 255 - (gweiFee * 8.5);
        red = 0 + (gweiFee * 8.5);
    }
    let colors = {red: red, blue: blue};
    return colors;
}

//############################################################//
// Change Bottom Right Box Input Function
//############################################################//
function changeContent(data){
    if((data.blockPrices[0].estimatedPrices[0].maxPriorityFeePerGas + data.blockPrices[0].baseFeePerGas) <= 8) {
        console.log((data.blockPrices[0].estimatedPrices[0].maxPriorityFeePerGas + data.blockPrices[0].baseFeePerGas));

        cost.innerHTML = `
        <div class="container">
        <div class="row my-4"><p>The cost to transact on Ethereum is currently low.</p></div>
        <div class="row my-4 justify-content-md-center">
        <div class="col-md-auto">
            <img src= "/static/assets/eth.png" width="30" height="30" class="d-inline-block align-top" alt="Ethereum">
        </div>
        <div class="col-md-auto">
            <img src= "/static/assets/eth.png" width="30" height="30" style="opacity:0.2"  class="d-inline-block align-top" alt="Ethereum">
        </div>
        <div class="col-md-auto">
            <img src= "/static/assets/eth.png" width="30" height="30" style="opacity:0.2" class="d-inline-block align-top" alt="Ethereum">
            </div>
        </div>
        </div>` 
    }

    else if(8 < (data.blockPrices[0].estimatedPrices[0].maxPriorityFeePerGas + data.blockPrices[0].baseFeePerGas) && (data.blockPrices[0].estimatedPrices[0].maxPriorityFeePerGas + data.blockPrices[0].baseFeePerGas) <= 20) {
        console.log((data.blockPrices[0].estimatedPrices[0].maxPriorityFeePerGas + data.blockPrices[0].baseFeePerGas));

        cost.innerHTML = `
        <div class="container">
        <div class="row my-4"><p>The cost to transact on Ethereum is currently average.</p></div>
        <div class="row my-4 justify-content-md-center">
        <div class="col-md-auto">
            <img src= "/static/assets/eth.png" width="30" height="30" class="d-inline-block align-top" alt="Ethereum">
        </div>
        <div class="col-md-auto">
            <img src= "/static/assets/eth.png" width="30" height="30" class="d-inline-block align-top" alt="Ethereum">
        </div>
        <div class="col-md-auto">
            <img src= "/static/assets/eth.png" width="30" height="30" style="opacity:0.2" class="d-inline-block align-top" alt="Ethereum">
            </div>
        </div>
        </div>` 
    }

    else {
        console.log((data.blockPrices[0].estimatedPrices[0].maxPriorityFeePerGas + data.blockPrices[0].baseFeePerGas));

        cost.innerHTML = `
        <div class="container">
        <div class="row my-4"><p>The cost to transact on Ethereum is currently high.</p></div>
        <div class="row my-4 justify-content-md-center">
        <div class="col-md-auto">
            <img src= "/static/assets/eth.png" width="30" height="30" class="d-inline-block align-top" alt="Ethereum">
        </div>
        <div class="col-md-auto">
            <img src= "/static/assets/eth.png" width="30" height="30" class="d-inline-block align-top" alt="Ethereum">
        </div>
        <div class="col-md-auto">
            <img src= "/static/assets/eth.png" width="30" height="30" class="d-inline-block align-top" alt="Ethereum">
            </div>
        </div>
        </div>` 
    }
}

//############################################################//
// Create Card Function
//############################################################//
function createCard(data) {
    const output = `
    <div id="dashboard" class="p-1 box1 m-2">
        <div class="m-5">
            <h3>Next Ethereum Block - Gas Prediction</h3>
            <p>Pending Block Number: <span class="hyper">${data.blockPrices[0].blockNumber}</span></p>
        </div>
        <div class="row m-5">
            <div class="text-center col m-2">
                <h6>priority fee</h6>
                <h2 class="gwei">${data.blockPrices[0].estimatedPrices[0].maxPriorityFeePerGas}</h2>
                <h6>max fee</h6>
                <p>${data.blockPrices[0].estimatedPrices[0].maxFeePerGas}</p>
                <div class="box2 py-3">
                    <h6 class="mb-0">99% probability</h6>
                </div>
            </div>
            <div class="text-center col m-2">
                <h6>priority fee</h6>
                <h2 class="gwei">${data.blockPrices[0].estimatedPrices[1].maxPriorityFeePerGas}</h2>
                <h6>max fee</h6>
                <p>${data.blockPrices[0].estimatedPrices[1].maxFeePerGas}</p>
                <div class="box2 py-3">
                    <h6 class="mb-0">95% probability</h6>
                </div>
            </div>
            <div class="text-center col m-2">
                <h6>priority fee</h6>
                <h2 class="gwei">${data.blockPrices[0].estimatedPrices[2].maxPriorityFeePerGas}</h2>
                <h6>max fee</h6>
                <p>${data.blockPrices[0].estimatedPrices[2].maxFeePerGas}</p>
                <div class="box2 py-3">
                    <h6 class="mb-0">90% probability</h6>
                </div>
            </div>
            <div class="text-center col m-2">
                <h6>priority fee</h6>
                <h2 class="gwei">${data.blockPrices[0].estimatedPrices[3].maxPriorityFeePerGas}</h2>
                <h6>max fee</h6>
                <p>${data.blockPrices[0].estimatedPrices[3].maxFeePerGas}</p>
                <div class="box2 py-3">
                    <h6 class="mb-0">80% probability</h6>
                </div>
            </div>
            <div class="text-center col m-2">
                <h6>priority fee</h6>
                <h2 class="gwei">${data.blockPrices[0].estimatedPrices[4].maxPriorityFeePerGas}</h2>
                <h6>max fee</h6>
                <p>${data.blockPrices[0].estimatedPrices[4].maxFeePerGas}</p>
                <div class="box2 py-3">
                    <h6 class="mb-0">70% probability</h6>
                </div>
            </div>
        </div>
    </div>
    <div class="row p-1 m-2 gap-3">
        <div class="text-center col box1 p-3 d-flex justify-content-center align-items-center">
            <div class="">
                <p>Time since last block: <span class="hyper">${Math.round(data.msSinceLastBlock / 1000)} seconds</span></p>
                <p>Estimated number of transactions in pending block: <span class="hyper">${data.blockPrices[0].estimatedTransactionCount}</span></p>
                <p>Max Price in pending block: <span class="hyper">${data.maxPrice} gwei</span></p>
                <p class="mb-0">Base Fee: <span class="hyper">${Math.round(((data.blockPrices[0].baseFeePerGas)*100))/100} gwei</span></p>
            </div>
        </div>
        <div id ="cost" class="text-center col-4 box1 p-3 d-flex justify-content-center align-items-center"></div>
    </div>
    <div id="line" class="line m-2"></div>

    `;
    return output;
}