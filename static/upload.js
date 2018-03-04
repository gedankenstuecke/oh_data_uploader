var file, response;
var xhr = new XMLHttpRequest();
var put_xhr = new XMLHttpRequest();
var finish_xhr = new XMLHttpRequest();

function startUpload() {
  var uploaded = false;
  file_metadata.forEach(function(file) {
    var files = document.getElementById('file_'+file.pk).files;
    uploaded = uploaded || files.length;
  });
  if (!uploaded) {
    alert("Please select some files");
    return;
  }
  var replacement = '<div class="progress"><div class="progress-bar progress-bar-striped active" role="progressbar" aria-valuenow="45" aria-valuemin="0" aria-valuemax="100" style="width: 45%"></div></div>';
  $("#infotext").replaceWith('<div id="upload_form">' + replacement + '</div>');
  file_metadata.forEach(function (file) {
    var data = file.fields;
    var metadata = {'tags': JSON.parse(data.tags), 'description': data.description};
    uploadFile(file.pk, JSON.stringify(metadata));
  });
}

function uploadFile(id, metadata) {
  var files = document.getElementById('file_'+id).files;
  if (!files.length) {
    return;
  }
  file = files[0];
  xhr.open('POST', "https://www.openhumans.org/api/direct-sharing/project/files/upload/direct/?access_token="+access_token, true);
  xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
  xhr.send('project_member_id='+member_id+'&filename='+file.name+'&metadata='+metadata);
  xhr.onreadystatechange = putFile;
}

function putFile(e) {
  if (xhr.readyState === 4 && xhr.status === 201) {
    response = JSON.parse(xhr.responseText);
    put_xhr.open('PUT', response.url, true);
    put_xhr.setRequestHeader('Content-type','');
    put_xhr.send(file);
    put_xhr.onreadystatechange = uploadedFile;
  } else {
    console.log('checking status of upload url XHR');
  }
}

function uploadedFile(e) {
  if (put_xhr.readyState === 4 && put_xhr.status === 200) {
    finish_xhr.open('POST', "https://www.openhumans.org/api/direct-sharing/project/files/upload/complete/?access_token="+access_token, true);
    finish_xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    finish_xhr.send('project_member_id='+member_id+'&file_id='+response.id);
    finish_xhr.onreadystatechange = finishedFile;
  } else {
    console.log('checking status of upload XHR');
  }
}

function finishedFile(e) {
      if (finish_xhr.readyState === 4 && finish_xhr.status === 200) {
        console.log('uploaded file');
        var done = "<h3>Upload successful.</h3>";
        $("#upload_form").replaceWith('<div id="upload_form">'+done+'</div>');
      } else {
        console.log('checking status of finalizing XHR');
      }
    }
