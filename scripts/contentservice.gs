// Function to add a treasure entry
function addTreasureEntry(keyword, description, solution, date, tags) {
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName("Treasure Chest");
  if (!sheet) {
    sheet = SpreadsheetApp.getActiveSpreadsheet().insertSheet("Treasure Chest");
    sheet.appendRow(["Keyword", "Description", "Solution", "Date", "Tags"]);
  }
  sheet.appendRow([keyword, description, solution, date, tags]);
}

// Basic authentication function
function isAuthorized(e) {
  var authHeader = e.parameter.authHeader || e.requestHeaders.Authorization;
  logDebugInfo('Google Apps Script', 'authHeader', authHeader);

  if (!authHeader) {
    logDebugInfo('Google Apps Script', 'authHeader', 'No auth header provided');
    return false;
  }

  var encodedCredentials = authHeader.split(" ")[1];
  logDebugInfo('Google Apps Script', 'encodedCredentials', encodedCredentials);

  var decodedCredentials = Utilities.base64Decode(encodedCredentials);
  var decodedString = Utilities.newBlob(decodedCredentials).getDataAsString();
  logDebugInfo('Google Apps Script', 'decodedString', decodedString);

  var username = decodedString.split(":")[0];
  var password = decodedString.split(":")[1];
  logDebugInfo('Google Apps Script', 'username', username);
  logDebugInfo('Google Apps Script', 'password', password);

  var validUsername = "peanut";
  var validPassword = "3R@5CL3";

  var isAuthorized = username === validUsername && password === validPassword;
  logDebugInfo('Google Apps Script', 'isAuthorized', isAuthorized);

  return isAuthorized;
}

// Function to handle POST requests with basic authentication
function doPost(e) {
  if (!isAuthorized(e)) {
    return ContentService.createTextOutput('Unauthorized').setMimeType(ContentService.MimeType.TEXT);
  }

  var params = JSON.parse(e.postData.contents);
  var action = params.action;
  var data = params.data;

  if (action === "addConversationLog") {
    addConversationLog(data.date, data.summary, data.details);
  } else if (action === "addTaskOrParkingLotItem") {
    addTaskOrParkingLotItem(data.sheetName, data.id, data.description, data.status, data.notes, data.date);
  } else if (action === "addOrUpdateProjectState") {
    addOrUpdateProjectState(data.projectName, data.description, data.architecture, data.designs, data.roadmap, data.links);
  } else if (action === "addTreasureEntry") {
    addTreasureEntry(data.keyword, data.description, data.solution, data.date, data.tags);
  }
  logAction(action, JSON.stringify(data));
  return ContentService.createTextOutput("Success");
}

// Function to log debug information
function logDebugInfo(location, variableName, value) {
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName("Debug Logs");
  if (!sheet) {
    sheet = SpreadsheetApp.getActiveSpreadsheet().insertSheet("Debug Logs");
    sheet.appendRow(["Timestamp", "Location", "Variable Name", "Value"]);
  }
  sheet.appendRow([new Date(), location, variableName, value]);
}
