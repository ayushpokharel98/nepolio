loading.classList.add('show');
let stocks = [];
fetch('http://127.0.0.1:8000/get-stock-names')
    .then(response => response.json())
    .then(data => {
        stocks = data;  // Use the data as needed
        populateStocks();
    })
    .catch(error => {
        console.error('Error:', error);
    });

document.addEventListener('DOMContentLoaded', () => {
    let index_data = [];
    fetch('http://127.0.0.1:8000/get-index-data')
        .then(response => response.json())
        .then(data => {
            index_data = data;
            const indicesData = document.querySelector(".indicesData");
            if (indicesData && index_data.length > 0) {
                for (let i = 0; i < index_data.length; i++) {
                    indicesData.innerHTML += `<div class="p-4 bg-gray-100 shadow-md rounded-lg">
                    <h2 class="font-semibold">${index_data[i].name}</h2>
                    <p class="font-bold text-green-600">${index_data[i].value}</p>
                    <p class="font-bold text-green-600">${index_data[i].percent} </p>
                    <p> ${index_data[i].price} </p>
                </div>`;
                }
            }
            loading.classList.remove('show');
        })
        .catch(error => {
            console.error('Error:', error);
            loading.classList.remove('show')
        });


});
const resultBox = document.querySelector(".suggestions");
const inputBox = document.querySelector(".input-box");
const searchBox = document.querySelector(".search-box");
const selectStocks = document.getElementById("stock-select");
inputBox.onkeyup = function () {
    let result = [];
    let input = inputBox.value.trim();  // Trim input to avoid blank spaces issues
    if (input.length) {
        result = stocks.filter((keyword) => {
            return keyword.toLowerCase().includes(input.toLowerCase());
        });
    }
    display(result);
};

function display(result) {
    if (result.length) {
        const content = result.map((stock) => {
            return `<a href="/stock/${stock}" target="_blank"><li class='stock-name-list w-full'>${stock}</li></a>  \n <hr>`;
        });
        resultBox.innerHTML = "<ul>" + content.join('') + "</ul>";
        resultBox.style.display = 'block'; // Ensure the suggestions box is visible
    } else {
        resultBox.innerHTML = "";
        resultBox.style.display = 'none'; // Hide the suggestions box if no result
    }
}

// Show suggestions box when input is focused
inputBox.addEventListener('focus', () => {
    if (resultBox.innerHTML.trim()) {
        resultBox.style.display = 'block';
    }
});

// Hide suggestions when clicking outside the search box or suggestions box
document.addEventListener('click', (event) => {
    // If the click is outside both search box and result box, hide the result box
    if (!searchBox.contains(event.target) && !resultBox.contains(event.target)) {
        resultBox.style.display = 'none';
    }
});

// Prevent hiding suggestions when clicking inside the suggestions box or search box
resultBox.addEventListener('click', (event) => {
    event.stopPropagation(); // Prevent the click from reaching the document
});

inputBox.addEventListener('click', (event) => {
    event.stopPropagation(); // Prevent the click from reaching the document
});

function populateStocks() {
    stocks.forEach(symbol => {
        let option = document.createElement("option");
        option.value = symbol;
        option.text = symbol;
        selectStocks.add(option);
    });
}

function deleteStock(symbol) {
    window.location.href = `/delete-stock/${symbol}`;
}


const ltp = () => {
    // Get the stock symbols present in the portfolio table
    const visibleStocks = Array.from(document.querySelectorAll('[class^="td-ltp-"]'))
      .map(cell => cell.className.replace('td-ltp-', ''));
  
    fetch(`http://127.0.0.1:8000/all-data`)
      .then(response => response.json())
      .then(data => {
        let totalValue = 0;
        let totalPL = 0;
  
        // Filter API data to only include stocks that are in the portfolio
        const filteredData = data.filter(stockDetails => visibleStocks.includes(stockDetails.Symbol));
  
        // Loop through filtered stock data
        filteredData.forEach(stockDetails => {
          const stockSymbol = stockDetails.Symbol;
          const ltpValue = parseFloat(stockDetails.LTP.replace(/,/g, ''));
  
          // Update the corresponding table cells
          const ltpCell = document.querySelector(`.td-ltp-${stockSymbol}`);
          const plCell = ltpCell.nextElementSibling;
  
          if (ltpCell && ltpValue) {
            ltpCell.textContent = ltpValue;
  
            const atBought = parseFloat(ltpCell.previousElementSibling.textContent.replace(/,/g, ''));
            const quantity = parseFloat(ltpCell.previousElementSibling.previousElementSibling.textContent.replace(/,/g, ''));
            const profitLoss = ((ltpValue - atBought) * quantity).toFixed(2);
  
            // Update Profit/Loss cell
            if (plCell) {
              plCell.textContent = profitLoss;
              plCell.classList.add(profitLoss >= 0 ? 'text-green-500' : 'text-red-500');
            }
  
            // Calculate Total Value and Total P/L
            totalValue += ltpValue * quantity;
            totalPL += parseFloat(profitLoss);
          }
        });
  
        // Update the Total Value and Total P/L
        document.querySelector('.total-value').textContent = totalValue.toFixed(2);
        const totalPLTag = document.querySelector('.total-pl');
        totalPLTag.textContent = totalPL.toFixed(2);
        totalPLTag.classList.add(totalPL >= 0 ? 'text-green-500' : 'text-red-500');
      })
      .catch(error => {
        console.error('Error:', error);
      });
  }
  
  // Call the ltp function to populate the table and calculate totals
  ltp();
  