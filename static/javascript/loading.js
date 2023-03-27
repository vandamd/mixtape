// Loading animation for the "Generating" message
function showLoading() {
    var loadingDiv = document.getElementById("loading");
    loadingDiv.style.display = "block";
}

function isValidUrl() {
    var url = document.getElementById("playlist_url").value;
    if (url.startsWith("https://open.spotify.com/playlist/")) {
        return true;
    } else {
        alert("Oops! Looks like this URL is invalid, have another go.");
        return false;
    }
}
