/** This script handles the BMI calculation, validates the user input, calculates the user's bmi and highlights 
 * the correct table row and updates the UI of the table
 * Also, it makes sure that the form resets every time the user presses the Calculate bmi button amd also the table highlish sets also.
 * */

document.getElementById("bmiForm").addEventListener("submit", function(e) {
  e.preventDefault();

  // Defines the variables
  const heightField = document.getElementById("height");
  const weightField = document.getElementById("weight");

  const heightInput = parseFloat(heightField.value);
  const weight = parseFloat(weightField.value);

  // Detect meters and centimeters
  const height = heightInput > 10 ? heightInput / 100 : heightInput;

  const bmiValue = document.getElementById("bmiValue");
  const bmiCategory = document.getElementById("bmiCategory");
  const bmiIdealRange = document.getElementById("bmiIdealRange");

  // Clear previous highlights
  document.querySelectorAll(".bmi-table-box tbody tr").forEach(row => {
    row.classList.remove("active");
  });

  // Input validation using the loop function
  let invalid = false;

  if (!height || isNaN(height) || height <= 0) {
    heightField.setCustomValidity("Please enter a valid numeric value for height.");
    invalid = true;
  } else {
    heightField.setCustomValidity("");
  }

  if (!weight || isNaN(weight) || weight <= 0) {
    weightField.setCustomValidity("Please enter a valid numeric value for weight.");
    invalid = true;
  } else {
    weightField.setCustomValidity("");
  }

  if (invalid) {
    // Show native tooltip bubble
    if (!heightField.checkValidity()) heightField.reportValidity();
    else weightField.reportValidity();

    // Reset displayed values
    bmiValue.textContent = "--";
    bmiCategory.textContent = "";
    bmiIdealRange.textContent = "";
    return;
  }

  // BMI calculation
  const bmi = (weight / (height * height)).toFixed(1);
  let category = "";

  if (bmi < 18.5) {
    category = "Underweight";
    document.getElementById("underweight").classList.add("active");
  } else if (bmi < 25) {
    category = "Healthy weight";
    document.getElementById("healthy").classList.add("active");
  } else if (bmi < 30) {
    category = "Overweight";
    document.getElementById("overweight").classList.add("active");
  } else {
    category = "Obese";
    document.getElementById("obese").classList.add("active");
  }

  // Ideal weight range
  const minWeight = (18.5 * height * height).toFixed(1);
  const maxWeight = (24.9 * height * height).toFixed(1);

  //  Make BMI bold using innerHTML
  bmiValue.innerHTML = `<strong>${bmi}</strong>`;

  bmiCategory.textContent = `Your BMI category is ${category}. See table for more details on your BMI and how and if you must improve it.`;
  bmiIdealRange.textContent = `Your ideal weight range is between ${minWeight} kg – ${maxWeight} kg.`;

  // RESET BUTTON FUNCTIONALITY
  document.getElementById("resetBtn").addEventListener("click", function () {

    // Clear inputs
    document.getElementById("bmiForm").reset();

    // Clear displayed BMI results
    document.getElementById("bmiValue").textContent = "--";
    document.getElementById("bmiCategory").textContent = "";
    document.getElementById("bmiIdealRange").textContent = "";

    // Remove table highlights
    document.querySelectorAll(".bmi-table-box tbody tr").forEach(row => {
      row.classList.remove("active");
    });
  });
});
