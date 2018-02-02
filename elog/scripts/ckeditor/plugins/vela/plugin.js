/**
 * Plugin for CKEditor with some VELA-specific functios.
 * Ben Shepherd, June 2015
 */

// Register the plugin within the editor.
CKEDITOR.plugins.add( 'vela', {

	// Register the icons.
	icons: 'timestamp,callout,gunstatus,linac1status',

	// The plugin initialization logic goes inside this method.
	init: function( editor ) {
		// Command to insert a timestamp (HH:mm) on new line
		editor.addCommand( 'timestamp', {
			exec: function( editor ) {
				// format time as HH:mm
				var now = new Date();
				var h = now.getHours();
				var m = now.getMinutes();
				var timestamp = ((h<10) ? '0' : '') + h + ':' + ((m<10) ? '0' : '') + m;

				// insert timestamp
				var body = editor.document.getBody().$;
				var ckbody = new CKEDITOR.dom.element(body);
				var p = new CKEDITOR.dom.element( 'p' );
				var strong = new CKEDITOR.dom.element( 'strong' );
				strong.appendText(timestamp + ' ');
				strong.appendTo( p );
				p.appendTo(ckbody);

				// move cursor to end
				var range = editor.createRange();
				range.moveToPosition( p, CKEDITOR.POSITION_BEFORE_END );
				editor.getSelection().selectRanges( [ range ] );
				range.scrollIntoView();
			}
		} );

		// Create a toolbar button that executes the above command.
		editor.ui.addButton( 'Timestamp', {
			// The text part of the button (if available) and the tooltip.
			label: 'Insert Timestamp',
			// The command to execute on click.
			command: 'timestamp',
			// The button placement in the toolbar (toolbar group name).
			toolbar: 'insert'
		});

		// Command to insert a callout table.
		editor.addCommand( 'callout', {
			exec: function( editor ) {
				// format date/time
				var timestamp = (new Date).toString().substring(4,21);

				// insert table
				var body = editor.document.getBody().$;
				var ckbody = new CKEDITOR.dom.element(body);
				var p = new CKEDITOR.dom.element( 'p' );
				var table = new CKEDITOR.dom.element( 'table' );
				rowHeaders = ['Callout', 'Name', 'Reason for call', 'Result / Action Taken'];
				for (row = 0; row <= 3; row++) {
					var tr = new CKEDITOR.dom.element( 'tr' );
					var th = new CKEDITOR.dom.element( 'th' );
					th.appendText(rowHeaders[row]);
					th.appendTo(tr);
					var td = new CKEDITOR.dom.element( 'td' );
					if (row == 0) {
						td.appendText(timestamp);
					} else if (row == 1) {
						cursorTD = td;
					}
					td.appendTo(tr);
					tr.appendTo(table);
				}
				table.appendTo(p);
				p.appendTo(ckbody);

				// move cursor to first editable cell and scroll whole table into view
				var selRange = editor.createRange();
				selRange.moveToPosition( cursorTD, CKEDITOR.POSITION_BEFORE_END );
				editor.getSelection().selectRanges( [ selRange ] );
				var cursorRange = editor.createRange();
				cursorRange.moveToPosition( td, CKEDITOR.POSITION_BEFORE_END ); //last row/column
				cursorRange.scrollIntoView();
			}
		} );

		editor.ui.addButton( 'Callout', {label: 'Insert Callout', command: 'callout', toolbar: 'insert'});

		// added so we can have a Ctrl-S shortcut
		editor.addCommand( 'elogSave', {
			exec: function( editor ) {
				window.top.save_draft();
			}
		} );

		// add buttons for machine status
		machineAreas = ['Gun', 'Linac1'];//, 'ST1', 'Arc 1', 'ST2', 'ST3', 'Arc 2', 'ST4', 'RF', 'RF Sliders', 'FEL'];

		function reqStatus(name, editor) {
			window.top.elogRequestMachineStatus (name);
		}

		for (i = 0; i < machineAreas.length; i++) {

            name = machineAreas[i];
            nameNoSpace = name.replace(' ', '');
            commandName = nameNoSpace + 'Status';
            editor.addCommand( commandName, {
                allowedContent: 'table[class]',
                exec: reqStatus.bind(null, nameNoSpace) // call the request function with specified name
            } );

            editor.ui.addButton( commandName, {label: name, command: commandName, toolbar: 'machine-status'});
		}

	}
});
