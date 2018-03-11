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

  var count = 0;

  for (var i = 0; i < file_metadata.length; i++) {
    (function (fle,index) {
      count++;
      function makeRequest (opts) {
        return new Promise(function (resolve, reject) {
          var xhr = new XMLHttpRequest();
          xhr.open(opts.method, opts.url);
          xhr.onload = function () {
            if (this.status >= 200 && this.status < 300) {
              resolve(xhr.response);
            } else {
              reject({
                status: this.status,
                statusText: xhr.statusText
              });
            }
          };
          xhr.onerror = function () {
            reject({
              status: this.status,
              statusText: xhr.statusText
            });
          };
          if (opts.headers) {
            Object.keys(opts.headers).forEach(function (key) {
              xhr.setRequestHeader(key, opts.headers[key]);
            });
          }
          var params = opts.params;
          xhr.send(params);
        });
      }

      var data = fle.fields;
      var metadata = {'tags': JSON.parse(data.tags), 'description': data.description};
      metadata = JSON.stringify(metadata);

      fle = document.getElementById('file_'+fle.pk).files[0];

      makeRequest({
        method: 'POST',
        url: "https://www.openhumans.org/api/direct-sharing/project/files/upload/direct/?access_token="+access_token,
        headers: {
          "Content-type": "application/x-www-form-urlencoded"
        },
        params: 'project_member_id='+member_id+'&filename='+fle.name+'&metadata='+metadata
      })
      .then(function (responseText) {
        response = JSON.parse(responseText);
        makeRequest({
          method: 'PUT',
          url: response.url,
          params: fle,
          headers: {
            'Content-type': ''
          }
        })
        .then(function(response1) {
          response = JSON.parse(responseText);
          makeRequest({
            method: 'POST',
            url: "https://www.openhumans.org/api/direct-sharing/project/files/upload/complete/?access_token="+access_token,
            params: 'project_member_id='+member_id+'&file_id='+response.id,
            headers: {
              "Content-type": "application/x-www-form-urlencoded"
            }
          });
          if(count == file_metadata.length) {
            var done = "<h3>Upload successful.</h3>";
            $("#upload_form").replaceWith('<div id="upload_form">'+done+'</div>');
          }
        })
        .catch(function (err) {
          console.error('ERROR in PUT', err.statusText);
        });
      })
      .catch(function (err) {
        console.error('Error in POST', err.statusText);
      });
    })(file_metadata[i], i);
  }
}
