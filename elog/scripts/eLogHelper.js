//eLog helper functions, v1.20v
//Ben Shepherd, January 2007

/*
1.20 (1/2/16) changed dlfiles03 address to fed.cclrc.ac.uk one
1.19 (23/6/15) fixed bugs interfering with eLog's native autosave
		changed to jQuery to run initALICE function on load
		(jQuery needs to be explicitly loaded for non-edit pages - see toptext.html)
1.18 (18/6/15) eLog updated to v3.1, CKEditor updated to 4.4.7
		updated routine to get machine status table
		(auto)save functionality now built into eLog
1.17 (1/5/15) changed: new convention for shift folders: Work\yyyy\mm\dd\*.* (no Shift 1/2/3 folders)
1.16   changed: now waits until 30s after entry has stopped being changed
    (previously, it would save as you were typing - this was especially irritating on the first save,
     as it neccesitated a page reload)
     also updated erlpfaults -> alicefaults; no autosaving will happen in this logbook
1.15.1 changed: suppress email notification on save
1.15   changed: access to dlfiles03 is now possible via HTTP
       (http://alice.stfc.ac.uk/ maps to \\dlfiles03\astec\projects\alice)
       so no need to have file:///// links that won't work (by default) in Firefox or off the site network
1.14   fixed: autosave (had to change POST address to e.g. /alicelog/
	     (was /alicelog/ID - wasn't working, presumably ELOG change)
1.13   changed: apsv4 -> dlfiles03
1.12	 fixed: work folder links in list page
1.11   added: .snap file links to each status table
1.10	 added: image browser (again, needs to talk to erlpcon2)
1.9.2  removed: machine status buttons - in FCKeditor code now
1.9.1  fixed: after machine status inserted, scrolls to end so it's visible
1.9	 added: machine status buttons (server running on erlpcon2)
1.8.3  fixed: autosave really works now
1.8.2  fixed: (auto)save function with FCKeditor
1.8.1	 fixed: times in bold, extended regexp to include nbsp, works in IE too
1.8	 changed: updated to work with eLog 2.7.1, works with FCKeditor textarea
1.7	 changed: only checks once if entry has been changed - less CPU intensive
		 added: grabs 'edit' page in background after saving to avoid 'locked' error
1.6	 changed: adds buttons to operations log too
1.5	 added: change rows of ---, ===, ___ to <hr> horizontal line tags
1.4.2  changed: only puts 'save' button in erlplog pages
1.4.1  fixed: times in bold only at start of lines; works in IE
1.4	 changed: hide edit button in list page for entries >8h old
		 added: links to work folder in log page and list page
1.3.1  fixed: (almost) everything works in IE now :)
1.3:	 added: add link to print stylesheet (so specific elements can be dropped from print version)
1.2:	 added: message comment on all edit pages (not just new)
1.1: 	 fixed: showing edit button when not logged in
		 added: hide 'report fault' when not logged in
		 fixed: time in bold on first line of entry
1.0: 	 added: puts times in bold (in format \nHH:MM )
		 added: edit box on list page for most recent entry
0.2:   fixed new entry problem
0.1:   first version */

var msgText;

function getElementsByClass(searchClass,node,tag) {var classElements = new Array(); if ( node == null ) node = document; if ( tag == null ) tag = '*'; var els = node.getElementsByTagName(tag); var elsLen = els.length; var pattern = new RegExp("(^|\\s)"+searchClass+"(\\s|$)"); for (i = 0, j = 0; i < elsLen; i++) { if ( pattern.test(els[i].className) ) { classElements[j] = els[i]; j++; } } return classElements; }

function addTime()
{
	var box = document.getElementsByName ('Text')[0];
	if (!box) {return};
	var text = box.value;
	//add a new line if one does not exist
	if (text.substring(text.length-1,text.length) != '\n' && text.length != 0) {text = text + '\n';};
	if (text.substring(text.length-2,text.length) != '\n\n' && text.substring(text.length-4,text.length) != '\r\n\r\n' && text.length != 0) {text = text + '\n';};
	text = text + getTime() + ' ';
	box.value = text;
	//go to the end of the log entry
	box.focus();
	box.selectionStart = box.value.length;
	box.selectionEnd = box.value.length;
	box.scrollTop = box.scrollHeight;
	box.scrollLeft = 0;
	checkMod();
}

function getTime() {
	return (new Date).toTimeString().substring(0,5);
}

var currentTime, folder, files, currentFiles, foundTime, currentIndex, gridOn = false;

//callback from Machine Status Server that returns the work folder listing for a particular date
//this routine goes through the current log, adding links to timestamps to display inline images
function elogWorkFolderListing (res) {
	if (res.status == 'ok') {
		folder = res.folder;
		files = res.files;
		foundTime = new Array (files.length);
		var repFault = document.getElementById ('repFault');
		repFault.parentNode.innerHTML = repFault.parentNode.innerHTML + ' (' + files.length + ' files)';
		//find the timestamps (in bold or strong, five characters)
		var timeStamps = document.getElementsByTagName ('b');
		var timeStampsStrong = document.getElementsByTagName ('strong');
		for (var i=0; i<timeStamps.length; i++) {
			checkAndAddLink (timeStamps[i]);
		}
		for (var i=0; i<timeStampsStrong.length; i++) {
			checkAndAddLink (timeStampsStrong[i]);
		}

	}
}

var wfReq;
//callback from HTTP folder listing request
function wfReqCallback() {
    if (wfReq.readyState == 4 && wfReq.status == 200) {
        var html = wfReq.responseText;
        var re = /href="(\d{4}%20[^"]*\.png)"/gi;
        RegExp.lastIndex = 0;
        files = new Array;
        while ((a = re.exec (html)) != null) {
            files.push (unescape(a[1]));
        }
		foundTime = new Array (files.length);
		var repFault = document.getElementById ('repFault');
		repFault.parentNode.innerHTML = repFault.parentNode.innerHTML + ' (' + files.length + ' files)';
		//find the timestamps (in bold or strong, five characters)
		var timeStamps = document.getElementsByTagName ('b');
		var timeStampsStrong = document.getElementsByTagName ('strong');
		for (var i=0; i<timeStamps.length; i++) {
			checkAndAddLink (timeStamps[i]);
		}
		for (var i=0; i<timeStampsStrong.length; i++) {
			checkAndAddLink (timeStampsStrong[i]);
		}
        //something like objHTTP.responseText.match (/href="(\d{4}%20[^"]*\.png)"/g)
    }
}

//add a blue dashed border link to a timestamp - clicking it will display an image from the work folder with that timestamp
function checkAndAddLink (el) {
	if (/^[0-2]\d:[0-5]\d ?$/.test (el.innerHTML)) { //match times in bold, with or without trailing space
		//~ console.log (el.innerHTML);
		for (var i=0; i<files.length; i++) {
			if (el.innerHTML.match (files[i].substring(0,2) + ':' + files[i].substring(2,4))) {
				if (el.addEventListener) {
					el.addEventListener ('click', showImage, false);
				} else {
					el.attachEvent ('onclick', showImage);
				}
				foundTime[i] = true;
				el.style.cursor = 'pointer';
				el.style.border = '2px blue dashed';
				return; //only add one event!
			}
		}
	}
}

//initialisation function - add code and links to eLog pages
function initVELA(jQuery)
{
	// add print style sheet
	head = document.getElementsByTagName ('head')[0];
	link = document.createElement ('link');
	link.rel = 'stylesheet';
	link.media = 'print';
	link.href = 'print.css';
	link.type = 'text/css';
	head.appendChild (link);

	// make it play nicely with smaller screens
	var meta = document.createElement('meta');
	meta.name = 'viewport';
	meta.content = "width=device-width, initial-scale=1.0";
	head.appendChild(meta);

	//~ var menuFrame = getElementsByClass ('menuframe');
	//~ if (menuFrame.length > 0) {
		//~ menuFrame = menuFrame[0].parentNode;
		//~ notifyMsg = document.createElement ('tr');
		//~ notifyMsgTD = document.createElement ('td');
		//~ notifyMsgTD.class = "notifymsg";
		//~ notifyMsgTD.colspan = "2";
		//~ notifyMsgTD.innerHTML = '<strong>ERLP Announcement</strong>';
		//~ notifyMsg.appendChild (notifyMsgTD);
		//~ menuFrame.parentNode.insertBefore (notifyMsg, menuFrame);
	//~ }
	var textBox = document.getElementsByName ('Text');
	var listFrame = getElementsByClass ('listframe');
	var headers = listFrame[0].getElementsByTagName ('th');
	var msg = getElementsByClass ('messageframe');
	//~ var findLogout = document.evaluate ('//a[@href="?cmd=Logout"]', document, null, 0, null);
	var l = document.links;
	var loggedIn=false;
	for (var i=1;i<l.length;i++) {
		if (l[i].href.indexOf('?cmd=Logout') > -1) {
			loggedIn = true;
			//~ break;
		}
	}
	var pageType = '';
	if (headers.length > 0) {pageType = 'list';}
	else if (msg.length > 0) {pageType = 'log';}
	else if (textBox.length > 0) {pageType = 'edit';}

	var inLogBook = (/\/vela\//.test (location.pathname));
	var inOpsLog = (/\/operations\//.test (location.pathname));
	var inCBSLog = (/\/cbslog\//.test (location.pathname));
	var inCryoLog = (/\/cryogenics\//.test (location.pathname));
	var inFaultsLog = (/\/alicefaults\//.test (location.pathname));

	if (pageType == 'list') {
		var idI = -1, dateI = -1, entryTypeI = -1;
		for (var i=0; i<headers.length; i++) {
			if (headers[i].textContent == 'ID' || headers[i].innerText == 'ID') {idI = i;}
			if (headers[i].textContent == 'Date' || headers[i].innerText == 'Date') {dateI = i;}
			if (headers[i].textContent == 'Entry Type' || headers[i].innerText == 'Entry Type') {entryTypeI = i;}}

		if (loggedIn) {
			//on a list page and logged in - add an edit button to the top entry
			var cells = listFrame[0].getElementsByTagName ('td');
			var logTime = new Date();
			if (dateI > -1) {
				var datestr = cells[dateI].innerText;
				if (!datestr) {datestr = cells[dateI].textContent}; //innerText is IE only
				logTime = new Date (datestr.replace (/\w\w\w (\d\d)-(\w\w\w)-(\d\d) (\d\d:\d\d)/, '$2 $1, 20$3 $4'));}

			var now = new Date();

			//check it's not locked (there'll be an image there)
			//also check is <8h old
			//~ if (cells[idI].innerHTML.indexOf ('<img') == -1) {
			if (cells[idI].getElementsByTagName('img').length == 0 && (now-logTime) / (1000 * 60 * 60) <= 8) {
				cells[idI].innerHTML = cells[idI].innerHTML + cells[idI].innerHTML;
				cells[idI].getElementsByTagName ('a')[1].href += '?cmd=Edit';
				cells[idI].getElementsByTagName ('a')[1].innerHTML = '<img src="icons/edit.png" border=0>';
			}
		}

		//add work folder links - whether logged in or not
		var rows = listFrame[0].getElementsByTagName ('tr');
		for (var i=1; i<rows.length; i++) {
			var cells = rows[i].getElementsByTagName ('td');
			if (cells.length >= entryTypeI + 1 && cells.length >= dateI + 1) {
				var text = cells[entryTypeI].innerText;
				if (!text) {text = cells[entryTypeI].textContent};
				if (text == 'Shift Log') {
					var datestr = cells[dateI].innerText;
					if (!datestr) {datestr = cells[dateI].textContent}; //innerText is IE only
					var blank = document.createElement('br');
					var folderLink = document.createElement ('a');
					folderLink.innerHTML = 'Work folder';
					folderLink.target = '_blank';
					folderLink.href = 'file://///fed.cclrc.ac.uk/org/NLab/ASTeC/Projects/VELA/Work/' + shiftFolderName (datestr, true);
					cells[dateI].appendChild (blank);
					cells[dateI].appendChild (folderLink);
					//~ blank = document.createTextNode (' ');
					//~ folderLink = document.createElement ('a');
					//~ folderLink.innerHTML = 'work folder';
					//~ folderLink.target = '_blank';
					//~ folderLink.href = shiftFolderName (datestr, false);
					//~ var closeBracket = document.createTextNode (']');
					//~ cells[dateI].appendChild (blank);
					//~ cells[dateI].appendChild (folderLink);
					//~ cells[dateI].appendChild (closeBracket);
				}
			}
		}
	}
	else if (pageType == 'log')
	{
		//we're on a log page

		//highlight the times at the start of paragraphs
		msg = msg[0];
		msgText = msg.innerHTML;
		msgText = msgText.replace (/\<p\>(\d\d:\d\d)(?:\s|&nbsp;)/gi, '<p><strong>$1</strong> ');
		//replace ===, ___, and --- by horizontal line tags
		//alert (msgText.replace (/[=-_]{10,}/, 'hello<hr>'));
		msgText = msgText.replace (/[=\-_]{10,}/g, '<hr>');
		msg.innerHTML = msgText;

		//shift log?
		attribValues = getElementsByClass ('attribvalue');
		for (var i=0; i<attribValues.length; i++) {
			if (/Shift Log/.test (attribValues[i].innerHTML)) {
				//add link to work folder
				var repFault = document.getElementById ('repFault');
				var attribhead = getElementsByClass ('attribhead')[0];
				var date = attribhead.getElementsByTagName ('b')[1];
				//~ var folderHref = shiftFolderName (date.innerHTML, false);
                var folderFileHref = 'file://///fed.cclrc.ac.uk/org/NLab/ASTeC/Projects/VELA/Work/' + shiftFolderName (date.innerHTML, true);
				//~ var folderLink = document.createElement ('a');
				//~ folderLink.innerHTML = 'external';
				//~ folderLink.target = '_blank';
				//~ folderLink.href = folderHref;
				var blank = document.createTextNode (' | ');
				repFault.parentNode.appendChild (blank);
				//~ repFault.parentNode.appendChild (folderLink);
				var folderLink = document.createElement ('a');
				folderLink.innerHTML = 'Work folder';
				folderLink.target = '_blank';
				folderLink.href = folderFileHref;
				//~ blank = document.createTextNode (' ');
				repFault.parentNode.appendChild (blank);
				repFault.parentNode.appendChild (folderLink);

				//add image browser to each link
				//~ var remoteScript=document.createElement('script');
				//~ remoteScript.id = 'rs';
				//~ remoteScript.setAttribute('lang','text/javascript');
				//~ remoteScript.setAttribute('src', 'http://' + mcServer + ':27643/work/' + shiftFolderName (date.innerHTML, true));
				//~ var hd=document.getElementsByTagName('head')[0];
				//~ hd.appendChild(remoteScript);
                if (window.XMLHttpRequest){
                    // If IE7, Mozilla, Safari, etc: Use native object
                    wfReq = new XMLHttpRequest;
                } else {
                if (window.ActiveXObject){
                        // ...otherwise, use the ActiveX control for IE5.x and IE6
                        wfReq = new ActiveXObject("MSXML2.XMLHTTP.3.0");
                    }
                }
                folder = '/files/work/' + shiftFolderName (date.innerHTML, true) + '/'  ;
                wfReq.onreadystatechange = wfReqCallback;
                wfReq.open('GET', folder);
                wfReq.send();

				//add .snap file links to machine status tables
				//~ var headings = document.getElementsByTagName ('i');
				//~ for (var j=0; j<headings.length; j++) {
					//~ var tableName = headings[j].innerHTML;
					//~ var result = tableName.match (/(.*) ((?:Status)|(?:Sliders))/);
					//~ if (result && headings[j].parentNode.nodeName == 'B' && headings[j].parentNode.parentNode.nodeName == 'DIV') {
						//~ var dtString = headings[j].parentNode.parentNode.nextSibling.innerHTML.replace (/[\/:]/g, '').replace (' ', '_');
						//~ dtString = dtString.replace (/([0-9]{2})([0-9]{2})([0-9]{2})_([0-9]{6})/, '20$3$2$1_$4'); // ddmmyy_hhmmss -> 20yymmdd_hhmmss
						//~ var ssfolder = (result[2] == 'Sliders') ? 'RF Sliders' : result[1].replace (' ', '_');
						//~ var href = 'http://alice.stfc.ac.uk/files/Snapshots/' + ssfolder + '/' + dtString + '.snap';
						//~ headings[j].parentNode.parentNode.innerHTML = headings[j].parentNode.parentNode.innerHTML + '&nbsp;<small><a href="' + href + '">.snap file</a></small>';
					//~ }
				//~ }
			}
		}

	}
	else if (pageType == 'edit')// && (inLogBook || inOpsLog || inCBSLog || inCryoLog))
	{
        textBox = textBox[0];

		//add text above the edit box
		if (inLogBook) {
            topText = document.createElement ('div');
            topText.innerHTML = 'Entries will be <strong>automatically saved</strong> (or press <strong>Ctrl-S</strong>). Type <strong>Ctrl+D</strong> for a timestamp.' +
                ' Please use <strong>headings</strong> above each separate task or activity. <span id="mcWorking"></span>';
            topText.id = 'addedText';
            if (!document.getElementById ('addedText')) textBox.parentNode.insertBefore (topText, textBox);
            }

	}

	if (!loggedIn && document.getElementById ('repFault'))
	{
		repFault = document.getElementById ('repFault');
		document.getElementById ('repFault').innerHTML = '';
	}
}

var mcTimer, mcServer = 'apsv2.dl.ac.uk';
function elogRequestMachineStatus (area) {
	document.getElementById ('mcWorking').innerHTML = 'Working...';
	mcTimer = setTimeout ('mcRequestTimeout()', 10*1000);
	var remoteScript=document.createElement('script');
	remoteScript.id = 'rs';
	remoteScript.setAttribute('type','text/javascript');
	remoteScript.setAttribute('src', 'https://' + mcServer + ':27643/' + area);
	var hd=document.getElementsByTagName('head')[0];
	hd.appendChild(remoteScript);
}

function elogInsertMachineStatus (rsp) {
	document.getElementById ('mcWorking').innerHTML = '';
	clearTimeout (mcTimer);
	if (rsp.status == 'ok') {
		// Get the editor instance that we want to interact with.
		var editor = CKEDITOR.instances['Text'];
		var body = editor.document.getBody().$;
		var ckbody = new CKEDITOR.dom.element(body);
		ckbody.appendHtml(rsp.params);

		// Move cursor to end and scroll into view
		var range = editor.createRange();
		range.moveToPosition( ckbody, CKEDITOR.POSITION_BEFORE_END );
		editor.getSelection().selectRanges( [ range ] );
		range.scrollIntoView();

	} else {
		document.getElementById ('mcWorking').innerHTML = 'Machine Status: failed (' + rsp.status + ').';
	}
	var remoteScript = document.getElementById ('rs');
	remoteScript.parentNode.removeChild (remoteScript);
}

function mcRequestTimeout() {
	document.getElementById ('mcWorking').innerHTML = 'Machine Status request timed out. Is the server running on ' + mcServer + '? Try restarting it - instructions <a href="http://projects.astec.ac.uk/ERLPManual/index.php/ELog#Machine_Status" target="_blank">here</a>.';
}

var camNameRE = /[0-9]{4} ([A-Z][A-Z][A-Z1-4](-Y?[1-6])?)/;
function showImage(e) {

	//~ console.log ('showImage');
	if (!e) {e = window.event;}
	if (e.target) {var link = e.target;}
	else if (e.srcElement) {var link = e.srcElement;}

	var time = link.innerHTML.replace (':', '').substr(0,4);
	//~ console.log (time);
	//~ currentFiles = new Array;
	currentIndex = -1;
	for (i = 0; i < files.length; i++) {
		if (files[i].substr(0, 4) == time) {
			currentIndex = i;
			break;
		}
	}
	if (currentIndex == -1) {return;}
	currentFiles = files;

	var inlineImage = document.getElementById ('inlineImage');
	if (inlineImage) { //remove image if one already shown
		inlineImage.parentNode.removeChild (inlineImage);
		if (currentTime == time) {
			if (e.preventDefault) {e.preventDefault();}
			return;}
	}
	currentTime = time;

	//~ console.log (currentFiles);
	if (currentFiles.length == 0) {return;}

	var container = document.createElement('div');

	// Setup some constants for use in creating the inline window...
	var windowPadding = 13;
	var windowTextPadding = 5;
	var windowFontSize = 10;
	var windowBorderSize = 1;
	var windowButtonHeight = 12;
	var windowButtonTextSize = 11;

	// setup the y-positioning of the inline window...

	var imgWidth = 768;
	var imgHeight = 572;

	var cssBoxWidth = imgWidth + windowPadding;//Math.round((windowWidth - (windowPadding+windowBorderSize)*2)/document.width*100);
	var cssBoxHeight = imgHeight + windowPadding + windowTextPadding;//windowHeight - (windowPadding+windowBorderSize*2);
	var windowHeight = cssBoxHeight + windowPadding + windowBorderSize * 2;//Math.round(window.innerHeight * 0.45);
	var windowWidth = cssBoxHeight + (windowPadding + windowBorderSize) * 2;

	// stop the window before getting this close to the left/right/top/bottom of the screen
	var pageBoundPadding = 10;

	var xpos, ypos;

	if (document.width) {var docWidth = document.width;} else {var docWidth = document.body.clientWidth;}
	// get the position of the element that was clicked on...
	var elementTop = getElementOffset(link,'Top');
	var elementLeft = getElementOffset(link,'Left');
	if (window.getComputedStyle) {
		var elementHeight = parseInt(window.getComputedStyle(link,"").getPropertyValue('line-height'));
	} else {
		elementHeight = 14;
	}

	// setup the x-position of the inline window...
	// check to see if the left 1/3 of the window will overlap the left page bound..
	if ( elementLeft - (windowWidth/3) < pageBoundPadding ) {
		xpos = pageBoundPadding;
	}
	// check to see if the right 2/3 of the window will overlap the right page bound...
	else if ( elementLeft > docWidth - pageBoundPadding ) {
		xpos = docWidth - pageBoundPadding - windowWidth - (windowPadding + windowBorderSize) * 2;
	}
	else {
		// if we're not going to hit either wall, set the window to be offset
		// by 1/3 to the left of where we clicked (looks better than centering)
		xpos = elementLeft - (windowWidth/3);
	}

	// check to see if the window goes beyond the bottom of the viewport...
	if (window.innerHeight) {
		var winHeight = window.innerHeight;
		var pyo = window.pageYOffset;
	} else {
		var winHeight = document.body.clientHeight;
		var pyo = document.body.scrollTop;
	}
	if ( elementTop + windowHeight + pageBoundPadding > pyo + winHeight ) {
		ypos = elementTop - windowHeight;
	} else {
		ypos = elementTop + elementHeight;
	}

	//~ currentIndex = 0;
	reMatch = currentFiles[currentIndex].match (camNameRE);
	if (reMatch) {camera = reMatch[1];}

	divParams = 'background-color: #DDD; '+
				'margin: 0 3px ' + Math.round((windowPadding-windowButtonHeight)/2) +'px; '+
				'padding: 0 3px; '+
				'-moz-border-radius: 2px; '+
				'height: ' + windowButtonHeight + 'px; '+
				'font-size: ' + windowButtonTextSize + 'px; '+
				'line-height: ' + windowButtonTextSize + 'px; '+
				'font-weight: bold">';

	container.innerHTML = '<div id="inlineImage" name="' + time + '" style="' +
		'position: absolute; '+
		'margin: ' + ypos + 'px 0 0 ' + xpos + 'px; ' +
		'padding: ' + Math.round((windowPadding-windowButtonHeight)/2) +'px ' + windowPadding + 'px ' + windowPadding + 'px; ' +
		'width: ' + cssBoxWidth + 'px; ' +
		'height: '+ cssBoxHeight + 'px; ' +
		'background-color: #FFFFE0; '+
		'border: ' + windowBorderSize + 'px solid #E0E0E0; '+
		'-moz-border-radius: 5px; '+
		'z-index: 998; '+
		'opacity: 0.85; filter:alpha(opacity=85); '+
		'font-size: ' + windowFontSize + 'pt; ">'+
			'<div style="float: left; ' + divParams + '<a href="javascript:changeImage(-1);">&lt;</a></div>'+
			'<div style="float: left; ' + divParams + '<a href="javascript:changeImage(1);">&gt;</a></div>'+
			'<div id="inlineImageName" style="float: left; ' + divParams + unescape(currentFiles[currentIndex]) + '</div>' +
			'<div style="float: right; ' + divParams +
			'<a href="#" onClick="innerWindow = this.parentNode.parentNode.parentNode; innerWindow.parentNode.removeChild(innerWindow); return false;" style="text-decoration: none;">close</a></div>'+
			(reMatch ? ('<div style="float: right; ' + divParams +
			'<a id="inlineImgGridSwitch" href="javascript:toggleGrid();" style="text-decoration: none;">' + (gridOn ? 'hide' : 'show') + ' grid</a></div>') : '') +
			'<div style="float: right; ' + divParams + '<span id="inlineImageIndex">' + (currentIndex + 1) + '</span>/' + currentFiles.length + '</div>'+
			'<div style="'+
				'border: 1px dashed black; '+
				'background: white; '+
				'padding: ' + windowTextPadding + 'px; '+
				'overflow: auto; '+
				'clear: both; '+
				'height: ' + imgHeight + 'px' +
			'"><img oncontextmenu="changeImage(1);return false;" onclick="changeImage(-1)" id="inlineImageImg" src="http://alice.stfc.ac.uk' + folder + '/' + currentFiles[currentIndex] + '"></div>'+
			(reMatch ? ('<div id="inlineImgGrid" style="'+
				'position:absolute; left:19px; top:18px; z-index:999; opacity: 1.0; border: 1px dashed black; '+
				'background: none; display: '+ ((gridOn && reMatch) ? 'block' : 'none') +
				'padding: ' + windowTextPadding + 'px; '+
				'overflow: auto; '+
				'clear: both; '+
				'height: ' + imgHeight + 'px' +
			'"><img id="inlineImgGridImage" oncontextmenu="changeImage(1);return false;" onclick="changeImage(-1)" src="http://alice.stfc.ac.uk/files/Analysis/YAG%20Images%20Calibration/Grids/' + camera + '.png"></div>') : '')+
		'</div>';
	document.body.insertBefore(container, document.body.firstChild);
	if (reMatch) {document.getElementById ('inlineImgGrid').style.display = gridOn ? 'block' : 'none';}

	if (e.preventDefault) {e.preventDefault();}
	return true;
}

function toggleGrid() {
	gridOn = !gridOn;
	document.getElementById ('inlineImgGridSwitch').innerHTML = gridOn ? 'hide grid' : 'show grid';
	document.getElementById ('inlineImgGrid').style.display = gridOn ? 'block' : 'none';
}

function changeImage(offset) {
	currentIndex = (currentIndex + offset) % currentFiles.length;
	if (currentIndex < 0) {currentIndex = currentFiles.length - 1};
	document.getElementById ('inlineImageName').innerHTML = unescape (currentFiles[currentIndex]);
	document.getElementById ('inlineImageIndex').innerHTML = currentIndex + 1;
	document.getElementById ('inlineImageImg').src = 'http://alice.stfc.ac.uk' + folder + '/' + currentFiles[currentIndex];
	reMatch = currentFiles[currentIndex].match (camNameRE);
	if (reMatch) {
		camera = reMatch[1];
		document.getElementById ('inlineImgGridImage').src = 'http://alice.stfc.ac.uk/files/Analysis/YAG%20Images%20Calibration/Grids/' + camera + '.png';
	}
}

function getElementOffset(element,whichCoord) {
	var count = 0
	while (element!=null) {
	 	count += element['offset' + whichCoord];
		element = element.offsetParent;
	}
	return count;
}

// BJAS 1/5/15: new convention for shift folders: Work\yyyy\mm\dd\*.* (no Shift 1/2/3 folders)
function shiftFolderName (datestr, shortForm) {
	var logTime = new Date (datestr.replace (/\w\w\w (\d\d)-(\w\w\w)-(\d\d) (\d\d:\d\d)/, '$2 $1, 20$3 $4'));

	var subFolder = logTime.getFullYear() + '/' + nf2 (logTime.getMonth() + 1) + '/' + nf2 (logTime.getDate());// + '/Shift%20' + shift;
	if (shortForm) {
		return subFolder.replace (/\\/g, '/'); //use forward slashes
	} else {
		return 'http://alice.stfc.ac.uk/files/Work/' + subFolder;
	}
}

function nf2 (n) {
	if (n < 10) {return '0' + n.toString()} else {return n.toString()}
}

function restoreMode (el) {
	var table = el.parentNode.parentNode.parentNode.parentNode.parentNode.parentNode;
	el.parentNode.innerHTML = '[<a style="cursor: pointer;" onclick="restoreExit(this);">Restore Mode Off</a> | ' +
		'<a style="cursor: pointer;" onclick="restoreAll(this);">Restore All</a>]';
	var pvCells = getElementsByClass ('pvCell', table);
	for (var i in pvCells) {
		pvCells[i].style.cursor = 'pointer';
		pvCells[i].onmouseover = pvCellMouseOver;
		pvCells[i].onmouseout = pvCellMouseOut;
		pvCells[i].onclick = restore;
	}
}

function restoreExit (el) {
	var table = el.parentNode.parentNode.parentNode.parentNode.parentNode.parentNode;
	var pvCells = getElementsByClass ('pvCell', table);
	for (var i in pvCells) {
		pvCells[i].style.cursor = '';
		pvCells[i].onmouseover = '';
		pvCells[i].onmouseout = '';
		pvCells[i].onclick = '';
	}
	var statusLine = getElementsByClass ('caPutStatus', table);
	for (var i in statusLine) {
		statusLine[i].parentNode.removeChild (statusLine[i]);
	}
	el.parentNode.innerHTML = '[<a style="cursor: pointer;" onclick="restoreMode(this);">Restore Mode On</a>]';
}
function pvCellMouseOver () {
	this.style.backgroundColor = '#45D7DD';
}

function pvCellMouseOut () {
	this.style.backgroundColor = '';
}

function restoreAll (el) {
	var table = el.parentNode.parentNode.parentNode.parentNode.parentNode.parentNode;
	var pvCells = getElementsByClass ('pvCell', table);
	for (var i in pvCells) {
		restoreElement (pvCells[i]);
	}
}

function restore () {
	restoreElement (this);
}

function restoreElement (el) {
	var values = getElementsByClass ('pvValue', el);
	for (var i in values) {
		var updateCell = values[i].parentNode;
		var statusLine = getElementsByClass ('caPutStatus', updateCell);
		if (statusLine.length == 0) {
			updateCell.innerHTML = updateCell.innerHTML + '<br><small class=caPutStatus>Working...</small>';
		} else {
			statusLine[0].innerHTML = 'Working...';
		}
		var remoteScript=document.createElement('script');
		var id = Math.random();
		updateCell.id = id;
		remoteScript.id = 'rs' + id;
		remoteScript.setAttribute('type','text/javascript');
		remoteScript.setAttribute('src', 'http://' + mcServer + ':27643/caput?' + values[i].id + '=' + values[i].innerHTML +
			'&reqid=' + id);
		var hd=document.getElementsByTagName('head')[0];
		hd.appendChild(remoteScript);
	}
}

function caPutOutput (res) {
	var updateCell = document.getElementById (res.reqid);
	var statusText = (res.status == 'Normal successful completion' ? 'OK' : 'Failed');
	var statusLine = getElementsByClass ('caPutStatus', updateCell);
	if (statusLine.length == 0) {
		updateCell.innerHTML = updateCell.innerHTML + '<br><small title="' + res.status + '" class=caPutStatus>' + statusText + '</small>';
	} else {
		statusLine[0].innerHTML = statusText;
		statusLine[0].title = res.status;
	}
}

//this bit runs when the script is loaded
$(document).ready(initVELA);
