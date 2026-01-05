/** This script calculates the total daily carbs, fats , proteins
 * and calories from the selected food and then updates the numeric 
 * totals and the doughnut chart 
 */


document.addEventListener("DOMContentLoaded", function () {

  // The main food table in which the rows are added dynamically
  const table = document.querySelector(".food-table tbody");

  // Variables in which the totals are going to be displayed
  const totalCarbs = document.getElementById("totalCarbs");
  const totalProtein = document.getElementById("totalProtein");
  const totalFats = document.getElementById("totalFats");
  const totalCalories = document.getElementById("totalCalories");

  /** This function is used to update the totals
   * It is using a loop in the table rows and calculates the given totals
   * it sums the totals and updates the chart
  */ 
  function updateTotals() {
    let carbsSum = 0, proteinSum = 0, fatsSum = 0, caloriesSum = 0;

    table.querySelectorAll("tr").forEach(row => {
      const cells = row.querySelectorAll("td");

      // Each row must contain at least 5 columns
      if (cells.length >= 5) {
        carbsSum += parseFloat(cells[1].textContent) || 0;
        proteinSum += parseFloat(cells[2].textContent) || 0;
        fatsSum += parseFloat(cells[3].textContent) || 0;
        caloriesSum += parseFloat(cells[4].textContent) || 0;
      }
    });

    // Updates totals regarding the chart and rounds them to one decimal
    totalCarbs.textContent = carbsSum.toFixed(1);
    totalProtein.textContent = proteinSum.toFixed(1);
    totalFats.textContent = fatsSum.toFixed(1);
    totalCalories.textContent = caloriesSum.toFixed(1);

    // Updates the calories chart based on the previous totals
    updateChart(carbsSum, proteinSum, fatsSum);
  }

  // Initiliazes the chart.js for nutrient breakdown
  const ctx = document.getElementById("nutrientsChart").getContext("2d");
  const nutrientsChart = new Chart(ctx, {
    type: "doughnut",
    data: {
      labels: ["Carbs", "Protein", "Fats"],
      datasets: [{
        data: [0, 0, 0],
        backgroundColor: ["#ff6384", "#36a2eb", "#ffcd56"], 
        borderWidth: 1,
      }],
    },
    options: {
      responsive: true,
      plugins: {
        legend: { position: "bottom" },
      },
    },
  });

  /** Updates the chart with new values
   * If the values are all zero, it resets
   */
  function updateChart(carbs, protein, fats) {
    const total = carbs + protein + fats;
    if (total > 0) {
      nutrientsChart.data.datasets[0].data = [
        carbs, protein, fats
      ];
    } else {
      nutrientsChart.data.datasets[0].data = [0, 0, 0];
    }
    nutrientsChart.update();
  }

  // Initial calculation when reloading the page
  updateTotals();
});