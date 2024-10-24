function doPost(e) {
  try {
    var data = JSON.parse(e.postData.contents);
    for (var i = 0; i < data.length; i++) {
      var message = GmailApp.getMessageById(data[i].id);
      message.reply(data[i].body);
    }
    return ContentService.createTextOutput('Success');
  } catch (e) {
    return ContentService.createTextOutput('Error: ' + e);
  }
}

function doGet(e) {
  try {
    var threads = GmailApp.search('is:unread');
    var messages = GmailApp.getMessagesForThreads(threads);

    var data = [];
    
    for (var i = 0; i < messages.length; i++) {
      for (var j = 0; j < messages[i].length; j++) {
        var message = messages[i][j];
        data.push({
          id: message.getId(),
          sender: message.getFrom(),
          subject: message.getSubject(),
          body: message.getPlainBody()
        });
      }
    }

    var jsonOutput = JSON.stringify(data);

    Logger.log(jsonOutput);

    return ContentService
      .createTextOutput(jsonOutput)
      .setMimeType(ContentService.MimeType.JSON);
    
  } catch (e) {
    Logger.log('Error: ' + e);
    return ContentService.createTextOutput('Error: ' + e);
  }
}
