var lanternTracker = function(window, document){
function doTrack() {

//UK
var searchTerm = 'awin1.com/cread.php?awinmid=5577';
var searchTermA = 'v=5577';

for(var i=0; i<document.links.length; i++) {
if (document.links[i].href.indexOf(searchTerm) > -1 || document.links[i].href.indexOf(searchTermA) > -1) {

// Actually fire
var img = document.createElement('img'),src = 'https://lantern.roeye.com/pixel.php?site=PLTUK&cid=1&sv_tax1=affiliate&sv_campaign_id=304459';
img.src = src;
img.width = img.height = img.border = 0;
img.style.position = 'absolute';
img.style.visibility = 'hidden';

// Break, as we only fire once
break;
}
}

//US
var searchTerm = 'awin1.com/cread.php?awinmid=7533';
var searchTermA = 'v=7533';

for(var i=0; i<document.links.length; i++) {
if (document.links[i].href.indexOf(searchTerm) > -1 || document.links[i].href.indexOf(searchTermA) > -1) {

// Actually fire
var img = document.createElement('img'),src = 'https://lantern.roeye.com/pixel.php?site=PLTUS&cid=1&sv_tax1=affiliate&sv_campaign_id=304459';
img.src = src;
img.width = img.height = img.border = 0;
img.style.position = 'absolute';
img.style.visibility = 'hidden';

// Break, as we only fire once
break;
}
}


}

return {
'doTrack' : doTrack
}
}(window, document, window.lantern)
window.onload = function () {
lanternTracker.doTrack();
}
