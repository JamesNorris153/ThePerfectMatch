// Sort a table by a given column using Bubble Sort method
function sortTable(column,element) {

  // Set the number of swaps undertaken to 0
  swapCounter = 0;

  // Get the table being sorted
  table = $(element).parent().parent().parent();

  // By default sort in ascending order
  direction = "A";

  // While there is still sorting left to do, perform another iteration of the sorting loop
  sortComplete = false;
  while (!sortComplete) {

    // Assume that there is nothing left to sort to start
    sortComplete = true;

    // Get all VISIBLE rows in the table
    rows = $(table).find('tbody tr:not(.template)');

    // Loop over each row, checking if it needs to be swapped with its current successor
    for (i = 0; i < ($(rows).length - 1); i++) {
      // Assume that the rows don't need to be swapped
      swapRows = false;

      // Get the current and next rows in the selected column
      curRow = $(rows[i]).find('td').get(column);
      nextRow = $(rows[i+1]).find('td').get(column);

      curRowData = $(curRow).html();
      nextRowData = $(nextRow).html();

      // If either of the data are not a number, data needs to be processed as string
      if (isNaN(curRowData) || isNaN(nextRowData)) {

        // Check the direction of sorting, perform the correct comparison accordingly
        if (direction == "A") {
          // Lowercase both strings to compare, then break from the loop to swap the items
          if (curRowData.toLowerCase() > nextRowData.toLowerCase()) {
            swapRows = true;
            break;
          }
        } else {
          if (curRowData.toLowerCase() < nextRowData.toLowerCase()) {
            swapRows = true;
            break;
          }
        }
      } else {
        if (direction == "A") {
          // If data is numbers, parse them as base 10 integers, and then compare
          if (parseInt(curRowData,10) > parseInt(nextRowData,10)) {
            swapRows = true;
            break;
          }
        } else {
          if (parseInt(curRowData,10) < parseInt(nextRowData,10)) {
            swapRows = true;
            break;
          }
        }
      }
    }

    // If the current and next row need to be swapped, swapRows will have been set to true
    if (swapRows) {

      // Move the next row before the current row
      $(rows[i+1]).insertBefore($(rows[i]));

      // Reset the sortComplete variable to continue checking the rows
      sortComplete = false;

      // Increment the number of swaps undertaken
      swapCounter ++;
    } else {

      // If no swapping has occurred, and this is the first pass (Ascending order), try sort in Descending order
      if (swapCounter == 0 && direction == "A") {
        direction = "D";
        sortComplete = false;
      }
    }
  }
}
