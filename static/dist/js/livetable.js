const cellStyle = "padding: 4px 32px 4px 0px;";
const headerStyle = "border-bottom: 2px solid #e7e5e4;";
const numberingStyle = "color: #e7e5e4; padding-bottom: 0px;"
const evenRowStyle = "";
const oddRowStyle = "border-bottom: 1px solid #e7e5e4;border-top: 1px solid #e7e5e4;";

function readCSVFile() {
  const fileInput = document.getElementById('csv_file');
  const file = fileInput.files[0];
  const reader = new FileReader();
  const table = document.getElementById('live_table');
  const tableDiv = document.getElementById('live_table_div');
  reader.onload = function(event) {
    const csvContent = event.target.result;
    const rows = csvContent.split('\n');
    const headerRow = table.insertRow(0);
    for (let j = 0; j < rows[0].split(',').length; j++) {
      const headerCell = headerRow.insertCell();
      headerCell.style.cssText = `${cellStyle} ${numberingStyle}`;
      headerCell.innerHTML = j;
    }
    tableDiv.classList.remove("hidden");
    for (let i = 0; i < rows.length; i++) {
      const row = table.insertRow();
      const cells = rows[i].split(',');
      row.style.cssText = i % 2 == 0 ? evenRowStyle : oddRowStyle;
      for (let j = 0; j < cells.length; j++) {
        const cell = row.insertCell();
        cell.innerHTML = cells[j];
        if (i == 0) {
          cell.style.cssText = `${cellStyle} ${headerStyle}`;
        } else {
          cell.style.cssText = cellStyle;
        }
      }
    }
  };
  reader.readAsText(file);
}