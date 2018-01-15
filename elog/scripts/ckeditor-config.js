/**
 * @license Copyright (c) 2003-2013, CKSource - Frederico Knabben. All rights reserved.
 * For licensing, see LICENSE.html or http://ckeditor.com/license
 */

CKEDITOR.editorConfig = function( config ) {
	// Define changes to default configuration here. For example:
	// config.language = 'fr';
	// config.uiColor = '#AADC6E';
	config.extraPlugins = 'vela';//,timestamp,dndfiles,eqneditor,fileupload';
    config.toolbarCanCollapse = true;

	// allow machine status table styles to be preserved
	var regions = ['gun', 'injector', 'st1', 'arc1', 'st2', 'st3', 'arc2', 'st4', 'rf', 'rfsliders', 'fel']
	var eac = 'table[class]';
	//~ for (i = 0; i < regions.length; i++) {
		//~ eac += 'table(' + regions[i] + ');';
	//~ }

	//~ config.allowedContent = true;
	config.extraAllowedContent = 'table(*);th(*)';

	config.keystrokes = [
		[ CKEDITOR.CTRL + 68, 'timestamp' ],    // Ctrl+D
		[ CKEDITOR.CTRL + 83, 'elogSave' ],    // Ctrl+S
	];

	// Toolbar configuration
	//~ config.toolbar = [
		//~ { name: 'document', groups: [ 'mode', 'document', 'doctools' ], items: [ 'Source', '-', 'Save', 'Preview', 'Print', '-', 'Templates' ] },
		//~ { name: 'clipboard', groups: [ 'clipboard', 'undo' ], items: [ 'Cut', 'Copy', 'Paste', 'PasteText', 'PasteFromWord', '-', 'Undo', 'Redo' ] },
		//~ { name: 'editing', groups: [ 'find', 'selection', 'spellchecker' ], items: [ 'Find', 'Replace', '-', 'SelectAll', '-', 'Scayt' ] },
		//~ '/',
		//~ { name: 'basicstyles', groups: [ 'basicstyles', 'cleanup' ], items: [ 'Bold', 'Italic', 'Underline', 'Strike', 'Subscript', 'Superscript', '-', 'RemoveFormat' ] },
		//~ { name: 'paragraph', groups: [ 'list', 'indent', 'blocks', 'align', 'bidi' ], items: [ 'NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'Blockquote', 'CreateDiv', '-', 'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock', '-', 'BidiLtr', 'BidiRtl', 'Language' ] },
		//~ { name: 'links', items: [ 'Link', 'Unlink', 'Anchor' ] },
		//~ { name: 'insert', items: [ 'Image', 'Table', 'HorizontalRule', 'Smiley', 'SpecialChar', 'PageBreak', 'FileUpload', 'EqnEditor', 'Timestamp' ] },
		//~ '/',
		//~ { name: 'styles', items: [ 'Styles', 'Format', 'Font', 'FontSize' ] },
		//~ { name: 'colors', items: [ 'TextColor', 'BGColor' ] },
		//~ { name: 'tools', items: [ 'Maximize', 'ShowBlocks' ] },
		//~ { name: 'others', items: [ '-' ] },
		//~ { name: 'about', items: [ 'About' ] }
		//~ { name: 'machine-status', items: [ 'InsertGunParams', 'InsertInjectorParams', 'InsertST1Params', 'InsertAR1Params', 'InsertST2Params', 'InsertST3Params', 'InsertAR2Params', 'InsertST4Params', 'InsertRFParams', 'InsertRFSlidersParams', 'InsertFELParams'] }
	//~ ];
};
