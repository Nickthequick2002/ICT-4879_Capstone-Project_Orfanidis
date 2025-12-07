/** This script is used for scanning the food table, sums the total carbs,
 * fats, proteins and calories and updates the displayed totals
 * Focuses only in the values and not in the making of the chart
 */

document.addEventListener("DOMContentLoaded", function () {

  // Main table bodu that contains the food entries
  const table = document.querySelector(".food-table tbody");

  // Output variables for the total calculation
  const totalCarbs = document.getElementById("totalCarbs");
  const totalProtein = document.getElementById("totalProtein");
  const totalFats = document.getElementById("totalFats");
  const totalCalories = document.getElementById("totalCalories");

  /** Loops through the rows of the table, reads the values,
   * converts them into numbers and then extracts them, sums them,
   * and updates the totals
   */
  function updateTotals() {
    let carbsSum = 0, proteinSum = 0, fatsSum = 0, caloriesSum = 0;

    table.querySelectorAll("tr").forEach(row => {
      const cells = row.querySelectorAll("td");

      // Ensure that the row contains enough columsn to read the values
      if (cells.length >= 5) {
        const carbs = parseFloat(cells[1].textContent) || 0;
        const protein = parseFloat(cells[2].textContent) || 0;
        const fats = parseFloat(cells[3].textContent) || 0;
        const calories = parseFloat(cells[4].textContent) || 0;

        carbsSum += carbs;
        proteinSum += protein;
        fatsSum += fats;
        caloriesSum += calories;
      }
    });

    // Updates the user interface by formatting nicely the totals
    totalCarbs.textContent = carbsSum.toFixed(1);
    totalProtein.textContent = proteinSum.toFixed(1);
    totalFats.textContent = fatsSum.toFixed(1);
    totalCalories.textContent = caloriesSum.toFixed(1);
  }

  // Runs immediately when the page loads
  updateTotals(); 
});