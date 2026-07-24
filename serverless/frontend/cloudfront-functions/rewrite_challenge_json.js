function handler(event) {
  var request = event.request;
  var uri = request.uri;
  var prefix = "/api/v2/playground/challenges/";
  var lang = "";

  if (request.method !== "GET" && request.method !== "HEAD") {
    return request;
  }

  if (request.querystring.lang) {
    var value = request.querystring.lang.value;
    if (value === "en" || value === "es") {
      lang = "." + value;
    }
  }

  if (uri === "/api/v2/playground/challenges" || uri === prefix) {
    request.uri = "/api/v2/playground/challenges/index" + lang + ".json";
    return request;
  }

  if (uri.indexOf(prefix) === 0 && uri.indexOf("/submit") === -1) {
    if (uri.slice(-5) !== ".json") {
      request.uri = uri + lang + ".json";
    }
  }

  return request;
}

