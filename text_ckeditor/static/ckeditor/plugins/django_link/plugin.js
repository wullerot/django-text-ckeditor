CKEDITOR.plugins.add( 'django_link', {
    icons: 'django_link',
    init: function( editor ) {
        editor.addCommand( 'django_link', new CKEDITOR.dialogCommand( 'django_linkDialog' ) );
        editor.ui.addButton( 'Django_link', {
            label: 'Insert Link',
            command: 'django_link',
            toolbar: 'insert'
        });

        CKEDITOR.dialog.add( 'django_linkDialog', this.path + 'dialogs/django_link.js' );
    }
});
